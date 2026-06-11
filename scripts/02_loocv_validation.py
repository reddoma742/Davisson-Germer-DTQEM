"""
DTQEM: LOOCV Validation
=======================
Performs Leave-One-Out Cross-Validation to verify Table II metrics.
"""
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import r2_score
import json
import os

os.makedirs('data/calibration', exist_ok=True)

def model_v18(X, C0, a, b, c):
    I_path, dT_Tref = X
    return C0 * np.exp(-a * I_path - b * dT_Tref - c * I_path * dT_Tref)

# Load or generate data
if os.path.exists('data/calibration/synthetic_grid.csv'):
    df = pd.read_csv('data/calibration/synthetic_grid.csv')
else:
    # Fallback: generate on the fly
    print("⚠️ Synthetic data not found. Generating...")
    C0_true, a_true, b_true, c_true = 0.3675, 1.6968, 0.8055, 0.5000
    T_ref = 300.0
    I_vals = np.linspace(0, 1, 21)
    T_vals = np.linspace(300, 550, 21)
    rows = []
    for I in I_vals:
        for T in T_vals:
            dT = T - T_ref
            C = C0_true * np.exp(-a_true * I - b_true * (dT/T_ref) - c_true * I * (dT/T_ref))
            rows.append({'I_path': I, 'T': T, 'C': C})
    df = pd.DataFrame(rows)

I_path = df['I_path'].values
T = df['T'].values
C_obs = df['C'].values
T_ref = 300.0
X_data = np.vstack([I_path, (T - T_ref)/T_ref])

# Initial guess
p0 = [0.3, 1.5, 0.7, 0.4]

# Full fit
popt, pcov = curve_fit(model_v18, X_data, C_obs, p0=p0, maxfev=5000)
C_pred_full = model_v18(X_data, *popt)
r2_full = r2_score(C_obs, C_pred_full)
rmse_full = np.sqrt(np.mean((C_obs - C_pred_full)**2))

# LOOCV
loo = LeaveOneOut()
pred_cv = np.zeros_like(C_obs)
for train_idx, test_idx in loo.split(C_obs):
    X_train = X_data[:, train_idx]
    y_train = C_obs[train_idx]
    X_test = X_data[:, test_idx]
    p, _ = curve_fit(model_v18, X_train, y_train, p0=p0, maxfev=5000)
    pred_cv[test_idx] = model_v18(X_test, *p)

r2_cv = r2_score(C_obs, pred_cv)
rmse_cv = np.sqrt(np.mean((C_obs - pred_cv)**2))

# Save results
results = {
    "parameters": {"C0": popt[0], "a": popt[1], "b": popt[2], "c": popt[3]},
    "uncertainties_1sigma": np.sqrt(np.diag(pcov)).tolist(),
    "R2_full": r2_full,
    "LOOCV_R2": r2_cv,
    "RMSE_full": rmse_full,
    "LOOCV_RMSE": rmse_cv
}

with open('data/calibration/fitted_parameters.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "="*50)
print("📊 LOOCV Validation Results (Table II)")
print("="*50)
print(f"Parameters:")
print(f"  C0 = {popt[0]:.4f} ± {np.sqrt(pcov[0,0]):.4f}")
print(f"  a  = {popt[1]:.4f} ± {np.sqrt(pcov[1,1]):.4f}")
print(f"  b  = {popt[2]:.4f} ± {np.sqrt(pcov[2,2]):.4f}")
print(f"  c  = {popt[3]:.4f} ± {np.sqrt(pcov[3,3]):.4f}")
print(f"\nMetrics:")
print(f"  R² (full)    = {r2_full:.4f}  (Target: 0.9982)")
print(f"  LOOCV R²     = {r2_cv:.4f}   (Target: 0.9814)")
print(f"  RMSE (full)  = {rmse_full:.4f}")
print(f"  LOOCV RMSE   = {rmse_cv:.4f}")
print("="*50)
print("✅ Results saved to: data/calibration/fitted_parameters.json")
