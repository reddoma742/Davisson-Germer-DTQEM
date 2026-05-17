# DTQEM v22.0 – Self‑Calibrating Spectral Inversion for Hydrogen‑like Atoms

**Author:** Reddouane Berramdane  
**AI‑assisted tools:** Gemini, DeepSeek, Claude, Perplexity  
**License:** CC BY‑NC 4.0  
**Previous DOIs:** 10.5281/zenodo.20090038 (v13), v16, v17, v18, v19, v20  
**Concept DOI:** (same repository)

---

## Abstract (English)

DTQEM v22.0 introduces a **three‑stage self‑calibrating inversion protocol** for hydrogen‑like atomic spectra. From three sets of FWHM linewidth measurements (at \(E=0\), at a known calibration strength \(E_{\text{cal}}\), and at an unknown observer strength \(E_{\text{unk}}\)), the model recovers three fundamental physical parameters:
- **Temperature** \(T\) (K) – from Doppler broadening,
- **Dephasing coefficient** \(\alpha\) (dimensionless) – characterising the intrinsic decoherence of the system,
- **Observer strength** \(E\) (0…1) – quantifying the environmental measurement back‑action.

The core innovation is that \(\alpha\) is calibrated **before** \(T\) using the difference \(\Delta\Gamma_i = \Gamma_i(E_{\text{cal}}) - \Gamma_i(E=0) = \alpha\,\omega_{0,i}\,E_{\text{cal}}\), which completely eliminates the temperature dependence. This breaks the degeneracy between Doppler and dephasing broadening that plagued earlier multi‑line inversion attempts. The protocol is validated on synthetic data (noise‑free error < 0.001 %) and shows robust performance (error < 5 % for 1 % measurement noise). A bootstrap method provides realistic uncertainty estimates. The code is open‑source, production‑grade, and ready for experimental spectra.

---

## Abstract (العربية)

يقدم الإصدار v22.0 **بروتوكولاً عكسياً ذاتي المعايرة بثلاث مراحل** للأطياف الذرية الشبيهة بالهيدروجين. من ثلاث مجموعات من قياسات عرض الخط الطيفي (عند \(E=0\)، وعند قوة معايرة معلومة \(E_{\text{cal}}\)، وعند قوة مراقب مجهولة \(E_{\text{unk}}\))، يستعيد النموذج ثلاثة معاملات فيزيائية أساسية:
- **درجة الحرارة** \(T\) (كلفن) – من التوسيع الدوبلري،
- **معامل إزالة الطور** \(\alpha\) (بدون أبعاد) – يحدد فك التماسك الذاتي للنظام،
- **قوة المراقب** \(E\) (0…1) – يحدد تأثير القياس البيئي.

الابتكار الأساسي هو معايرة \(\alpha\) **قبل** \(T\) باستخدام الفرق \(\Delta\Gamma_i = \Gamma_i(E_{\text{cal}}) - \Gamma_i(E=0) = \alpha\,\omega_{0,i}\,E_{\text{cal}}\)، الذي يلغي الاعتماد على درجة الحرارة تماماً. هذا يكسر الانحلال (degeneracy) بين التوسيع الدوبلري وتبديد DTQEM الذي كان يعيق محاولات الانعكاس متعددة الخطوط السابقة. تم التحقق من صحة البروتوكول على بيانات اصطناعية (خطأ < 0.001 % بدون ضوضاء) ويظهر أداءً متيناً (خطأ < 5 % عند 1 % ضوضاء في القياس). طريقة bootstrap توفر تقديرات واقعية لعدم اليقين. الكود مفتوح المصدر، جاهز للإنتاج، ومهيأ للأطياف التجريبية.

---

## 1. The degeneracy problem and its solution

In the baseline DTQEM forward model (v16.0–v20.0), the total linewidth (FWHM) of a hydrogen‑like transition is:

\[
\Delta\nu_i = \frac{1}{2\pi}\left[A_{si} + \underbrace{\frac{\omega_{0,i}}{c}\sqrt{\frac{2k_B T}{m_H}}}_{\text{Doppler}} + \underbrace{\alpha\,\omega_{0,i}\,(1+E)}_{\text{DTQEM dephasing}} + \gamma_{\text{col}}\right],
\]

where \(\omega_{0,i}=2\pi c/\lambda_i\) and \(A_{si}\) is the Einstein A coefficient.  
Both the Doppler term and the dephasing term are proportional to \(\omega_{0,i}\); therefore, when several lines are used together, the parameters \(T\) and \(\alpha(1+E)\) cannot be uniquely separated – this is the **degeneracy** that caused earlier multi‑line inversions to fail (e.g., giving \(T \approx 2260\) K instead of 800 K).

**The key insight** (due to a collaborator) is to first measure the linewidth at a **known** observer strength \(E_{\text{cal}}\) (e.g., \(E_{\text{cal}}=1\)) and at \(E=0\). Subtracting the two:

\[
\Delta\Gamma_i = \Gamma_i(E_{\text{cal}}) - \Gamma_i(E=0) = \alpha\,\omega_{0,i}\,E_{\text{cal}} .
\]

All temperature‑dependent terms (\(A_{si}\), Doppler, collisions) cancel out. Thus \(\alpha\) can be calibrated **independently of \(T\)** using the weighted average over several lines:

\[
\alpha = \frac{\sum_i \omega_{0,i}\,\Delta\Gamma_i}{\sum_i \omega_{0,i}^2\,E_{\text{cal}}}.
\]

Once \(\alpha\) is known, \(T\) is determined from the \(E=0\) measurements alone (no degeneracy left), and finally the unknown \(E_{\text{unk}}\) is obtained from the third set of measurements.

---

## 2. The three‑stage protocol

| Stage | Measurements | Parameters used | Output |
|-------|--------------|-----------------|--------|
| **0** | FWHM at \(E=0\) and \(E=E_{\text{cal}}\) | – | \(\alpha\) (and per‑line consistency) |
| **1** | FWHM at \(E=0\) | \(\alpha\) | \(T\) |
| **2** | FWHM at unknown \(E\) | \(\alpha\), \(T\) | \(E\) |

All inversions use a log‑squared residual objective function:

\[
\mathcal{L}(\theta) = \sum_{i} \left[\ln\frac{\Delta\nu_i^{\text{model}}(\theta)}{\Delta\nu_i^{\text{meas}}}\right]^2,
\]

minimised with bounded scalar optimisation (`scipy.optimize.minimize_scalar`). Uncertainty is estimated via **bootstrap** (500–1000 resampling trials with 1 % multiplicative noise).

---

## 3. Numerical validation (synthetic data)

True parameters:  
\(T_{\text{true}} = 800.0\ \text{K},\quad \alpha_{\text{true}} = 2\alpha_{\text{ref}},\quad E_{\text{true}} = 0.7,\quad E_{\text{cal}}=1.0\).

**Noise‑free inversion:**
- Inferred \(T = 800.000\ \text{K}\) (error 0.0000 %)
- Inferred \(\alpha = 1.4847\times10^{-5}\) (error 0.0000 %)
- Inferred \(E = 0.700001\) (error \(< 10^{-5}\))

**Per‑line \(\alpha\) calibration** (all identical, confirming consistency):
\[
\alpha_{\text{Hα}} = \alpha_{\text{Hβ}} = \alpha_{\text{Hγ}} = \alpha_{\text{Hδ}} = 1.4847\times10^{-5}.
\]

**Noise robustness** (median errors, 200 trials per level):

| Noise level | \(\Delta T/T\) med (%) | \(\Delta E\) med (abs) |
|-------------|------------------------|------------------------|
| 0.0 %       | 0.00                   | 0.00000                |
| 0.5 %       | 1.85                   | 0.00575                |
| 1.0 %       | 3.86                   | 0.01273                |
| 2.0 %       | 7.67                   | 0.02099                |
| 5.0 %       | 19.14                  | 0.05091                |

These results demonstrate that even with 1 % measurement noise the temperature error stays below 4 % and the absolute error in \(E\) is ~0.01, which is excellent for experimental work.

---

## 4. Comparison with previous versions

| Feature | v20.0 (entanglement decay) | v21.0 (pre‑bootstrap inversion) | v22.0 (production inversion) |
|---------|----------------------------|----------------------------------|------------------------------|
| Physical system | Two‑qubit entanglement | Hydrogen Balmer lines | Hydrogen Balmer lines |
| Inverse protocol | – | Three‑stage (no uncertainties) | Three‑stage + bootstrap + consistency |
| Uncertainty estimates | – | – | ✅ sigma_T, sigma_alpha, sigma_E |
| Per‑line α consistency check | – | – | ✅ σ/μ < 5% |
| Convergence warnings | – | – | ✅ residual checks + boundary alerts |
| Hydrogen mass | – | \(m_p\) | \(m_p + m_e\) |
| User‑defined bounds | – | fixed | T_max, E_max parameters |

---

## 5. Code and usage

The main script is `dtqem_v22_inversion.py`. It can be run as‑is to reproduce the validation tables and figures. To apply to real spectra, prepare three dictionaries of measured FWHM (in Hz) for the same set of lines (Hα, Hβ, Hγ, Hδ) and call:

```python
from dtqem_v22_inversion import invert_v22

result = invert_v22(fwhm_E0, fwhm_Ecal, E_cal, fwhm_Eunk,
                    noise_est=0.01, N_bootstrap=500)
result.summary()
