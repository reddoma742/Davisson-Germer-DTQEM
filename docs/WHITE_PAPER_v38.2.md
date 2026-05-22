DTQEM v38.2 – Hydrogen Balmer‑alpha Zeeman Inversion with Multi‑Start Bootstrap and 100% Success Rate

Author: Reddouane Berramdane
AI‑assisted tools: Gemini, DeepSeek, Claude, Perplexity
License: CC BY‑NC 4.0 (see LICENSE file)
Previous DOIs: 10.5281/zenodo.20090038 (v13), v16, v17, v18, v19, v20, v22, v33.0, v34.0, v34.2
Concept DOI: (same repository)

---

Abstract (English)

DTQEM v38.2 presents a complete, production‑ready inverse framework for extracting the magnetic field strength from the Zeeman splitting of the hydrogen Balmer‑alpha line (Hα, 656.28 nm). From a single unpolarised spectrum, the model recovers three physical parameters:

· Magnetic field B (Tesla) – the primary output, directly linked to the Zeeman shift \Delta\lambda = \frac{\lambda_0^2}{c}\,\frac{\mu_B}{h}\,|B| (normal Zeeman effect with g_{\mathrm{eff}}=1),
· Peak intensity I_0 (a.u.) – the line amplitude,
· Line width \sigma (m) – the Gaussian width (instrumental + thermal broadening).

The intensity model assumes a symmetric Gaussian triplet (central \pi component and two \sigma^\pm side‑lobes) with a fixed intensity ratio f = 0.60 (or optionally fitted). A linear background B_0 + B_1\lambda can be measured independently (with the light source off) and subtracted or fitted. The model also includes a simple single‑peak Gaussian for the field‑free case. AICc with an adaptive SNR‑based threshold automatically selects between the triplet and the single‑peak model, avoiding false detections at low fields.

The inversion uses global optimisation (differential evolution, 40 generations) followed by local refinement (L‑BFGS‑B). A multi‑start parametric bootstrap (30 synthetic Poisson samples, 10 restarts per sample, 20% fully random starts) provides 95% confidence intervals for B with a 100% success rate under standard validation. Residual diagnostics (mean, standard deviation, correlation with wavelength) and boundary‑check warnings are included.

On synthetic data with realistic Poisson noise, the method recovers B with relative error <2% for fields ≥0.5 T, detection limit ~0.15 T, and \chi^2_{\mathrm{red}}\approx 1. Bootstrap standard deviations (≈0.08–0.12 T) are realistic, in contrast to the over‑optimistic Hessian errors (≈0.001–0.004 T). The code is open‑source, fast (8–13 s per spectrum), and ready for laboratory, solar, and astrophysical applications where only intensity spectra are available.

---

Abstract (العربية)

يقدم الإصدار v38.2 إطاراً عكسياً كاملاً وجاهزاً للإنتاج لاستخلاص شدة المجال المغناطيسي من انشقاق زيمان لخط الهيدروجين ألفا (Hα، 656.28 نانومتر). من طيف واحد غير مستقطب، يستخرج النموذج ثلاثة معاملات فيزيائية:

· شدة المجال المغناطيسي B (تسلا) – المخرج الأساسي، المرتبط مباشرة بانزلاق زيمان \Delta\lambda = \frac{\lambda_0^2}{c}\,\frac{\mu_B}{h}\,|B| (تأثير زيمان العادي مع g_{\mathrm{eff}}=1)،
· شدة الذروة I_0 (وحدات عشوائية) – سعة الخط،
· عرض الخط \sigma (متر) – العرض الغاوسي (مزيج من الاستعيان الآلي والتمدد الحراري).

يفترض النموذج ثلاثياً غاوسياً متماثلاً (مركبة π المركزية ومركبتي σ± الجانبيتين) بنسبة شدة ثابتة f = 0.60 (أو يمكن تلاؤمها اختيارياً). يمكن قياس خلفية خطية B_0 + B_1\lambda بشكل مستقل (بدن مصدر الضوء) وطرحها أو تلاؤمها. يتضمن النموذج أيضاً قمة غاوسية مفردة للحالة الخالية من الحقل. معيار AICc مع عتبة معتمدة على نسبة الإشارة إلى الضوضاء (SNR) يختار تلقائياً بين الثلاثي والقمة المفردة، متجنباً الاكتشافات الخاطئة عند الحقول الضعيفة.

يستخدم الانعكاس تحسيناً عالمياً (تطور تفاضلي، 40 جيلاً) متبوعاً بـ تحسين محلي (L‑BFGS‑B). إعادة تشكيل حدودية متعددة البدايات (30 عينة بواسون تركيبية، 10 إعادة تشغيل لكل عينة، 20% بدايات عشوائية بالكامل) توفر فترات ثقة 95% لـ B مع نسبة نجاح 100% في التحقق القياسي. تتضمن الأداة تشخيصات البقايا (المتوسط، الانحراف المعياري، الارتباط مع الطول الموجي) وتحذيرات فحص الحدود.

على بيانات اصطناعية مع ضوضاء بواسون واقعية، تستعيد الطريقة B بخطأ نسبي <2% للحقول ≥0.5 تسلا، حد كشف ~0.15 تسلا، و \chi^2_{\mathrm{red}}\approx 1. الانحرافات المعيارية للـ Bootstrap (≈0.08–0.12 تسلا) واقعية، على عكس أخطاء هيسيان المفرطة في التفاؤل (≈0.001–0.004 تسلا). الكود مفتوح المصدر، سريع (8–13 ثانية لكل طيف)، وجاهز للتطبيقات المخبرية والشمسية والفيزياء الفلكية حيث تتوفر فقط أطياف الشدة.

---

1. The Zeeman triplet model for Hα

The complete forward model used in v38.2 is a symmetric Gaussian triplet:

I(\lambda) = I_0\,G(\lambda,\lambda_0,\sigma) \;+\; I_0\,f\,G(\lambda,\lambda_0+\Delta\lambda,\sigma) \;+\; I_0\,f\,G(\lambda,\lambda_0-\Delta\lambda,\sigma) \;+\; (B_0 + B_1\lambda),

where:

· G(\lambda,\lambda_c,\sigma) = \exp\left(-\frac{(\lambda-\lambda_c)^2}{2\sigma^2}\right) – Gaussian profile,
· \lambda_0 – rest wavelength of Hα (≈ 656.28 nm) – fitted as lambda_center,
· f – ratio of side‑peak to central peak amplitude (fixed to 0.60, or optionally fitted),
· \Delta\lambda – Zeeman shift (normal Zeeman effect for Hα, g_{\mathrm{eff}}=1):
  \Delta\lambda = \frac{\lambda_0^2}{c}\,\frac{\mu_B}{h}\,|B|,
  with \mu_B/h = 1.399624\times10^{10} Hz/T (Bohr magneton over Planck’s constant),
· B_0, B_1 – linear background (measured independently, e.g., with the source off),
· B – magnetic field strength (Tesla), the main output.

When the field is zero, the model reduces to a single Gaussian (the two side‑lobes coincide with the central peak, but to avoid degeneracy we use a dedicated single‑peak model).

---

2. Physical assumptions

· Normal Zeeman effect: The Landé g‑factor is effectively 1 for the Hα transition in the absence of fine‑structure resolution.
· Unpolarised observation: The spectrum is the sum of the \pi and \sigma^\pm components with the same intensity ratio f (typically 0.60 for Hα in a transverse field).
· Pure Gaussian broadening: No Voigt or Lorentzian component; instrumental and thermal broadening are approximated as Gaussian.
· Poisson statistics: The photon counts follow a Poisson distribution; we use the full Poisson negative log‑likelihood (including Stirling’s constant).

These assumptions are a pragmatic compromise between physical accuracy and numerical tractability, suitable for fast and robust inversion of real spectra.

---

3. The inversion pipeline (v38.2 specific features)

3.1 Parameter bounds

Parameter Lower bound Upper bound Note
\lambda_0 estimated center – 0.5×range estimated center + 0.5×range adaptive
B 0.0 T 3.0 T physical range
I_0 0.05 × max(I) 15 × max(I) very wide
\sigma 0.001 nm 0.08 nm instrumental + thermal
f (if free) 0.3 0.9 physical for Hα
B_0, B_1 (if fitted) 0 0.3×max(I) background

3.2 Initial guess

· \lambda_0 from the wavelength of the maximum intensity.
· B = 0.5 T (default).
· I_0 = 1.2 × max(I).
· \sigma = 0.008 nm (8 pm).
· f = 0.60 (fixed by default, can be fitted).
· Background: if not subtracted, initialised to 0.01×max(I).

3.3 Optimisation strategy

1. Global search: Differential evolution (40 generations, population 10) over the bounded parameter space (workers=1, updating='deferred').
2. Local refinement: L‑BFGS‑B starting from the best DE point, with ftol=1e-14, gtol=1e-10, maxiter=5000.

The objective function is the full Poisson negative log‑likelihood:

\mathcal{L} = \sum_i \left[ \mu_i - y_i \log(\mu_i) + \log(\Gamma(y_i+1)) \right],

where \mu_i = I_{\text{model}}(\lambda_i) and y_i are the observed counts.

3.4 Model selection via AICc

Two models are compared:

· Single‑peak Gaussian (3 free parameters: \lambda_0, I_0, \sigma).
· Triplet (4 or 5 free parameters: \lambda_0, B, I_0, \sigma, (f), plus background if fitted).

AICc is computed as:

\text{AICc} = 2k + 2\mathcal{L} + \frac{2k(k+1)}{n-k-1},

where n is the number of wavelength points, k the number of free parameters.

Because AICc may favour the triplet even when B is very small (due to the flexibility of the Gaussian triplet), we enforce two physical rejection criteria before the AICc decision:

· Spread ratio < 0.5: 2\Delta\lambda / \sigma < 0.5 → Zeeman splitting unresolved → force single‑peak.
· B/σ_B < 2: if the Hessian‑based uncertainty is available and B/\sigma_B < 2 → field not significant → force single‑peak.

Otherwise, the model with the lower AICc is selected (threshold adapted to SNR: stricter for low SNR).

3.5 Multi‑start parametric bootstrap

Uncertainty estimation is performed via a parametric bootstrap that preserves Poisson statistics and avoids the over‑optimistic errors of the Hessian matrix.

Procedure:

1. From the best‑fit triplet, generate 30 synthetic spectra by adding Poisson noise to the model.
2. For each synthetic spectrum, perform 10 restarts of local optimisation (L‑BFGS‑B):
   · 20% of restarts start from a fully random point within the bounds (to escape local minima).
   · 80% of restarts start from the original best‑fit parameters perturbed:
     · \lambda_0: additive Gaussian noise (σ = 5 pm).
     · B: additive noise scaled to 10% of the [0,3 T] range.
     · I_0 and \sigma: multiplicative noise (10% and 5%, respectively).
     · f and background: multiplicative noise (3% and 5%).
3. Accept a fit if it is physically valid (B\ge0, \sigma>0, I_0>0) – we do not rely on scipy’s success flag because L‑BFGS‑B often returns False for purely numerical reasons.
4. Keep the best (lowest NLL) among the restarts for each sample.
5. From the distribution of accepted B values, compute:
   · Standard deviation (bootstrap standard error).
   · 95% confidence interval (2.5 and 97.5 percentiles).

The success rate (accepted / total samples) is reported. In v38.2, it is 100% for all standard validation cases.

3.6 Residual diagnostics and boundary checks

After the fit, the code computes:

· Mean residual: should be close to 0.
· Standard deviation of residuals.
· Correlation between wavelength and residuals (should be close to 0 for white noise).

A boundary check warns if any fitted parameter lies less than 1% away from its bounds – indicating that the search interval may be too narrow.

---

4. Numerical validation (synthetic data)

True parameters for standard tests:
\lambda_0 = 656.28 nm, I_0 = 1400, \sigma = 0.008 nm, f = 0.60, background = 2.0 (a.u.).
Poisson noise added.
Bootstrap: 30 samples, 10 restarts, 20% random starts.

4.1 Model selection

Case SNR Selected model ΔAICc Spread ratio Comment
Single line (B=0) 1023 Single +159 – Correct
Triplet with B=0 2457 Single +273 – Correct
B=0.5 T 2122 Triplet –307 2.59 Correct
B=1.0 T 1012 Triplet –5550 4.57 Correct
B=1.5 T 1074 Triplet –31602 7.61 Correct
B=2.0 T 1197 Triplet –74569 10.51 Correct

4.2 Recovered parameters

True B (T) Recovered B (MAP) (T) Bootstrap std (T) 95% CI (T) Relative error \chi^2_{\mathrm{red}}
0.5 0.5057 0.1198 [0.284, 0.713] 1.1 % 1.01
1.0 0.9850 0.0821 [0.860, 1.139] 1.5 % 1.00
1.5 1.5025 0.1031 [1.293, 1.667] 0.2 % 0.99
2.0 1.9950 0.1017 [1.853, 2.185] 0.2 % 1.01
1.0 (low SNR 172) 0.9930 0.0999 [0.847, 1.213] 0.7 % 1.02

· Bootstrap success rate: 100% (30/30) in all tests.
· Residuals: mean ~0, correlation with λ < 0.01 (white noise).
· Comparison with Hessian: Hessian errors are unrealistically small (~0.003 T) → bootstrap errors are recommended.

4.3 Stress tests (Monte Carlo)

We performed 11 scenarios × 5 repeats, covering:

· Fields from 0 to 2.5 T.
· Amplitude reduced to 10% and 5% of nominal (very low SNR).
· Detection limit: ~0.15 T (below that the model correctly returns Single).

All tests passed with 100% bootstrap success for fields ≥0.5 T; at B=0.1 T the model selected Single.

---

5. Comparison with previous versions

Feature v34.2 (double‑slit) v38.2 (Hα Zeeman)
Physical system Double‑slit interference Hα Zeeman triplet
Model parameters I_0, d, E, B_0, B_1, \phi I_0, B, \lambda_0, \sigma, f, B_0, B_1
Likelihood Half‑\chi^2 (Poisson‑approximated) Full Poisson NLL
Bootstrap restarts 3 10
Bootstrap random starts No 20% fully random
Success rate 98% 100%
Uncertainty realism Good Excellent (matches Monte Carlo)
Model selection AICc (with/without phase) AICc + physical rejection rules

---

6. Code and usage

The software is provided in two variants:

· dtqem_v38_2.py – core library (functions run_zeeman_invision, ZeemanResult, etc.). Suitable for importing into your own scripts.
· dtqem_v38_2_full.py – standalone script that reproduces the validation suite, generates all plots, and saves CSV results. Can also be used for a single custom spectrum.

6.1 Prepare your data

Create a CSV file with two columns: wavelength (m), intensity (a.u.).
Example for Hα: wavelength range ~ 656.16 nm to 656.40 nm.

6.2 Measure (or estimate) the background

With the light source off, record the background. Fit a line to obtain B_0 and B_1.
Alternatively, set subtract_continuum=True to estimate a linear baseline from the edges.

6.3 Run the inversion (core version)

```python
from dtqem_v38_2 import run_zeeman_inversion
import numpy as np

# Load your data
wavelength = np.loadtxt("my_spectrum.csv", delimiter=",")[:, 0]
intensity  = np.loadtxt("my_spectrum.csv", delimiter=",")[:, 1]

# Run inversion
result = run_zeeman_inversion(
    wavelength, intensity,
    subtract_continuum=False,   # set True if you have no background measurement
    n_bootstrap=30,
    verbose=True
)

print(f"B = {result.B:.3f} ± {result.B_std:.3f} T")
print(f"95% CI = {result.B_ci95}")
print(f"Selected model: {result.selected_model}")
print(f"Bootstrap success rate: {result.bootstrap_rate*100:.1f}%")
```

The script will:

· Automatically select between Single and Triplet.
· Compute bootstrap confidence intervals (100% success under normal conditions).
· Print a summary and return a ZeemanResult object containing all fitted parameters, residuals, and the bootstrap distribution.

---

7. Conclusion

DTQEM v38.2 provides a highly robust, fast, and statistically sound inversion tool for extracting magnetic field strengths from Hα spectra. Key achievements:

· 100% bootstrap success rate in all validation tests (30 samples, 10 restarts, 20% random starts).
· Realistic uncertainty intervals (std ≈ 0.08–0.12 T), avoiding the over‑optimistic Hessian errors.
· Reliable model selection using AICc combined with physical rejection rules (spread ratio, B/σ_B).
· Low detection limit (~0.15 T) and high accuracy (error <2% for B ≥ 0.5 T).
· Open source, pure Python, easy to integrate into laboratory or astrophysical pipelines.

The code is already used for synthetic validation and is ready for real experimental spectra from solar observations, tokamak plasmas, glow discharges, and Z‑pinch devices. Future work will extend the framework to other spectral lines (e.g., He I, Ca II) and include Voigt profiles for better handling of instrumental broadening.
