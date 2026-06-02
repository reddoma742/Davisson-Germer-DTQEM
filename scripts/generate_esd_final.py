#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_esd_final.py

Generate Entanglement Sudden Death (ESD) time landscape figure for DTQEM.
Output: figures/figure_esd_final.png

Acknowledgment:
    AI assistance: DeepSeek, Claude (Anthropic), Arena AI
    Human supervision: Reddouane Berramdane

License: CC BY-NC-SA 4.0
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Create figures directory if it doesn't exist
os.makedirs('figures', exist_ok=True)

# ============================================================
# 1. Academic plotting style
# ============================================================
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2

# ============================================================
# 2. DTQEM parameters for ESD
# ============================================================
alpha = 1.0      # Path information coefficient
beta = 0.85      # Temperature coefficient
gamma = 0.5      # Joint-bath crossover coefficient
T_ref = 300.0    # Reference temperature (K)

# Initial state populations (X-state)
rho14_0 = 0.35   # |rho_14(0)|
rho22_0 = 0.10   # rho_22(0)
rho33_0 = 0.10   # rho_33(0)

# Calculate numerator K = ln(|rho_14(0)| / sqrt(rho_22(0) * rho_33(0)))
K = np.log(rho14_0 / np.sqrt(rho22_0 * rho33_0))

# ============================================================
# 3. Grid setup
# ============================================================
I_vals = np.linspace(0.0, 1.0, 300)      # I_path from 0 to 1
T_vals = np.linspace(300.0, 500.0, 300)  # Temperature from 300 to 500 K

I_grid, T_grid = np.meshgrid(I_vals, T_vals)

# Normalized temperature difference (non-negative)
dT_grid = (T_grid - T_ref) / T_ref
dT_grid = np.maximum(dT_grid, 0.0)

# Denominator: total dephasing rate
rate = alpha * I_grid + beta * dT_grid + gamma * I_grid * dT_grid

# ============================================================
# 4. Safe calculation of t_ESD
# ============================================================
t_esd = np.full_like(rate, np.nan)
mask = rate > 0
t_esd[mask] = K / rate[mask]

# Remove extreme outliers for better visual contrast
p99 = np.nanpercentile(t_esd, 99)
t_esd = np.clip(t_esd, 0, p99)

# ============================================================
# 5. Create the publication-ready figure
# ============================================================
fig, ax = plt.subplots(figsize=(7.5, 5.5))

# Filled contour with reversed viridis colormap
cf = ax.contourf(I_grid, T_grid, t_esd, levels=20, cmap='viridis_r')

# White contour lines with labels
contour_levels = [1.5, 2.0, 3.0, 5.0, 10.0, 20.0, 30.0, 50.0]
cs = ax.contour(I_grid, T_grid, t_esd, levels=contour_levels,
                colors='white', linewidths=0.8, alpha=0.9)
ax.clabel(cs, inline=True, fontsize=8, fmt='%.1f')

# Colorbar
cbar = fig.colorbar(cf, ax=ax)
cbar.set_label(r'$t_{\mathrm{ESD}}$ (ps)', fontsize=10)

# Labels and title
ax.set_xlabel(r'Path Information Parameter $I_{\mathrm{path}}$', fontsize=11)
ax.set_ylabel(r'Temperature $T$ (K)', fontsize=11)
ax.set_title(r'Entanglement Sudden Death Time in DTQEM', fontsize=12, fontweight='bold')

# Axis limits
ax.set_xlim(0, 1)
ax.set_ylim(300, 500)

# Grid
ax.grid(True, linestyle=':', alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure_esd_final.png', dpi=300, bbox_inches='tight')
plt.close()

print("=" * 60)
print("✅ ESD figure generated successfully!")
print("   Location: figures/figure_esd_final.png")
print("   Resolution: 300 DPI")
print("=" * 60)
