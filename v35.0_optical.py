"""
DTQEM v35.0-optical – Double‑Slit Inversion for Photons (Observer Strength E)
================================================================================
Author: Reddouane Berramdane
License: CC BY‑NC 4.0

Model: I(x) = I₀[(1-E) cos²(π d x/(λ L)) + E] * sinc²(π a x/(λ L)) + (B₀+B₁x)
Parameters: I₀, d, E
B₀, B₁ fixed (measured with laser off)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution, minimize
from scipy.fft import fft, fftfreq
from dataclasses import dataclass
from typing import Optional, Tuple
import warnings

def model_optical(x, I0, d, E, B0, B1, lam, L, a=None):
    theta = np.pi * d * x / (lam * L)
    interference = (1.0 - E) * np.cos(theta)**2 + E
    model = I0 * interference
    if a is not None and a > 0:
        arg_env = np.pi * a * x / (lam * L)
        model *= np.sinc(arg_env / np.pi)**2
    return model + (B0 + B1 * x)

def objective(params, x, I, sigma, lam, L, a, B0, B1):
    I0, d, E = params
    model = model_optical(x, I0, d, E, B0, B1, lam, L, a)
    var = np.maximum(model, 1e-9)
    resid = (I - model) / np.sqrt(var)
    return 0.5 * np.sum(resid**2)

def estimate_d_fft(x, I, lam, L):
    coeffs = np.polyfit(x, I, 1)
    detrended = I - np.polyval(coeffs, x)
    n = len(x)
    dx = x[1] - x[0]
    freqs = fftfreq(n, dx)
    f_fft = fft(detrended)
    power = np.abs(f_fft)**2
    idx = np.argmax(power[1:n//2]) + 1
    f_peak = freqs[idx]
    d_est = lam * L * f_peak
    return np.clip(d_est, 1e-6, 2e-3)

def fit_optical(x, I, sigma, lam, L, a, B0, B1, use_global=True):
    I_max = np.max(I)
    bounds = [(0.01*I_max, 100*I_max), (1e-6, 2e-3), (0.0, 1.0)]
    d_est = estimate_d_fft(x, I, lam, L)
    I0_est = I_max - np.min(I)
    E_est = 0.5
    init = [I0_est, d_est, E_est]
    x0 = np.array(init)
    if use_global:
        res_de = differential_evolution(
            objective, bounds, args=(x, I, sigma, lam, L, a, B0, B1),
            maxiter=60, popsize=12, seed=42, disp=False, workers=1, updating='deferred'
        )
        x0 = res_de.x
    res = minimize(objective, x0, args=(x, I, sigma, lam, L, a, B0, B1),
                   method='L-BFGS-B', bounds=bounds, options={'ftol':1e-12, 'maxiter':2000})
    params = {'I0': res.x[0], 'd': res.x[1], 'E': res.x[2]}
    chi2 = res.fun * 2.0
    return params, chi2, res.success, res.x

def bootstrap_optical(x, I, sigma, lam, L, a, B0, B1, best_params, best_x0, n_bootstrap=150, n_restarts=3):
    I_max = np.max(I)
    bounds = [(0.01*I_max, 100*I_max), (1e-6, 2e-3), (0.0, 1.0)]
    I_model = model_optical(x, best_params['I0'], best_params['d'], best_params['E'], B0, B1, lam, L, a)
    I_model = np.maximum(I_model, 1e-9)
    boot = {'I0': [], 'd': [], 'E': []}
    n_success = 0
    for _ in range(n_bootstrap):
        I_synth = np.random.poisson(I_model)
        sigma_synth = np.sqrt(np.maximum(I_synth, 1e-9))
        best_f = np.inf
        best_p = None
        for _ in range(n_restarts):
            pert = 1.0 + np.random.normal(0, 0.03, size=3)
            x0 = np.clip(best_x0 * pert, [b[0] for b in bounds], [b[1] for b in bounds])
            res = minimize(objective, x0, args=(x, I_synth, sigma_synth, lam, L, a, B0, B1),
                           method='L-BFGS-B', bounds=bounds, options={'ftol':1e-12, 'maxiter':2000})
            if res.success and res.fun < best_f:
                best_f = res.fun
                best_p = res.x
        if best_p is not None:
            n_success += 1
            boot['I0'].append(best_p[0])
            boot['d'].append(best_p[1])
            boot['E'].append(best_p[2])
    result = {}
    for k in boot:
        arr = np.array(boot[k])
        result[f'{k}_std'] = np.std(arr) if len(arr)>1 else np.nan
        result[f'{k}_ci95'] = (np.percentile(arr,2.5), np.percentile(arr,97.5)) if len(arr)>1 else (np.nan,np.nan)
    result['success_rate'] = n_success / n_bootstrap
    return result

@dataclass
class ResultOptical:
    I0: float; d: float; E: float; chi2_red: float; success: bool
    d_um: float; I0_std: float; d_std: float; E_std: float
    I0_ci95: Tuple[float,float]; d_ci95: Tuple[float,float]; E_ci95: Tuple[float,float]

def run_optical(x, I, lam, L, a, fixed_B0, fixed_B1, use_global=True, n_bootstrap=150, verbose=True):
    sigma = np.sqrt(np.maximum(I, 1e-9))
    params, chi2, success, x0 = fit_optical(x, I, sigma, lam, L, a, fixed_B0, fixed_B1, use_global)
    n_data = len(x)
    chi2_red = chi2 / (n_data - 3)
    boot = bootstrap_optical(x, I, sigma, lam, L, a, fixed_B0, fixed_B1, params, x0, n_bootstrap)
    if verbose:
        print("\n=== DTQEM v35.0 Optical ===")
        print(f"d = {params['d']*1e6:.2f} µm")
        print(f"E = {params['E']:.5f} ± {boot['E_std']:.5f}")
        print(f"I0 = {params['I0']:.2f}")
        print(f"χ²_red = {chi2_red:.4f}")
    return ResultOptical(I0=params['I0'], d=params['d'], E=params['E'], chi2_red=chi2_red, success=success,
                         d_um=params['d']*1e6, I0_std=boot['I0_std'], d_std=boot['d_std'], E_std=boot['E_std'],
                         I0_ci95=boot['I0_ci95'], d_ci95=boot['d_ci95'], E_ci95=boot['E_ci95'])

if __name__ == "__main__":
    # Example
    x = np.linspace(-0.01, 0.01, 500)
    I_clean = model_optical(x, I0=100, d=500e-6, E=0.2, B0=5, B1=185, lam=650e-9, L=1.0, a=80e-6)
    I_data = np.random.poisson(np.maximum(I_clean,1e-9))
    res = run_optical(x, I_data, lam=650e-9, L=1.0, a=80e-6, fixed_B0=5.0, fixed_B1=185.0)
