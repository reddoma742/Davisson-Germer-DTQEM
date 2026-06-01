#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_figure2_only.py

Generates Figure 2: AICc Model Selection Probability vs Sample Size N
for DTQEM v17.0-C (baseline) vs v18.0-C (joint-bath)

Data from simulation: c=0.5, noise σ=0.005, 100 trials per N.
Statistical threshold: N >= 36 required for reliable crossover detection.
"""

import numpy as np
import matplotlib.pyplot as plt

# Set academic plotting style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2

# Data (from simulation results)
N = np.array([10, 20, 30, 40, 50, 60, 70, 80])

# Selection probabilities (%)
v17_prob = np.array([88.0, 56.0, 48.0, 22.0, 12.0, 10.0, 8.0, 4.0])   # v17.0-C (c=0)
v18_prob = np.array([12.0, 44.0, 52.0, 78.0, 88.0, 90.0, 92.0, 96.0])   # v18.0-C (c=0.5)

# Create figure
fig, ax = plt.subplots(figsize=(7, 5))

# Plot lines
ax.plot(N, v17_prob, 'o--', color='crimson', linewidth=2.0, markersize=8,
        label='Baseline Model v17.0-C (c=0)')
ax.plot(N, v18_prob, 's-', color='darkblue', linewidth=2.0, markersize=8,
        label='Joint Model v18.0-C (c=0.5)')

# Highlight threshold at N=36
ax.axvline(x=36, color='forestgreen', linestyle=':', linewidth=2.0)
ax.text(37, 75, r'Reliability Threshold $N \geq 36$',
        color='forestgreen', fontsize=11, fontweight='bold')

# Labels and title
ax.set_title('AICc Model Selection Probability vs. Sample Size $N$',
             fontsize=13, pad=15)
ax.set_xlabel('Sample Size $N$ (Measurement Points)', fontsize=12)
ax.set_ylabel('Selection Probability (%)', fontsize=12)
ax.set_ylim(-2, 102)
ax.set_xlim(8, 82)

# Grid and legend
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='center right', frameon=True, fancybox=False, edgecolor='black')

# Annotate key points
ax.annotate('N=36 threshold', xy=(36, 50), xytext=(45, 40),
            arrowprops=dict(arrowstyle='->', color='forestgreen', lw=1.2),
            fontsize=9, color='forestgreen')

plt.tight_layout()
plt.savefig('figure2.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ figure2.png has been generated successfully!")
