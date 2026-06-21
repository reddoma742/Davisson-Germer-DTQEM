"""
Figure 2 - Monte Carlo Parameter-Uncertainty Bands (Single-File, Verified Save)
================================================================================
- Fits DTQEM and Power law to Ouyang et al. data (weighted by u_D)
- Propagates parameter uncertainty via Monte Carlo (N=10,000)
- Plots 95% parameter-uncertainty bands for both models
- Saves final figure as PDF and PNG in ./output/
- Includes explicit check that files exist after saving.
"""

import matplotlib
matplotlib.use('Agg')  # Must be before importing pyplot
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path

# Create output directory (always succeeds)
OUTDIR = Path('output')
OUTDIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# 1. DATA
# =============================================================================
kB_cm = 0.69503476

T_ouy = np.array([298.15, 303.15, 308.15, 313.15, 318.15, 323.15, 328.15,
                   333.15, 338.15, 343.15, 348.15, 353.15, 358.15, 363.15,
                   368.15, 373.15, 378.15, 383.15], dtype=float)
D_ouy = np.array([2.87007, 2.86969, 2.86928, 2.86891, 2.86850, 2.86810,
                   2.86766, 2.86719, 2.86675, 2.86629, 2.86582, 2.86534,
                   2.86485, 2.86438, 2.86385, 2.86340, 2.86289, 2.86234], dtype=float)
u_D   = np.array([5.83e-5, 4.46e-5, 4.77e-5, 5.11e-5, 4.70e-5, 5.18e-5,
                  3.62e-5, 6.51e-5, 5.43e-5, 5.36e-5, 3.93e-5, 5.01e-5,
                  7.27e-5, 7.43e-5, 7.80e-5, 8.54e-5, 7.17e-5, 5.56e-5], dtype=float)

T_liu = np.array([300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000], dtype=float)
D_liu = np.array([2.868, 2.864, 2.860, 2.855, 2.849, 2.843, 2.836, 2.829,
                   2.821, 2.813, 2.805, 2.797, 2.788, 2.779, 2.770], dtype=float)

# =============================================================================
# 2. MODELS
# =============================================================================
def dtqem_model(T, D0, A, omega):
    x = omega / (kB_cm * T)
    x = np.clip(x, 1e-6, 50)
    return D0 + A / np.expm1(x)

def powerlaw_model(T, D0, a, n):
    return D0 + a * T**n

# =============================================================================
# 3. WEIGHTED FITS
# =============================================================================
popt_dtqem, pcov_dtqem = curve_fit(
    dtqem_model, T_ouy, D_ouy,
    p0=[2.876, -0.189, 711],
    sigma=u_D, absolute_sigma=True
)

popt_pow, pcov_pow = curve_fit(
    powerlaw_model, T_ouy, D_ouy,
    p0=[2.88, -2e-8, 2.3],
    sigma=u_D, absolute_sigma=True
)

perr_dtqem = np.sqrt(np.diag(pcov_dtqem))
perr_pow   = np.sqrt(np.diag(pcov_pow))

print(f"[DTQEM] D0 = {popt_dtqem[0]:.6f} ± {perr_dtqem[0]:.6f} GHz")
print(f"[DTQEM] A  = {popt_dtqem[1]:.6f} ± {perr_dtqem[1]:.6f} GHz")
print(f"[DTQEM] ω  = {popt_dtqem[2]:.2f}  ± {perr_dtqem[2]:.2f} cm⁻¹")
print(f"[Power] D0 = {popt_pow[0]:.6f} ± {perr_pow[0]:.6f} GHz")
print(f"[Power] a  = {popt_pow[1]:.3e} ± {perr_pow[1]:.3e} GHz/K^n")
print(f"[Power] n  = {popt_pow[2]:.6f} ± {perr_pow[2]:.6f}")

# =============================================================================
# 4. MONTE CARLO UNCERTAINTY PROPAGATION
# =============================================================================
np.random.seed(42)
N = 10000
T_ext = np.linspace(280, 1020, 200)

samples_dtqem = np.random.multivariate_normal(popt_dtqem, pcov_dtqem, N)
samples_pow   = np.random.multivariate_normal(popt_pow, pcov_pow, N)

D_dtqem_curves = np.array([dtqem_model(T_ext, *s) for s in samples_dtqem])
D_pow_curves   = np.array([powerlaw_model(T_ext, *s) for s in samples_pow])

def band95(arr):
    lo = np.percentile(arr, 2.5, axis=0)
    hi = np.percentile(arr, 97.5, axis=0)
    mean = arr.mean(axis=0)
    return mean, lo, hi

D_dtqem_mean, D_dtqem_low, D_dtqem_high = band95(D_dtqem_curves)
D_pow_mean,   D_pow_low,   D_pow_high   = band95(D_pow_curves)

# =============================================================================
# 5. RESIDUALS ON LIU DIGITIZED POINTS
# =============================================================================
res_dtqem = D_liu - dtqem_model(T_liu, *popt_dtqem)
res_pow   = D_liu - powerlaw_model(T_liu, *popt_pow)

rmse_dtqem = np.sqrt(np.mean(res_dtqem**2)) * 1000  # GHz -> MHz
rmse_pow   = np.sqrt(np.mean(res_pow**2))   * 1000

# =============================================================================
# 6. PLOT (save only, no display)
# =============================================================================
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))

ax = axes[0]
ax.axvspan(298, 383, alpha=0.1, color='gray', label='Calibration window')
ax.fill_between(T_ext, D_dtqem_low, D_dtqem_high, alpha=0.22, color='red',
                label='DTQEM: 95% band (parameter uncertainty)')
ax.plot(T_ext, D_dtqem_mean, 'r-', linewidth=1.6, label='DTQEM (mean)')
ax.fill_between(T_ext, D_pow_low, D_pow_high, alpha=0.18, color='green',
                label='Power law: 95% band (parameter uncertainty)')
ax.plot(T_ext, D_pow_mean, 'g--', linewidth=1.2, alpha=0.85, label='Power law (mean)')
ax.plot(T_liu, D_liu, 'o', color='blue', markersize=3.5, label='Liu et al. (digitized)')
ax.set_xlabel('T (K)')
ax.set_ylabel('D (GHz)')
ax.set_title('(a) Extrapolation with parameter-uncertainty bands')
ax.legend(fontsize=6.5, loc='upper right')   # legend placed neatly
ax.grid(True, alpha=0.2)

ax = axes[1]
ax.plot(T_liu, res_dtqem * 1000, 'o-', color='red', markersize=3, linewidth=1.2,
        label=f'DTQEM (RMSE={rmse_dtqem:.1f} MHz)')
ax.plot(T_liu, res_pow * 1000, 's--', color='green', markersize=2.5, linewidth=1,
        label=f'Power law (RMSE={rmse_pow:.1f} MHz)')
ax.axhline(0, color='gray', linestyle='--', alpha=0.6)
ax.fill_between(T_liu, -5, 5, alpha=0.08, color='gray',
                label='±5 MHz visual guide')
ax.set_xlabel('T (K)')
ax.set_ylabel('Residuals (MHz)')
ax.set_title('(b) Residuals vs. Liu parametrization')
ax.legend(fontsize=6.5, loc='upper right')
ax.set_ylim(-80, 80)
ax.grid(True, alpha=0.2)

fig.suptitle('DTQEM vs Power-law: Parameter-uncertainty bands (MC)', fontsize=10, fontweight='bold')
fig.tight_layout(pad=1.5)

# Save to output folder
png_path = OUTDIR / 'fig2_MC_bands_final.png'
pdf_path = OUTDIR / 'fig2_MC_bands_final.pdf'

fig.savefig(png_path, dpi=220, bbox_inches='tight', facecolor='white')
fig.savefig(pdf_path, bbox_inches='tight', facecolor='white')
plt.close(fig)

# Explicit verification
print(f"\nSaved PNG: {png_path} | exists = {png_path.exists()} | size = {png_path.stat().st_size} bytes")
print(f"Saved PDF: {pdf_path} | exists = {pdf_path.exists()} | size = {pdf_path.stat().st_size} bytes")
print("Done.")
