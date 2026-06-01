#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Experimental code for the balance condition V = D in pure dephasing.
This is part of DTQEM v13.0 (experimental branch).
Author: Redouane Berramdane & DTQEM Team.

DISCLAIMER: This is a theoretical/numerical exploration. Not yet experimentally validated.

The equation: gamma_phi0 * t_obs = 2 * ln(tan(theta)), for theta > 45°.

Run this script to interactively change parameters and see the balance point.
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Analytical formulas (derived from Lindblad for pure dephasing)
# ----------------------------------------------------------------------
def compute_V_D(gamma_phi0, t_obs, theta_deg):
    """
    Compute visibility V and distinguishability D using the analytic formulas.
    gamma_phi0 : dephasing rate (1/s) as used in DTQEM code (the physical rate is gamma_phi0/2)
    t_obs      : observation time (seconds)
    theta_deg  : initial angle (degrees)
    """
    theta_rad = np.radians(theta_deg)
    sin_theta = np.sin(theta_rad)
    cos_theta = np.cos(theta_rad)
    V = sin_theta * np.exp(- (gamma_phi0 / 2.0) * t_obs)
    D = np.abs(cos_theta)
    return V, D

def find_balance_angle(gamma_phi0, t_obs):
    """
    Returns the angle theta (degrees) that satisfies V = D.
    Derived from gamma_phi0 * t_obs = 2 * ln(tan theta).
    """
    product = gamma_phi0 * t_obs
    tan_theta = np.exp(product / 2.0)
    # avoid overflow for very large product
    if tan_theta > 1e6:
        return 89.999
    theta_rad = np.arctan(tan_theta)
    return np.degrees(theta_rad)

# ----------------------------------------------------------------------
# Interactive console example
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("="*60)
    print("DTQEM Balance Condition V = D (experimental)")
    print("Enter parameters (press Enter to use default values)")
    try:
        g = input("gamma_phi0 (1/s) [default=1000]: ")
        gamma = float(g) if g.strip() else 1000.0
        t = input("t_obs (microseconds) [default=1.0]: ")
        t_obs = float(t) * 1e-6 if t.strip() else 1e-6
    except ValueError:
        gamma = 1000.0
        t_obs = 1e-6
        print("Using default values.")
    
    theta_bal = find_balance_angle(gamma, t_obs)
    V_bal, D_bal = compute_V_D(gamma, t_obs, theta_bal)
    print(f"\nBalance angle θ = {theta_bal:.4f}°")
    print(f"V = {V_bal:.6f}, D = {D_bal:.6f}, difference = {abs(V_bal-D_bal):.2e}")
    
    # Plot V(theta) and D(theta) around balance point
    theta_range = np.linspace(0.1, 89.9, 300)
    V_list = []
    D_list = []
    for th in theta_range:
        vv, dd = compute_V_D(gamma, t_obs, th)
        V_list.append(vv)
        D_list.append(dd)
    
    plt.figure(figsize=(10,5))
    plt.plot(theta_range, V_list, 'b-', label='V(θ)')
    plt.plot(theta_range, D_list, 'r--', label='D(θ)')
    plt.plot(theta_bal, V_bal, 'go', markersize=8, label=f'Balance at θ={theta_bal:.2f}°')
    plt.xlabel('θ (degrees)')
    plt.ylabel('V, D')
    plt.title(f'Balance condition: γφ₀ = {gamma} 1/s, t_obs = {t_obs*1e6:.2f} μs')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
