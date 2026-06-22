#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dtqem_v63_joint.py

DTQEM v63.2-C : Joint Scaling Model & AICc Threshold Simulation

Implements the generalized scaling model for massive particle interferometry,
introducing a mass-velocity crossover coupling term (c_mv) representing
cross-correlated environmental dephasing (e.g., friction-induced heating).

Core equation:
    tau_c = tau_c0 / [ (m/m_u)^beta * (v/c)^delta * (1 + zeta*N) *
                       exp(c_mv * ln(m/m_u) * ln(v/c)) ]

This script runs a Monte Carlo simulation using AICc to find the minimum
number of experimental data points (N_threshold) required to detect the
joint-bath crossover coupling c_mv.

Acknowledgment:
    This code was developed with the assistance of AI language models:
    - DeepSeek (critical analysis, methodology validation)
    - Claude (Anthropic) (code writing, derivations, documentation)
    - Arena AI (first-principles derivations of scaling exponents and crossover)
    Human scientific supervision and validation: Reddouane Berramdane

Version: v63.2-C (Zenodo-ready)
Date: 2026-06-01

License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
See LICENSE file for full terms.
"""

import numpy as np
import scipy.stats as stats
import warnings
from scipy.optimize import minimize

# Constants
C_LIGHT = 299792458.0
M_U = 1.660539e-27


class JointScalingModel:
    """
    DTQEM v63.2-C Joint Scaling Model with mass-velocity crossover coupling.
    """
    def __init__(self, tau_c0=9.8e-27, beta=0.44, delta=0.33, zeta=0.005, c_mv=0.15):
        self.tau_c0 = tau_c0
        self.beta = beta
        self.delta = delta
        self.zeta = zeta
        self.c_mv = c_mv  # Mass-velocity crossover coupling

    def calculate_tau_c(self, m_kg, v_ms, N_atoms):
        """
        Calculate coherence time tau_c including mass-velocity crossover.
        """
        m_scaled = m_kg / M_U
        v_scaled = v_ms / C_LIGHT
        
        # Base terms
        mass_term = m_scaled ** self.beta
        vel_term = v_scaled ** self.delta
        complexity_term = 1.0 + self.zeta * N_atoms
        
        # Crossover term: exp(c_mv * ln(m) * ln(v))
        crossover_term = np.exp(self.c_mv * np.log(m_scaled) * np.log(v_scaled))
        
        return self.tau_c0 / (mass_term * vel_term * complexity_term * crossover_term)


def fit_scaling_model(m_vals, v_vals, N_vals, tau_vals, fit_crossover=False):
    """
    Fits the scaling parameters in log-space:
    ln(tau_c) = ln(tau_c0) - beta * ln(m) - delta * ln(v) 
                - c_mv * ln(m) * ln(v) - ln(1 + zeta*N)
    
    Returns parameters and Residual Sum of Squares (RSS).
    """
    m_scaled = m_vals / M_U
    v_scaled = v_vals / C_LIGHT
    
    Y = np.log(tau_vals) + np.log(1.0 + 0.005 * N_vals)  # zeta = 0.005 fixed
    
    if fit_crossover:
        # X: [1, -ln(m), -ln(v), -ln(m)*ln(v)]
        X = np.column_stack([np.ones_like(m_scaled), 
                             -np.log(m_scaled), 
                             -np.log(v_scaled), 
                             -np.log(m_scaled) * np.log(v_scaled)])
        beta_fit, rss, _, _ = np.linalg.lstsq(X, Y, rcond=None)
        rss_val = np.sum((Y - X @ beta_fit)**2)
        k = 4  # tau_c0, beta, delta, c_mv
    else:
        # X: [1, -ln(m), -ln(v)]
        X = np.column_stack([np.ones_like(m_scaled), 
                             -np.log(m_scaled), 
                             -np.log(v_scaled)])
        beta_fit, rss, _, _ = np.linalg.lstsq(X, Y, rcond=None)
        rss_val = np.sum((Y - X @ beta_fit)**2)
        k = 3  # tau_c0, beta, delta
        
    return k, rss_val


def run_aicc_simulation(noise_std=0.15, trials=200):
    """
    Simulates AICc model selection between Independent v63.1-C and Joint v63.2-C
    as a function of the experimental dataset size N_samples.
    """
    np.random.seed(42)
    true_model = JointScalingModel(c_mv=0.15)
    
    sample_sizes = [8, 16, 24, 32, 40, 60, 100]
    report = {}
    
    # Typical experimental molecules (masses and atomic complexity)
    typical_particles = [
        {"name": "C60", "m": 720 * M_U, "N": 60},
        {"name": "C70", "m": 840 * M_U, "N": 70},
        {"name": "C84", "m": 1008 * M_U, "N": 84},
        {"name": "Giant-A", "m": 2500 * M_U, "N": 180},
        {"name": "Giant-B", "m": 5000 * M_U, "N": 350},
        {"name": "Giant-C", "m": 10000 * M_U, "N": 700},
    ]
    
    for N in sample_sizes:
        v63_1_wins = 0
        v63_2_wins = 0
        
        for _ in range(trials):
            # Generate random experimental configurations
            m_sim = []
            v_sim = []
            N_sim = []
            for _ in range(N):
                p = np.random.choice(typical_particles)
                m_sim.append(p["m"])
                N_sim.append(p["N"])
                v_sim.append(np.random.uniform(80.0, 350.0))  # Velocity range in ms^-1
                
            m_sim = np.array(m_sim)
            v_sim = np.array(v_sim)
            N_sim = np.array(N_sim)
            
            # Generate true tau_c with crossover + proper log-normal experimental noise
            tau_clean = true_model.calculate_tau_c(m_sim, v_sim, N_sim)
            tau_noisy = tau_clean * np.exp(np.random.normal(0, noise_std, N))
            
            # 1. Fit Independent Model (v63.1-C, K=3)
            K1, rss1 = fit_scaling_model(m_sim, v_sim, N_sim, tau_noisy, fit_crossover=False)
            s2_1 = rss1 / N
            if (N - K1 - 1) > 0:
                aicc1 = N * np.log(s2_1 if s2_1 > 0 else 1e-15) + 2*K1 + (2*K1*(K1+1)) / (N - K1 - 1)
            else:
                aicc1 = np.inf
            
            # 2. Fit Joint Model (v63.2-C, K=4)
            K2, rss2 = fit_scaling_model(m_sim, v_sim, N_sim, tau_noisy, fit_crossover=True)
            s2_2 = rss2 / N
            if (N - K2 - 1) > 0:
                aicc2 = N * np.log(s2_2 if s2_2 > 0 else 1e-15) + 2*K2 + (2*K2*(K2+1)) / (N - K2 - 1)
            else:
                aicc2 = np.inf
            
            if aicc1 < aicc2:
                v63_1_wins += 1
            else:
                v63_2_wins += 1
                
        accuracy = (v63_2_wins / trials) * 100
        report[N] = {
            "v63.1-C (Independent) Selection %": (v63_1_wins / trials) * 100,
            "v63.2-C (Joint Crossover) Selection %": accuracy,
            "Reliability": "Low (Biased to v63.1-C)" if accuracy < 50.0 else (
                "Moderate" if accuracy < 85.0 else "High (Correctly Detects Crossover)"
            )
        }
    return report


if __name__ == "__main__":
    print("=" * 80)
    print("DTQEM v63.2-C: AICc Simulation for Mass-Velocity Crossover Detection")
    print("=" * 80)
    
    results = run_aicc_simulation(noise_std=0.15, trials=200)
    
    print("\nSample Size N | v63.1-C (Independent) | v63.2-C (Joint) | Reliability")
    print("-" * 80)
    for n, stats_data in results.items():
        print(f"     N = {n:<3}    |      {stats_data['v63.1-C (Independent) Selection %']:5.1f}%         |     {stats_data['v63.2-C (Joint Crossover) Selection %']:5.1f}%     | {stats_data['Reliability']}")
    
    print("\n" + "=" * 80)
    print("\n📝 Acknowledgment:")
    print("   This code was developed with the assistance of AI models:")
    print("   - DeepSeek (critical analysis, methodology validation)")
    print("   - Claude (Anthropic) (code writing, derivations, documentation)")
    print("   - Arena AI (first-principles derivations of scaling exponents and crossover)")
    print("   Human scientific supervision and validation: Reddouane Berramdane")
    print("\n✅ Model ready for use.")
