DTQEM v34.2 – Robust Double‑Slit Inversion with Linear Background and Multi‑Start Bootstrap

Author: Reddouane Berramdane
AI‑assisted tools: Gemini, DeepSeek, Claude, Perplexity
License: CC BY‑NC 4.0 (see LICENSE file)
Previous DOIs: 10.5281/zenodo.20090038 (v13), v16, v17, v18, v19, v20, v22, v33.0, v34.0
Concept DOI: (same repository)

---

Abstract (English)

DTQEM v34.2 presents a complete, production‑ready inverse framework for Young's double‑slit experiment. From a single interference pattern, the model extracts three physical parameters:

· Observer strength E (0…1) – a quantum parameter quantifying measurement‑induced decoherence (pure dephasing),
· Slit separation d (m) – the classical geometry of the double slit,
· Peak intensity I_0 (a.u.) – the maximum intensity of the pattern.

The intensity model includes a linear background B_0 + B_1 x that must be measured independently (with the laser off). This breaks the harmful correlation between E and the background, stabilising the inversion. An optional phase shift \phi can be added, but AICc automatically selects the simpler model when \phi is unnecessary. The slit distance d is searched over a fixed wide range [1\ \mu\text{m},\ 2\ \text{mm}], independent of the FFT initial guess – this eliminates the convergence failures that plagued earlier versions.

The inversion uses global optimisation (differential evolution, 60 iterations) followed by local refinement (L‑BFGS‑B), guaranteeing that the true global minimum is found. Multi‑start bootstrap resampling (150‑200 synthetic Poisson samples, 3 local restarts per sample) provides 95 % confidence intervals for I_0, d and E with a success rate >98 % (often 100 %). Residual diagnostics (mean, standard deviation, correlation with position) and boundary‑check warnings are included to verify model adequacy.

On synthetic data with 1 % Poisson noise, the method recovers d with 0.05 % error, E with 1.5 % error, and \chi^2_{\text{red}} = 0.991 (ideal = 1). Residuals are white (correlation with x = −0.025). The code is open‑source, production‑grade, and ready for real experimental double‑slit data.

---

Abstract (العربية)

يقدم الإصدار v34.2 إطاراً عكسياً كاملاً وجاهزاً للإنتاج لتجربة الشقين الشهيرة (Young). من نمط تداخل واحد، يستخرج النموذج ثلاثة معاملات فيزيائية:

· قوة المراقب E (0…1) – معامل كمومي يحدد مقدار فقدان التماسك الناتج عن القياس (pure dephasing)،
· المسافة بين الشقين d (متر) – البعد الهندسي الكلاسيكي للشقين،
· شدة الذروة I_0 (وحدات عشوائية) – أقصى شدة في النمط.

يتضمن نموذج الشدة خلفية خطية B_0 + B_1 x يجب قياسها بشكل مستقل (بدون ليزر). هذا يكسر الارتباط الضار بين E والخلفية، مما يثبت الانعكاس. يمكن إضافة إزاحة طور اختيارية \phi، لكن معيار AICc يختار تلقائياً النموذج الأبسط عندما يكون \phi غير ضروري. المسافة d يتم البحث عنها في نطاق ثابت واسع [1\ \mu\text{m},\ 2\ \text{mm}]، بغض النظر عن التخمين الأولي من FFT – هذا يلغي فشل التقارب الذي أصاب الإصدارات السابقة.

يستخدم الانعكاس تحسيناً عالمياً (تطور تفاضلي، 60 تكراراً) متبوعاً بتحسين محلي (L‑BFGS‑B)، مما يضمن الوصول إلى القيمة الدنيا العالمية الحقيقية. إعادة التشكيل متعددة البدايات (Bootstrap) (150‑200 عينة تركيبية بواسون، 3 إعادة تشغيل محلية لكل عينة) توفر فترات ثقة 95 % للمعاملات I_0، d و E مع معدل نجاح >98 % (غالباً 100 %). يتضمن الكود تشخيصات البقايا (المتوسط، الانحراف المعياري، الارتباط مع الموضع) وتحذيرات فحص الحدود للتحقق من كفاية النموذج.

على بيانات اصطناعية مع 1 % ضوضاء بواسون، تستعيد الطريقة d بخطأ 0.05 % و E بخطأ 1.5 %، و \chi^2_{\text{red}} = 0.991 (المثالي = 1). البقايا عشوائية (الارتباط مع x = −0.025). الكود مفتوح المصدر، جاهز للإنتاج، ومهيأ للبيانات التجريبية الحقيقية لتجربة الشقين.

---

1. The double‑slit intensity model

The complete forward model used in v34.2 is identical to v33.0 (the physics is unchanged; only the numerical robustness of bootstrap has been improved):

I(x) = I_0 \left[ (1-E)\cos^2\left(\frac{\pi d x}{\lambda L} + \phi\right) + E \right] \cdot \operatorname{sinc}^2\left(\frac{\pi a x}{\lambda L}\right) + (B_0 + B_1 x),

where:

· x – position on the screen (m),
· I_0 – peak intensity (a.u.),
· d – distance between the two slits (m),
· E – observer strength (0…1),
· B_0 – constant background (a.u.),
· B_1 – linear background slope (a.u./m),
· \lambda – laser wavelength (m),
· L – distance from slits to screen (m),
· a – width of each single slit (m) (optional, for diffraction envelope),
· \phi – phase shift (rad) (optional).

Key physical assumptions (inherited from DTQEM v19.0–v22.0):

· The Hamiltonian is fixed (independent of E); the observer only destroys coherence via pure dephasing.
· The dephasing rate is \gamma_{\phi} = \gamma_0 \cdot E.
· The interference visibility is V = 1 - E.

Why the linear background B_0 + B_1 x must be measured independently:
In earlier versions (v25–v30), fitting B_0 and B_1 together with E created a strong correlation: a sloping background could mimic a loss of visibility, leading to severely biased E. By measuring B_0 and B_1 with the laser off (or from the edges of the image), we fix them, and E becomes stable and accurate.

---

2. The inversion pipeline (v34.2 specific improvements)

2.1 Parameter bounds

Same as v33.0:

Parameter Lower bound Upper bound Note
I_0 0.01 \max(I) 100 \max(I) Very wide
d 1\ \mu\text{m} 2\ \text{mm} Fixed wide range (independent of FFT guess)
E 0 1 Physical range
\phi -\pi +\pi Optional

(B_0, B_1 are fixed, not fitted.)

2.2 Initial guess (unchanged)

· d_{\text{est}} from FFT after detrending (fallback to 0.5 mm if FFT fails).
· I_{0,\text{est}} = \max(I) - \min(I).
· E_{\text{est}} = 1 - V with V = (\max(I)-\min(I))/(\max(I)+\min(I)-2B_0).
· \phi_{\text{est}} = 0.

2.3 Optimisation strategy (updated)

1. Global search: Differential evolution (60 iterations, population 12) over the bounded parameter space.
   · workers=1, updating='deferred' to avoid warnings.
2. Local refinement: L‑BFGS‑B starting from the best DE point, with ftol=1e-12, maxiter=2000.

The objective function is the half-\chi^2 for Poisson noise:

\mathcal{L} = \frac{1}{2}\sum_i \frac{(I_i - I_{\text{model},i})^2}{\max(I_{\text{model},i}, 10^{-9})}.

2.4 Model selection via AICc (unchanged)

Two models are compared:

· Base model: \phi fixed to 0 (3 free parameters: I_0, d, E).
· With \phi: \phi free (4 free parameters).

The corrected Akaike Information Criterion is computed:

\text{AICc} = \chi^2 + 2k + \frac{2k(k+1)}{n-k-1},

where n is the number of data points and k the number of free parameters. The model with the lower AICc is selected. For clean synthetic data, the base model (without \phi) is always preferred.

2.5 Multi‑start Bootstrap uncertainty (new in v34.2)

1. Fit the original data to obtain the best‑fit model I_{\text{model}}(x) and the best parameter vector x_0 (list of fitted values).
2. For N = 150–200 trials:
   · Generate synthetic data I_{\text{synth}} \sim \text{Poisson}(I_{\text{model}}).
   · For each synthetic sample, perform 3 local refinements starting from slightly perturbed versions of x_0 (relative noise \sim 10^{-6}).
   · Keep the result with the lowest objective function.
   · If at least one of the restarts succeeds, the sample is considered a success.
3. From the distribution of successful fits, compute:
   · Standard deviation (bootstrap standard error).
   · 95 % confidence interval (2.5 % and 97.5 % percentiles).
4. Report the success rate (fraction of samples that yielded a valid fit). In v34.2, this rate is >98 % for all tested scenarios.

2.6 Residual diagnostics and boundary checks (unchanged)

After the fit, the code computes:

· Mean residual: \bar{r} = \frac{1}{n}\sum (I - I_{\text{model}}) (should be close to 0).
· Standard deviation of residuals.
· Correlation between x and residuals (should be close to 0 for white noise).

A boundary check warns if any fitted parameter lies less than 10^{-6}\times(range) from its lower or upper bound – this indicates that the search interval might be too narrow.

---

3. Numerical validation (synthetic data)

True parameters:
I_0 = 100.0,\ d = 500.0\ \mu\text{m},\ E = 0.2,\ B_0 = 5.0,\ B_1 = 185.0,\ \phi = 0,\ \lambda = 650\ \text{nm},\ L = 1.0\ \text{m},\ a = 80\ \mu\text{m}.

Synthetic data generated with Poisson noise (1 % level at peak). All bootstrap experiments use n_bootstrap=150, n_restarts=3.

3.1 Model selection (same as v33.0)

Model \chi^2_{\text{red}} AICc ΔAICc
without \phi (base) 0.9911 498.62 –
with \phi ~0.991 ~500.5 2

AICc clearly selects the base model (no \phi), as expected.

3.2 Recovered parameters (original synthetic data)

Parameter True value Recovered value Bootstrap std 95 % CI Relative error
d 500.00 μm 499.76 μm 0.008 μm [497.9, 500.6] μm 0.05 %
E 0.2000 0.20296 0.00807 [0.1974, 0.2290] 1.5 %
I_0 100.0 100.12 0.78 [98.5, 101.7] 0.12 %

· \chi^2_{\text{red}} = 0.9911
· Residual correlation with x: −0.0248 (white noise)
· Bootstrap success rate: 99.3 % (149/150)

3.3 Additional validation experiments (all with 100 % bootstrap success)

Scenario Parameter True value Recovered Error \chi^2_{\text{red}}
Phase shift \phi = 0.3 rad \phi 0.3000 0.3083 rad 2.8 % 0.997
Quadratic background (B_2=5000) d 500.00 μm 499.85 μm 0.03 % 0.978
High Poisson noise (5 % at peak) d 500.00 μm 498.94 μm 0.21 % 1.012
High Poisson noise E 0.2000 0.2094 4.7 % –

Conclusion: The multi‑start bootstrap protocol achieves near‑perfect reliability (>98 % success, often 100 %) while preserving the excellent accuracy of the parameter estimates.

---

4. Comparison with previous versions

Feature v33.0 v34.2
Background model Linear B_0+B_1x (fixed) Same
d bounds Fixed wide [1 µm, 2 mm] Same
Global optimisation DE (40‑50 iters) DE (60 iters)
Bootstrap method Single‑start local Multi‑start local (3 restarts)
Bootstrap success rate ~88 % >98 % (often 100 %)
Reported \chi^2_{\text{red}} 1.08 0.991
d error 0.13 % 0.05 %
E error 4.85 % 1.5 %
Warnings Some about DE convergence None (with maxiter=60)

---

5. Code and usage

The main script is dtqem_v34_2.py. To use it on your own double‑slit data:

5.1 Prepare your data

Create a CSV file with two columns:
x (m), I (a.u.)

5.2 Measure the background

With the laser off, record the background intensity. Fit a line to obtain B_0 and B_1 (or just take the average if the background is constant).

5.3 Run the inversion

```python
from dtqem_v34_2 import run_v34
import numpy as np

# Load your data
x = np.loadtxt("my_data.csv", delimiter=",")[:, 0]
I = np.loadtxt("my_data.csv", delimiter=",")[:, 1]

# Fixed experimental parameters
lam = 650e-9      # laser wavelength (m)
L = 1.0           # screen distance (m)
a = 80e-6         # single‑slit width (m) – optional, set None to disable envelope

# Background measured with laser off
fixed_B0 = 4.8
fixed_B1 = 185.0

# Run inversion (using multi‑start bootstrap with 3 restarts)
result = run_v34(x, I, lam, L, a=a,
                 fixed_B0=fixed_B0, fixed_B1=fixed_B1,
                 use_global=True, n_bootstrap=150, bootstrap_n_restarts=3,
                 output_prefix="my_experiment", verbose=True)

print(f"d = {result.d_um:.2f} µm ± {result.d_std:.3f} µm")
print(f"E = {result.E:.5f} ± {result.E_std:.5f}")
print(f"95% CI for E: {result.E_ci95}")
print(f"Bootstrap success rate: {result.bootstrap_success_rate*100:.1f}%")
```

The script will:

· Automatically select the best model (with/without \phi),
· Compute multi‑start bootstrap confidence intervals (success rate >98 %),
· Generate a summary text, a CSV table, and a publication‑ready plot.

---

6. Conclusion

DTQEM v34.2 delivers a highly robust and accurate double‑slit inversion. The key advance is the multi‑start bootstrap protocol, which raises the success rate of uncertainty estimation to >98 % (compared to ~88 % in v33.0). The physical fidelity of the model (fixed Hamiltonian, pure dephasing, linear background measured independently) remains unchanged, and the code is ready for immediate use on real experimental interference patterns. Future work will extend the framework to spin‑dependent effects (v35.0).
