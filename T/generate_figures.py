"""
Generate final figures for DTQEM Paper I
=========================================
Fig. 1: (a) DTQEM fit to Ouyang, (b) Residuals, (c) R² comparison
Fig. 2: (a) Extrapolation to Liu 300-1000 K, (b) Residuals
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.size'] = 11
rcParams['font.family'] = 'serif'
rcParams['mathtext.fontset'] = 'dejavuserif'

# =============================================================================
# DATA
# =============================================================================
kB_cm = 0.69503476

# Ouyang data
T_ouy = np.array([298.15, 303.15, 308.15, 313.15, 318.15, 323.15, 328.15,
                   333.15, 338.15, 343.15, 348.15, 353.15, 358.15, 363.15,
                   368.15, 373.15, 378.15, 383.15])
D_ouy = np.array([2.87007, 2.86969, 2.86928, 2.86891, 2.86850, 2.86810,
                   2.86766, 2.86719, 2.86675, 2.86629, 2.86582, 2.86534,
                   2.86485, 2.86438, 2.86385, 2.86340, 2.86289, 2.86234])
u_D = np.array([5.83e-5, 4.46e-5, 4.77e-5, 5.11e-5, 4.70e-5, 5.18e-5,
                3.62e-5, 6.51e-5, 5.43e-5, 5.36e-5, 3.93e-5, 5.01e-5,
                7.27e-5, 7.43e-5, 7.80e-5, 8.54e-5, 7.17e-5, 5.56e-5])

# Liu data (extracted from published curve)
T_liu = np.array([300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000])
D_liu = np.array([2.868, 2.864, 2.860, 2.855, 2.849, 2.843, 2.836, 2.829,
                   2.821, 2.813, 2.805, 2.797, 2.788, 2.779, 2.770])

# DTQEM parameters (from fit)
D0_dtqem = 2.87638659
A_dtqem  = -0.18890215
omega_dtqem = 711.13

# Power law parameters
D0_pow = 2.87990464
a_pow  = -2e-8
n_pow  = 2.31991273

# =============================================================================
# MODEL FUNCTIONS
# =============================================================================
def dtqem_D(T):
    x = np.clip(omega_dtqem / (kB_cm * T), 1e-6, 50)
    n = 1.0 / (np.exp(x) - 1.0)
    return D0_dtqem + A_dtqem * n

def powerlaw_D(T):
    return D0_pow + a_pow * T**n_pow

def empirical_ouyang(T):
    return 2.87749 + 2.679e-5 * T - 1.7312e-7 * T**2

# =============================================================================
# FIGURE 1
# =============================================================================
fig1, (ax1a, ax1b, ax1c) = plt.subplots(1, 3, figsize=(16, 4.5))

T_smooth = np.linspace(290, 390, 100)
ax1a.errorbar(T_ouy, D_ouy, yerr=u_D, fmt='o', capsize=3, color='black',
              alpha=0.7, markersize=4, label='Ouyang et al. data')
ax1a.plot(T_smooth, dtqem_D(T_smooth), 'r-', linewidth=2, label='This work')
ax1a.plot(T_smooth, empirical_ouyang(T_smooth), 'k--', linewidth=1.5, alpha=0.7, label='Empirical poly.')
ax1a.plot(T_smooth, powerlaw_D(T_smooth), 'g-.', linewidth=1.5, alpha=0.7, label='Power law')
ax1a.set_xlabel('Temperature (K)')
ax1a.set_ylabel('D (GHz)')
ax1a.set_title('(a) Fit to Ouyang Data')
ax1a.legend(fontsize=7, loc='lower left')
ax1a.grid(True, alpha=0.3)

res_dtqem = D_ouy - dtqem_D(T_ouy)
res_emp = D_ouy - empirical_ouyang(T_ouy)
res_pow = D_ouy - powerlaw_D(T_ouy)
ax1b.plot(T_ouy, res_dtqem*1e6, 'o-', color='red', markersize=4, linewidth=1, label=f'This work')
ax1b.plot(T_ouy, res_emp*1e6, 's--', color='black', markersize=4, linewidth=1, alpha=0.6, label=f'Empirical')
ax1b.plot(T_ouy, res_pow*1e6, '^:', color='green', markersize=4, linewidth=1, alpha=0.6, label=f'Power law')
ax1b.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax1b.set_xlabel('Temperature (K)')
ax1b.set_ylabel(r'Residuals ($10^{-6}$ GHz)')
ax1b.set_title('(b) Fit Residuals')
ax1b.legend(fontsize=7)
ax1b.grid(True, alpha=0.3)

def calc_r2(y_true, y_pred):
    return 1 - np.sum((y_true - y_pred)**2) / np.sum((y_true - np.mean(y_true))**2)
r2_dtqem = calc_r2(D_ouy, dtqem_D(T_ouy))
r2_emp = calc_r2(D_ouy, empirical_ouyang(T_ouy))
r2_pow = calc_r2(D_ouy, powerlaw_D(T_ouy))

models = ['This work', 'Empirical\npoly.', 'Power\nlaw']
r2_vals = [r2_dtqem, r2_emp, r2_pow]
colors = ['red', 'black', 'green']
bars = ax1c.bar(models, r2_vals, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
for bar, val in zip(bars, r2_vals):
    ax1c.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.000005,
              f'{val:.6f}', ha='center', va='top', fontsize=9, fontweight='bold', color='white')
ax1c.set_ylabel('$R^2$')
ax1c.set_title('(c) Model $R^2$ Comparison')
ax1c.set_ylim(0.9998, 1.0000)
ax1c.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('fig1_dtqem_fit.pdf', dpi=300, bbox_inches='tight')
print("Fig. 1 saved as 'fig1_dtqem_fit.pdf'")

# =============================================================================
# FIGURE 2
# =============================================================================
fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(12, 4.5))

T_ext = np.linspace(280, 1020, 300)
ax2a.axvspan(298, 383, alpha=0.15, color='gray', label='Calibration window')
ax2a.plot(T_ext, dtqem_D(T_ext), 'r-', linewidth=2, label='This work')
ax2a.plot(T_ext, powerlaw_D(T_ext), 'g--', linewidth=2, label='Power law')
ax2a.errorbar(T_liu, D_liu, yerr=np.full_like(T_liu, 0.002), fmt='o', color='blue',
              capsize=3, alpha=0.7, markersize=5, label='Liu et al. parametrization')
ax2a.set_xlabel('Temperature (K)')
ax2a.set_ylabel('D (GHz)')
ax2a.set_title('(a) Extrapolation to 1000 K')
ax2a.legend(fontsize=9)
ax2a.grid(True, alpha=0.3)

res_liu_dtqem = D_liu - dtqem_D(T_liu)
res_liu_pow = D_liu - powerlaw_D(T_liu)
ax2b.plot(T_liu, res_liu_dtqem*1000, 'o-', color='red', linewidth=1.5, markersize=5,
          label=f'This work (RMSE={np.std(res_liu_dtqem)*1000:.2f} MHz)')
ax2b.plot(T_liu, res_liu_pow*1000, 's--', color='green', linewidth=1.5, markersize=5,
          label=f'Power law (RMSE={np.std(res_liu_pow)*1000:.2f} MHz)')
ax2b.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax2b.fill_between(T_liu, -5, 5, alpha=0.1, color='gray', label=r'$\pm 5$ MHz band')
ax2b.set_xlabel('Temperature (K)')
ax2b.set_ylabel('Residuals (MHz)')
ax2b.set_title('(b) Extrapolation Residuals')
ax2b.legend(fontsize=9)
ax2b.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fig2_extrapolation.pdf', dpi=300, bbox_inches='tight')
print("Fig. 2 saved as 'fig2_extrapolation.pdf'")

print("\nAll figures generated successfully.")
