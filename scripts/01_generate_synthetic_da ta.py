"""
DTQEM: Generate Synthetic Calibration Data
==========================================
Generates the synthetic dataset used for calibration in Paper I.
Output: data/calibration/synthetic_grid.csv
"""
import numpy as np
import pandas as pd
import os

# Create directory if it doesn't exist
os.makedirs('data/calibration', exist_ok=True)

# True parameters from Table I
C0_true = 0.3675
a_true = 1.6968
b_true = 0.8055
c_true = 0.5000
T_ref = 300.0

# Generate grid
I_path_vals = np.linspace(0, 1, 21)
T_vals = np.linspace(300, 550, 21)

data = []
for I in I_path_vals:
    for T in T_vals:
        delta_T = T - T_ref
        C = C0_true * np.exp(-a_true * I - b_true * (delta_T / T_ref) - c_true * I * (delta_T / T_ref))
        data.append({'I_path': I, 'T': T, 'C': C})

df = pd.DataFrame(data)
df.to_csv('data/calibration/synthetic_grid.csv', index=False)

print(f"✅ Generated {len(df)} samples")
print(f"📁 Saved to: data/calibration/synthetic_grid.csv")
print(f"   I_path range: [{I_path_vals.min():.0f}, {I_path_vals.max():.0f}]")
print(f"   T range: [{T_vals.min():.0f}, {T_vals.max():.0f}] K")
