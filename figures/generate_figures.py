#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_figures.py

DTQEM Figure Generation Script

This script generates two key figures for the DTQEM paper:
    - figure1.png: Lorentzian spectral line shape of the path-decoherence coefficient a(ω_c)
    - figure2.png: AICc model selection probability vs. sample size N (threshold at N=36)

Usage:
    python generate_figures.py

Output:
    figure1.png, figure2.png (saved in the current directory or specified output path)

Acknowledgment:
    This code was developed with the assistance of AI language models:
    - DeepSeek (critical analysis, methodology validation)
    - Claude (Anthropic) (code writing, derivations, documentation)
    - Arena AI (first-principles derivations, unified framework)
    Human scientific supervision and validation: Reddouane Berramdane

Version: 1.0 (Zenodo-ready)
Date: 2026-06-01

License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
See LICENSE file for full terms.
"""

import numpy as np
import matplotlib.pyplot as plt

# Set academic plotting style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['figure.dpi'] = 150


# ----------------------------------------------------------------------
# Figure 1: Lorentzian Curve of a(ω_c, T)
# ----------------------------------------------------------------------
def generate_figure1(output_path="figure1.png"):
    """
    Generates Figure 1: Lorentzian spectral line shape of the path-decoherence
    coefficient a(ω_c) as a function of detector coupling frequency.
    
    The analytical form is derived from the spin-boson model with a Lorentzian
    spectral density, representing a structured cavity mode.
    """
    print("Generating Figure 1: Lorentzian Peak...")
    
    # Parameters
    omega_path = 5.0  # GHz (path-probe frequency)
    gamma = 1.0       # GHz (cavity spectral width)
    eta = 1.6968      # coupling strength (calibrated from v18.0-C)
    
    # Frequency range
    omega_c = np.linspace(1.0, 9.0, 500)
    
    # Lorentzian line shape (high-temperature limit, coth ~ 1 for qualitative plot)
    # a_omega = (eta / gamma) / (1 + ((omega_c - omega_path) / gamma)^2)
    a_omega = (eta / gamma) / (1.0 + ((omega_c - omega_path) / gamma) ** 2)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    ax.plot(omega_c, a_omega, color='darkblue', linewidth=2.0,
            label=r'Analytical $a(\omega_c, T)$')
    ax.axvline(x=omega_path, color='red', linestyle='--', linewidth=1.2,
               label=r'$\omega_{path} = 5.0$ GHz')
    ax.scatter([omega_path], [eta/gamma], color='red', s=50, zorder=5)
    
    ax.set_title(r'Detector Path-Decoherence Spectral Line Shape $a(\omega_c)$',
                 fontsize=12, pad=12)
    ax.set_xlabel(r'Detector Coupling Frequency $\omega_c$ (GHz)', fontsize=11)
    ax.set_ylabel(r'Path Decoherence Coefficient $a(\omega_c)$', fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, fancybox=False, edgecolor='black')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Figure 1 saved as '{output_path}'")
    return output_path


# ----------------------------------------------------------------------
# Figure 2: AICc Model Selection Probability vs N
# ----------------------------------------------------------------------
def generate_figure2(output_path="figure2.png"):
    """
    Generates Figure 2: AICc model selection probability as a function of
    sample size N.
    
    This figure demonstrates the statistical threshold discovered by the DTQEM team:
    - Small datasets (N=8) are biased toward the simpler v17.0-C model (89%).
    - At N >= 36, the correct joint-bath model v18.0-C is reliably selected (>=79%).
    
    Data from simulation with c=0.5, noise σ=0.005, 100 trials per N.
    """
    print("Generating Figure 2: AICc Threshold...")
    
    # Sample sizes and selection probabilities (from simulation results)
    N = np.array([8, 16, 24, 32, 36, 50, 80])
    v17_prob = np.array([89.0, 57.0, 43.0, 33.0, 21.0, 10.0, 5.0])
    v18_prob = np.array([11.0, 43.0, 57.0, 67.0, 79.0, 90.0, 95.0])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    ax.plot(N, v17_prob, 'o--', color='crimson', linewidth=1.8, markersize=8,
            label='Baseline Model v17.0-C (c=0)')
    ax.plot(N, v18_prob, 's-', color='darkblue', linewidth=2.0, markersize=8,
            label='Joint Model v18.0-C (c=0.5)')
    
    # Highlight threshold at N=36
    ax.axvline(x=36, color='forestgreen', linestyle=':', linewidth=1.5)
    ax.text(37, 75, r'Reliability Threshold $N \geq 36$',
            color='forestgreen', fontsize=10, fontweight='bold')
    
    ax.set_title('AICc Model Selection Probability vs. Sample Size $N$',
                 fontsize=12, pad=12)
    ax.set_xlabel('Sample Size $N$ (Measurement Points)', fontsize=11)
    ax.set_ylabel('Selection Probability (%)', fontsize=11)
    ax.set_ylim(-5, 105)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='center right', frameon=True, fancybox=False, edgecolor='black')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Figure 2 saved as '{output_path}'")
    return output_path


# ----------------------------------------------------------------------
# Main execution
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("DTQEM Figure Generation Script")
    print("=" * 60)
    
    # Generate both figures
    generate_figure1("figure1.png")
    generate_figure2("figure2.png")
    
    print("\n" + "=" * 60)
    print("All figures generated successfully!")
    print("\n📝 Acknowledgment:")
    print("   This code was developed with the assistance of AI models:")
    print("   - DeepSeek (critical analysis, methodology validation)")
    print("   - Claude (Anthropic) (code writing, derivations, documentation)")
    print("   - Arena AI (first-principles derivations, unified framework)")
    print("   Human scientific supervision and validation: Reddouane Berramdane")
    print("\n✅ Ready for use.")
    print("=" * 60)
