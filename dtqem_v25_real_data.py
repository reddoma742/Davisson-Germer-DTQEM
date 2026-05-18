"""
DTQEM v25.0 – Real-Data Double-Slit Inversion with Model Comparison
====================================================================
This module is designed for real experimental data. It allows:
- Fixing any parameter (I0, d, L, lam, a, E, B) based on prior knowledge.
- Choosing background model: constant, linear, or quadratic.
- Optionally convolving the model with a Gaussian source (extended source).
- Computing AICc to compare different model configurations.
- Analysing residuals (normality, autocorrelation, heteroscedasticity).

Physical meaning of parameters:
- I0  : peak intensity at central fringe (a.u.)
- d   : slit separation (m) → determines fringe spacing Δx = λL/d
- L   : slit-to-screen distance (m) → fixed from geometry
- lam : wavelength (m) → fixed from laser specification
- a   : slit width (m) → if fixed, adds sinc² envelope; if free, fitted
- E   : observer strength (0→1) → reduces fringe visibility, 1 = no fringes
- B0, B1, B2 : background offset coefficients (constant, linear, quadratic)
- sigma_src : standard deviation of Gaussian source (m) → simulates extended source

Usage example:
    result = invert_real_data(x, I, sigma_I=None,
                              fixed={'L':1.0, 'lam':650e-9, 'a':50e-6},
                              free=['I0','d','E','B0'],
                              background='linear',
                              source_width=0.002,
                              compare_models=True)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.ndimage import convolve1d
from scipy.stats import norm, shapiro, jarque_bera
from statsmodels.stats.diagnostic import acorr_ljungbox
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict, Union
import json
import os
import time
import warnings

# ==================================================================
# 1. Forward model with optional extended source convolution
# ==================================================================
def double_slit_kernel(x: np.ndarray,
                       I0: float,
                       d: float,
                       L: float,
                       lam: float,
                       E: float,
                       B_coeff: List[float],
                       a: Optional[float] = None,
                       fit_envelope: bool = True,
                       background: str = 'constant') -> np.ndarray:
    """
    Core intensity model (no convolution).
    Background: constant -> B0; linear -> B0 + B1*x; quadratic -> B0 + B1*x + B2*x².
    """
    arg = np.pi * d * x / (lam * L)
    interference = (1.0 - E) * np.cos(arg)**2 + E
    model = I0 * interference
    if fit_envelope and a is not None and a > 0:
        arg_env = np.pi * a * x / (lam * L)
        envelope = np.sinc(arg_env / np.pi)**2
        model *= envelope

    # Background
    if background == 'constant':
        B = B_coeff[0]
    elif background == 'linear':
        B = B_coeff[0] + B_coeff[1] * x
    elif background == 'quadratic':
        B = B_coeff[0] + B_coeff[1] * x + B_coeff[2] * x**2
    else:
        raise ValueError("background must be 'constant', 'linear', or 'quadratic'")
    return model + B

def convolve_with_source(model: np.ndarray,
                         x: np.ndarray,
                         sigma_src: float) -> np.ndarray:
    """
    Convolve model with Gaussian kernel of width sigma_src (m).
    Assumes uniform x spacing.
    """
    dx = x[1] - x[0]
    kernel_size = int(10 * sigma_src / dx)
    if kernel_size % 2 == 0:
        kernel_size += 1
    x_kernel = np.linspace(-3*sigma_src, 3*sigma_src, kernel_size)
    kernel = np.exp(-0.5 * (x_kernel / sigma_src)**2)
    kernel /= kernel.sum()
    return convolve1d(model, kernel, mode='nearest')

# ==================================================================
# 2. Parameter handling (fixed / free)
# ==================================================================
def pack_params(free_params: Dict[str, float],
                fixed_params: Dict[str, Union[float, List[float]]],
                background: str) -> List[float]:
    """Pack free parameters into a list in fixed order."""
    order = []
    if 'I0' in free_params:
        order.append('I0')
    if 'd' in free_params:
        order.append('d')
    if 'L' in free_params:
        order.append('L')
    if 'lam' in free_params:
        order.append('lam')
    if 'a' in free_params:
        order.append('a')
    if 'E' in free_params:
        order.append('E')
    if background == 'constant' and 'B0' in free_params:
        order.append('B0')
    elif background == 'linear':
        if 'B0' in free_params:
            order.append('B0')
        if 'B1' in free_params:
            order.append('B1')
    elif background == 'quadratic':
        if 'B0' in free_params:
            order.append('B0')
        if 'B1' in free_params:
            order.append('B1')
        if 'B2' in free_params:
            order.append('B2')
    if 'sigma_src' in free_params:
        order.append('sigma_src')
    return [free_params[p] for p in order], order

def unpack_params(params: List[float],
                  free_order: List[str],
                  fixed_params: Dict[str, Union[float, List[float]]],
                  background: str) -> Dict[str, Union[float, List[float]]]:
    """Unpack list back into dictionary, merging with fixed parameters."""
    full = fixed_params.copy()
    for name, val in zip(free_order, params):
        full[name] = val
    # Ensure background coefficients are in list form
    if background == 'constant':
        full['B'] = full.get('B0', 0.0)
    elif background == 'linear':
        full['B'] = [full.get('B0', 0.0), full.get('B1', 0.0)]
    elif background == 'quadratic':
        full['B'] = [full.get('B0', 0.0), full.get('B1', 0.0), full.get('B2', 0.0)]
    return full

# ==================================================================
# 3. Objective function (chi²)
# ==================================================================
def chi2_objective(params: List[float],
                   free_order: List[str],
                   fixed_params: Dict,
                   x_data: np.ndarray,
                   I_meas: np.ndarray,
                   sigma_I: np.ndarray,
                   fit_envelope: bool,
                   background: str,
                   source_width: Optional[float]) -> float:
    full = unpack_params(params, free_order, fixed_params, background)
    # Extract needed quantities
    I0 = full.get('I0', 1.0)
    d = full.get('d', 0.5e-3)
    L = full.get('L', 1.0)
    lam = full.get('lam', 650e-9)
    a = full.get('a', None)
    E = full.get('E', 0.0)
    B = full.get('B', 0.0)
    sigma_src = full.get('sigma_src', 0.0)

    model = double_slit_kernel(x_data, I0, d, L, lam, E, B,
                               a=a, fit_envelope=fit_envelope, background=background)
    if source_width is not None and source_width > 0:
        model = convolve_with_source(model, x_data, source_width)

    resid = (I_meas - model) / sigma_I
    return 0.5 * np.sum(resid**2)

# ==================================================================
# 4. Model fitting with fixed/free parameters
# ==================================================================
def fit_model(x_data: np.ndarray,
              I_data: np.ndarray,
              sigma_I: np.ndarray,
              fixed: Dict[str, Union[float, List[float]]],
              free: List[str],
              fit_envelope: bool,
              background: str = 'constant',
              source_width: Optional[float] = None,
              p0: Optional[Dict[str, float]] = None,
              bounds: Optional[Dict[str, Tuple[float, float]]] = None,
              method: str = 'L-BFGS-B',
              options: Optional[Dict] = None) -> Tuple[Dict, float, bool, str]:
    """
    Fit model with specified fixed and free parameters.
    Returns (best_params, chi2_min, success, message).
    """
    # Build initial guess for free parameters
    if p0 is None:
        p0 = {}
        # Provide sensible defaults based on data
        I_max = np.max(I_data)
        I_min = np.min(I_data)
        p0['I0'] = I_max - I_min
        p0['d'] = fixed.get('d', 0.5e-3)
        p0['E'] = 0.5
        if background == 'constant':
            p0['B0'] = I_min
        elif background == 'linear':
            p0['B0'] = I_min
            p0['B1'] = 0.0
        elif background == 'quadratic':
            p0['B0'] = I_min
            p0['B1'] = 0.0
            p0['B2'] = 0.0
        if 'a' in free:
            p0['a'] = 50e-6
        if 'sigma_src' in free:
            p0['sigma_src'] = 0.001

    free_vals, free_order = pack_params({k: p0.get(k, 0.0) for k in free}, fixed, background)

    # Bounds
    lb, ub = [], []
    for name in free_order:
        if bounds and name in bounds:
            lb.append(bounds[name][0])
            ub.append(bounds[name][1])
        else:
            if name == 'I0':
                lb.append(0.01*np.max(I_data))
                ub.append(100*np.max(I_data))
            elif name == 'd':
                lb.append(1e-7)
                ub.append(5e-3)
            elif name == 'L':
                lb.append(0.05)
                ub.append(20.0)
            elif name == 'lam':
                lb.append(300e-9)
                ub.append(1000e-9)
            elif name == 'a':
                lb.append(1e-6)
                ub.append(500e-6)
            elif name == 'E':
                lb.append(0.0)
                ub.append(1.0)
            elif name.startswith('B'):
                lb.append(-1000)
                ub.append(1000)
            elif name == 'sigma_src':
                lb.append(0.0)
                ub.append(0.01)
    bounds_list = list(zip(lb, ub))

    def obj(params):
        return chi2_objective(params, free_order, fixed, x_data, I_data, sigma_I,
                              fit_envelope, background, source_width)

    res = minimize(obj, free_vals, bounds=bounds_list, method=method, options=options or {'ftol':1e-14,'maxiter':5000})
    best_full = unpack_params(res.x, free_order, fixed, background)
    return best_full, res.fun, res.success, res.message

# ==================================================================
# 5. Model comparison: AICc, BIC, residual analysis
# ==================================================================
def compute_aicc(chi2_min: float, n_data: int, n_params: int) -> float:
    """AICc for small sample size."""
    if n_data - n_params - 1 <= 0:
        return np.inf
    return chi2_min + 2*n_params + (2*n_params*(n_params+1))/(n_data - n_params - 1)

def compute_bic(chi2_min: float, n_data: int, n_params: int) -> float:
    """Bayesian Information Criterion."""
    return chi2_min + n_params * np.log(n_data)

def analyse_residuals(resid: np.ndarray, bins: int = 20) -> Dict:
    """
    Analyse residuals: normality, autocorrelation, heteroscedasticity.
    Returns dictionary with statistics.
    """
    # Normality tests
    _, p_shapiro = shapiro(resid)
    _, p_jb = jarque_bera(resid)
    # Autocorrelation (Ljung-Box up to lag 10)
    lb_result = acorr_ljungbox(resid, lags=10, return_df=True)
    p_autocorr = lb_result['lb_pvalue'].min()
    # Heteroscedasticity: correlation between absolute residuals and x
    x = np.arange(len(resid))
    from scipy.stats import pearsonr
    corr, p_hetero = pearsonr(x, np.abs(resid))
    return {
        'shapiro_p': p_shapiro,
        'jarque_bera_p': p_jb,
        'autocorr_min_p': p_autocorr,
        'hetero_corr': corr,
        'hetero_p': p_hetero,
        'std': np.std(resid),
        'mean': np.mean(resid),
    }

# ==================================================================
# 6. Main inversion function for real data
# ==================================================================
@dataclass
class RealDataResult:
    best_params: Dict
    chi2_min: float
    chi2_red: float
    n_data: int
    n_params: int
    aicc: float
    bic: float
    residual_stats: Dict
    success: bool
    message: str
    fixed_spec: Dict
    free_list: List[str]
    background: str
    source_width: Optional[float]
    fit_envelope: bool
    runtime: float

def invert_real_data(x_data: np.ndarray,
                     I_data: np.ndarray,
                     sigma_I: Optional[np.ndarray] = None,
                     fixed: Optional[Dict] = None,
                     free: Optional[List[str]] = None,
                     fit_envelope: bool = True,
                     background: str = 'constant',
                     source_width: Optional[float] = None,
                     compare_models: bool = False,
                     verbose: bool = True) -> Union[RealDataResult, List[RealDataResult]]:
    """
    Invert real double-slit data with flexible parameter fixing.

    Parameters
    ----------
    x_data, I_data : screen positions (m) and intensity (a.u.)
    sigma_I : measurement uncertainty (if None, estimated from data)
    fixed : dict of fixed parameters (e.g., {'L':1.0, 'lam':650e-9, 'a':50e-6})
    free : list of parameter names to fit (e.g., ['I0','d','E','B0'])
    fit_envelope : whether to include sinc² envelope from slit width a
    background : 'constant', 'linear', or 'quadratic'
    source_width : if >0, convolve model with Gaussian of this sigma (m)
    compare_models : if True, run multiple configurations and return list of results.
    verbose : print progress

    Returns
    -------
    result or list of results (if compare_models)
    """
    if sigma_I is None:
        sigma_I = np.maximum(np.sqrt(np.maximum(I_data, 1e-9)), 1e-9)
    if fixed is None:
        fixed = {}
    if free is None:
        free = ['I0', 'd', 'E', 'B0']
        if 'L' not in fixed:
            free.append('L')
        if 'lam' not in fixed:
            free.append('lam')
        if fit_envelope and 'a' not in fixed:
            free.append('a')
        if source_width is not None and source_width > 0:
            free.append('sigma_src')

    # Define default bounds
    bounds = {}
    if 'I0' in free:
        bounds['I0'] = (0.01*np.max(I_data), 100*np.max(I_data))
    if 'd' in free:
        bounds['d'] = (1e-7, 5e-3)
    if 'L' in free:
        bounds['L'] = (0.05, 20.0)
    if 'lam' in free:
        bounds['lam'] = (300e-9, 1000e-9)
    if 'a' in free:
        bounds['a'] = (1e-6, 500e-6)
    if 'E' in free:
        bounds['E'] = (0.0, 1.0)
    if background == 'constant' and 'B0' in free:
        bounds['B0'] = (-0.5*np.max(I_data), 0.5*np.max(I_data))
    elif background == 'linear':
        if 'B0' in free:
            bounds['B0'] = (-0.5*np.max(I_data), 0.5*np.max(I_data))
        if 'B1' in free:
            bounds['B1'] = (-0.1*np.max(I_data)/(x_data[-1]-x_data[0]), 0.1*np.max(I_data)/(x_data[-1]-x_data[0]))
    elif background == 'quadratic':
        if 'B0' in free:
            bounds['B0'] = (-0.5*np.max(I_data), 0.5*np.max(I_data))
        if 'B1' in free:
            bounds['B1'] = (-0.1*np.max(I_data)/(x_data[-1]-x_data[0]), 0.1*np.max(I_data)/(x_data[-1]-x_data[0]))
        if 'B2' in free:
            bounds['B2'] = (-0.01*np.max(I_data)/(x_data[-1]-x_data[0])**2, 0.01*np.max(I_data)/(x_data[-1]-x_data[0])**2)
    if source_width is not None and source_width > 0 and 'sigma_src' in free:
        bounds['sigma_src'] = (0.0, 0.01)

    if compare_models:
        # Generate list of configurations to try
        configs = []
        # Base config: all free as specified
        configs.append({'free': free, 'fixed': fixed, 'background': background,
                        'fit_envelope': fit_envelope, 'source_width': source_width})
        # Without envelope
        if fit_envelope and 'a' in free:
            configs.append({'free': [p for p in free if p != 'a'],
                            'fixed': fixed,
                            'background': background,
                            'fit_envelope': False,
                            'source_width': source_width})
        # Without E (set E=0 fixed)
        if 'E' in free:
            new_fixed = fixed.copy()
            new_fixed['E'] = 0.0
            configs.append({'free': [p for p in free if p != 'E'],
                            'fixed': new_fixed,
                            'background': background,
                            'fit_envelope': fit_envelope,
                            'source_width': source_width})
        # With linear background instead of constant
        if background == 'constant' and 'B0' in free:
            new_free = [p for p in free if p != 'B0']
            new_free.extend(['B0','B1']) if 'B0' not in new_free else new_free.append('B1')
            configs.append({'free': new_free,
                            'fixed': fixed,
                            'background': 'linear',
                            'fit_envelope': fit_envelope,
                            'source_width': source_width})
        # With source width (if not already)
        if source_width is None or source_width == 0:
            configs.append({'free': free + ['sigma_src'],
                            'fixed': fixed,
                            'background': background,
                            'fit_envelope': fit_envelope,
                            'source_width': 0.001})  # initial guess

        results = []
        for cfg in configs:
            if verbose:
                print(f"\nTrying model: free={cfg['free']}, fixed={cfg['fixed']}, background={cfg['background']}, envelope={cfg['fit_envelope']}")
            try:
                best, chi2, success, msg = fit_model(
                    x_data, I_data, sigma_I,
                    fixed=cfg['fixed'],
                    free=cfg['free'],
                    fit_envelope=cfg['fit_envelope'],
                    background=cfg['background'],
                    source_width=cfg['source_width'],
                    bounds=bounds
                )
                if success:
                    n_params = len(cfg['free'])
                    n_data = len(x_data)
                    chi2_red = chi2 / (n_data - n_params)
                    aicc = compute_aicc(chi2, n_data, n_params)
                    bic = compute_bic(chi2, n_data, n_params)
                    model = double_slit_kernel(x_data, best.get('I0',1), best.get('d',0.5e-3), best.get('L',1), best.get('lam',650e-9),
                                               best.get('E',0), best.get('B',0), a=best.get('a',None),
                                               fit_envelope=cfg['fit_envelope'], background=cfg['background'])
                    if cfg['source_width'] is not None and cfg['source_width'] > 0:
                        model = convolve_with_source(model, x_data, cfg['source_width'])
                    resid = (I_data - model) / sigma_I
                    resid_stats = analyse_residuals(resid)
                    results.append(RealDataResult(
                        best_params=best,
                        chi2_min=chi2,
                        chi2_red=chi2_red,
                        n_data=n_data,
                        n_params=n_params,
                        aicc=aicc,
                        bic=bic,
                        residual_stats=resid_stats,
                        success=success,
                        message=msg,
                        fixed_spec=cfg['fixed'],
                        free_list=cfg['free'],
                        background=cfg['background'],
                        source_width=cfg['source_width'],
                        fit_envelope=cfg['fit_envelope'],
                        runtime=0
                    ))
                else:
                    if verbose:
                        print(f"  Fit failed: {msg}")
            except Exception as e:
                if verbose:
                    print(f"  Exception: {e}")
        # Return results sorted by AICc
        results.sort(key=lambda r: r.aicc)
        if verbose:
            print("\nModel comparison (sorted by AICc):")
            for i, r in enumerate(results):
                print(f"{i+1}. AICc={r.aicc:.2f}, BIC={r.bic:.2f}, params={len(r.free_list)}, background={r.background}, envelope={r.fit_envelope}, source={r.source_width}")
        return results
    else:
        # Single fit
        start = time.time()
        best, chi2, success, msg = fit_model(x_data, I_data, sigma_I,
                                             fixed=fixed, free=free,
                                             fit_envelope=fit_envelope,
                                             background=background,
                                             source_width=source_width,
                                             bounds=bounds)
        runtime = time.time() - start
        n_params = len(free)
        n_data = len(x_data)
        chi2_red = chi2 / (n_data - n_params) if n_data > n_params else np.inf
        aicc = compute_aicc(chi2, n_data, n_params)
        bic = compute_bic(chi2, n_data, n_params)
        model = double_slit_kernel(x_data, best.get('I0',1), best.get('d',0.5e-3), best.get('L',1), best.get('lam',650e-9),
                                   best.get('E',0), best.get('B',0), a=best.get('a',None),
                                   fit_envelope=fit_envelope, background=background)
        if source_width is not None and source_width > 0:
            model = convolve_with_source(model, x_data, source_width)
        resid = (I_data - model) / sigma_I
        resid_stats = analyse_residuals(resid)
        return RealDataResult(
            best_params=best,
            chi2_min=chi2,
            chi2_red=chi2_red,
            n_data=n_data,
            n_params=n_params,
            aicc=aicc,
            bic=bic,
            residual_stats=resid_stats,
            success=success,
            message=msg,
            fixed_spec=fixed,
            free_list=free,
            background=background,
            source_width=source_width,
            fit_envelope=fit_envelope,
            runtime=runtime
        )

# ==================================================================
# 7. Plotting function for real data results
# ==================================================================
def plot_real_data_result(x_data: np.ndarray,
                          I_data: np.ndarray,
                          result: RealDataResult,
                          sigma_I: np.ndarray,
                          title: str = "Double-slit inversion (real data)",
                          filename: Optional[str] = None):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # Model
    model = double_slit_kernel(x_data,
                               result.best_params.get('I0',1),
                               result.best_params.get('d',0.5e-3),
                               result.best_params.get('L',1),
                               result.best_params.get('lam',650e-9),
                               result.best_params.get('E',0),
                               result.best_params.get('B',0),
                               a=result.best_params.get('a',None),
                               fit_envelope=result.fit_envelope,
                               background=result.background)
    if result.source_width is not None and result.source_width > 0:
        model = convolve_with_source(model, x_data, result.source_width)

    resid = (I_data - model) / sigma_I
    xmm = x_data * 1e3

    # Panel 1: data and fit
    ax = axes[0,0]
    ax.plot(xmm, I_data, '.', ms=2, alpha=0.5, label='Data')
    ax.plot(xmm, model, 'b-', lw=2, label='Fit')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('Intensity (a.u.)')
    ax.set_title(f'Fit, χ²_red = {result.chi2_red:.3f}')
    ax.legend()
    ax.grid(alpha=0.3)

    # Panel 2: residuals
    ax = axes[0,1]
    ax.plot(xmm, resid, '.', ms=2, alpha=0.6, color='steelblue')
    ax.axhline(0, color='k', lw=1.5)
    ax.axhline(1, color='g', ls='--', label='+1σ')
    ax.axhline(-1, color='g', ls='--', label='-1σ')
    ax.fill_between(xmm, -1, 1, alpha=0.1, color='green')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('Residual (σ)')
    ax.set_title(f'Residuals, std={np.std(resid):.3f}')
    ax.legend()
    ax.grid(alpha=0.3)

    # Panel 3: histogram of residuals + normal curve
    ax = axes[1,0]
    ax.hist(resid, bins='auto', density=True, alpha=0.7, color='steelblue')
    x0 = np.linspace(-3, 3, 200)
    ax.plot(x0, norm.pdf(x0, 0, 1), 'r-', lw=2, label='N(0,1)')
    ax.set_xlabel('Residual (σ)')
    ax.set_ylabel('Density')
    ax.set_title(f"Residuals normality (Shapiro p={result.residual_stats['shapiro_p']:.3f})")
    ax.legend()
    ax.grid(alpha=0.3)

    # Panel 4: parameter summary
    ax = axes[1,1]
    ax.axis('off')
    txt = f"Fixed: {result.fixed_spec}\nFree: {result.free_list}\nBackground: {result.background}\nEnvelope: {result.fit_envelope}\nSource width: {result.source_width}\n\n"
    txt += f"I0 = {result.best_params.get('I0',0):.3f}\n"
    txt += f"d = {result.best_params.get('d',0)*1e6:.2f} µm\n"
    txt += f"E = {result.best_params.get('E',0):.5f}\n"
    if 'a' in result.best_params:
        txt += f"a = {result.best_params['a']*1e6:.2f} µm\n"
    txt += f"χ²_red = {result.chi2_red:.3f}\nAICc = {result.aicc:.2f}\nBIC = {result.bic:.2f}"
    ax.text(0.05, 0.95, txt, transform=ax.transAxes, va='top', fontsize=10, family='monospace')
    ax.set_title("Parameter estimates")

    plt.tight_layout(rect=[0,0.01,1,0.95])
    if filename:
        plt.savefig(filename, dpi=170, bbox_inches='tight')
    plt.show()

# ==================================================================
# 8. Example with synthetic data (for demonstration)
# ==================================================================
if __name__ == "__main__":
    np.random.seed(42)
    # Generate synthetic data with known parameters
    true = {'I0':100.0, 'd':0.5e-3, 'L':1.0, 'lam':650e-9, 'a':50e-6, 'E':0.3, 'B0':5.0}
    x = np.linspace(-0.01, 0.01, 500)
    model_true = double_slit_kernel(x, true['I0'], true['d'], true['L'], true['lam'], true['E'],
                                    [true['B0']], a=true['a'], fit_envelope=True, background='constant')
    I_data = np.random.poisson(np.maximum(model_true, 1e-9))
    sigma_I = np.sqrt(np.maximum(I_data, 1e-9))

    # Run with fixed L, lam, a and free I0, d, E, B0
    result = invert_real_data(x, I_data, sigma_I,
                              fixed={'L':1.0, 'lam':650e-9, 'a':50e-6},
                              free=['I0','d','E','B0'],
                              fit_envelope=True,
                              background='constant',
                              compare_models=False,
                              verbose=True)
    plot_real_data_result(x, I_data, result, sigma_I, title="DTQEM v25.0 – Real-data inversion demo")
    print("\nBest parameters:", result.best_params)
    print("Residual stats:", result.residual_stats)
