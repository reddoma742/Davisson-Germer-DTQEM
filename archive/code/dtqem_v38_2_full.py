"""
DTQEM v38.2-final – Hydrogen Balmer-alpha Zeeman Inversion
===========================================================
Author  : Reddouane Berramdane
Developed & Programmed with AI Assistance from DeepSeek, Gemini, and Claude.

License : CC BY-NC 4.0

النسخة الكاملة الموحدة — كل الأجزاء في ملف واحد
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution, minimize
from scipy.special  import gammaln
from dataclasses    import dataclass, field
from typing         import Dict, List, Optional, Tuple
from pathlib        import Path
import csv, sys, time, warnings
import scipy

warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════
# 0. CONSTANTES PHYSIQUES (CODATA 2018)
# ══════════════════════════════════════════════════════════════════
class PhysicalConstants:
    C           = 299_792_458.0
    H           = 6.626_070_15e-34
    HBAR        = H / (2.0 * np.pi)
    E_CHARGE    = 1.602_176_634e-19
    M_E         = 9.109_383_701_5e-31
    MU_B        = E_CHARGE * HBAR / (2.0 * M_E)
    MU_B_OVER_H = MU_B / H

PC          = PhysicalConstants
C           = PC.C
MU_B        = PC.MU_B
MU_B_OVER_H = PC.MU_B_OVER_H

assert 9.273e-24 < MU_B < 9.275e-24, \
    f"ERREUR μ_B = {MU_B:.6e} J/T"

# ══════════════════════════════════════════════════════════════════
# 1. PARAMÉTRAGE DU TRIPLET
# ══════════════════════════════════════════════════════════════════
def triplet_param_info(fix_frac: bool,
                       subtract_continuum: bool) -> Dict:
    """
    Source unique de vérité pour l'ordre et le nombre de paramètres.

    Ordre canonique dans le vecteur x :
        [0] lambda_center
        [1] B
        [2] amplitude
        [3] sigma_width
        [4] frac_side      (si NOT fix_frac)
        [4|5] background   (si NOT subtract_continuum)
    """
    idx = {'idx_lc': 0, 'idx_B': 1, 'idx_amp': 2, 'idx_sig': 3}
    n = 4
    if fix_frac:
        idx['idx_frac'] = None
    else:
        idx['idx_frac'] = n
        n += 1
    if subtract_continuum:
        idx['idx_bg'] = None
    else:
        idx['idx_bg'] = n
        n += 1
    return {
        **idx,
        'n_params'          : n,
        'fix_frac'          : fix_frac,
        'subtract_continuum': subtract_continuum,
    }

def unpack_triplet(x: np.ndarray, info: Dict) -> Tuple:
    """Décompresse x → (lc, B, amp, sig, frac, bg). Toujours 6 valeurs."""
    lc   = x[info['idx_lc']]
    B    = x[info['idx_B']]
    amp  = x[info['idx_amp']]
    sig  = x[info['idx_sig']]
    frac = 0.60 if info['idx_frac'] is None else x[info['idx_frac']]
    bg   = 0.0  if info['idx_bg']   is None else x[info['idx_bg']]
    return lc, B, amp, sig, frac, bg

def pack_triplet(lc: float, B: float, amp: float, sig: float,
                 frac: float, bg: float, info: Dict) -> np.ndarray:
    """Construit x à partir des valeurs scalaires."""
    x = np.empty(info['n_params'])
    x[info['idx_lc']]  = lc
    x[info['idx_B']]   = B
    x[info['idx_amp']] = amp
    x[info['idx_sig']] = sig
    if info['idx_frac'] is not None:
        x[info['idx_frac']] = frac
    if info['idx_bg'] is not None:
        x[info['idx_bg']] = bg
    return x

def build_triplet_bounds(wl: np.ndarray, I: np.ndarray,
                          info: Dict) -> List[Tuple[float, float]]:
    """
    Bornes physiquement motivées.
    Garantit : len(bounds) == info['n_params'].
    """
    I_max   = float(np.max(I))
    lc_est  = float(wl[np.argmax(I)])
    wl_span = float(wl[-1] - wl[0])

    bounds = [
        (lc_est - 0.5 * wl_span, lc_est + 0.5 * wl_span),
        (0.0,  3.0),
        (0.05 * I_max, 15.0 * I_max),
        (0.001e-9, 0.08e-9),
    ]
    if info['idx_frac'] is not None:
        bounds.append((0.3, 0.9))
    if info['idx_bg'] is not None:
        bounds.append((0.0, 0.3 * I_max))

    assert len(bounds) == info['n_params'], \
        f"ERREUR: len(bounds)={len(bounds)} ≠ n_params={info['n_params']}"
    return bounds

def build_triplet_x0(wl: np.ndarray, I: np.ndarray,
                      info: Dict) -> np.ndarray:
    """Point de départ déterministe pour l'optimisation."""
    I_max  = float(np.max(I))
    lc_est = float(wl[np.argmax(I)])
    return pack_triplet(lc_est, 0.5, 1.2 * I_max,
                         0.008e-9, 0.60, 0.01 * I_max, info)

# ══════════════════════════════════════════════════════════════════
# 2. PROFILS SPECTRAUX
# ══════════════════════════════════════════════════════════════════
def _gaussian(wl: np.ndarray, c: float, s: float) -> np.ndarray:
    return np.exp(-0.5 * ((wl - c) / s) ** 2)

def triplet_spectrum(wl: np.ndarray,
                     lc: float, B: float,
                     amp: float, sig: float,
                     frac: float = 0.60,
                     bg:   float = 0.0) -> np.ndarray:
    """
    Triplet Zeeman symétrique Hα :
        π  (Δm=0)  : amp × G(lc)
        σ± (Δm=±1) : amp × frac × G(lc ± Δλ)

    Δλ = (lc²/c) × (μ_B/h) × g_eff × |B|,  g_eff = 1.0
    """
    G_EFF     = 1.0
    delta_lam = (lc ** 2 / C) * MU_B_OVER_H * G_EFF * abs(B)
    model  = amp               * _gaussian(wl, lc,             sig)
    model += amp * frac        * _gaussian(wl, lc + delta_lam, sig)
    model += amp * frac        * _gaussian(wl, lc - delta_lam, sig)
    return model + bg

def single_spectrum(wl: np.ndarray,
                    lc: float, amp: float,
                    sig: float, bg: float = 0.0) -> np.ndarray:
    return amp * _gaussian(wl, lc, sig) + bg

# ══════════════════════════════════════════════════════════════════
# 3. FONCTIONS OBJECTIF
# ══════════════════════════════════════════════════════════════════
def poisson_nll(y: np.ndarray, mu: np.ndarray) -> float:
    """NLL Poisson complète (terme de Stirling inclus)."""
    mu = np.maximum(mu, 1e-12)
    y  = np.maximum(y,  0.0)
    return float(np.sum(mu - y * np.log(mu) + gammaln(y + 1.0)))

def obj_triplet(x: np.ndarray, wl: np.ndarray,
                I: np.ndarray, info: Dict) -> float:
    lc, B, amp, sig, frac, bg = unpack_triplet(x, info)
    return poisson_nll(I, triplet_spectrum(wl, lc, B, amp, sig, frac, bg))

def obj_single_fn(x: np.ndarray, wl: np.ndarray,
                  I: np.ndarray, has_bg: bool) -> float:
    if has_bg:
        lc, amp, sig, bg = x
    else:
        lc, amp, sig = x
        bg = 0.0
    return poisson_nll(I, single_spectrum(wl, lc, amp, sig, bg))

# ══════════════════════════════════════════════════════════════════
# 4. AJUSTEMENT
# ══════════════════════════════════════════════════════════════════
def fit_triplet(wl: np.ndarray, I: np.ndarray,
                subtract_continuum: bool = True,
                fix_frac: bool = True,
                ) -> Tuple[Dict, float, bool, np.ndarray, Dict]:
    """
    Ajustement du modèle triplet Zeeman.
    Stratégie : DE global → L-BFGS-B local.

    Returns
    -------
    params  : dict des paramètres nommés
    nll     : NLL à l'optimum
    success : bool
    x_opt   : vecteur optimal
    info    : dictionnaire de paramétrage
    """
    info   = triplet_param_info(fix_frac, subtract_continuum)
    bounds = build_triplet_bounds(wl, I, info)
    x0     = build_triplet_x0(wl, I, info)
    for k, (lo, hi) in enumerate(bounds):
        x0[k] = np.clip(x0[k], lo, hi)

    def obj(x):
        return obj_triplet(x, wl, I, info)

    res_de = differential_evolution(
        obj, bounds,
        maxiter=40, popsize=10, seed=42,
        disp=False, workers=1, updating='deferred',
        atol=1e-10, tol=1e-10, polish=True,
    )
    res = minimize(
        obj, res_de.x, method='L-BFGS-B', bounds=bounds,
        options={'ftol': 1e-14, 'gtol': 1e-10, 'maxiter': 5000},
    )
    x_opt = res.x
    lc, B, amp, sig, frac, bg = unpack_triplet(x_opt, info)
    params = {
        'lambda_center': float(lc),
        'B'            : float(B),
        'amplitude'    : float(amp),
        'sigma_width'  : float(sig),
        'frac_side'    : float(frac),
        'background'   : float(bg),
    }
    return params, float(res.fun), bool(res.success), x_opt, info

def fit_single(wl: np.ndarray, I: np.ndarray,
               subtract_continuum: bool = True,
               ) -> Tuple[Dict, float, bool, np.ndarray]:
    """Ajustement du modèle Single Gaussien."""
    I_max  = float(np.max(I))
    lc_est = float(wl[np.argmax(I)])
    has_bg = not subtract_continuum
    bounds = [
        (lc_est - 0.1e-9, lc_est + 0.1e-9),
        (0.05 * I_max, 10.0 * I_max),
        (0.001e-9, 0.08e-9),
    ]
    if has_bg:
        bounds.append((0.0, 0.3 * I_max))
    x0 = np.array(
        [lc_est, 1.2 * I_max, 0.008e-9] +
        ([0.01 * I_max] if has_bg else [])
    )
    for k, (lo, hi) in enumerate(bounds):
        x0[k] = np.clip(x0[k], lo, hi)

    def obj(x):
        return obj_single_fn(x, wl, I, has_bg)

    res_de = differential_evolution(
        obj, bounds,
        maxiter=40, popsize=10, seed=42,
        disp=False, workers=1, updating='deferred', polish=True,
    )
    res = minimize(
        obj, res_de.x, method='L-BFGS-B', bounds=bounds,
        options={'ftol': 1e-14, 'gtol': 1e-10, 'maxiter': 5000},
    )
    x   = res.x
    lc  = float(x[0])
    amp = float(x[1])
    sig = float(x[2])
    bg  = float(x[3]) if has_bg else 0.0
    params = {
        'lambda_center': lc,
        'B'            : 0.0,
        'amplitude'    : amp,
        'sigma_width'  : sig,
        'background'   : bg,
    }
    return params, float(res.fun), bool(res.success), res.x

# ══════════════════════════════════════════════════════════════════
# 5. STATISTIQUES ET SÉLECTION DE MODÈLE
# ══════════════════════════════════════════════════════════════════
def aicc(nll: float, n: int, k: int) -> float:
    denom = n - k - 1
    if denom <= 0:
        return np.inf
    return 2 * k + 2 * nll + (2 * k * (k + 1)) / denom

def estimate_snr(I: np.ndarray, n_edge: int = 20) -> float:
    n_edge = max(5, min(n_edge, len(I) // 6))
    noise  = float(np.std(I[:n_edge]))
    signal = float(np.max(I)) - float(np.mean(I[:n_edge]))
    return signal / max(noise, 1e-12)

def aicc_threshold(snr: float) -> float:
    """Seuil adaptatif : plus strict à faible SNR."""
    if   snr > 50: return -2.0
    elif snr > 20: return -4.0
    elif snr > 10: return -6.0
    else:          return -10.0

def zeeman_spread_pure(B: float, lc: float, sig: float,
                        g_eff: float = 1.0) -> float:
    """
    Rapport déplacement Zeeman pur / sigma_width.
    Calculé SANS les offsets de structure fine.
    """
    if B <= 0 or sig <= 0:
        return 0.0
    delta_lam = (lc ** 2 / C) * MU_B_OVER_H * g_eff * abs(B)
    return (2.0 * delta_lam) / sig

def estimate_linear_baseline(wl: np.ndarray, I: np.ndarray,
                              n_edge: int = 20) -> np.ndarray:
    n_edge = max(10, min(n_edge, len(wl) // 8))
    idx    = np.r_[0:n_edge, len(wl) - n_edge:len(wl)]
    coeff  = np.polyfit(wl[idx], I[idx], 1)
    return np.polyval(coeff, wl)

def poisson_deviance(y: np.ndarray, mu: np.ndarray) -> float:
    mu  = np.maximum(mu, 1e-12)
    y   = np.maximum(y,  0.0)
    val = np.zeros_like(y)
    m   = y > 0
    val[m] = y[m] * np.log(y[m] / mu[m])
    return float(2.0 * np.sum(val - (y - mu)))

def residual_stats(wl: np.ndarray, I: np.ndarray,
                   model: np.ndarray) -> Dict[str, float]:
    r    = I - model
    corr = float(np.corrcoef(wl, r)[0, 1]) if len(wl) > 2 else 0.0
    return {
        'mean'          : float(np.mean(r)),
        'std'           : float(np.std(r, ddof=1)),
        'correlation_x' : corr,
    }

def hessian_std(obj_func, x0: np.ndarray,
                param_idx: int = 1) -> float:
    """Incertitude par inverse de la Hessienne (information de Fisher)."""
    eps = np.sqrt(np.finfo(float).eps)
    n   = len(x0)
    H   = np.zeros((n, n))
    for i in range(n):
        hi = eps * max(abs(x0[i]), 1e-10)
        ei = np.zeros(n); ei[i] = hi
        for j in range(i, n):
            hj = eps * max(abs(x0[j]), 1e-10)
            ej = np.zeros(n); ej[j] = hj
            try:
                H[i, j] = H[j, i] = (
                    obj_func(x0 + ei + ej) - obj_func(x0 + ei - ej) -
                    obj_func(x0 - ei + ej) + obj_func(x0 - ei - ej)
                ) / (4 * hi * hj)
            except Exception:
                return np.nan
    H = 0.5 * (H + H.T)
    try:
        cov = np.linalg.inv(H)
        var = cov[param_idx, param_idx]
        return float(np.sqrt(abs(var))) if var > 0 else np.nan
    except np.linalg.LinAlgError:
        return np.nan

def select_model(aicc_t: float, aicc_s: float,
                 B_trip: float, B_hess: float,
                 spread: float, snr: float,
                 verbose: bool = True) -> str:
    """
    Sélection de modèle (priorité décroissante) :
    1. B/σ_B < 2  → Single
    2. spread < 0.5 → Single
    3. ΔAICc < seuil(SNR) → Triplet
    4. Sinon → Single
    """
    delta = aicc_t - aicc_s
    thr   = aicc_threshold(snr)

    if not np.isnan(B_hess) and B_hess > 0:
        b_sig = B_trip / B_hess
        if b_sig < 2.0:
            if verbose:
                print(f'   [Sélection] Single  ← B/σ_B={b_sig:.2f} < 2')
            return 'Single'

    if spread < 0.5:
        if verbose:
            print(f'   [Sélection] Single  ← spread={spread:.3f} < 0.5')
        return 'Single'

    if delta < thr:
        if verbose:
            print(f'   [Sélection] Triplet ← ΔAICc={delta:.1f} < {thr:.1f}')
        return 'Triplet'

    if verbose:
        print(f'   [Sélection] Single  ← ΔAICc={delta:.1f} ≥ {thr:.1f}')
    return 'Single'

# ══════════════════════════════════════════════════════════════════
# 6. BOOTSTRAP v38.2
# ══════════════════════════════════════════════════════════════════
def _sample_x0_bootstrap(x_opt: np.ndarray,
                          bounds: List[Tuple],
                          info: Dict,
                          rng: np.random.Generator,
                          pert: float,
                          use_random: bool) -> np.ndarray:
    """
    Génère un point de départ pour un restart bootstrap.

    use_random=True  (20%) : tirage uniforme global
    use_random=False (80%) : perturbation locale adaptée par paramètre
    """
    if use_random:
        return np.array([rng.uniform(lo, hi) for lo, hi in bounds])

    x = x_opt.copy()

    # lambda_center : additif ±5 pm
    lo, hi = bounds[info['idx_lc']]
    x[info['idx_lc']] += rng.normal(0, 0.005e-9)
    x[info['idx_lc']]  = np.clip(x[info['idx_lc']], lo, hi)

    # B : additif ±pert × plage
    lo_B, hi_B = bounds[info['idx_B']]
    x[info['idx_B']] += rng.normal(0, pert * (hi_B - lo_B))
    x[info['idx_B']]  = np.clip(x[info['idx_B']], lo_B, hi_B)

    # Amplitude : multiplicatif
    lo, hi = bounds[info['idx_amp']]
    x[info['idx_amp']] *= (1.0 + rng.normal(0, pert))
    x[info['idx_amp']]  = np.clip(x[info['idx_amp']], lo, hi)

    # Sigma : multiplicatif réduit
    lo, hi = bounds[info['idx_sig']]
    x[info['idx_sig']] *= (1.0 + rng.normal(0, pert * 0.5))
    x[info['idx_sig']]  = np.clip(x[info['idx_sig']], lo, hi)

    # frac_side (optionnel)
    if info['idx_frac'] is not None:
        lo, hi = bounds[info['idx_frac']]
        x[info['idx_frac']] *= (1.0 + rng.normal(0, pert * 0.3))
        x[info['idx_frac']]  = np.clip(x[info['idx_frac']], lo, hi)

    # background (optionnel)
    if info['idx_bg'] is not None:
        lo, hi = bounds[info['idx_bg']]
        x[info['idx_bg']] = abs(
            x[info['idx_bg']] * (1.0 + rng.normal(0, pert * 0.5))
        )
        x[info['idx_bg']] = np.clip(x[info['idx_bg']], lo, hi)

    return x

def _is_valid_solution(x: np.ndarray, info: Dict) -> bool:
    """
    Critère de validité physique (pas res.success).
    L-BFGS-B retourne souvent success=False pour des raisons
    numériques mineures même si la solution est correcte.
    """
    return (
        float(x[info['idx_B']])   >= 0.0 and
        float(x[info['idx_sig']]) >  0.0 and
        float(x[info['idx_amp']]) >  0.0
    )

def bootstrap_triplet(wl: np.ndarray,
                       I: np.ndarray,
                       best_params: Dict,
                       x_opt: np.ndarray,
                       info: Dict,
                       n_bootstrap:  int   = 30,
                       n_restarts:   int   = 10,
                       pert:         float = 0.10,
                       random_frac:  float = 0.20,
                       maxiter_boot: int   = 4000,
                       seed:         int   = 42,
                       verbose:      bool  = True,
                       ) -> Tuple[float, Tuple[float, float], float,
                                  np.ndarray]:
    """
    Bootstrap paramétrique Poisson — v38.2

    Returns
    -------
    B_std   : écart-type bootstrap
    B_ci95  : (percentile 2.5%, percentile 97.5%)
    rate    : taux de succès
    B_arr   : tableau numpy des valeurs B acceptées
    """
    rng    = np.random.default_rng(seed)
    bounds = build_triplet_bounds(wl, I, info)

    # Spectre de référence
    lc_r, B_r, amp_r, sig_r, frac_r, bg_r = unpack_triplet(x_opt, info)
    mu_ref = triplet_spectrum(wl, lc_r, B_r, amp_r, sig_r, frac_r, bg_r)
    mu_ref = np.maximum(mu_ref, 1e-12)

    boot_B           = []
    n_success        = 0
    n_total_restarts = 0
    n_restarts_ok    = 0

    if verbose:
        print(f'   Bootstrap v38.2 : n={n_bootstrap}, '
              f'restarts={n_restarts}, pert={pert:.0%}, '
              f'random={random_frac:.0%}')

    for i in range(n_bootstrap):
        # Échantillon Poisson
        I_synth = rng.poisson(mu_ref).astype(float)

        # Objectif local — default arg évite la closure
        def obj_local(x, _I=I_synth):
            return obj_triplet(x, wl, _I, info)

        best_f = np.inf
        best_x = None

        for r in range(n_restarts):
            n_total_restarts += 1
            use_rnd = (rng.random() < random_frac)
            x0_try  = _sample_x0_bootstrap(
                x_opt, bounds, info, rng, pert, use_rnd
            )
            try:
                res = minimize(
                    obj_local, x0_try,
                    method='L-BFGS-B', bounds=bounds,
                    options={
                        'ftol'   : 1e-12,
                        'gtol'   : 1e-9,
                        'maxiter': maxiter_boot,
                    },
                )
                if (_is_valid_solution(res.x, info) and
                        res.fun < best_f):
                    best_f = res.fun
                    best_x = res.x.copy()
                    n_restarts_ok += 1
            except Exception:
                pass

        if best_x is not None:
            n_success += 1
            boot_B.append(float(best_x[info['idx_B']]))

        if verbose and (i + 1) % 5 == 0:
            rate_tmp = n_success / (i + 1)
            print(f'   Bootstrap {i+1:3d}/{n_bootstrap}'
                  f'  succès: {n_success:3d}/{i+1}'
                  f'  ({rate_tmp*100:.0f}%)'
                  f'  restarts_ok: {n_restarts_ok}/{n_total_restarts}')

    rate  = n_success / max(n_bootstrap, 1)
    if rate < 0.80:
        warnings.warn(
            f'⚠ Bootstrap: taux={rate*100:.1f}% (<80%). '
            f'Augmenter n_restarts ou vérifier le modèle.'
        )

    B_arr = np.array(boot_B, dtype=float)
    if len(B_arr) > 2:
        B_std = float(np.std(B_arr, ddof=1))
        B_ci  = (float(np.percentile(B_arr,  2.5)),
                 float(np.percentile(B_arr, 97.5)))
    else:
        B_std = np.nan
        B_ci  = (np.nan, np.nan)
        warnings.warn('⚠ Trop peu de solutions valides pour calculer CI.')

    if verbose:
        print(f'\n   ── Résumé Bootstrap ──────────────────────')
        print(f'   Valides  : {n_success}/{n_bootstrap} ({rate*100:.1f}%)')
        if len(B_arr) > 2:
            print(f'   B médian : {float(np.median(B_arr)):.4f} T')
            print(f'   B std    : {B_std:.4f} T')
            print(f'   B IC95%  : [{B_ci[0]:.4f}, {B_ci[1]:.4f}] T')
            print(f'   B range  : [{float(B_arr.min()):.4f},'
                  f' {float(B_arr.max()):.4f}] T')

    return B_std, B_ci, rate, B_arr

# ══════════════════════════════════════════════════════════════════
# 7. RÉSULTAT
# ══════════════════════════════════════════════════════════════════
@dataclass
class ZeemanResult:
    B                : float
    B_std            : float
    B_ci95           : Tuple[float, float]
    B_hessian        : float
    B_median         : float
    lambda_center    : float
    sigma_width      : float
    poisson_deviance : float
    aicc_triplet     : float
    aicc_single      : float
    spread_ratio     : float
    selected_model   : str
    bootstrap_rate   : float
    B_bootstrap      : np.ndarray
    residuals        : Dict[str, float]
    snr              : float
    success          : bool
    fit_time         : float
    fit_params       : Dict = field(default_factory=dict)

# ══════════════════════════════════════════════════════════════════
# 8. PIPELINE PRINCIPAL
# ══════════════════════════════════════════════════════════════════
def run_zeeman_inversion(wl: np.ndarray,
                         I:  np.ndarray,
                         subtract_continuum: bool  = True,
                         n_bootstrap:        int   = 30,
                         n_restarts:         int   = 10,
                         pert:               float = 0.10,
                         random_frac:        float = 0.20,
                         fix_frac:           bool  = True,
                         verbose:            bool  = True,
                         ) -> ZeemanResult:
    """
    Inversion Zeeman Hα complète — DTQEM v38.2-final

    Pipeline
    ────────
    1. Prétraitement  (baseline optionnelle)
    2. Ajustement Triplet + Single  (DE → L-BFGS-B)
    3. AICc + spread_ratio + B/σ_B  → sélection de modèle
    4. Bootstrap paramétrique  (si Triplet)
    5. Diagnostics et rapport
    """
    t0 = time.time()
    wl = np.asarray(wl, dtype=float)
    I  = np.asarray(I,  dtype=float)
    if len(wl) != len(I):
        raise ValueError('wl et I doivent avoir la même longueur.')

    I_work = I.copy()
    if subtract_continuum:
        I_work = np.maximum(
            I_work - estimate_linear_baseline(wl, I_work), 0.0
        )

    snr = estimate_snr(I_work)
    if verbose:
        print(f'   SNR = {snr:.1f}')

    # Ajustements
    p_t, nll_t, ok_t, x_t, info_t = fit_triplet(
        wl, I_work, subtract_continuum, fix_frac
    )
    p_s, nll_s, ok_s, x_s = fit_single(
        wl, I_work, subtract_continuum
    )

    # AICc
    n_data = len(wl)
    ac_t   = aicc(nll_t, n_data, info_t['n_params'])
    ac_s   = aicc(nll_s, n_data, 3 + (0 if subtract_continuum else 1))

    # Spread ratio Zeeman pur
    sr = zeeman_spread_pure(
        p_t['B'], p_t['lambda_center'], p_t['sigma_width']
    )

    # Incertitude Hessienne sur B
    def obj_h(x):
        return obj_triplet(x, wl, I_work, info_t)
    B_hess = hessian_std(obj_h, x_t, param_idx=info_t['idx_B'])

    # Sélection de modèle
    model = select_model(ac_t, ac_s, p_t['B'], B_hess, sr, snr, verbose)

    # Bootstrap
    empty_arr = np.array([], dtype=float)
    if model == 'Triplet':
        if verbose:
            print('   → Bootstrap...')
        B_std, B_ci, boot_rate, B_arr = bootstrap_triplet(
            wl, I_work, p_t, x_t, info_t,
            n_bootstrap=n_bootstrap,
            n_restarts=n_restarts,
            pert=pert,
            random_frac=random_frac,
            maxiter_boot=4000,
            seed=42,
            verbose=verbose,
        )
        B_val   = p_t['B']
        B_med   = float(np.median(B_arr)) if len(B_arr) > 0 else np.nan
        best_p  = p_t
        success = ok_t
        sr = zeeman_spread_pure(B_val, p_t['lambda_center'],
                                 p_t['sigma_width'])
    else:
        B_val = B_std = B_med = 0.0
        B_ci        = (0.0, 0.0)
        boot_rate   = 1.0
        B_arr       = empty_arr
        best_p      = p_s
        success     = ok_s

    # Modèle final
    bp = best_p
    if model == 'Triplet':
        final_model = triplet_spectrum(
            wl, bp['lambda_center'], bp['B'],
            bp['amplitude'], bp['sigma_width'],
            bp['frac_side'], bp['background'],
        )
    else:
        final_model = single_spectrum(
            wl, bp['lambda_center'], bp['amplitude'],
            bp['sigma_width'], bp['background'],
        )

    dev     = poisson_deviance(I_work, final_model)
    resid   = residual_stats(wl, I_work, final_model)
    elapsed = time.time() - t0

    if verbose:
        _print_report(model, B_val, B_std, B_med, B_hess, B_ci,
                      sr, best_p, dev, ac_t, ac_s,
                      boot_rate, resid, snr, elapsed)

    return ZeemanResult(
        B=float(B_val), B_std=float(B_std), B_ci95=B_ci,
        B_hessian=float(B_hess), B_median=float(B_med),
        lambda_center=float(best_p['lambda_center']),
        sigma_width=float(best_p['sigma_width']),
        poisson_deviance=float(dev),
        aicc_triplet=float(ac_t), aicc_single=float(ac_s),
        spread_ratio=float(sr), selected_model=model,
        bootstrap_rate=float(boot_rate), B_bootstrap=B_arr,
        residuals=resid, snr=float(snr),
        success=bool(success), fit_time=elapsed,
        fit_params=best_p.copy(),
    )

def _print_report(model, B, B_std, B_med, B_hess, B_ci,
                  sr, params, dev, ac_t, ac_s,
                  boot_rate, resid, snr, elapsed):
    sep = '═' * 68
    print(f'\n{sep}')
    print('DTQEM v38.2-final — Résultats')
    print(sep)
    print(f'  Modèle      : {model}')
    print(f'  SNR         : {snr:.1f}')
    if model == 'Triplet':
        print(f'  B (MAP)     : {B:.4f} T')
        print(f'  B ± std     : {B:.4f} ± {B_std:.4f} T  (bootstrap)')
        print(f'  B médian    : {B_med:.4f} T')
        if not np.isnan(B_hess):
            print(f'  B ± Hessian : {B:.4f} ± {B_hess:.4f} T')
        print(f'  IC 95%      : [{B_ci[0]:.4f}, {B_ci[1]:.4f}] T')
        print(f'  Spread/σ    : {sr:.3f}')
    else:
        print('  → Aucun champ magnétique détecté.')
    print(f'  λ_center    : {params["lambda_center"]*1e9:.5f} nm')
    print(f'  σ_width     : {params["sigma_width"]*1e12:.3f} pm')
    print(f'  Déviance    : {dev:.1f}')
    print(f'  AICc T/S    : {ac_t:.1f} / {ac_s:.1f}  (Δ={ac_t - ac_s:.1f})')
    print(f'  Bootstrap   : {boot_rate*100:.1f}%')
    print(f'  Résidus     : moy={resid["mean"]:.3f} '
          f'std={resid["std"]:.3f} '
          f'corr={resid["correlation_x"]:.3f}')
    print(f'  Temps       : {elapsed:.2f} s')
    print(sep)

# ══════════════════════════════════════════════════════════════════
# 9. VISUALISATION
# ══════════════════════════════════════════════════════════════════
def plot_result(wl: np.ndarray, I: np.ndarray,
                result: ZeemanResult,
                B_true: Optional[float] = None,
                outfile: Optional[Path] = None):
    """Figure diagnostique 3+1 panneaux."""
    bp = result.fit_params
    if result.selected_model == 'Triplet':
        model = triplet_spectrum(
            wl, bp['lambda_center'], bp['B'],
            bp['amplitude'], bp['sigma_width'],
            bp['frac_side'], bp['background']
        )
    else:
        model = single_spectrum(
            wl, bp['lambda_center'], bp['amplitude'],
            bp['sigma_width'], bp['background']
        )

    wl_nm    = wl * 1e9
    has_boot = (result.selected_model == 'Triplet' and
                len(result.B_bootstrap) > 2)
    ncols    = 2 if has_boot else 1
    fig      = plt.figure(figsize=(12 if has_boot else 10, 9))
    gs       = fig.add_gridspec(3, ncols,
                                height_ratios=[3, 1, 1],
                                hspace=0.35, wspace=0.30)

    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[2, 0])

    # Spectre + ajustement
    ax0.plot(wl_nm, I,     'k.', ms=2, alpha=0.4, label='Données')
    ax0.plot(wl_nm, model, 'r-', lw=2,            label='Ajustement')
    title = f'DTQEM v38.2 — {result.selected_model}'
    if result.selected_model == 'Triplet':
        title += f'\nB={result.B:.3f}±{result.B_std:.3f} T'
    if B_true is not None:
        title += f'  (vrai={B_true:.2f} T)'
    ax0.set_title(title, fontsize=10)
    ax0.set_ylabel('Intensité')
    ax0.legend(fontsize=8)
    ax0.grid(alpha=0.25)

    # Résidus
    resid = I - model
    ax1.axhline(0, color='k', lw=0.8)
    ax1.plot(wl_nm, resid, 'b.', ms=1.5, alpha=0.5)
    ax1.set_ylabel('Résidus')
    ax1.grid(alpha=0.25)

    # Résidus normalisés
    resid_n = resid / np.sqrt(np.maximum(model, 1.0))
    ax2.axhline( 0, color='k', lw=0.8)
    ax2.axhline( 2, color='r', lw=0.5, ls='--')
    ax2.axhline(-2, color='r', lw=0.5, ls='--')
    ax2.plot(wl_nm, resid_n, 'g.', ms=1.5, alpha=0.5)
    ax2.set_ylabel('Résidus / √modèle')
    ax2.set_xlabel('λ (nm)')
    ax2.grid(alpha=0.25)

    # Distribution Bootstrap
    if has_boot:
        ax3   = fig.add_subplot(gs[:, 1])
        B_arr = result.B_bootstrap
        ax3.hist(B_arr, bins=min(15, len(B_arr) // 2 + 1),
                 color='steelblue', edgecolor='white', alpha=0.80)
        ax3.axvline(result.B,
                    color='r', lw=2,
                    label=f'MAP={result.B:.3f}')
        ax3.axvline(result.B_median,
                    color='orange', lw=1.5, ls='--',
                    label=f'Médian={result.B_median:.3f}')
        ax3.axvline(result.B_ci95[0],
                    color='gray', lw=1, ls=':')
        ax3.axvline(result.B_ci95[1],
                    color='gray', lw=1, ls=':',
                    label=f'IC95%=[{result.B_ci95[0]:.3f},'
                          f'{result.B_ci95[1]:.3f}]')
        if B_true is not None:
            ax3.axvline(B_true,
                        color='green', lw=2, ls='-.',
                        label=f'Vrai={B_true:.2f}')
        ax3.set_xlabel('B (T)')
        ax3.set_ylabel('Comptage')
        ax3.set_title(f'Distribution Bootstrap\n'
                      f'n={len(B_arr)}, std={result.B_std:.4f} T')
        ax3.legend(fontsize=8)
        ax3.grid(alpha=0.25)

    if outfile:
        plt.savefig(outfile, dpi=150, bbox_inches='tight')
        print(f'   Figure → {outfile}')
    plt.close()

# ══════════════════════════════════════════════════════════════════
# 10. STRESS TESTS MONTE CARLO
# ══════════════════════════════════════════════════════════════════
def run_stress_tests(wl: np.ndarray,
                     lam0: float,
                     sigma_sim: float,
                     amp_sim: float,
                     bg_sim: float,
                     out: Path,
                     n_mc: int = 5,
                     verbose: bool = True) -> List[Dict]:
    """
    Stress tests Monte Carlo :
    11 cas × n_mc répétitions → robustesse complète.
    """
    stress_cases = [
        (0.00, 1.00, 'B0_high_snr'),
        (0.10, 1.00, 'B0.1_weak'),
        (0.25, 1.00, 'B0.25_marginal'),
        (0.50, 1.00, 'B0.5_normal'),
        (1.00, 1.00, 'B1.0_normal'),
        (1.50, 1.00, 'B1.5_normal'),
        (2.00, 1.00, 'B2.0_normal'),
        (2.50, 1.00, 'B2.5_strong'),
        (1.00, 0.10, 'B1.0_low_snr'),
        (1.00, 0.05, 'B1.0_very_low_snr'),
        (1.50, 0.20, 'B1.5_low_snr'),
    ]

    rng_mc      = np.random.default_rng(2024)
    all_results = []

    for B_true, amp_f, label in stress_cases:
        if verbose:
            print(f'\n  ── Stress: {label}')
        mc_B, mc_err, mc_ok = [], [], []

        for mc in range(n_mc):
            seed_mc = int(rng_mc.integers(0, 99999))
            np.random.seed(seed_mc)

            I_clean = triplet_spectrum(
                wl, lam0, B_true,
                amp_sim * amp_f, sigma_sim, 0.60, bg_sim
            )
            I_noisy = np.random.poisson(
                np.maximum(I_clean, 1e-12)
            ).astype(float)

            try:
                res = run_zeeman_inversion(
                    wl, I_noisy,
                    subtract_continuum=False,
                    n_bootstrap=20,
                    n_restarts=10,
                    pert=0.10,
                    random_frac=0.20,
                    fix_frac=True,
                    verbose=False,
                )
                mc_B.append(res.B)
                mc_err.append(abs(res.B - B_true))
                mc_ok.append(
                    res.selected_model == (
                        'Single' if B_true < 0.15 else 'Triplet'
                    )
                )
            except Exception as e:
                if verbose:
                    print(f'    MC {mc}: ERREUR → {e}')
                mc_B.append(np.nan)
                mc_err.append(np.nan)
                mc_ok.append(False)

        mc_B_arr  = np.array(mc_B,  dtype=float)
        mc_err_arr = np.array(mc_err, dtype=float)
        valid     = ~np.isnan(mc_B_arr)

        summary = {
            'label'        : label,
            'B_true'       : B_true,
            'amp_factor'   : amp_f,
            'n_mc'         : n_mc,
            'B_mean'       : float(np.nanmean(mc_B_arr)),
            'B_std_mc'     : float(np.nanstd(mc_B_arr, ddof=1))
                             if valid.sum() > 1 else np.nan,
            'err_mean'     : float(np.nanmean(mc_err_arr)),
            'err_max'      : float(np.nanmax(mc_err_arr))
                             if valid.any() else np.nan,
            'model_correct': float(np.mean(mc_ok)),
            'n_valid'      : int(valid.sum()),
        }
        all_results.append(summary)

        if verbose:
            print(f'    B_true={B_true:.2f} T  →  '
                  f'B_mean={summary["B_mean"]:.3f} T  '
                  f'err={summary["err_mean"]:.3f} T  '
                  f'correct={summary["model_correct"]*100:.0f}%  '
                  f'valid={summary["n_valid"]}/{n_mc}')

    # CSV stress tests
    stress_csv = out / 'dtqem_v38_2_stress_tests.csv'
    with open(stress_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['# DTQEM v38.2 — Stress Tests'])
        w.writerow(['# Date',
                    time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())])
        w.writerow([])
        w.writerow(['label', 'B_true_T', 'amp_factor', 'n_mc',
                    'B_mean_T', 'B_std_mc_T',
                    'err_mean_T', 'err_max_T',
                    'model_correct_frac', 'n_valid'])
        for r in all_results:
            w.writerow([
                r['label'], r['B_true'], r['amp_factor'], r['n_mc'],
                r['B_mean'], r['B_std_mc'],
                r['err_mean'], r['err_max'],
                r['model_correct'], r['n_valid'],
            ])
    print(f'\n  ✅ Stress tests → {stress_csv}')
    return all_results

# ══════════════════════════════════════════════════════════════════
# 11. FIGURES SYNTHÈSE
# ══════════════════════════════════════════════════════════════════
def plot_recovery_curve(stress_results: List[Dict],
                        outfile: Optional[Path] = None):
    """Courbe de récupération B_rec vs B_true (cas amp=1)."""
    normal = [r for r in stress_results if r['amp_factor'] == 1.0]
    if not normal:
        return

    B_true_arr = np.array([r['B_true']   for r in normal])
    B_mean_arr = np.array([r['B_mean']   for r in normal])
    B_std_arr  = np.array([
        r['B_std_mc'] if not np.isnan(r['B_std_mc']) else 0.0
        for r in normal
    ])

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # B_rec vs B_true
    ax = axes[0]
    ax.errorbar(B_true_arr, B_mean_arr, yerr=B_std_arr,
                fmt='o', color='steelblue', capsize=4,
                label='B récupéré (mean ± std MC)')
    B_diag = np.linspace(0, max(float(B_true_arr.max()), 0.1), 100)
    ax.plot(B_diag, B_diag, 'k--', lw=1, label='Idéal (y=x)')
    ax.set_xlabel('B vrai (T)')
    ax.set_ylabel('B récupéré (T)')
    ax.set_title('Courbe de récupération — DTQEM v38.2')
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # Erreur relative
    ax2 = axes[1]
    err_rel = np.where(
        B_true_arr > 0,
        np.abs(B_mean_arr - B_true_arr) / B_true_arr * 100,
        np.abs(B_mean_arr) * 100,
    )
    ax2.bar(range(len(normal)), err_rel,
            color='coral', edgecolor='white', alpha=0.85)
    ax2.set_xticks(range(len(normal)))
    ax2.set_xticklabels(
        [f'{r["B_true"]:.1f}' for r in normal],
        rotation=45, ha='right', fontsize=8
    )
    ax2.set_xlabel('B vrai (T)')
    ax2.set_ylabel('Erreur relative (%)')
    ax2.set_title('Erreur relative de récupération')
    ax2.axhline(5, color='r', ls='--', lw=1, label='5%')
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3, axis='y')

    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=150, bbox_inches='tight')
        print(f'   Courbe → {outfile}')
    plt.close()

def plot_bootstrap_diagnostics(B_boot_all: Dict[str, np.ndarray],
                                outfile: Optional[Path] = None):
    """Grille de diagnostics Bootstrap : histogramme par cas."""
    cases = [(k, v) for k, v in B_boot_all.items() if len(v) > 2]
    if not cases:
        return

    n    = len(cases)
    ncol = min(3, n)
    nrow = (n + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol,
                              figsize=(5 * ncol, 4 * nrow))
    axes_flat = np.array(axes).flatten() if n > 1 else [axes]

    for ax, (label, B_arr) in zip(axes_flat, cases):
        bins = min(15, max(3, len(B_arr) // 2))
        ax.hist(B_arr, bins=bins,
                color='steelblue', edgecolor='white', alpha=0.8)
        ax.axvline(float(np.mean(B_arr)),
                   color='r', lw=2,
                   label=f'moy={np.mean(B_arr):.3f}')
        ax.axvline(float(np.median(B_arr)),
                   color='orange', lw=1.5, ls='--',
                   label=f'méd={np.median(B_arr):.3f}')
        ax.axvline(float(np.percentile(B_arr,  2.5)),
                   color='gray', lw=1, ls=':')
        ax.axvline(float(np.percentile(B_arr, 97.5)),
                   color='gray', lw=1, ls=':')
        ax.set_title(label, fontsize=8)
        ax.set_xlabel('B (T)', fontsize=8)
        ax.legend(fontsize=7)
        ax.grid(alpha=0.25)

    for ax in axes_flat[len(cases):]:
        ax.set_visible(False)

    fig.suptitle('DTQEM v38.2 — Distributions Bootstrap', fontsize=11)
    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=150, bbox_inches='tight')
        print(f'   Diagnostics → {outfile}')
    plt.close()

# ══════════════════════════════════════════════════════════════════
# 12. RAPPORT FINAL
# ══════════════════════════════════════════════════════════════════
def print_final_summary(rows: List, stress_results: List[Dict]):
    sep  = '─' * 78
    sep2 = '═' * 78
    print(f'\n{sep2}')
    print('DTQEM v38.2-final — Résumé Validation Principale')
    print(sep2)
    print(f'{"B_true":>8} {"variant":<20} {"B_rec":>8} '
          f'{"err":>8} {"IC95_ok":>8} {"boot%":>7} {"t(s)":>6}')
    print(sep)
    for r in rows:
        (B_true, variant, B_map, B_std, B_med,
         ci_lo, ci_hi, B_hess, model, dev,
         ac_t, ac_s, sr, snr, err, covered,
         boot_rate, ft) = r
        ic_str = ('✓' if covered else '✗') \
                 if covered is not None else 'N/A'
        print(f'{B_true:>8.2f} {variant:<20} {B_map:>8.4f} '
              f'{err:>8.4f} {ic_str:>8} '
              f'{boot_rate*100:>6.1f}% {ft:>6.2f}')

    print(f'\n{sep2}')
    print('DTQEM v38.2-final — Résumé Stress Tests')
    print(sep2)
    print(f'{"label":<25} {"B_true":>8} {"B_mean":>8} '
          f'{"err_moy":>8} {"modèle%":>9} {"n_ok":>6}')
    print(sep)
    for r in stress_results:
        print(f'{r["label"]:<25} {r["B_true"]:>8.2f} '
              f'{r["B_mean"]:>8.3f} {r["err_mean"]:>8.3f} '
              f'{r["model_correct"]*100:>8.0f}% '
              f'{r["n_valid"]:>4}/{r["n_mc"]}')
    print(sep2)

# ══════════════════════════════════════════════════════════════════
# 13. POINT D'ENTRÉE PRINCIPAL
# ══════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    np.random.seed(42)
    out = Path('output_zeeman_v382')
    out.mkdir(exist_ok=True)

    print('\n' + '=' * 70)
    print('DTQEM v38.2-final — Validation Complète')
    print('=' * 70)
    print(f'μ_B   = {MU_B:.6e} J/T')
    print(f'μ_B/h = {MU_B_OVER_H:.6e} Hz/T')

    # Paramètres de simulation
    wl        = np.linspace(656.16e-9, 656.40e-9, 500)
    lam0      = 656.28e-9
    sigma_sim = 0.008e-9
    amp_sim   = 1400.0
    bg_sim    = 2.0

    # Cas de test principaux
    test_cases = [
        (0.0, 'single_line'),
        (0.0, 'triplet_B0'),
        (0.5, 'normal'),
        (1.0, 'normal'),
        (1.5, 'normal'),
        (2.0, 'normal'),
        (1.0, 'low_amp'),
    ]

    rows       = []
    B_boot_all = {}

    for B_true, variant in test_cases:
        label = f'B={B_true:.1f}T_{variant}'
        print(f'\n{"─" * 60}')
        print(f'  Cas : {label}')

        if variant == 'single_line':
            I_clean = single_spectrum(
                wl, lam0, amp_sim, sigma_sim, bg_sim
            )
        elif variant == 'low_amp':
            I_clean = triplet_spectrum(
                wl, lam0, B_true,
                amp_sim * 0.15, sigma_sim, 0.60, bg_sim
            )
        else:
            I_clean = triplet_spectrum(
                wl, lam0, B_true,
                amp_sim, sigma_sim, 0.60, bg_sim
            )

        I_noisy = np.random.poisson(
            np.maximum(I_clean, 1e-12)
        ).astype(float)

        n_boot = 20 if B_true == 0.0 else 30
        res = run_zeeman_inversion(
            wl, I_noisy,
            subtract_continuum=False,
            n_bootstrap=n_boot,
            n_restarts=10,
            pert=0.10,
            random_frac=0.20,
            fix_frac=True,
            verbose=True,
        )

        err     = abs(res.B - B_true)
        covered = (
            (res.B_ci95[0] <= B_true <= res.B_ci95[1])
            if not np.isnan(res.B_ci95[0]) else None
        )
        B_boot_all[label] = res.B_bootstrap

        rows.append([
            B_true, variant,
            res.B, res.B_std, res.B_median,
            res.B_ci95[0], res.B_ci95[1], res.B_hessian,
            res.selected_model, res.poisson_deviance,
            res.aicc_triplet, res.aicc_single,
            res.spread_ratio, res.snr,
            err, covered, res.bootstrap_rate, res.fit_time,
        ])

        plot_result(wl, I_noisy, res,
                    B_true=B_true,
                    outfile=out / f'fit_{label}.png')

    # CSV validation principale
    csv_path = out / 'dtqem_v38_2_validation.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        for meta in [
            ['# DTQEM v38.2-final'],
            ['# Date',   time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                       time.gmtime())],
            ['# Python', sys.version.split()[0]],
            ['# NumPy',  np.__version__],
            ['# SciPy',  scipy.__version__],
            ['# mu_B',   f'{MU_B:.10e} J/T'],
            ['# mu_B_h', f'{MU_B_OVER_H:.10e} Hz/T'],
            [],
        ]:
            w.writerow(meta)
        w.writerow([
            'B_true_T', 'variant',
            'B_map_T', 'B_std_T', 'B_median_T',
            'B_ci95_low', 'B_ci95_high', 'B_hessian_T',
            'selected_model', 'poisson_deviance',
            'aicc_triplet', 'aicc_single', 'spread_ratio',
            'snr', 'abs_error_T', 'ci_covers_true',
            'bootstrap_rate', 'fit_time_s',
        ])
        w.writerows(rows)

    # CSV distributions Bootstrap
    boot_path = out / 'dtqem_v38_2_bootstrap_distributions.csv'
    with open(boot_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['# Distributions Bootstrap — une colonne par cas'])
        labels_b = list(B_boot_all.keys())
        w.writerow(labels_b)
        vals    = [B_boot_all[k] for k in labels_b]
        max_len = max((len(v) for v in vals), default=0)
        for i in range(max_len):
            w.writerow([
                f'{v[i]:.6f}' if i < len(v) else ''
                for v in vals
            ])

    # Stress tests Monte Carlo
    print('\n' + '=' * 70)
    print('DTQEM v38.2-final — Stress Tests (Monte Carlo)')
    print('=' * 70)
    stress_results = run_stress_tests(
        wl, lam0, sigma_sim, amp_sim, bg_sim,
        out, n_mc=5, verbose=True
    )

    # Figures synthèse
    plot_recovery_curve(
        stress_results,
        outfile=out / 'dtqem_v38_2_recovery_curve.png'
    )
    plot_bootstrap_diagnostics(
        B_boot_all,
        outfile=out / 'dtqem_v38_2_bootstrap_diagnostics.png'
    )

    # Rapport final
    print_final_summary(rows, stress_results)

    # Index fichiers
    print('\n' + '─' * 60)
    print('Fichiers générés :')
    for f in sorted(out.iterdir()):
        size_kb = f.stat().st_size / 1024
        print(f'  {f.name:<52}  {size_kb:6.1f} KB')
    print('─' * 60)
    print('✅  DTQEM v38.2-final — Terminé.')
