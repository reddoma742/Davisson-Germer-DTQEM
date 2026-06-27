"""
Paper II Figures — FINAL VERSION WITH AUTO-DOWNLOAD
=====================================================
- Generates Figure 1 (J5 fits for all samples) and Figure 2 (model comparison on S2).
- Computes fit metrics (R², RMSE, log RMSE) and saves them as CSV.
- Automatically downloads output files if run in Google Colab.
- Works as a standalone script on any platform.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad
from pathlib import Path

# ------------------------------
#  الإعدادات الأساسية
# ------------------------------
OUTDIR = Path('.')   # حفظ المخرجات في المجلد الحالي
OUTDIR.mkdir(parents=True, exist_ok=True)

kB_cm = 0.69503476    # ثابت بولتزمان بوحدات cm⁻¹·K⁻¹

# ------------------------------
#  بيانات Jarmola et al.
# ------------------------------
T_data = np.array([5.0, 7.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0,
                   90.0, 100.0, 150.0, 200.0, 300.0, 400.0])

rate_S2 = np.array([20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 22.0, 25.0, 35.0,
                    50.0, 80.0, 250.0, 400.0, 700.0, 900.0])

rate_S8 = np.array([0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5, 0.8, 1.5, 3.0,
                    7.0, 15.0, 150.0, 350.0, 650.0, 850.0])

rate_S3 = np.array([0.015, 0.015, 0.015, 0.015, 0.015, 0.018, 0.025, 0.04, 0.1, 0.3,
                    0.8, 2.0, 100.0, 300.0, 600.0, 800.0])

samples = {'S2': rate_S2, 'S8': rate_S8, 'S3': rate_S3}
Theta_fitted = {'S2': 581.0, 'S8': 608.0, 'S3': 599.0}
Theta_unc = {'S2': 73.0, 'S8': 81.0, 'S3': 94.0}

# ------------------------------
#  دوال تقييم النماذج
# ------------------------------
def r2_score(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    ss_res = np.sum((y_true - y_pred)**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((np.asarray(y_true, dtype=float) - np.asarray(y_pred, dtype=float))**2))

def rmse_log10(y_true, y_pred):
    y_true = np.clip(np.asarray(y_true, dtype=float), 1e-30, None)
    y_pred = np.clip(np.asarray(y_pred, dtype=float), 1e-30, None)
    return np.sqrt(np.mean((np.log10(y_true) - np.log10(y_pred))**2))

# ------------------------------
#  تكامل J₅
# ------------------------------
def j5_integrand(x):
    if x < 1e-6:
        return x**2
    if x > 50.0:
        return x**4 * np.exp(-x)
    exm1 = np.expm1(x)
    return x**4 * np.exp(x) / exm1**2

def j5_integral(y):
    if y <= 0:
        return 0.0
    val, _ = quad(j5_integrand, 0.0, y, limit=300, epsabs=1e-10, epsrel=1e-8)
    return val

# ------------------------------
#  تعريف النماذج الرياضية
# ------------------------------
def model_J5(T, G0, R, Theta):
    T = np.asarray(T, dtype=float)
    vals = np.array([j5_integral(Theta / Ti) for Ti in T])
    return G0 + R * (T / Theta)**5 * vals

def model_single_raman(T, G0, B, omega_cm):
    T = np.asarray(T, dtype=float)
    x = np.clip(omega_cm / (kB_cm * T), 1e-8, 700.0)
    n = 1.0 / np.expm1(x)
    return G0 + B * n * (n + 1.0)

def model_T5_offset(T, G0, A):
    T = np.asarray(T, dtype=float)
    return G0 + A * T**5

# ------------------------------
#  دوال التوفيق (curve_fit)
# ------------------------------
def fit_J5_fixed_theta(T, y, Theta):
    p0 = [max(np.min(y), 1e-12), 1e5]
    bounds = ([0.0, 0.0], [np.inf, np.inf])
    popt, pcov = curve_fit(lambda TT, G0, R: model_J5(TT, G0, R, Theta),
                           T, y, p0=p0, bounds=bounds, maxfev=50000)
    return popt, pcov

def fit_single_mode(T, y):
    p0 = [max(np.min(y), 1e-12), 1e4, 700.0]
    bounds = ([0.0, 0.0, 10.0], [np.inf, np.inf, 2500.0])
    popt, pcov = curve_fit(model_single_raman, T, y, p0=p0, bounds=bounds, maxfev=50000)
    return popt, pcov

def fit_T5_offset(T, y):
    p0 = [max(np.min(y), 1e-12), 1e-12]
    bounds = ([0.0, 0.0], [np.inf, np.inf])
    popt, pcov = curve_fit(model_T5_offset, T, y, p0=p0, bounds=bounds, maxfev=50000)
    return popt, pcov

# ------------------------------
#  تنفيذ التوفيق لجميع العينات
# ------------------------------
fit_results = {}
for name, rate in samples.items():
    Theta = Theta_fitted[name]
    popt_J5, _ = fit_J5_fixed_theta(T_data, rate, Theta)
    popt_SM, _ = fit_single_mode(T_data, rate)
    popt_T5, _ = fit_T5_offset(T_data, rate)

    pred_J5 = model_J5(T_data, popt_J5[0], popt_J5[1], Theta)
    pred_SM = model_single_raman(T_data, *popt_SM)
    pred_T5 = model_T5_offset(T_data, *popt_T5)

    fit_results[name] = {
        'Theta': Theta,
        'Theta_unc': Theta_unc[name],
        'J5': popt_J5,
        'SM': popt_SM,
        'T5': popt_T5,
        'R2_J5': r2_score(rate, pred_J5),
        'R2_SM': r2_score(rate, pred_SM),
        'R2_T5': r2_score(rate, pred_T5),
        'RMSE_J5': rmse(rate, pred_J5),
        'RMSE_SM': rmse(rate, pred_SM),
        'RMSE_T5': rmse(rate, pred_T5),
        'RMSE_log_J5': rmse_log10(rate, pred_J5),
        'RMSE_log_SM': rmse_log10(rate, pred_SM),
        'RMSE_log_T5': rmse_log10(rate, pred_T5)
    }

# ------------------------------
#  الشكل 1: منحنيات J₅ للعينات الثلاث
# ------------------------------
T_smooth = np.linspace(4.0, 420.0, 500)
fig1, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, (name, rate) in zip(axes, samples.items()):
    fp = fit_results[name]
    G0, R = fp['J5']
    Theta = fp['Theta']
    dTheta = fp['Theta_unc']
    ax.plot(T_data, rate, 'ko', ms=5, label=f'{name} data')
    ax.plot(T_smooth, model_J5(T_smooth, G0, R, Theta), 'r-', lw=2,
            label=rf'$J_5$ fit, $\Theta_{{\rm eff}}={Theta:.0f}\pm{dTheta:.0f}$ K')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('Temperature (K)')
    ax.set_title(f'Sample {name}')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
axes[0].set_ylabel(r'$1/T_1$ (s$^{-1}$)')
fig1.suptitle(r'$J_5$ transport fits to Jarmola et al. samples', fontsize=13, fontweight='bold')
fig1.tight_layout()
fig1.savefig(OUTDIR / 'fig1_J5_fit_Jarmola_final.png', dpi=300, bbox_inches='tight')
fig1.savefig(OUTDIR / 'fig1_J5_fit_Jarmola_final.pdf', bbox_inches='tight')
plt.close(fig1)

# ------------------------------
#  الشكل 2: مقارنة النماذج للعينة S2
# ------------------------------
sample_name = 'S2'
rate = samples[sample_name]
fp = fit_results[sample_name]
G0_J5, R_J5 = fp['J5']
Theta = fp['Theta']
popt_SM = fp['SM']
popt_T5 = fp['T5']

pred_J5_smooth = model_J5(T_smooth, G0_J5, R_J5, Theta)
pred_SM_smooth = model_single_raman(T_smooth, *popt_SM)
pred_T5_smooth = model_T5_offset(T_smooth, *popt_T5)

pred_J5_data = model_J5(T_data, G0_J5, R_J5, Theta)
pred_SM_data = model_single_raman(T_data, *popt_SM)
pred_T5_data = model_T5_offset(T_data, *popt_T5)

fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
ax1.plot(T_data, rate, 'ko', ms=5, label='S2 data')
ax1.plot(T_smooth, pred_J5_smooth, 'r-', lw=2,
         label=rf'$J_5$: $R^2={fp["R2_J5"]:.4f}$, $\Theta_{{\rm eff}}={Theta:.0f}$ K')
ax1.plot(T_smooth, pred_SM_smooth, 'b--', lw=1.7, alpha=0.8,
         label=rf'$n(n+1)$ single-mode, $\omega\approx{popt_SM[2]:.0f}$ cm$^{{-1}}$')
ax1.plot(T_smooth, pred_T5_smooth, 'g:', lw=2.0, alpha=0.8,
         label=rf'$\Gamma_0+A T^5$')
ax1.set_xscale('log'); ax1.set_yscale('log')
ax1.set_xlabel('Temperature (K)'); ax1.set_ylabel(r'$1/T_1$ (s$^{-1}$)')
ax1.set_title('(a) Model comparison on S2')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=8)

resid_J5 = rate - pred_J5_data
resid_SM = rate - pred_SM_data
resid_T5 = rate - pred_T5_data

ax2.axhline(0, color='gray', ls='--', lw=1)
ax2.plot(T_data, resid_J5, 'o-', color='red', ms=4, lw=1,
         label=rf'$J_5$ RMSE={fp["RMSE_J5"]:.0f}, log={fp["RMSE_log_J5"]:.3f}')
ax2.plot(T_data, resid_SM, 's--', color='blue', ms=4, lw=1, alpha=0.7,
         label=rf'single-mode RMSE={fp["RMSE_SM"]:.0f}, log={fp["RMSE_log_SM"]:.3f}')
ax2.plot(T_data, resid_T5, '^:', color='green', ms=4, lw=1, alpha=0.7,
         label=rf'$\Gamma_0+A T^5$ RMSE={fp["RMSE_T5"]:.0f}, log={fp["RMSE_log_T5"]:.3f}')
ax2.set_xlabel('Temperature (K)'); ax2.set_ylabel(r'Residuals (s$^{-1}$)')
ax2.set_title('(b) Linear residuals')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=8)

fig2.suptitle(r'Model comparison: $J_5$ vs single-mode vs offset $T^5$', fontsize=13, fontweight='bold')
fig2.tight_layout()
fig2.savefig(OUTDIR / 'fig2_model_comparison_final.png', dpi=300, bbox_inches='tight')
fig2.savefig(OUTDIR / 'fig2_model_comparison_final.pdf', bbox_inches='tight')
plt.close(fig2)

# ------------------------------
#  حفظ ملخص النتائج في CSV
# ------------------------------
with open(OUTDIR / 'fit_summary_metrics.csv', 'w', encoding='utf-8') as f:
    f.write('Sample,Model,R2,RMSE,RMSE_log10,Characteristic_scale\n')
    for name in samples:
        fp = fit_results[name]
        f.write(f"{name},J5,{fp['R2_J5']:.8f},{fp['RMSE_J5']:.8g},{fp['RMSE_log_J5']:.8g},Theta_eff={fp['Theta']:.1f} K\n")
        f.write(f"{name},single_mode,{fp['R2_SM']:.8f},{fp['RMSE_SM']:.8g},{fp['RMSE_log_SM']:.8g},omega={fp['SM'][2]:.2f} cm^-1\n")
        f.write(f"{name},offset_T5,{fp['R2_T5']:.8f},{fp['RMSE_T5']:.8g},{fp['RMSE_log_T5']:.8g},Gamma0+A*T^5\n")

print('✅ تم حفظ جميع المخرجات بنجاح.')

# ------------------------------
#  تحميل الملفات تلقائياً (خاص بـ Google Colab)
# ------------------------------
try:
    from google.colab import files
    print('🔄 جارٍ تحميل الملفات إلى جهازك...')
    files.download('fig1_J5_fit_Jarmola_final.png')
    files.download('fig1_J5_fit_Jarmola_final.pdf')
    files.download('fig2_model_comparison_final.png')
    files.download('fig2_model_comparison_final.pdf')
    files.download('fit_summary_metrics.csv')
    print('✔️ تم بدء التحميل. إذا لم يبدأ تلقائياً، استخدم الروابط الظاهرة.')
except ImportError:
    print('⚠️ لستَ في بيئة Google Colab. الملفات محفوظة في المجلد الحالي ويمكنك تحميلها يدوياً.')
