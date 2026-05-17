# ================================================================
# DTQEM v22.0 – Production-Grade Self-Calibrating Inversion
#
# This code implements the complete three-stage inversion protocol
# for hydrogen-like atomic spectra. It recovers temperature (T),
# dephasing coefficient (alpha), and unknown observer strength (E)
# from three sets of FWHM linewidth measurements:
#   (1) at E = 0          (no observer)
#   (2) at E = E_cal      (known calibration observer strength)
#   (3) at E = E_unk      (unknown observer strength to be inferred)
#
# Key improvements over v21.0:
#   [1] Bootstrap uncertainty quantification (sigma_T, sigma_alpha, sigma_E)
#   [2] Consistency check: per-line alpha dispersion < threshold
#   [3] Convergence guard on all minimizations (residual check)
#   [4] Corrected hydrogen mass: m_H = m_p + m_e
#   [5] T_max and E_max as user parameters (no hard-coded limits)
#   [6] InversionResult dataclass — structured output
#   [7] Full warnings module integration
#   [8] Publication-quality figure with uncertainty bands
#
# Author: DTQEM Team
# License: CC BY-NC 4.0
# ================================================================

import warnings
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple
from scipy.optimize import minimize_scalar
from scipy.constants import c, k, m_p, m_e

# ================================================================
# 1. Physical constants and Balmer series
# ================================================================
C_LIGHT = c                       # m/s
K_B     = k                       # J/K
M_H     = m_p + m_e               # kg — hydrogen atom (proton + electron)

HYDROGEN_LINES: Dict[str, dict] = {
    'Hα': {'lambda_nm': 656.28, 'A_si': 4.41e7},
    'Hβ': {'lambda_nm': 486.13, 'A_si': 8.42e6},
    'Hγ': {'lambda_nm': 434.05, 'A_si': 2.53e6},
    'Hδ': {'lambda_nm': 410.17, 'A_si': 9.73e5},
}

T_REF     = 300.0
ALPHA_REF = (1.0 / C_LIGHT) * np.sqrt(2.0 * K_B * T_REF / M_H)

# ================================================================
# 2. Structured output: InversionResult
# ================================================================
@dataclass
class InversionResult:
    """Container for inversion results with diagnostics."""
    T_K:         float = np.nan
    alpha:       float = np.nan
    E:           float = np.nan
    sigma_T:     float = np.nan
    sigma_alpha: float = np.nan
    sigma_E:     float = np.nan
    alpha_per_line:     Dict[str, float] = field(default_factory=dict)
    alpha_consistency:  float = np.nan
    T_residual:         float = np.nan
    E_residual:         float = np.nan
    converged:          bool  = False
    warnings:           list  = field(default_factory=list)

    def summary(self):
        """Print a nicely formatted summary."""
        print("=" * 56)
        print("  DTQEM v22.0 – Inversion Result")
        print("=" * 56)
        print(f"  T     = {self.T_K:.2f} ± {self.sigma_T:.2f} K")
        print(f"  α     = {self.alpha:.4e} ± {self.sigma_alpha:.1e}  "
              f"(α/α_ref = {self.alpha/ALPHA_REF:.4f})")
        print(f"  E     = {self.E:.5f} ± {self.sigma_E:.5f}")
        print(f"  α consistency (σ/μ): {self.alpha_consistency:.4f}"
              f"  {'✓ OK' if self.alpha_consistency < 0.05 else '⚠ inconsistent'}")
        print(f"  T residual: {self.T_residual:.2e}  |  "
              f"E residual: {self.E_residual:.2e}")
        print(f"  Converged: {self.converged}")
        if self.warnings:
            for w in self.warnings:
                print(f"  ⚠ {w}")
        print("-" * 56)
        print("  Per-line α calibration:")
        for name, a in self.alpha_per_line.items():
            print(f"    {name}: {a:.4e}  (α/α_ref = {a/ALPHA_REF:.4f})")
        print("=" * 56)

# ================================================================
# 3. Forward model
# ================================================================
def omega0(lambda_nm: float) -> float:
    """Angular frequency ω₀ (rad/s) from wavelength (nm)."""
    return 2.0 * np.pi * C_LIGHT / (lambda_nm * 1e-9)

def gamma_doppler(om: float, T: float) -> float:
    """1‑sigma Doppler decoherence rate (rad/s)."""
    return (om / C_LIGHT) * np.sqrt(2.0 * K_B * T / M_H)

def gamma_total(om: float, A_si: float, T: float,
                alpha: float, E: float) -> float:
    """Total decoherence rate (rad/s): natural + Doppler + dephasing."""
    return A_si + gamma_doppler(om, T) + alpha * om * (1.0 + E)

def fwhm_hz(om: float, A_si: float, T: float,
            alpha: float, E: float) -> float:
    """Lorentzian FWHM linewidth in Hz."""
    return gamma_total(om, A_si, T, alpha, E) / (2.0 * np.pi)

def generate_fwhm(T: float, alpha: float, E: float,
                  lines: dict = HYDROGEN_LINES) -> Dict[str, float]:
    """Generate synthetic FWHM measurements for all Balmer lines."""
    return {n: fwhm_hz(omega0(d['lambda_nm']), d['A_si'], T, alpha, E)
            for n, d in lines.items()}

# ================================================================
# 4. Stage 0: Alpha calibration (T-independent)
#    ΔΓ_i = Γ_i(E_cal) − Γ_i(E=0) = α · ω₀_i · E_cal
# ================================================================
def calibrate_alpha(
    fwhm_E0:   Dict[str, float],
    fwhm_Ecal: Dict[str, float],
    E_cal:     float,
    lines:     dict = HYDROGEN_LINES,
    consistency_threshold: float = 0.05,
) -> Tuple[float, Dict[str, float], float, list]:
    """
    Calibrate α from differential measurements at E=0 and E=E_cal.

    Returns
    -------
    alpha_inf      : weighted mean alpha
    alpha_per_line : per-line alpha dict
    consistency    : std/mean (0 = perfect)
    warns          : list of warning strings
    """
    alphas, weights, apl, warns = [], [], {}, []

    for name, data in lines.items():
        om = omega0(data['lambda_nm'])
        dg = (fwhm_Ecal[name] - fwhm_E0[name]) * 2.0 * np.pi
        a_i = dg / (om * E_cal)
        apl[name] = a_i
        if a_i > 0:
            alphas.append(a_i)
            weights.append(om)
        else:
            warns.append(f"Negative alpha for {name} — check E_cal sign or data")

    if not alphas:
        warns.append("All per-line alphas negative — returning ALPHA_REF as fallback")
        return ALPHA_REF, apl, np.nan, warns

    w = np.array(weights)
    a = np.array(alphas)
    alpha_inf = float(np.sum(w * a) / np.sum(w))
    consistency = float(np.std(a) / alpha_inf) if alpha_inf > 0 else np.nan

    if consistency > consistency_threshold:
        warns.append(
            f"Alpha consistency σ/μ = {consistency:.4f} > {consistency_threshold} "
            f"— per-line variability detected (instrument drift?)"
        )
    return alpha_inf, apl, consistency, warns

# ================================================================
# 5. Stage 1: Temperature inference
# ================================================================
def infer_temperature(
    fwhm_E0: Dict[str, float],
    alpha:   float,
    T_min:   float = 10.0,
    T_max:   float = 100_000.0,
    residual_tol: float = 1e-8,
    lines:   dict  = HYDROGEN_LINES,
) -> Tuple[float, float, list]:
    """
    Infer T (K) from E=0 measurements using known α.

    Returns T_inf, residual, warns.
    """
    warns = []

    def objective(T: float) -> float:
        if T <= 0:
            return 1e30
        err = 0.0
        for n, d in lines.items():
            om = omega0(d['lambda_nm'])
            model = fwhm_hz(om, d['A_si'], T, alpha, 0.0)
            err += np.log(model / fwhm_E0[n]) ** 2
        return err

    res = minimize_scalar(objective, bounds=(T_min, T_max), method='bounded',
                          options={'xatol': 1e-6})
    residual = float(res.fun)

    if residual > residual_tol:
        warns.append(f"T inference residual = {residual:.2e} > tol {residual_tol:.0e} "
                     f"— consider widening T bounds or checking alpha")
    if res.x <= T_min * 1.01 or res.x >= T_max * 0.99:
        warns.append(f"T_inf = {res.x:.1f} K is at search boundary — increase T_max")

    return float(res.x), residual, warns

# ================================================================
# 6. Stage 2: Observer strength inference
# ================================================================
def infer_E(
    fwhm_Eunk: Dict[str, float],
    T:         float,
    alpha:     float,
    E_min:     float = 0.0,
    E_max:     float = 10.0,
    residual_tol: float = 1e-8,
    lines:     dict  = HYDROGEN_LINES,
) -> Tuple[float, float, list]:
    """
    Infer E from measurements at unknown observer strength.

    Returns E_inf, residual, warns.
    """
    warns = []

    def objective(E: float) -> float:
        if E < 0:
            return 1e30
        err = 0.0
        for n, d in lines.items():
            om = omega0(d['lambda_nm'])
            model = fwhm_hz(om, d['A_si'], T, alpha, E)
            err += np.log(model / fwhm_Eunk[n]) ** 2
        return err

    res = minimize_scalar(objective, bounds=(E_min, E_max), method='bounded',
                          options={'xatol': 1e-8})
    residual = float(res.fun)

    if residual > residual_tol:
        warns.append(f"E inference residual = {residual:.2e} > tol {residual_tol:.0e}")
    if res.x >= E_max * 0.99:
        warns.append(f"E_inf = {res.x:.4f} at upper boundary — increase E_max")

    return float(res.x), residual, warns

# ================================================================
# 7. Bootstrap uncertainty quantification
# ================================================================
def bootstrap_uncertainty(
    fwhm_E0:   Dict[str, float],
    fwhm_Ecal: Dict[str, float],
    fwhm_Eunk: Dict[str, float],
    E_cal:     float,
    noise_est: float = 0.01,
    N:         int   = 500,
    seed:      int   = 42,
    lines:     dict  = HYDROGEN_LINES,
) -> Tuple[float, float, float]:
    """
    Estimate 1‑sigma uncertainties via multiplicative noise bootstrap.

    Parameters
    ----------
    noise_est : fractional noise level (e.g. 0.01 = 1%)
    N         : number of bootstrap trials

    Returns sigma_T, sigma_alpha, sigma_E
    """
    rng = np.random.default_rng(seed)
    T_samples, a_samples, E_samples = [], [], []

    for _ in range(N):
        f0n = {nm: v * (1 + noise_est * rng.standard_normal()) for nm, v in fwhm_E0.items()}
        f1n = {nm: v * (1 + noise_est * rng.standard_normal()) for nm, v in fwhm_Ecal.items()}
        fun = {nm: v * (1 + noise_est * rng.standard_normal()) for nm, v in fwhm_Eunk.items()}

        a_i, _, _, _ = calibrate_alpha(f0n, f1n, E_cal, lines)
        T_i, _, _    = infer_temperature(f0n, a_i, lines=lines)
        E_i, _, _    = infer_E(fun, T_i, a_i, lines=lines)

        T_samples.append(T_i)
        a_samples.append(a_i)
        E_samples.append(E_i)

    return (float(np.std(T_samples)),
            float(np.std(a_samples)),
            float(np.std(E_samples)))

# ================================================================
# 8. Full v22.0 pipeline
# ================================================================
def invert_v22(
    fwhm_E0:   Dict[str, float],
    fwhm_Ecal: Dict[str, float],
    E_cal:     float,
    fwhm_Eunk: Dict[str, float],
    noise_est: float = 0.01,
    N_bootstrap: int = 500,
    T_max:     float = 100_000.0,
    E_max:     float = 10.0,
    lines:     dict  = HYDROGEN_LINES,
    verbose:   bool  = True,
) -> InversionResult:
    """
    Full three‑stage self‑calibrating inversion with uncertainty quantification.

    Parameters
    ----------
    fwhm_E0    : FWHM measurements at E = 0         {line_name: Hz}
    fwhm_Ecal  : FWHM measurements at E = E_cal     {line_name: Hz}
    E_cal      : known calibration observer strength (float > 0)
    fwhm_Eunk  : FWHM measurements at unknown E     {line_name: Hz}
    noise_est  : fractional noise level for bootstrap (default 1%)
    N_bootstrap: number of bootstrap samples
    T_max      : upper bound for T search (K)
    E_max      : upper bound for E search
    verbose    : print warnings in real time

    Returns
    -------
    InversionResult dataclass with all estimates and diagnostics
    """
    result = InversionResult()
    all_warns = []

    # Stage 0: alpha calibration (T‑independent)
    alpha_inf, apl, consistency, w0 = calibrate_alpha(fwhm_E0, fwhm_Ecal, E_cal, lines)
    result.alpha = alpha_inf
    result.alpha_per_line = apl
    result.alpha_consistency = consistency
    all_warns.extend(w0)

    # Stage 1: temperature
    T_inf, T_res, w1 = infer_temperature(fwhm_E0, alpha_inf, T_max=T_max, lines=lines)
    result.T_K = T_inf
    result.T_residual = T_res
    all_warns.extend(w1)

    # Stage 2: observer strength
    E_inf, E_res, w2 = infer_E(fwhm_Eunk, T_inf, alpha_inf, E_max=E_max, lines=lines)
    result.E = E_inf
    result.E_residual = E_res
    all_warns.extend(w2)

    # Bootstrap uncertainty
    sT, sa, sE = bootstrap_uncertainty(fwhm_E0, fwhm_Ecal, fwhm_Eunk,
                                       E_cal, noise_est=noise_est,
                                       N=N_bootstrap, lines=lines)
    result.sigma_T = sT
    result.sigma_alpha = sa
    result.sigma_E = sE

    # Convergence flag
    result.converged = (T_res < 1e-6 and E_res < 1e-6 and consistency < 0.05)
    result.warnings = all_warns

    if verbose and all_warns:
        for w in all_warns:
            warnings.warn(w, UserWarning, stacklevel=2)

    return result

# ================================================================
# 9. Demo and validation
# ================================================================
if __name__ == "__main__":
    # True parameters (unknown in real experiment)
    T_true     = 800.0
    alpha_true = ALPHA_REF * 2.0
    E_cal      = 1.0
    E_true     = 0.7

    print(f"ALPHA_REF = {ALPHA_REF:.4e}  (g_dep = g_Doppler at {T_REF} K)")

    # Generate synthetic "measured" FWHM data
    fwhm_E0   = generate_fwhm(T_true, alpha_true, 0.0)
    fwhm_Ecal = generate_fwhm(T_true, alpha_true, E_cal)
    fwhm_Eunk = generate_fwhm(T_true, alpha_true, E_true)

    # Full inversion with uncertainty
    res = invert_v22(fwhm_E0, fwhm_Ecal, E_cal, fwhm_Eunk,
                     noise_est=0.01, N_bootstrap=500)
    res.summary()

    print(f"\n  True values: T = {T_true} K,  α = {alpha_true:.4e},  E = {E_true}")
    print(f"  Errors: dT = {100*abs(res.T_K-T_true)/T_true:.4f}%,  "
          f"dα = {100*abs(res.alpha-alpha_true)/alpha_true:.4f}%,  "
          f"dE = {abs(res.E-E_true):.6f}")

    # Noise robustness sweep
    print("\n--- Noise robustness (200 trials each) ---")
    noise_levels = [0, 0.5, 1.0, 2.0, 5.0]
    noise_records = []
    np.random.seed(42)

    for noise_pct in noise_levels:
        dTs, das, dEs = [], [], []
        n = noise_pct / 100.0
        for _ in range(200):
            f0n = {nm: v*(1+n*np.random.randn()) for nm,v in fwhm_E0.items()}
            f1n = {nm: v*(1+n*np.random.randn()) for nm,v in fwhm_Ecal.items()}
            fun = {nm: v*(1+n*np.random.randn()) for nm,v in fwhm_Eunk.items()}
            r = invert_v22(f0n, f1n, E_cal, fun,
                           noise_est=n if n>0 else 0.001,
                           N_bootstrap=100, verbose=False)
            dTs.append(100*abs(r.T_K - T_true)/T_true)
            das.append(100*abs(r.alpha - alpha_true)/alpha_true)
            dEs.append(abs(r.E - E_true))
        noise_records.append({
            'noise_%': noise_pct,
            'dT_med':  np.median(dTs), 'dT_p95': np.percentile(dTs, 95),
            'da_med':  np.median(das), 'da_p95': np.percentile(das, 95),
            'dE_med':  np.median(dEs), 'dE_p95': np.percentile(dEs, 95),
        })
        r_ = noise_records[-1]
        print(f"  {noise_pct:4.1f}%  dT_med={r_['dT_med']:6.3f}%  "
              f"da_med={r_['da_med']:6.3f}%  dE_med={r_['dE_med']:.4f}")

    # Save noise robustness table
    pd.DataFrame(noise_records).to_csv('dtqem_v22_noise_robustness.csv', index=False)

    # Publication‑quality figure
    df = pd.DataFrame(noise_records)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle('DTQEM v22.0 – Inversion Uncertainty & Robustness',
                 fontsize=13, fontweight='bold')

    # Panel 1: noise robustness with uncertainty bands
    ax = axes[0]
    nl = df['noise_%']
    ax.fill_between(nl, df['dT_p95'], alpha=0.15, color='steelblue')
    ax.plot(nl, df['dT_med'], 'o-', color='steelblue', lw=2.5, ms=7,
            label='ΔT/T median')
    ax.plot(nl, df['dT_p95'], 's--', color='steelblue', lw=1.5, ms=5,
            label='ΔT/T 95th%')
    ax2 = ax.twinx()
    ax2.fill_between(nl, df['dE_p95'], alpha=0.15, color='darkorange')
    ax2.plot(nl, df['dE_med'], 'o-', color='darkorange', lw=2.5, ms=7,
             label='ΔE median')
    ax2.plot(nl, df['dE_p95'], 's--', color='darkorange', lw=1.5, ms=5,
             label='ΔE 95th%')
    ax.set_xlabel('Measurement noise (%)', fontsize=11)
    ax.set_ylabel('ΔT/T (%)', color='steelblue', fontsize=11)
    ax2.set_ylabel('ΔE (absolute)', color='darkorange', fontsize=11)
    ax.set_title(f'Robustness (T={T_true}K, α=2×α_ref, E={E_true})', fontsize=10)
    h1,l1 = ax.get_legend_handles_labels()
    h2,l2 = ax2.get_legend_handles_labels()
    ax.legend(h1+h2, l1+l2, fontsize=9, loc='upper left')
    ax.grid(alpha=0.3)

    # Panel 2: all parameters vs noise
    ax3 = axes[1]
    ax3.plot(nl, df['dT_med'], 'o-', color='steelblue', lw=2.5, label='ΔT/T median (%)')
    ax3.plot(nl, df['da_med'], '^-', color='green', lw=2.5, label='Δα/α median (%)')
    ax4 = ax3.twinx()
    ax4.plot(nl, df['dE_med'], 's-', color='darkorange', lw=2.5, label='ΔE median')
    ax3.set_xlabel('Measurement noise (%)', fontsize=11)
    ax3.set_ylabel('Relative error (%)', fontsize=11)
    ax4.set_ylabel('ΔE (absolute)', color='darkorange', fontsize=11)
    ax3.set_title('All three parameters vs noise', fontsize=10)
    h3,l3 = ax3.get_legend_handles_labels()
    h4,l4 = ax4.get_legend_handles_labels()
    ax3.legend(h3+h4, l3+l4, fontsize=9, loc='upper left')
    ax3.grid(alpha=0.3)

    plt.tight_layout(rect=[0, 0.01, 1, 0.95])
    plt.savefig('dtqem_v22_inversion.png', dpi=180, bbox_inches='tight')
    plt.show()

    print("\n✅ Files saved: dtqem_v22_noise_robustness.csv , dtqem_v22_inversion.png")
