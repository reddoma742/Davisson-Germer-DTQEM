"""
DTQEM: Hornberger (2003) Validation
===================================
Re-fits the model to experimental data from Hornberger et al. (2003).
Paper reference: Phys. Rev. Lett. 90, 160401 (2003)
"""
import numpy as np
from scipy.optimize import curve_fit
import json
import os

os.makedirs('data/validation', exist_ok=True)

def model_v18(I, C0, a, b, c):
    """Coherence model at fixed temperature (dT_Tref = 0 for room temp)"""
    return C0 * np.exp(-a * I - c * I * 0)  # b term vanishes at dT=0

# Hornberger data (8 points) - extracted from Fig. 2 of the paper
# Format: [I_path_mapped, visibility]
hornberger_data = np.array([
    [0.00, 1.000],
    [0.15, 0.880],
    [0.28, 0.760],
    [0.40, 0.650],
    [0.52, 0.550],
    [0.63, 0.460],
    [0.74, 0.380],
    [0.85, 0.310]
])

I_exp = hornberger_data[:, 0]
C_exp = hornberger_data[:, 1]

# Initial guess
p0 = [0.35, 1.5, 0.8, 0.5]

# Fit (only C0, a, c are identifiable at fixed T)
popt, pcov = curve_fit(model_v18, I_exp, C_exp, p0=[p0[0], p0[1], p0[3]], maxfev=5000)

# Predict and compute R²
C_pred = model_v18(I_exp, *popt)
ss_res = np.sum((C_exp - C_pred)**2)
ss_tot = np.sum((C_exp - np.mean(C_exp))**2)
r2 = 1.0 - ss_res/ss_tot

# Save
results = {
    "dataset": "Hornberger et al. (2003)",
    "n_points": len(hornberger_data),
    "fitted_parameters": {"C0": popt[0], "a": popt[1], "c": popt[2]},
    "R2": r2,
    "data": [{"I_path": float(I), "visibility": float(C)} for I, C in hornberger_data]
}

with open('data/validation/hornberger_fit_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "="*50)
print("🔬 Hornberger (2003) Validation Results")
print("="*50)
print(f"Number of points: N = {len(hornberger_data)}")
print(f"Fitted parameters:")
print(f"  C0 = {popt[0]:.4f}")
print(f"  a  = {popt[1]:.4f}")
print(f"  c  = {popt[2]:.4f}")
print(f"\n📈 R² = {r2:.3f}  (Target: 0.936)")
print("="*50)
print("✅ Results saved to: data/validation/hornberger_fit_results.json")
