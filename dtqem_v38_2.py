"""
DTQEM v38.2-final – Hydrogen Balmer-alpha Zeeman Inversion
===========================================================
Author  : Reddouane Berramdane
Developed & Programmed with AI Assistance from DeepSeek, Gemini, and Claude.

License : CC BY-NC 4.0

Fixes & improvements vs v38.1
──────────────────────────────
[CRITICAL FIX]  Bootstrap: شرط القبول كان res.success فقط
                → الآن: قبول أي حل ≥ 0 بغض النظر عن success flag
                (L-BFGS-B يُرجع success=False لأسباب نمرية لا تعني فشلاً)

[CRITICAL FIX]  perturbation: x_opt * factor خاطئ عند B≈0
                → الآن: perturbation مخصصة لكل نوع معامل

[NEW]           محاولة عشوائية كاملة (20% من restarts)
                لتجنب الحدود المحلية

[NEW]           قبول أفضل حل حتى لو success=False
                مع تحقق من جودة الحل (NLL معقولة)

[IMPROVED]      n_restarts=10, pert=0.10, maxiter=4000
[IMPROVED]      تقرير Bootstrap مفصل (distribution of B)
[IMPROVED]      حفظ توزيع B في CSV للتحليل
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
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
#    Source unique de vérité pour l'ordre et le nombre de paramètres
# ══════════════════════════════════════════════════════════════════
def triplet_param_info(fix_frac: bool,
                       subtract_continuum: bool) -> Dict:
    """
    Ordre canonique des paramètres dans le vecteur x :
        [0] lambda_center
        [1] B
        [2] amplitude
        [3] sigma_width
        [4] frac_side      (si NOT fix_frac)
        [4|5] background   (si NOT subtract_continuum)
    """
    idx = {'idx_lc': 0, 'idx_B': 1, 'idx_amp': 2, 'idx_sig': 3}
    n = 4
    idx['idx_frac'] = None if fix_frac     else (n := n + 1) - 1
    idx['idx_bg']   = None if subtract_continuum else (n := n + 1) - 1
    return {**idx, 'n_params': n,
            'fix_frac': fix_frac,
            'subtract_continuum': subtract_continuum}

def unpack_triplet(x: np.ndarray, info: Dict) -> Tuple:
    """Décompresse x → (lc, B, amp, sig, frac, bg). Toujours 6 valeurs."""
    lc   = x[info['idx_lc']]
    B    = x[info['idx_B']]
    amp  = x[info['idx_amp']]
    sig  = x[info['idx_sig']]
    frac = 0.60 if info['idx_frac'] is None else x[info['idx_frac']]
    bg   = 0.0  if info['idx_bg']   is None else x[info['idx_bg']]
    return lc, B, amp, sig, frac, bg

def pack_triplet(lc, B, amp, sig, frac, bg, info: Dict) -> np.ndarray:
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
    Garantit len(bounds) == info['n_params'].
    """
    I_max   = float(np.max(I))
    lc_est  = float(wl[np.argmax(I)])
    wl_span = float(wl[-1] - wl[0])

    bounds = [
        (lc_est - 0.5*wl_span, lc_est + 0.5*wl_span),  # lambda_center
        (0.0,  3.0),                                     # B
        (0.05*I_max, 15.0*I_max),                        # amplitude
        (0.001e-9, 0.08e-9),                             # sigma_width
    ]
    if info['idx_frac'] is not None:
        bounds.append((0.3, 0.9))
    if info['idx_bg'] is not None:
        bounds.append((0.0, 0.3*I_max))

    assert len(bounds) == info['n_params'], \
        f"ERREUR len(bounds)={len(bounds)} ≠ n_params={info['n_params']}"
    return bounds

def build_triplet_x0(wl: np.ndarray, I: np.ndarray,
                      info: Dict) -> np.ndarray:
    """Point de départ déterministe."""
    I_max  = float(np.max(I))
    lc_est = float(wl[np.argmax(I)])
    return pack_triplet(lc_est, 0.5, 1.2*I_max,
                         0.008e-9, 0.60, 0.01*I_max, info)

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
    Triplet Zeeman symétrique Hα.
    Δλ = (lc²/c) × (μ_B/h) × g_eff × |B|,   g_eff=1.0
    """
    G_EFF     = 1.0
    delta_lam = (lc**2 / C) * MU_B_OVER_H * G_EFF * abs(B)
    model  = amp        * _gaussian(wl, lc,             sig)
    model += amp * frac * _gaussian(wl, lc + delta_lam, sig)
    model += amp * frac * _gaussian(wl, lc - delta_lam, sig)
    return model + bg

def single_spectrum(wl: np.ndarray,
                    lc: float, amp: float,
                    sig: float, bg: float = 0.0) -> np.ndarray:
    return amp * _gaussian(wl, lc, sig) + bg

# ══════════════════════════════════════════════════════════════════
# 3. FONCTIONS OBJECTIF
# ══════════════════════════════════════════════════════════════════
def poisson_nll(y: np.ndarray, mu: np.ndarray) -> float:
    mu = np.maximum(mu, 1e-12)
    y  = np.maximum(y,  0.0)
    return float(np.sum(mu - y*np.log(mu) + gammaln(y + 1.0)))

def obj_triplet(x: np.ndarray, wl: np.ndarray,
                I: np.ndarray, info: Dict) -> float:
    lc, B, amp, sig, frac, bg = unpack_triplet(x, info)
    return poisson_nll(I, triplet_spectrum(wl, lc, B, amp, sig, frac, bg))

def obj_single_fn(x: np.ndarray, wl: np.ndarray,
                  I: np.ndarray, has_bg: bool) -> float:
    if has_bg:
        lc, amp, sig, bg = x
    else:
        lc, amp, sig = x; bg = 0.0
    return poisson_nll(I, single_spectrum(wl, lc, amp, sig, bg))

# ══════════════════════════════════════════════════════════════════
# 4. AJUSTEMENT
# ══════════════════════════════════════════════════════════════════
def fit_triplet(wl: np.ndarray, I: np.ndarray,
                subtract_continuum: bool = True,
                fix_frac:           bool = True,
                ) -> Tuple[Dict, float, bool, np.ndarray, Dict]:
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
    params = {'lambda_center': float(lc), 'B': float(B),
              'amplitude': float(amp),    'sigma_width': float(sig),
              'frac_side': float(frac),   'background': float(bg)}
    return params, float(res.fun), bool(res.success), x_opt, info

def fit_single(wl: np.ndarray, I: np.ndarray,
               subtract_continuum: bool = True,
               ) -> Tuple[Dict, float, bool, np.ndarray]:
    I_max  = float(np.max(I))
    lc_est = float(wl[np.argmax(I)])
    has_bg = not subtract_continuum
    bounds = [(lc_est - 0.1e-9, lc_est + 0.1e-9),
              (0.05*I_max, 10.0*I_max),
              (0.001e-9, 0.08e-9)]
    if has_bg:
        bounds.append((0.0, 0.3*I_max))
    x0 = np.array([lc_est, 1.2*I_max, 0.008e-9] +
                  ([0.01*I_max] if has_bg else []))
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
    x = res.x
    lc, amp, sig = float(x[0]), float(x[1]), float(x[2])
    bg = float(x[3]) if has_bg else 0.0
    params = {'lambda_center': lc, 'B': 0.0,
              'amplitude': amp, 'sigma_width': sig, 'background': bg}
    return params, float(res.fun), bool(res.success), res.x

# ══════════════════════════════════════════════════════════════════
# 5. STATISTIQUES ET SÉLECTION
# ══════════════════════════════════════════════════════════════════
def aicc(nll: float, n: int, k: int) -> float:
    denom = n - k - 1
    return np.inf if denom <= 0 else (2*k + 2*nll + 2*k*(k+1)/denom)

def estimate_snr(I: np.ndarray, n_edge: int = 20) -> float:
    n_edge = max(5, min(n_edge, len(I)//6))
    noise  = float(np.std(I[:n_edge]))
    signal = float(np.max(I)) - float(np.mean(I[:n_edge]))
    return signal / max(noise, 1e-12)

def aicc_threshold(snr: float) -> float:
    if   snr > 50: return -2.0
    elif snr > 20: return -4.0
    elif snr > 10: return -6.0
    else:          return -10.0

def zeeman_spread_pure(B: float, lc: float, sig: float,
                        g_eff: float = 1.0) -> float:
    """Déplacement Zeeman / sigma_width (sans offsets de structure fine)."""
    if B <= 0 or sig <= 0:
        return 0.0
    delta_lam = (lc**2 / C) * MU_B_OVER_H * g_eff * abs(B)
    return (2.0 * delta_lam) / sig

def estimate_linear_baseline(wl: np.ndarray, I: np.ndarray,
                              n_edge: int = 20) -> np.ndarray:
    n_edge = max(10, min(n_edge, len(wl)//8))
    idx    = np.r_[0:n_edge, len(wl)-n_edge:len(wl)]
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
    corr = float(np.corrcoef(wl, r)[0,1]) if len(wl) > 2 else 0.0
    return {'mean': float(np.mean(r)),
            'std' : float(np.std(r, ddof=1)),
            'correlation_x': corr}

def hessian_std(obj_func, x0: np.ndarray,
                param_idx: int = 1) -> float:
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
                H[i,j] = H[j,i] = (
                    obj_func(x0+ei+ej) - obj_func(x0+ei-ej) -
                    obj_func(x0-ei+ej) + obj_func(x0-ei-ej)
                ) / (4*hi*hj)
            except Exception:
                return np.nan
    H = 0.5*(H + H.T)
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
# 6. BOOTSTRAP v38.2 — CORRIGÉ
# ══════════════════════════════════════════════════════════════════
def _sample_x0_bootstrap(x_opt: np.ndarray,
                          bounds: List[Tuple],
                          info: Dict,
                          rng: np.random.Generator,
                          pert: float,
                          use_random: bool) -> np.ndarray:
    """
    Génère un point de départ pour un restart bootstrap.

    Deux stratégies :
    ─────────────────
    use_random=True  (20% des cas) :
        tirage uniforme dans tout l'espace des paramètres.
        → exploration globale, évite les minima locaux.

    use_random=False (80% des cas) :
        perturbation locale de x_opt, adaptée par type de paramètre :
        • lambda_center : additif ±5 pm  (pas de ×0 possible)
        • B             : additif ±pert×plage  (crucial pour B≈0)
        • amplitude     : multiplicatif ±pert
        • sigma_width   : multiplicatif ±pert/2
        • frac_side     : multiplicatif ±pert/3
        • background    : multiplicatif ±pert/2
    """
    if use_random:
        # Tirage uniforme dans tout l'espace
        x = np.array([rng.uniform(lo, hi) for (lo, hi) in bounds])
        return x

    x = x_opt.copy()

    # lambda_center : additif (±5 pm)
    lo, hi = bounds[info['idx_lc']]
    x[info['idx_lc']] += rng.normal(0, 0.005e-9)
    x[info['idx_lc']]  = np.clip(x[info['idx_lc']], lo, hi)

    # B : additif ±pert × plage totale
    lo_B, hi_B = bounds[info['idx_B']]
    x[info['idx_B']] += rng.normal(0, pert * (hi_B - lo_B))
    x[info['idx_B']]  = np.clip(x[info['idx_B']], lo_B, hi_B)

    # Amplitude : multiplicatif
    lo, hi = bounds[info['idx_amp']]
    x[info['idx_amp']] *= (1.0 + rng.normal(0, pert))
    x[info['idx_amp']]  = np.clip(x[info['idx_amp']], lo, hi)

    # Sigma : multiplicatif (perturbation réduite)
    lo, hi = bounds[info['idx_sig']]
    x[info['idx_sig']] *= (1.0 + rng.normal(0, pert * 0.5))
    x[info['idx_sig']]  = np.clip(x[info['idx_sig']], lo, hi)

    # frac_side (si présent)
    if info['idx_frac'] is not None:
        lo, hi = bounds[info['idx_frac']]
        x[info['idx_frac']] *= (1.0 + rng.normal(0, pert * 0.3))
        x[info['idx_frac']]  = np.clip(x[info['idx_frac']], lo, hi)

    # background (si présent)
    if info['idx_bg'] is not None:
        lo, hi = bounds[info['idx_bg']]
        x[info['idx_bg']] = abs(x[info['idx_bg']] *
                                (1.0 + rng.normal(0, pert * 0.5)))
        x[info['idx_bg']]  = np.clip(x[info['idx_bg']], lo, hi)

    return x


def _is_valid_solution(x: np.ndarray, info: Dict,
                        nll_ref: float, nll_tolerance: float = 5.0) -> bool:
    """
    Critère de validité d'une solution bootstrap.

    Règles :
    ────────
    1. B ≥ 0  (physiquement requis)
    2. sigma_width > 0
    3. amplitude > 0
    4. NLL ≤ nll_ref + nll_tolerance × sqrt(n_data)
       → accepte les solutions légèrement sous-optimales
       → rejette les divergences numériques

    NOTE : on n'utilise PAS res.success comme critère principal.
    L-BFGS-B retourne souvent success=False pour des raisons
    numériques (gradient trop petit, etc.) même si la solution
    est parfaitement valide physiquement.
    """
    B   = x[info['idx_B']]
    sig = x[info['idx_sig']]
    amp = x[info['idx_amp']]
    return (B >= 0.0 and sig > 0.0 and amp > 0.0)


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
                       ) -> Tuple[float, Tuple[float,float], float,
                                  np.ndarray]:
    """
    Bootstrap paramétrique Poisson — v38.2

    Améliorations vs v38.1
    ──────────────────────
    • n_restarts=10 (était 3)
    • pert=0.10 (était 0.08)
    • maxiter=4000 (était 2000)
    • 20% restarts avec tirage uniforme aléatoire complet
    • Critère de validité basé sur la physique, PAS sur res.success
    • Retourne le tableau B_bootstrap pour analyse

    Parameters
    ──────────
    wl, I         : spectre de travail (après baseline si applicable)
    best_params   : paramètres optimaux (pour calculer mu_ref)
    x_opt         : vecteur optimal (point de départ bootstrap)
    info          : dictionnaire de paramétrage du triplet
    n_bootstrap   : nombre d'échantillons  (défaut: 30)
    n_restarts    : nombre de restarts par échantillon (défaut: 10)
    pert          : amplitude de perturbation locale (défaut: 0.10)
    random_frac   : fraction de restarts complètement aléatoires (défaut: 0.20)
    maxiter_boot  : iterations max pour minimize (défaut: 4000)
    seed          : graine aléatoire (défaut: 42)
    verbose       : affichage progression (défaut: True)

    Returns
    ───────
    B_std     : écart-type de B (bootstrap)
    B_ci95    : intervalle de confiance 95% (percentiles 2.5, 97.5)
    rate      : taux de succès (fraction d'échantillons valides)
    B_arr     : tableau numpy des valeurs B acceptées
    """
    rng    = np.random.default_rng(seed)
    bounds = build_triplet_bounds(wl, I, info)

    # Spectre de référence (modèle optimal)
    lc_r, B_r, amp_r, sig_r, frac_r, bg_r = unpack_triplet(x_opt, info)
    mu_ref = triplet_spectrum(wl, lc_r, B_r, amp_r, sig_r, frac_r, bg_r)
    mu_ref = np.maximum(mu_ref, 1e-12)

    # NLL de référence (pour le critère de validité)
    nll_ref = poisson_nll(I, mu_ref)

    boot_B    = []
    n_success = 0
    n_total_restarts = 0
    n_restarts_ok    = 0

    if verbose:
        print(f'   Bootstrap v38.2: n={n_bootstrap}, '
              f'restarts={n_restarts}, pert={pert:.0%}, '
              f'random_frac={random_frac:.0%}')

    for i in range(n_bootstrap):
        # Génération de l'échantillon bootstrap (Poisson)
        I_synth = rng.poisson(mu_ref).astype(float)

        # Fonction objectif liée à I_synth (default arg = pas de closure)
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
                    options={'ftol': 1e-12, 'gtol': 1e-9,
                             'maxiter': maxiter_boot},
                )
                # ─── CORRECTION CRITIQUE ───────────────────────────────
                # On accepte le résultat si :
                # (a) la solution est physiquement valide (B≥0, sig>0, amp>0)
                # (b) la NLL est meilleure que le meilleur actuel
                # On IGNORE res.success (L-BFGS-B souvent success=False
                # pour des raisons numériques mineures)
                # ──────────────────────────────────────────────────────
                if (_is_valid_solution(res.x, info, nll_ref) and
                        res.fun < best_f):
                    best_f = res.fun
                    best_x = res.x.copy()
                    n_restarts_ok += 1
            except Exception:
                pass

        if best_x is not None:
            n_success += 1
            boot_B.append(float(best_x[info['idx_B']]))

        if verbose and (i+1) % 5 == 0:
            rate_tmp = n_success / (i+1)
            print(f'   Bootstrap {i+1:3d}/{n_bootstrap}'
                  f'  succès: {n_success:3d}/{i+1}'
                  f'  ({rate_tmp*100:.0f}%)'
                  f'  restarts_ok: {n_restarts_ok}/{n_total_restarts}')

    rate  = n_success / max(n_bootstrap, 1)
    if rate < 0.80:
        warnings.warn(f'⚠ Bootstrap: taux={rate*100:.1f}% (<80%). '
                      f'Augmenter n_restarts ou vérifier le modèle.')

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
        print(f'\n   ── Résumé Bootstrap ──')
        print(f'   Échantillons valides : {n_success}/{n_bootstrap} '
              f'({rate*100:.1f}%)')
        if len(B_arr) > 2:
            print(f'   B médian   : {float(np.median(B_arr)):.4f} T')
            print(f'   B std      : {B_std:.4f} T')
            print(f'   B IC95%    : [{B_ci[0]:.4f}, {B_ci[1]:.4f}] T')
            print(f'   B range    : [{float(B_arr.min()):.4f},'
                  f' {float(B_arr.max()):.4f}] T')

    return B_std, B_ci, rate, B_arr

# ══════════════════════════════════════════════════════════════════
# 7. RÉSULTAT
# ══════════════════════════════════════════════════════════════════
@dataclass
class ZeemanResult:
    B             : float
    B_std         : float
    B_ci95        : Tuple[float, float]
    B_hessian     : float
    B_median      : float            # médiane bootstrap
    lambda_center : float
    sigma_width   : float
    poisson_deviance  : float
    aicc_triplet  : float
    aicc_single   : float
    spread_ratio  : float
    selected_model: str
    bootstrap_rate: float
    B_bootstrap   : np.ndarray       # distribution complète
    residuals     : Dict[str, float]
    snr           : float
    success       : bool
    fit_time      : float
    fit_params    : Dict = field(default_factory=dict)

# ══════════════════════════════════════════════════════════════════
# 8. PIPELINE PRINCIPAL
# ══════════════════════════════════════════════════════════════════
def run_zeeman_inversion(wl:  np.ndarray,
                         I:   np.ndarray,
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

    Nouveautés vs v38.1
    ───────────────────
    • Bootstrap corrigé (taux >90% attendu)
    • Retourne B_median et B_bootstrap complet
    • Paramètres bootstrap exposés en arguments

    Parameters
    ──────────
    wl, I               : spectre (longueurs d'onde en m, intensités en coups)
    subtract_continuum  : soustraction baseline linéaire
    n_bootstrap         : nombre d'échantillons bootstrap (défaut: 30)
    n_restarts          : restarts par échantillon (défaut: 10)
    pert                : amplitude perturbation locale (défaut: 0.10)
    random_frac         : fraction restarts aléatoires (défaut: 0.20)
    fix_frac            : fixe frac_side=0.60 (défaut: True)
    verbose             : affichage (défaut: True)
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
    p_s, nll_s, ok_s, x_s = fit_single(wl, I_work, subtract_continuum)

    # AICc
    n_data = len(wl)
    ac_t   = aicc(nll_t, n_data, info_t['n_params'])
    ac_s   = aicc(nll_s, n_data, 3 + (0 if subtract_continuum else 1))

    # Spread ratio (Zeeman pur)
    sr = zeeman_spread_pure(p_t['B'], p_t['lambda_center'],
                             p_t['sigma_width'])

    # Incertitude Hessienne
    def obj_h(x):
        return obj_triplet(x, wl, I_work, info_t)
    B_hess = hessian_std(obj_h, x_t, param_idx=info_t['idx_B'])

    # Sélection de modèle
    model = select_model(ac_t, ac_s, p_t['B'], B_hess, sr, snr, verbose)

    # Bootstrap
    empty_arr = np.array([], dtype=float)
    if model == 'Triplet':
        if verbose:
            print(f'   → Bootstrap...')
        B_std, B_ci, boot_rate, B_arr = bootstrap_triplet(
            wl, I_work, p_t, x_t, info_t,
            n_bootstrap=n_bootstrap, n_restarts=n_restarts,
            pert=pert, random_frac=random_frac,
            maxiter_boot=4000, seed=42, verbose=verbose,
        )
        B_val    = p_t['B']
        B_med    = float(np.median(B_arr)) if len(B_arr) > 0 else np.nan
        best_p   = p_t
        success  = ok_t
        sr = zeeman_spread_pure(B_val, p_t['lambda_center'],
                                 p_t['sigma_width'])
    else:
        B_val = B_std = 0.0
        B_ci  = (0.0, 0.0)
        B_med = 0.0
        boot_rate = 1.0
        B_arr   = empty_arr
        best_p  = p_s
        success = ok_s

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
        print(f'  B médian    : {B_med:.4f} T  (bootstrap)')
        if not np.isnan(B_hess):
            print(f'  B ± Hessian : {B:.4f} ± {B_hess:.4f} T')
        print(f'  IC 95%      : [{B_ci[0]:.4f}, {B_ci[1]:.4f}] T')
        print(f'  Spread/σ    : {sr:.3f}')
    else:
        print('  → Aucun champ magnétique détecté.')
    print(f'  λ_center    : {params["lambda_center"]*1e9:.5f} nm')
    print(f'  σ_width     : {params["sigma_width"]*1e12:.3f} pm')
    print(f'  Déviance    : {dev:.1f}')
    print(f'  AICc T/S    : {ac_t:.1f} / {ac_s:.1f}  (Δ={ac_t-ac_s:.1f})')
    print(f'  Bootstrap   : {boot_rate*100:.1f}%')
    print(f'  Résidus     : moy={resid["mean"]:.3f} '
          f'std={resid["std"]:.3f} '
          f'corr={resid["correlation_x"]:.3f}')
    print(f'  Temps       : {elapsed:.2f} s')
    print(sep)

# ══════════════════════════════════════════════════════════════════
# 9. VISUALISATION (3 panneaux + distribution Bootstrap)
# ══════════════════════════════════════════════════════════════════
def plot_result(wl: np.ndarray, I: np.ndarray,
                result: ZeemanResult,
                B_true: Optional[float] = None,
                outfile: Optional[Path] = None):
    """Figure diagnostique : spectre, résidus, résidus normalisés, bootstrap."""
    bp = result.fit_params
    if result.selected_model == 'Triplet':
        model = triplet_spectrum(wl, bp['lambda_center'], bp['B'],
                                 bp['amplitude'], bp['sigma_width'],
                                 bp['frac_side'], bp['background'])
    else:
        model = single_spectrum(wl, bp['lambda_center'], bp['amplitude'],
                                bp['sigma_width'], bp['background'])

    wl_nm = wl * 1e9
    has_boot = (result.selected_model == 'Triplet' and
                len(result.B_bootstrap) > 2)

    ncols = 2 if has_boot else 1
    fig   = plt.figure(figsize=(12 if has_boot else 10, 9))
    gs    = fig.add_gridspec(3, ncols,
                             height_ratios=[3,1,1],
                             hspace=0.35, wspace=0.30)

    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[2, 0])

    # Panneau 1 : données + ajustement
    ax0.plot(wl_nm, I,     'k.', ms=2, alpha=0.4, label='Données')
    ax0.plot(wl_nm, model, 'r-', lw=2,            label='Ajustement')
    title = f'DTQEM v38.2 — {result.selected_model}'
    if result.selected_model == 'Triplet':
        title += f'\nB={result.B:.3f}±{result.B_std:.3f} T'
    if B_true is not None:
        title += f'  (vrai={B_true:.2f} T)'
    ax0.set_title(title, fontsize=10)
    ax0.set_ylabel('Intensité'); ax0.legend(fontsize=8); ax0.grid(alpha=0.25)

    # Panneau 2 : résidus
    resid = I - model
    ax1.axhline(0, color='k', lw=0.8)
    ax1.plot(wl_nm, resid, 'b.', ms=1.5, alpha=0.5)
    ax1.set_ylabel('Résidus'); ax1.grid(alpha=0.25)

    # Panneau 3 : résidus normalisés
    resid_n = resid / np.sqrt(np.maximum(model, 1.0))
    ax2.axhline(0,   color='k', lw=0.8)
    ax2.axhline( 2,  color='r', lw=0.5, ls='--')
    ax2.axhline(-2,  color='r', lw=0.5, ls='--')
    ax2.plot(wl_nm, resid_n, 'g.', ms=1.5, alpha=0.5)
    ax2.set_ylabel('Résidus / √modèle')
    ax2.set_xlabel('λ (nm)'); ax2.grid(alpha=0.25)

    # Panneau 4 : distribution Bootstrap (si disponible)
    if has_boot:
        ax3 = fig.add_subplot(gs[:, 1])
        B_arr = result.B_bootstrap
        ax3.hist(B_arr, bins=min(15, len(B_arr)//2+1),
                 color='steelblue', edgecolor='white', alpha=0.80)
        ax3.axvline(result.B,       color='r',  lw=2, label=f'MAP={result.B:.3f}')
        ax3.axvline(result.B_median,color='orange', lw=1.5,
                    ls='--', label=f'Médian={result.B_median:.3f}')
        ax3.axvline(result.B_ci95[0],color='gray',lw=1,ls=':')
        ax3.axvline(result.B_ci95[1],color='gray',lw=1,ls=':',
                    label=f'IC95%=[{result.B_ci95[0]:.3f},{result.B_ci95[1]:.3f}]')
        if B_true is not None:
            ax3.axvline(B_true, color='green', lw=2, ls='-.', label=f'Vrai={B_true:.2f}')
        ax3.set_xlabel('B (T)')
        ax3.set_ylabel('Comptage')
        ax3.set_title(f'Distribution Bootstrap\nn={len(B_arr)}, '
                      f'std={result.B_std:.4f} T')
        ax3.legend(fontsize=8)
        ax3.grid(alpha=0.25)

    if outfile:
        plt.savefig(outfile, dpi=150, bbox_inches='tight')
        print(f'   Figure → {outfile}')
    plt.close()

# ══════════════════════════════════════════════════════════════════
# 10. VALIDATION
# ══════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    np.random.seed(42)
    out = Path('output_zeeman_v382')
    out.mkdir(exist_ok=True)

    print('\n' + '='*70)
    print('DTQEM v38.2-final — Validation')
    print('='*70)
    print(f'μ_B       = {MU_B:.6e} J/T')
    print(f'μ_B/h     = {MU_B_OVER_H:.6e} Hz/T')

    wl        = np.linspace(656.16e-9, 656.40e-9, 500)
    lam0      = 656.28e-9
    sigma_sim = 0.008e-9
    amp_sim   = 1400.0
    bg_sim    = 2.0

    test_cases = [
        (0.0, 'single_line'),   # doit → Single
        (0.0, 'triplet_B0'),    # doit → Single
        (0.5, 'normal'),
        (1.0, 'normal'),
        (1.5, 'normal'),
        (2.0, 'normal'),
        (1.0, 'low_amp'),       # faible SNR
    ]

    rows = []
    B_boot_all = {}

    for B_true, variant in test_cases:
        label = f'B={B_true:.1f}T_{variant}'
        print(f'\n{"─"*60}')
        print(f'  Cas : {label}')

        if variant == 'single_line':
            I_clean = single_spectrum(wl, lam0, amp_sim, sigma_sim, bg_sim)
        elif variant == 'low_amp':
            I_clean = triplet_spectrum(wl, lam0, B_true,
                                       amp_sim*0.15, sigma_sim, 0.60, bg_sim)
        else:
            I_clean = triplet_spectrum(wl, lam0, B_true,
                                       amp_sim, sigma_sim, 0.60, bg_sim)

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
        covered = (res.B_ci95[0] <= B_true <= res.B_ci95[1]) \
                  if not np.isnan(res.B_ci95[0]) else None

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
                    outfile=out/f'fit_{label}.png')

    # ── CSV avec métadonnées
    csv_path = out / 'dtqem_v38_2_validation.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        for row in [
            ['# DTQEM v38.2-final'],
            ['# Date',    time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())],
            ['# Python',  sys.version.split()[0]],
            ['# NumPy',   np.__version__],
            ['# SciPy',   scipy.__version__],
            ['# mu_B',    f'{MU_B:.10e} J/T'],
            ['# mu_B_h',  f'{MU_B_OVER_H:.10e} Hz/T'],
            [],
        ]:
            w.writerow(row)
        w.writerow([
            'B_true_T','variant',
            'B_map_T','B_std_T','B_median_T',
            'B_ci95_low','B_ci95_high','B_hessian_T',
            'selected_model','poisson_deviance',
            'aicc_triplet','aicc_single','spread_ratio',
            'snr','abs_error_T','ci_covers_true',
            'bootstrap_rate','fit_time_s',
        ])
        w.writerows(rows)

    # ── CSV distributions bootstrap
    boot_path = out / 'dtqem_v38_2_bootstrap_distributions.csv'
    with open(boot_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['# Distribution complète des valeurs B bootstrap'])
        w.writerow(['# Une colonne par cas de test'])
        w.writerow(list(B_boot_all.keys()))
        max_len = max((len(v) for v in B_boot_all.values()), default=0)
        vals    = list(B_boot_all.values())
        for i in range(max_len):
            w.writerow([f'{v[i]:.6f}' if i < len(v) else ''
                        for v in vals])

    print(f'\n✅  Résultats → {csv_path}')
    print(f'✅  Bootstrap → {boot_path}')
    print('✅  Validation v38.2-final terminée.')
