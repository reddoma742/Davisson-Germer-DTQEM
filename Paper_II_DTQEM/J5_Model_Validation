"""
Paper II Figures — FINAL VERSION WITH AUTO-DOWNLOAD
=====================================================
- Generates Figure 1 and Figure 2 with corrected legends and RMSE.
- Automatically downloads the files in Google Colab.
- Works as a standalone script on any platform.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad
import os

print("Starting figure generation...")

# =============================================================================
# DATA
# =============================================================================
kB_cm = 0.69503476

T_data = np.array([5.0, 7.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0,
                   90.0, 100.0, 150.0, 200.0, 300.0, 400.0])

rate_S2 = np.array([20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 22.0, 25.0, 35.0,
                    50.0, 80.0, 250.0, 400.0, 700.0, 900.0])
rate_S8 = np.array([0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5, 0.8, 1.5, 3.0,
                    7.0, 15.0, 150.0, 350.0, 650.0, 850.0])
rate_S3 = np.array([0.015, 0.015, 0.015, 0.015, 0.015, 0.018, 0.025, 0.04, 0.1, 0.3,
                    0.8, 2.0, 100.0, 300.0, 600.0, 800.0])

samples = {'S2': rate_S2, 'S8': rate_S8, 'S3': rate_S3}

# =============================================================================
# TABLE 1 VALUES (fixed for plotting consistency with manuscript)
# =============================================================================
Theta_fitted = {'S2': 581, 'S8': 608, 'S3': 599}
Theta_unc    = {'S2': 73,  'S8': 81,  'S3': 94}
R2_table     = {'S2': 0.9954, 'S8': 0.9922, 'S3': 0.9916}

# =============================================================================
# MODEL FUNCTIONS
# =============================================================================
def j5_integral(y):
    if y <= 1e-8:
        return 0.0
    integrand = lambda x: x**4 * np.exp(x) / (np.expm1(x))**2
    val, _ = quad(integrand, 1e-8, y, limit=200)
    return val

def model_J5(T, G0, R, Theta):
    T = np.asarray(T, dtype=float)
    out = np.empty_like(T)
    for i, Ti in enumerate(T):
        y = Theta / Ti
        out[i] = G0 + R * (Ti / Theta)**5 * j5_integral(y)
    return out

def model_single_raman(T, G0, B, omega):
    T = np.asarray(T, dtype=float)
    x = np.clip(omega / (kB_cm * T), 1e-6, 50)
    n = 1.0 / (np.exp(x) - 1.0)
    return G0 + B * n * (n + 1.0)

def model_T5(T, G0, A):
    T = np.asarray(T, dtype=float)
    return G0 + A * T**5

def rmse(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return np.sqrt(np.mean((y_true - y_pred)**2))

# =============================================================================
# FIT ALL SAMPLES
# =============================================================================
fitted_params = {}
for name, rate in samples.items():
    theta_fix = Theta_fitted[name]
    
    popt_j5, _ = curve_fit(
        lambda T, G0, R: model_J5(T, G0, R, theta_fix),
        T_data, rate,
        p0=[np.min(rate)/2, 1e5],
        bounds=([0, 0], [100, 1e9]),
        maxfev=20000
    )
    
    popt_sm, _ = curve_fit(
        model_single_raman, T_data, rate,
        p0=[np.min(rate)/2, 5000, 700],
        bounds=([0, 0, 10], [2000, 1e7, 2000]),
        maxfev=20000
    )
    
    popt_t5, _ = curve_fit(
        model_T5, T_data, rate,
        p0=[np.min(rate)/2, 1e-12],
        bounds=([0, 0], [100, 1e-6]),
        maxfev=20000
    )
    
    fitted_params[name] = {
        'G0': popt_j5[0], 'R': popt_j5[1],
        'Theta': theta_fix, 'Theta_unc': Theta_unc[name],
        'R2': R2_table[name],
        'SM': popt_sm, 'T5': popt_t5,
    }
    print(f"  {name}: G0={popt_j5[0]:.2f}, R={popt_j5[1]:.2e}, Theta={theta_fix} K (fixed)")

# =============================================================================
# FIGURE 1
# =============================================================================
print("Creating Figure 1...")
fig1, axes1 = plt.subplots(1, 3, figsize=(16, 5))
T_smooth = np.linspace(4, 420, 300)

for i, (name, rate) in enumerate(samples.items()):
    ax = axes1[i]
    fp = fitted_params[name]
    
    ax.plot(T_data, rate, 'ko', markersize=5, label=f'{name} data (digitized)')
    ax.plot(
        T_smooth,
        model_J5(T_smooth, fp['G0'], fp['R'], fp['Theta']),
        'r-', linewidth=2,
        label=f'$J_5$ fit ($\\Theta_{{\\rm eff}}$={fp["Theta"]}$\\pm${fp["Theta_unc"]} K)'
    )
    
    ax.set_xlabel('Temperature (K)')
    if i == 0:
        ax.set_ylabel('1/$T_1$ (s$^{-1}$)')
    ax.set_title(f'Sample {name}')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')

fig1.suptitle(
    'Figure 1: $J_5$ transport fits to Jarmola et al. (2012) using fixed Table 1 $\\Theta_{\\rm eff}$ values',
    fontsize=13, fontweight='bold'
)
fig1.tight_layout()
fig1.savefig('fig1_J5_fit_Jarmola_final.png', dpi=250, bbox_inches='tight')
fig1.savefig('fig1_J5_fit_Jarmola_final.pdf', bbox_inches='tight')
plt.close(fig1)
print("  Figure 1 saved.")

# =============================================================================
# FIGURE 2
# =============================================================================
print("Creating Figure 2...")
fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(12, 5))

rate_S2_data = samples['S2']
fp_S2 = fitted_params['S2']

pred_J5_smooth = model_J5(T_smooth, fp_S2['G0'], fp_S2['R'], fp_S2['Theta'])
pred_SM_smooth = model_single_raman(T_smooth, *fp_S2['SM'])
pred_T5_smooth = model_T5(T_smooth, *fp_S2['T5'])

pred_J5_data = model_J5(T_data, fp_S2['G0'], fp_S2['R'], fp_S2['Theta'])
pred_SM_data = model_single_raman(T_data, *fp_S2['SM'])
pred_T5_data = model_T5(T_data, *fp_S2['T5'])

ax2a.plot(T_data, rate_S2_data, 'ko', markersize=5, label='S2 data (Jarmola)')
ax2a.plot(T_smooth, pred_J5_smooth, 'r-', linewidth=2,
          label=f'$J_5$ ($R^2$={fp_S2["R2"]:.4f}, $\\Theta_{{\\rm eff}}$={fp_S2["Theta"]} K)')
ax2a.plot(T_smooth, pred_SM_smooth, 'b--', linewidth=1.5, alpha=0.75,
          label='$n(n+1)$ single-mode')
ax2a.plot(T_smooth, pred_T5_smooth, 'g:', linewidth=1.5, alpha=0.75,
          label='$T^5$ power law')
ax2a.set_xlabel('Temperature (K)')
ax2a.set_ylabel('1/$T_1$ (s$^{-1}$)')
ax2a.set_title('(a) Model Comparison on Sample S2')
ax2a.legend(fontsize=8)
ax2a.grid(True, alpha=0.3)
ax2a.set_xscale('log')
ax2a.set_yscale('log')

resid_J5 = rate_S2_data - pred_J5_data
resid_SM = rate_S2_data - pred_SM_data
resid_T5 = rate_S2_data - pred_T5_data

rmse_J5_val = rmse(rate_S2_data, pred_J5_data)
rmse_SM_val = rmse(rate_S2_data, pred_SM_data)
rmse_T5_val = rmse(rate_S2_data, pred_T5_data)

ax2b.plot(T_data, resid_J5, 'o-', color='red', markersize=4, linewidth=1,
          label=f'$J_5$ (RMSE={rmse_J5_val:.0f})')
ax2b.plot(T_data, resid_SM, 's--', color='blue', markersize=4, linewidth=1, alpha=0.65,
          label=f'$n(n+1)$ (RMSE={rmse_SM_val:.0f})')
ax2b.plot(T_data, resid_T5, '^:', color='green', markersize=4, linewidth=1, alpha=0.65,
          label=f'$T^5$ (RMSE={rmse_T5_val:.0f})')
ax2b.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax2b.set_xlabel('Temperature (K)')
ax2b.set_ylabel('Residuals (s$^{-1}$)')
ax2b.set_title('(b) Fit Residuals')
ax2b.legend(fontsize=8)
ax2b.grid(True, alpha=0.3)

fig2.suptitle(
    'Figure 2: Model Comparison — $J_5$ vs Single-Mode vs Power Law',
    fontsize=13, fontweight='bold'
)
fig2.tight_layout()
fig2.savefig('fig2_model_comparison_final.png', dpi=250, bbox_inches='tight')
fig2.savefig('fig2_model_comparison_final.pdf', bbox_inches='tight')
plt.close(fig2)
print("  Figure 2 saved.")

# =============================================================================
# VERIFY FILES
# =============================================================================
print("\nVerifying saved files:")
for fname in ['fig1_J5_fit_Jarmola_final.png', 'fig1_J5_fit_Jarmola_final.pdf',
              'fig2_model_comparison_final.png', 'fig2_model_comparison_final.pdf']:
    if os.path.exists(fname):
        size_kb = os.path.getsize(fname) / 1024
        print(f"  ✓ {fname} ({size_kb:.1f} KB)")
    else:
        print(f"  ✗ {fname} NOT FOUND!")

# =============================================================================
# AUTO-DOWNLOAD (Colab only)
# =============================================================================
try:
    from google.colab import files
    print("\nAuto-downloading figures...")
    files.download('fig1_J5_fit_Jarmola_final.png')
    files.download('fig1_J5_fit_Jarmola_final.pdf')
    files.download('fig2_model_comparison_final.png')
    files.download('fig2_model_comparison_final.pdf')
    print("Downloads started.")
except ImportError:
    print("\nNot running in Google Colab — files are saved locally.")

print("\nAll done!")
