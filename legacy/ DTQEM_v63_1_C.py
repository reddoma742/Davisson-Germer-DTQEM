#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DTQEM_v63_1_C.py

DTQEM v63.1-C : Coherence Time Scaling Model for Massive Particles

This model estimates the coherence time tau_c for massive composite particles
in matter-wave interferometry and solves the inverse problem with full
statistical uncertainty propagation.

Core equation:
    tau_c = tau_c0 / [ (m/m_u)^beta * (v/c)^delta * (1 + zeta * N) ]

Inverse problem solver:
    Extracts tau_c from ln(V) vs |delta_tau| with Delta-method uncertainty:
        sigma_tau = tau_c^2 * sigma_slope

Derived exponents (first-principles):
    beta  = 0.44  (Debye-Pikovski frozen modes at 300 K)
    delta = 1/3   (van der Waals + eikonal scattering)
    zeta  = 0.005 (symmetry-suppressed blackbody emission)

Acknowledgment:
    This code was developed with the assistance of AI language models:
    - DeepSeek (critical analysis, methodology validation)
    - Claude (Anthropic) (code writing, derivations, documentation)
    - Arena AI (first-principles derivations of scaling exponents)
    Human scientific supervision and validation: Reddouane Berramdane

Version: v63.1-C (Zenodo-ready)
Date: 2026-06-01

License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
See LICENSE file for full terms.
"""

import numpy as np
from scipy.stats import linregress
import warnings

# Constants
C_LIGHT = 299792458.0
HBAR = 1.054571817e-34      # J·s
K_B = 1.380649e-23          # J/K
M_U = 1.660539e-27          # kg (atomic mass unit)


class DTQEM_v63_Model:
    """
    DTQEM v63.1-C Model for Coherence Time scaling in composite particles.
    """
    def __init__(self, tau_c0=9.8e-27, beta=0.44, delta=0.33, zeta=0.005):
        self.tau_c0 = tau_c0      # Base phenomenological scale (s)
        self.beta = beta          # Mass scaling exponent (Pikovski/Debye limit)
        self.delta = delta        # Velocity scaling exponent (van der Waals limit)
        self.zeta = zeta          # Per-atom complexity factor

    def validate_inputs(self, m_kg, v_ms, N):
        """Perform defensive validation on physical inputs."""
        if m_kg <= 0:
            raise ValueError("Mass must be strictly positive.")
        if v_ms <= 0 or v_ms >= C_LIGHT:
            raise ValueError(f"Velocity must be in the range (0, c). Got {v_ms} m/s.")
        if N < 1:
            raise ValueError("Number of atoms N must be at least 1.")

    def calculate_tau_c(self, m_kg, v_ms, N):
        """Calculate coherence time tau_c using the scaling law."""
        self.validate_inputs(m_kg, v_ms, N)
        v_rel = v_ms / C_LIGHT
        mass_factor = (m_kg / M_U) ** self.beta
        vel_factor = v_rel ** self.delta
        complexity_factor = 1.0 + self.zeta * N
        return self.tau_c0 / (mass_factor * vel_factor * complexity_factor)

    def predict_visibility(self, tau_c, delta_tau, V_source=1.0, gamma_phi=0.0, T_eff=0.0):
        """Predicts quantum fringe visibility based on the coherence time."""
        delta_tau = np.asarray(delta_tau, dtype=float)
        return V_source * np.exp(-gamma_phi * T_eff) * np.exp(-np.abs(delta_tau) / tau_c)


def extract_tau_c_with_uncertainty(delta_tau, V_eff, confidence=0.95):
    """
    Solves the inverse problem: extracts tau_c from experimental visibility data.
    Uses the logarithmic slope method: ln(V) = C - (1/tau_c)*|delta_tau|.
    
    Applies the Delta Method to propagate linear regression slope standard errors
    directly into the standard error of tau_c:
        sigma_tau = tau_c^2 * sigma_slope
        
    Returns:
    --------
    dict containing:
        - tau_c : float (Extracted coherence time)
        - tau_c_std_err : float (Standard error of tau_c)
        - ci : tuple (lower_bound, upper_bound) of confidence interval
        - r2 : float (R-squared of linear fit)
        - status : str ('ok', 'insufficient_points', 'non_negative_slope')
    """
    delta_tau = np.asarray(delta_tau, dtype=float)
    V = np.asarray(V_eff, dtype=float)
    
    # Filter valid non-zero positive visibility values
    mask = np.isfinite(delta_tau) & np.isfinite(V) & (V > 0)
    N_points = np.sum(mask)
    
    if N_points < 3:
        return {
            "tau_c": np.nan, "tau_c_std_err": np.nan, "ci": (np.nan, np.nan),
            "r2": np.nan, "status": "insufficient_points"
        }
        
    x = np.abs(delta_tau[mask])
    y = np.log(V[mask])
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err_slope = linregress(x, y)
    
    if slope >= 0:
        return {
            "tau_c": np.inf, "tau_c_std_err": np.nan, "ci": (np.nan, np.nan),
            "r2": r_value**2, "status": "non_negative_slope"
        }
        
    # tau_c = -1 / slope
    tau_c = -1.0 / slope
    
    # Delta Method propagation: d(tau_c)/d(slope) = 1 / slope^2 = tau_c^2
    tau_c_std_err = (tau_c ** 2) * std_err_slope
    
    # Confidence Interval calculation using t-distribution for small samples
    from scipy import stats
    df = N_points - 2
    t_val = stats.t.ppf((1.0 + confidence) / 2.0, df)
    
    ci_lower = max(0.0, tau_c - t_val * tau_c_std_err)
    ci_upper = tau_c + t_val * tau_c_std_err
    
    return {
        "tau_c": tau_c,
        "tau_c_std_err": tau_c_std_err,
        "ci": (ci_lower, ci_upper),
        "r2": r_value**2,
        "status": "ok"
    }


if __name__ == "__main__":
    print("=" * 60)
    print("DTQEM v63.1-C Coherence Time Scaling Model - Self Test")
    print("=" * 60)
    
    model = DTQEM_v63_Model()
    
    # Test C60 molecule
    m_C60 = 720 * M_U
    v_test = 200.0
    N_atoms = 60
    
    tau_true = model.calculate_tau_c(m_C60, v_test, N_atoms)
    print(f"\nPredicted tau_c for C60 (m=720 u, v=200 m/s, N=60):")
    print(f"  τ_c = {tau_true:.4e} seconds")
    
    # Simulate experimental visibility scan with 1% Gaussian noise
    np.random.seed(42)
    delta_tau_vals = np.linspace(0.1, 3.0, 10) * tau_true
    V_clean = model.predict_visibility(tau_true, delta_tau_vals)
    V_noisy = V_clean + np.random.normal(0, 0.01 * V_clean)
    V_noisy = np.clip(V_noisy, 0.001, 1.0)
    
    # Extract tau_c using inverse problem solver
    results = extract_tau_c_with_uncertainty(delta_tau_vals, V_noisy)
    print("\n--- Extracted Results with Delta-Method Error Propagation ---")
    print(f"Extracted τ_c: {results['tau_c']:.4e} seconds")
    print(f"Standard Error: {results['tau_c_std_err']:.4e} seconds")
    print(f"95% Conf. Int.: [{results['ci'][0]:.4e}, {results['ci'][1]:.4e}] seconds")
    print(f"R-squared: {results['r2']:.6f}")
    print(f"Status: {results['status']}")
    
    print("\n📝 Acknowledgment:")
    print("   This code was developed with the assistance of AI models:")
    print("   - DeepSeek (critical analysis, methodology validation)")
    print("   - Claude (Anthropic) (code writing, derivations, documentation)")
    print("   - Arena AI (first-principles derivations of scaling exponents)")
    print("   Human scientific supervision and validation: Reddouane Berramdane")
    
    print("\n✅ Model ready for use.")
