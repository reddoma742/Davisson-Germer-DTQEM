"""
DTQEM Paper I — Complete Figure Generation (Colab Version)
============================================================
Generates the two publication‑ready figures and downloads them
directly in Google Colab.  Also saves copies in ./output/.

Output files
------------
• fig1_dtqem_fit_final.png   /  fig1_dtqem_fit_final.pdf
• fig2_MC_bands_final.png    /  fig2_MC_bands_final.pdf

Usage in Colab
--------------
1. Upload this script (or paste it into a single cell).
2. Run the cell.
3. After execution the four files are downloaded automatically.

Author of the script: Claude (Anthropic), adapted for the DTQEM project.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path

# Output directory
OUTDIR = Path('output')
OUTDIR.mkdir(parents=True, exist_ok=True)

# Global plotting style
plt.rcParams.update({
    'font.size': 8, 'font.family': 'DejaVu Sans',
    'axes.titlesize': 9, 'axes.labelsize': 8,
    'xtick.labelsize': 7, 'ytick.labelsize': 7,
    'legend.fontsize': 6.5, 'pdf.fonttype': 42,
})

# =============================================================================
# 1. DATA
# =============================================================================
kB_cm = 0.69503476

# Ouyang et al. — calibration dataset
T_ouy = np.array([298.15, 303.15, 308.15, 313.15, 318.15, 323.15, 328.15, 333.15,
                  338.15, 343.15, 348.15, 353.15, 358.15, 363.15, 368.15, 373.15, 378.15, 383.15])
D_ouy = np.array([2.87007, 2.86969, 2.86928, 2.86891, 2.86850, 2.86810, 2.86766, 2.86719,
                  2.86675, 2.86629, 2.86582, 2.86534, 2.86485, 2.86438, 2.86385, 2.86340, 2.86289, 2.86234])
u_D   = np.array([5.83e-5, 4.46e-5, 4.77e-5, 5.11e-5, 4.70e-5, 5.18e-5, 3.62e-5, 6.51e-5,
                  5.43e-5, 5.36e-5, 3.93e-5, 5.01e-5, 7.27e-5, 7.43e-5, 7.80e-5, 8.54e-5, 7.17e-5, 5.56e-5])

# Liu et al. — digitised benchmark points
T_liu = np.array([300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000], dtype=float)
D_liu = np.array([2.868, 2.864, 2.860, 2.855, 2.849, 2.843, 2.836, 2.829,
                  2.821, 2.813, 2.805, 2.797, 2.788, 2.779, 2.770])

# =============================================================================
# 2. MODEL FUNCTIONS
# =============================================================================
def dtqem_model(T, D0, A, omega):
    x = np.clip(omega / (kB_cm * T), 1e-6, 50)
    return D0 + A / np.expm1(x)

def powerlaw_model(T, D0, a, n):
    return D0 + a * T**n

def empirical_ouyang(T):
    return 2.87749 + 2.679e-5 * T - 1.7312e-7 * T**2

def calc_r2(y_true, y_pred):
    return 1 - np.sum((y_true - y_pred)**2) / np.sum((y_true - np.mean(y_true))**2)

# =============================================================================
# 3. WEIGHTED FITS
# =============================================================================
popt_d, pcov_d = curve_fit(dtqem_model, T_ouy, D_ouy, p0=[2.876, -0.189, 711],
                            sigma=u_D, absolute_sigma=True)
popt_p, pcov_p = curve_fit(powerlaw_model, T_ouy, D_ouy, p0=[2.88, -2e-8, 2.3],
                            sigma=u_D, absolute_sigma=True)

# =============================================================================
# 4. MONTE CARLO UNCERTAINTY PROPAGATION
# =============================================================================
np.random.seed(42)
N = 10000
T_ext    = np.linspace(280, 1020, 200)
T_smooth = np.linspace(290, 390, 200)

samp_d = np.random.multivariate_normal(popt_d, pcov_d, N)
samp_p = np.random.multivariate_normal(popt_p, pcov_p, N)

Dd = np.array([dtqem_model(T_ext, *s) for s in samp_d])
Dp = np.array([powerlaw_model(T_ext, *s) for s in samp_p])

def band95(a):
    return a.mean(0), np.percentile(a, 2.5, 0), np.percentile(a, 97.5, 0)

Dm, Dl, Dh = band95(Dd)
Pm, Pl, Ph = band95(Dp)

# Residuals on Liu digitised points
res_d = (D_liu - dtqem_model(T_liu, *popt_d)) * 1000  # MHz
res_p = (D_liu - powerlaw_model(T_liu, *popt_p)) * 1000
rmse_d = np.sqrt(np.mean(res_d**2))
rmse_p = np.sqrt(np.mean(res_p**2))

# R² values
r2_d = calc_r2(D_ouy, dtqem_model(T_ouy, *popt_d))
r2_e = calc_r2(D_ouy, empirical_ouyang(T_ouy))
r2_p = calc_r2(D_ouy, powerlaw_model(T_ouy, *popt_p))

# =============================================================================
# 5. FIGURE 1 — Calibration fit, residuals, R² comparison
# =============================================================================
fig1, axes = plt.subplots(1, 3, figsize=(12, 4))

# Panel (a) — Fit
ax = axes[0]
ax.errorbar(T_ouy, D_ouy, yerr=u_D, fmt='o', color='black',
            capsize=2, alpha=0.6, ms=3, label='Ouyang et al.')
ax.plot(T_smooth, dtqem_model(T_smooth, *popt_d), 'r-', lw=1.5, label='DTQEM')
ax.plot(T_smooth, empirical_ouyang(T_smooth), 'k--', lw=1, alpha=0.6, label='Poly')
ax.plot(T_smooth, powerlaw_model(T_smooth, *popt_p), 'g-.', lw=1, alpha=0.6, label='Power')
ax.set_xlabel('T (K)'); ax.set_ylabel('D (GHz)')
ax.set_title('(a) Fit', fontweight='bold')
ax.legend(fontsize=6.5, loc='lower left'); ax.grid(True, alpha=0.2)

# Panel (b) — Residuals
ax = axes[1]
res_dt = (D_ouy - dtqem_model(T_ouy, *popt_d)) * 1e6
res_em = (D_ouy - empirical_ouyang(T_ouy)) * 1e6
res_pw = (D_ouy - powerlaw_model(T_ouy, *popt_p)) * 1e6
ax.plot(T_ouy, res_dt, 'o-', color='red', ms=3, lw=1, label='DTQEM')
ax.plot(T_ouy, res_em, 's--', color='black', ms=2, lw=1, alpha=0.6, label='Poly')
ax.plot(T_ouy, res_pw, '^:', color='green', ms=2, lw=1, alpha=0.6, label='Power')
ax.axhline(0, color='gray', ls='--', alpha=0.5)
ax.set_xlabel('T (K)'); ax.set_ylabel(r'Residuals ($10^{-6}$ GHz)')
ax.set_title('(b) Residuals', fontweight='bold')
ax.legend(fontsize=6.5); ax.grid(True, alpha=0.2)

# Panel (c) — R² comparison (fixed y‑axis)
ax = axes[2]
models_lbl = ['DTQEM', 'Poly', 'Power']
r2vals = [r2_d, r2_e, r2_p]
colors_bar = ['#c62828', '#1565c0', '#2e7d32']
bars = ax.bar(models_lbl, r2vals, color=colors_bar, alpha=0.75, edgecolor='black', lw=0.5)
for bar, val in zip(bars, r2vals):
    ax.text(bar.get_x() + bar.get_width()/2, val - 0.0000015,
            f'{val:.6f}', ha='center', va='top', fontsize=6,
            color='white', fontweight='bold')
ax.set_ylabel('$R^2$')
ax.set_ylim(0.99990, 1.00001)
ax.set_title('(c) $R^2$ Comparison', fontweight='bold')
ax.grid(True, alpha=0.2, axis='y')

fig1.suptitle('DTQEM Fit to Ouyang et al. Data', fontsize=10, fontweight='bold')
fig1.subplots_adjust(left=0.06, right=0.98, bottom=0.14, top=0.86, wspace=0.35)
fig1.savefig(str(OUTDIR / 'fig1_dtqem_fit_final.png'), dpi=220, bbox_inches='tight', facecolor='white')
fig1.savefig(str(OUTDIR / 'fig1_dtqem_fit_final.pdf'), bbox_inches='tight', facecolor='white')
plt.close(fig1)
print("Figure 1 saved (fig1_dtqem_fit_final.png / .pdf).")

# =============================================================================
# 6. FIGURE 2 — Extrapolation with Monte‑Carlo uncertainty bands
# =============================================================================
fig2, axes = plt.subplots(1, 2, figsize=(10, 4))

# Panel (a) — Extrapolation bands
ax = axes[0]
ax.axvspan(298, 383, alpha=0.10, color='gray', label='Calibration window')
ax.fill_between(T_ext, Dl, Dh, alpha=0.22, color='#c62828', label='DTQEM 95% param. band')
ax.plot(T_ext, Dm, color='#c62828', lw=1.6, label='DTQEM (mean)')
ax.fill_between(T_ext, Pl, Ph, alpha=0.18, color='#2e7d32', label='Power law 95% param. band')
ax.plot(T_ext, Pm, '--', color='#2e7d32', lw=1.2, alpha=0.85, label='Power law (mean)')
ax.plot(T_liu, D_liu, 'o', color='#1565c0', ms=3.5, label='Liu et al. (digitized)')
ax.set_xlabel('T (K)'); ax.set_ylabel('D (GHz)')
ax.set_title('(a) Extrapolation with parameter-uncertainty bands', fontweight='bold')
ax.legend(fontsize=6, loc='upper right'); ax.grid(True, alpha=0.2)

# Panel (b) — Residuals
ax = axes[1]
ax.plot(T_liu, res_d, 'o-', color='#c62828', ms=3, lw=1.3,
        label=f'DTQEM  (RMSE = {rmse_d:.1f} MHz)')
ax.plot(T_liu, res_p, 's--', color='#2e7d32', ms=2.5, lw=1.1,
        label=f'Power law (RMSE = {rmse_p:.1f} MHz)')
ax.axhline(0, color='gray', ls='--', lw=0.8, alpha=0.7)
ax.fill_between(T_liu, -5, 5, alpha=0.08, color='gray', label=r'$\pm$5 MHz visual guide')
ax.set_xlabel('T (K)'); ax.set_ylabel('Residuals (MHz)')
ax.set_title('(b) Residuals vs. Liu et al. (digitized)', fontweight='bold')
ax.legend(fontsize=6.5, loc='lower left'); ax.set_ylim(-80, 80)
ax.grid(True, alpha=0.2)

fig2.suptitle('DTQEM vs Power-law: Parameter-uncertainty bands (MC, N=10 000)',
              fontsize=9, fontweight='bold')
fig2.subplots_adjust(left=0.08, right=0.98, bottom=0.14, top=0.86, wspace=0.28)
fig2.savefig(str(OUTDIR / 'fig2_MC_bands_final.png'), dpi=220, bbox_inches='tight', facecolor='white')
fig2.savefig(str(OUTDIR / 'fig2_MC_bands_final.pdf'), bbox_inches='tight', facecolor='white')
plt.close(fig2)
print("Figure 2 saved (fig2_MC_bands_final.png / .pdf).")

# =============================================================================
# 7. DOWNLOAD (Colab)
# =============================================================================
from google.colab import files
files.download('output/fig1_dtqem_fit_final.pdf')
files.download('output/fig1_dtqem_fit_final.png')
files.download('output/fig2_MC_bands_final.pdf')
files.download('output/fig2_MC_bands_final.png')
print("All files downloaded.")
