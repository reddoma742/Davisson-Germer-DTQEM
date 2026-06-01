#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_figure3.py

DTQEM Figure 3 Generation Script

This script generates Figure 3 for the DTQEM paper:
    - Coherence time τ_c landscape as a function of temperature T and path information I_path
    - Two panels: (a) C60 molecule (N=60) and (b) Giant C700 cluster (N=700)

The unified DTQEM model combines particle-structure scaling (m, v, N) with
environmental conditions (I_path, T).

Usage:
    python generate_figure3.py

Output:
    figure3.png (saved in the current directory or specified output path)

Acknowledgment:
    This code was developed with the assistance of AI language models:
    - DeepSeek (critical analysis, methodology validation)
    - Claude (Anthropic) (code writing, derivations, documentation)
    - Arena AI (first-principles derivations of scaling exponents, unified framework)
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
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['figure.dpi'] = 150


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
C_LIGHT = 299792458.0          # m/s
M_U = 1.660539e-27             # kg (atomic mass unit)
T_REF = 300.0                  # K (reference temperature)

# Model parameters (Unified DTQEM)
tau_c0 = 9.8e-26               # s (base coherence time scale)
beta = 0.44                    # mass scaling exponent (Debye-Pikovski)
delta = 0.33                   # velocity scaling exponent (van der Waals)
zeta = 0.005                   # per-atom complexity factor
A = 1.0                        # kinetic term scaling
B = 1.5                        # thermal term scaling
C_joint = 0.8                  # joint-bath crossover coefficient

# Fixed velocity for comparison
v = 150.0                      # m/s (typical molecular beam velocity)


# ----------------------------------------------------------------------
# Unified DTQEM function
# ----------------------------------------------------------------------
def calculate_unified_tau_c(m_kg, N_atoms, I_path, T_kelvin):
    """
    Calculate coherence time tau_c using the Unified DTQEM equation.
    
    Parameters:
    -----------
    m_kg : float
        Mass in kilograms
    N_atoms : int
        Number of atoms in the particle
    I_path : float or array_like
        Path information (0 to 1)
    T_kelvin : float or array_like
        Temperature in Kelvin
    
    Returns:
    --------
    tau_c : float or ndarray
        Coherence time in seconds
    """
    m_scaled = m_kg / M_U
    v_scaled = v / C_LIGHT
    dT = (T_kelvin - T_REF) / T_REF
    
    # Kinetic term (particle + path information)
    kinetic_term = A * (m_scaled ** beta) * (v_scaled ** delta) * I_path
    
    # Thermal term (complexity + temperature)
    thermal_term = B * (1.0 + zeta * N_atoms) * dT
    
    # Joint term (crossover between particle and environment)
    joint_term = C_joint * (m_scaled ** beta) * (v_scaled ** delta) * I_path * (1.0 + zeta * N_atoms) * dT
    
    denom = kinetic_term + thermal_term + joint_term
    denom = np.maximum(denom, 1e-35)
    return tau_c0 / denom


# ----------------------------------------------------------------------
# Generate Figure 3
# ----------------------------------------------------------------------
def generate_figure3(output_path="figure3.png"):
    """
    Generates Figure 3: Coherence time τ_c landscape for C60 and C700.
    
    Panel (a): C60 fullerene (720 u, N=60)
    Panel (b): Giant carbon cluster (8400 u, N=700)
    
    The x-axis is Temperature (K), y-axis is Path Information I_path.
    Colors represent τ_c in units of 10^-26 seconds.
    """
    print("Generating Figure 3: Coherence Time Landscape...")
    
    # Define particle properties
    m_C60 = 720 * M_U          # kg (C60 fullerene)
    N_C60 = 60                 # number of atoms
    
    m_C700 = 8400 * M_U        # kg (giant cluster, roughly C700)
    N_C700 = 700              # number of atoms
    
    # Create grid for Temperature and Path Information
    T_vals = np.linspace(300.0, 500.0, 150)      # Kelvin
    I_vals = np.linspace(0.0, 1.0, 150)          # Path information (0 to 1)
    T_grid, I_grid = np.meshgrid(T_vals, I_vals)
    
    # Calculate tau_c for both molecules
    tau_C60 = calculate_unified_tau_c(m_C60, N_C60, I_grid, T_grid)
    tau_C700 = calculate_unified_tau_c(m_C700, N_C700, I_grid, T_grid)
    
    # Convert to units of 10^-26 seconds for better visualization
    tau_C60_plot = tau_C60 * 1e26
    tau_C700_plot = tau_C700 * 1e26
    
    # Create figure with two panels side by side
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    
    # Panel (a): C60
    im1 = axes[0].imshow(tau_C60_plot, 
                         extent=[300, 500, 0, 1], 
                         origin='lower', 
                         aspect='auto', 
                         cmap='plasma')
    axes[0].set_title(r'(a) Coherence Time $\tau_c$ Landscape for $C_{60}$ ($N=60$)', 
                      fontsize=11, fontweight='bold')
    axes[0].set_xlabel('Temperature $T$ (Kelvin)', fontsize=10)
    axes[0].set_ylabel('Path Information $I_{path}$', fontsize=10)
    
    # Panel (b): C700
    im2 = axes[1].imshow(tau_C700_plot, 
                         extent=[300, 500, 0, 1], 
                         origin='lower', 
                         aspect='auto', 
                         cmap='plasma')
    axes[1].set_title(r'(b) Coherence Time $\tau_c$ Landscape for Giant Cluster ($N=700$)', 
                      fontsize=11, fontweight='bold')
    axes[1].set_xlabel('Temperature $T$ (Kelvin)', fontsize=10)
    axes[1].set_ylabel('Path Information $I_{path}$', fontsize=10)
    
    # Add a single colorbar for both panels
    cbar = fig.colorbar(im1, ax=axes, orientation='vertical', pad=0.05, aspect=40)
    cbar.set_label(r'Coherence Time $\tau_c$ ($\times 10^{-26}$ s)', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Figure 3 saved as '{output_path}'")
    return output_path


# ----------------------------------------------------------------------
# Main execution
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("DTQEM Figure 3 Generation Script")
    print("=" * 60)
    
    # Generate figure
    generate_figure3("figure3.png")
    
    print("\n" + "=" * 60)
    print("Figure 3 generated successfully!")
    print("\n📝 Acknowledgment:")
    print("   This code was developed with the assistance of AI models:")
    print("   - DeepSeek (critical analysis, methodology validation)")
    print("   - Claude (Anthropic) (code writing, derivations, documentation)")
    print("   - Arena AI (first-principles derivations, unified framework)")
    print("   Human scientific supervision and validation: Reddouane Berramdane")
    print("\n✅ Ready for use.")
    print("=" * 60)
