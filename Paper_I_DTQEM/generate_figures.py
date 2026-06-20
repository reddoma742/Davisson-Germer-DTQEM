"""
DTQEM Figures 1 & 2 - Clean Version
=====================================
Generates two PNG figures for DTQEM Paper I.
Credits: [Friend's Name] — code architecture, clean implementation.

Output:
    output/fig1_dtqem_fit.png   — Figure 1: Fit, Residuals, R² comparison
    output/fig2_extrapolation.png — Figure 2: Extrapolation to 1000 K, Residuals
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.size': 8,
    'font.family': 'sans-serif',
    'figure.dpi': 100,
    'savefig.dpi': 150,
})

# Create output directory
OUTDIR = Path('output')
OUTDIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# CONSTANTS AND DATA
# =============================================================================
kB_cm = 0.69503476

# Ouyang et al. data
T_ouy = np.array([298.15, 303.15, 308.15, 313.15, 318.15, 323.15, 328.15,
                   333.15, 338.15, 343.15, 348.15, 353.15, 358.15, 363.15,
                   368.15, 373.15, 378.15, 383.15], dtype=float)
D_ouy = np.array([2.87007, 2.86969, 2.86928, 2.86891, 2.86850, 2.86810,
                   2.86766, 2.86719, 2.86675, 2.86629, 2.86582, 2.86534,
                   2.86485, 2.86438, 2.86385, 2.86340, 2.86289, 2.86234], dtype=float)
u_D = np.array([5.83e-5, 4.46e-5, 4.77e-5, 5.11e-5, 4.70e-5, 5.18e-5,
                3.62e-5, 6.51e-5, 5.43e-5, 5.36e-5, 3.93e-5, 5.01e-5,
                7.27e-5, 7.43e-5, 7.80e-5, 8.54e-5, 7.17e-5, 5.56e-5], dtype=float)

# Liu et al. data (extracted from published curve)
T_liu = np.array([300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000], dtype=float)
D_liu = np.array([2.868, 2.864, 2.860, 2.855, 2.849, 2.843, 2.836, 2.829,
                   2.821, 2.813, 2.805, 2.797, 2.788, 2.779, 2.770], dtype=float)

# DTQEM parameters (from Ouyang fit)
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
    T = np.asarray(T, dtype=float)
    x = np.clip(omega_dtqem / (kB_cm * T), 1e-6, 50)
    return D0_dtqem + A_dtqem / np.expm1(x)

def powerlaw_D(T):
    T = np.asarray(T, dtype=float)
    return D0_pow + a_pow * T**n_pow

def empirical_ouyang(T):
    T = np.asarray(T, dtype=float)
    return 2.87749 + 2.679e-5 * T - 1.7312e-7 * T**2

def calc_r2(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return 1 - np.sum((y_true - y_pred)**2) / np.sum((y_true - np.mean(y_true))**2)

def calc_rmse(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return np.sqrt(np.mean((y_true - y_pred)**2))

# =============================================================================
# FIGURE 1
# =============================================================================
def build_fig1():
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.8), constrained_layout=False)
    T_smooth = np.linspace(290, 390, 100)

    ax = axes[0]
    ax.errorbar(T_ouy, D_ouy, yerr=u_D, fmt='o', capsize=2, color='black',
                alpha=0.6, markersize=3, label='Ouyang et al.')
    ax.plot(T_smooth, dtqem_D(T_smooth), 'r-', linewidth=1.5, label='DTQEM')
    ax.plot(T_smooth, empirical_ouyang(T_smooth), 'k--', linewidth=1, alpha=0.5, label='Poly')
    ax.plot(T_smooth, powerlaw_D(T_smooth), 'g-.', linewidth=1, alpha=0.5, label='Power')
    ax.set_xlabel('T (K)', fontsize=8)
    ax.set_ylabel('D (GHz)', fontsize=8)
    ax.set_title('(a) Fit', fontsize=9, fontweight='bold')
    ax.legend(fontsize=6.5, loc='lower left')
    ax.grid(True, alpha=0.2)
    ax.tick_params(labelsize=7)

    ax = axes[1]
    res_dtqem = D_ouy - dtqem_D(T_ouy)
    res_emp = D_ouy - empirical_ouyang(T_ouy)
    res_pow = D_ouy - powerlaw_D(T_ouy)
    ax.plot(T_ouy, res_dtqem*1e6, 'o-', color='red', markersize=3, linewidth=1, label='DTQEM')
    ax.plot(T_ouy, res_emp*1e6, 's--', color='black', markersize=2, linewidth=1, alpha=0.5, label='Poly')
    ax.plot(T_ouy, res_pow*1e6, '^:', color='green', markersize=2, linewidth=1, alpha=0.5, label='Power')
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('T (K)', fontsize=8)
    ax.set_ylabel(r'Residuals ($10^{-6}$ GHz)', fontsize=8)
    ax.set_title('(b) Residuals', fontsize=9, fontweight='bold')
    ax.legend(fontsize=6.5)
    ax.grid(True, alpha=0.2)
    ax.tick_params(labelsize=7)

    ax = axes[2]
    r2_vals = [calc_r2(D_ouy, dtqem_D(T_ouy)),
               calc_r2(D_ouy, empirical_ouyang(T_ouy)),
               calc_r2(D_ouy, powerlaw_D(T_ouy))]
    models = ['DTQEM', 'Poly', 'Power']
    colors = ['#FF6B6B', '#4C72B0', '#55A868']
    bars = ax.bar(models, r2_vals, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    for bar, val in zip(bars, r2_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val - 0.000002,
                f'{val:.6f}', ha='center', va='top', fontsize=6, color='white', fontweight='bold')
    ax.set_ylabel('$R^2$', fontsize=8)
    ax.set_title('(c) Comparison', fontsize=9, fontweight='bold')
    ax.set_ylim(0.99990, 1.00001)
    ax.grid(True, alpha=0.2, axis='y')
    ax.tick_params(labelsize=7)

    fig.suptitle('DTQEM Fit to Ouyang Data', fontsize=10, fontweight='bold', y=0.98)
    fig.subplots_adjust(left=0.06, right=0.99, bottom=0.16, top=0.82, wspace=0.35)
    
    path = OUTDIR / 'fig1_dtqem_fit.png'
    fig.savefig(path, facecolor='white')
    plt.close(fig)
    return path

# =============================================================================
# FIGURE 2
# =============================================================================
def build_fig2():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=False)
    T_ext = np.linspace(280, 1020, 150)

    ax = axes[0]
    ax.axvspan(298, 383, alpha=0.1, color='gray', label='Calibration')
    ax.plot(T_ext, dtqem_D(T_ext), 'r-', linewidth=1.5, label='DTQEM')
    ax.plot(T_ext, powerlaw_D(T_ext), 'g--', linewidth=1, alpha=0.5, label='Power law')
    ax.errorbar(T_liu, D_liu, yerr=np.full(T_liu.shape, 0.002), fmt='o', color='blue',
                capsize=2, alpha=0.6, markersize=3, label='Liu et al.')
    ax.set_xlabel('T (K)', fontsize=8)
    ax.set_ylabel('D (GHz)', fontsize=8)
    ax.set_title('(a) Extrapolation', fontsize=9, fontweight='bold')
    ax.legend(fontsize=6.5, loc='lower left')
    ax.grid(True, alpha=0.2)
    ax.tick_params(labelsize=7)

    ax = axes[1]
    res_liu_dtqem = D_liu - dtqem_D(T_liu)
    res_liu_pow = D_liu - powerlaw_D(T_liu)
    rmse_dtqem = calc_rmse(D_liu, dtqem_D(T_liu)) * 1000
    rmse_pow = calc_rmse(D_liu, powerlaw_D(T_liu)) * 1000
    ax.plot(T_liu, res_liu_dtqem*1000, 'o-', color='red', markersize=3, linewidth=1.5,
            label=f'DTQEM (RMSE={rmse_dtqem:.1f} MHz)')
    ax.plot(T_liu, res_liu_pow*1000, 's--', color='green', markersize=2, linewidth=1.5,
            alpha=0.5, label=f'Power law (RMSE={rmse_pow:.1f} MHz)')
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.fill_between(T_liu, -5, 5, alpha=0.1, color='gray')
    ax.set_xlabel('T (K)', fontsize=8)
    ax.set_ylabel('Residuals (MHz)', fontsize=8)
    ax.set_title('(b) Residuals', fontsize=9, fontweight='bold')
    ax.legend(fontsize=6.5)
    ax.grid(True, alpha=0.2)
    ax.set_ylim(-80, 80)
    ax.tick_params(labelsize=7)

    fig.suptitle('DTQEM Extrapolation: Validated to 1000 K', fontsize=10, fontweight='bold', y=0.98)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.16, top=0.84, wspace=0.28)
    
    path = OUTDIR / 'fig2_extrapolation.png'
    fig.savefig(path, facecolor='white')
    plt.close(fig)
    return path

# =============================================================================
# BUILD AND DISPLAY
# =============================================================================
fig1_path = build_fig1()
fig2_path = build_fig2()

print(f'Saved figure 1: {fig1_path} | exists={fig1_path.exists()}')
print(f'Saved figure 2: {fig2_path} | exists={fig2_path.exists()}')
print('Done.')

# Display in notebook (optional)
try:
    from IPython.display import Image, display
    display(Image(filename=str(fig1_path)))
    display(Image(filename=str(fig2_path)))
except Exception:
    pass
