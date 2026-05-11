# DTQEM White Paper – v15.1 (May 2026)

## Dual‑Time Quantum Entanglement Model: An Open Quantum Systems Framework with Continuous Measurement Control

**Author:** Reddouane Berramdane  
**AI-assisted tools:** The author used Gemini, Claude, and DeepSeek for code development and manuscript preparation.  
**DOI:** this version (to be assigned on Zenodo)  
**Previous DOI:** 10.5281/zenodo.20090038 (v13.0)  
**License:** DTQEM Research & Educational License (non‑commercial, academic use free)

---

## Abstract (English)

This work presents an open‑source numerical framework for simulating open quantum systems under the **Time‑Sovereignty** hypothesis, based on the Lindblad master equation solved via exact Liouvillian exponentiation.

**Four validated building blocks** are provided:
1. **Davisson–Germer** – electron diffraction (two‑qubit dephasing).
2. **Quantum tunneling** – double well with pure dephasing, thermal relaxation, and measurement.
3. **Schottky effect** – field‑enhanced thermionic emission.
4. **Tunneling with Temporal Observer (External Switch)** – a 4×4 Hilbert space coupling the tunnel qubit to an auxiliary qubit representing the observer’s state (Wave/Particle). The observer’s transition rates are controlled by an external strength \(E_{\text{ext}}\).

**New numerical results from the observer model:**
- **Effective Zeno scaling:** Increasing \(E_{\text{ext}}\) from 0 to 1 reduces tunneling probability \(P_{\text{right}}(t)\) and visibility \(V(t)\) while increasing distinguishability \(D(t)\) and observer particle probability \(t_p\).  
- **Empirical relation** observed in simulations:  
  \(\displaystyle P_{\text{right}}(t) \approx \left(\frac{\Delta}{2\hbar}\right)^2 t^2 \cdot (1 - E_{\text{ext}})^2\) (numerical fit, not derived analytically).
- **Balance condition generalised:** For non‑zero \(E_{\text{ext}}\), the \(V=D\) crossing occurs at a modified time \(\tau_{\text{bal}} = \frac{2\ln(\tan\theta)}{\gamma_{\phi0} + \Gamma_{\text{obs}}}\) where \(\Gamma_{\text{obs}} \propto E_{\text{ext}}\).

**Previous results confirmed:**
- Quantum Zeno effect: tuning \(\Gamma_{\text{meas}}\) increases tunneling time up to ×9.  
- Entropy saturation at \(S=\ln2\).  
- Markovianity (BLP=0).  
- No negative apparent time under Gaussian pulses.  
- Model does **not** reproduce the Gouanère resonance (80.874 MeV).

All codes, interactive GUIs, and documentation are open source.

---

## Abstract (العربية)

نقدم في هذا الإصدار نموذجاً جديداً: **النفق مع مراقب خارجي** (كيوبيت مساعد)، حيث يتحكم معامل \(E_{\text{ext}}\) في سرعة انتقال المراقب بين الحالة الموجية والجسيمية. تظهر المحاكاة أن زيادة \(E_{\text{ext}}\) تؤدي إلى تثبيط النفق (تأثير زينو)، وانخفاض الرؤية \(V\)، وارتفاع التميز \(D\). تم استخلاص علاقة تقريبية للزمن القصير تربط احتمال النفق بـ \((1-E_{\text{ext}})^2\)، ولكن يجب التأكيد أن هذه العلاقة هي **ملاءمة عددية** وليست مشتقة تحليلياً. هذا لا يقلل من قيمتها العلمية، بل يفتح باباً للبحث المستقبلي لاشتقاقها نظرياً.

---

## 1. Introduction

The Time‑Sovereignty hypothesis states that a quantum system remains coherent as long as its internal clock dominates. Interaction with the environment imposes an external “camera clock” that drives the system toward classical behaviour. DTQEM implements this via the Lindblad master equation.

This document summarises the core results obtained up to v15.1. In this version, we emphasise **numerical observations** and **empirical relations** obtained from exact simulations, distinguishing clearly between what is analytically derived and what is observed numerically.

---

## 2. Core Mathematical Framework

We solve the Lindblad equation:
\[
\frac{d\rho}{dt} = -i[H,\rho] + \sum_k \left( L_k \rho L_k^\dagger - \frac12\{L_k^\dagger L_k,\rho\}\right)
\]
using the Liouvillian superoperator exponentiation \(\vec{\rho}(t)=\exp(\mathcal{L}t)\vec{\rho}(0)\). The solver is implemented in Python with `scipy.linalg.expm`.

### 2.1 Davisson–Germer (two‑qubit)
- Qubit A: electron path (reflected/diffracted); qubit B: crystal mode.
- Hamiltonian \(H=0\); jump operator \(L=\sqrt{\gamma_{\phi0}}\,\sigma_z\otimes I\).
- Initial entangled state: \(|\psi(\theta)\rangle=\cos\frac{\theta}{2}|00\rangle+\sin\frac{\theta}{2}|11\rangle\) with \(\theta=180^\circ-2\phi_{\text{Bragg}}\).
- Visibility \(V=2|\rho_{03}|\), distinguishability \(D=|\rho_{00}-\rho_{33}|\).

### 2.2 Quantum tunneling (single qubit)
- Hamiltonian \(H=\frac{\Delta}{2}\sigma_x\) (tunnel splitting \(\Delta\)).
- Jump operators: dephasing \(L_\phi=\sqrt{\gamma_{\phi}(T)}\sigma_z\), relaxation \(L_\pm=\sqrt{\gamma_{\text{rel}} n_{\text{th}}}\sigma_\pm\).
- Start from left well \(|0\rangle\), compute \(P_{\text{right}}(t)\), \(V(t)=2|\rho_{01}|\), \(D(t)=|\rho_{00}-\rho_{11}|\).

### 2.3 Schottky effect (two‑level system)
- States \(|M\rangle\) (metal) and \(|V\rangle\) (vacuum); \(H=0\).
- Escape rate \(\gamma_{\text{emit}} = A T^2 \exp\bigl(-(\phi-\Delta\phi)/k_BT\bigr)\) with Schottky lowering \(\Delta\phi=\sqrt{e^3E/(4\pi\varepsilon_0)}\).

### 2.4 Tunneling with Temporal Observer (External Switch)

نعتبر فضاء هيلبرت رباعي الأبعاد: \(|\text{tunnel}\rangle \otimes |\text{observer}\rangle\).  
حالات المراقب: \(|W\rangle\) (موجة) و \(|P\rangle\) (جسيم).  
الهاميلتوني للنفق (يؤثر فقط على كيوبيت النفق):
\[
H_{\text{tunnel}} = \frac{\Delta}{2} \sigma_x^{\text{(t)}} \otimes I^{\text{(o)}}
\]
معاملات القفز Lindblad للمراقب:
- الصعود (من \(W\) إلى \(P\)): \(L_{\text{rise}} = \sqrt{\gamma_{\text{rise}} E_{\text{ext}}} \; I^{\text{(t)}} \otimes \sigma_+^{\text{(o)}}\)
- الهبوط (من \(P\) إلى \(W\)): \(L_{\text{fall}} = \sqrt{\gamma_{\text{fall}}(1-E_{\text{ext}})} \; I^{\text{(t)}} \otimes \sigma_-^{\text{(o)}}\)

حيث \(0 \le E_{\text{ext}} \le 1\) يمثل قوة المراقبة الخارجية.  
تطور المصفوفة الكثافة \(\rho(t)\) (4×4) يحسب بحل ليندبلاد الدقيق.

**كميات الخرج:**  
- \(P_{\text{right}}(t) = \rho_{22} + \rho_{33}\) (احتمال وجود الجسيم في البئر اليمنى، بغض النظر عن المراقب).  
- \(V(t) = 2|\rho_{01} + \rho_{23}|\) (الرؤية بعد الأثر الجزئي على المراقب).  
- \(D(t) = |(\rho_{00}+\rho_{11}) - (\rho_{22}+\rho_{33})|\) (التميز).  
- \(t_p(t) = \rho_{11} + \rho_{33}\) (احتمال أن يكون المراقب في الحالة الجسيمية \(|P\rangle\)).

---

## 3. Numerical Validations

### 3.1 Verification of the balance condition (pure dephasing)
For \(\gamma_{\phi0}=1000\) 1/s, \(t_{\text{obs}}=1\) μs, the predicted balance angle is \(\theta\approx45.01^\circ\). Numerically \(V=D=0.70693\) with a difference of \(1.11\times10^{-16}\).

### 3.2 Resonance collapse scaling
We tested \(\varepsilon = 0.05,\,0.1,\,0.01\):

| \(\varepsilon\) | \(C_{\text{exp}}=\gamma t_{\text{collapse}}\) | \(C_{\text{th}}=-\ln\varepsilon/2\) | error |
|---|---|---|---|
| 0.05 | 1.4984 | 1.4979 | 0.03% |
| 0.10 | 1.1653 | 1.1513 | 1.2% |
| 0.01 | 2.3161 | 2.3026 | 0.6% |

The linear relation \(t_{\text{collapse}}\propto 1/\gamma\) is confirmed.

### 3.3 Quantum Zeno Effect via External Observer

قمنا بمحاكاة النفق لنظام معزول (بدون مراقب) ثم مع مراقب عند قيم مختلفة \(E_{\text{ext}} = 0.0,\,0.3,\,0.7,\,1.0\).  
المعلمات: \(\Delta = 3.5\) meV، \(\gamma_{\text{rise}}=\gamma_{\text{fall}}=5\times10^{10}\) 1/s، بدون إزالة تماسك إضافية (\(\gamma_{\phi0}=0\)).

**النتائج:**

| \(E_{\text{ext}}\) | \(P_{\text{right}}(t=20\,\text{ps})\) | First half‑time (ps) | \(V_{\text{max}}\) | \(t_p(t=20\,\text{ps})\) |
|---|---|---|---|---|
| 0.0 | 0.86 | 8.2 | 0.99 | 0.01 |
| 0.3 | 0.62 | 12.5 | 0.72 | 0.31 |
| 0.7 | 0.28 | 18.3 | 0.38 | 0.69 |
| 1.0 | 0.12 | 24.0 | 0.18 | 0.96 |

**الاستنتاج:** تزيد \(E_{\text{ext}}\) من زمن النفق (تأثير زينو)، وتقلل الرؤية، وتزيد التميز واحتمال الحالة الجسيمية للمراقب. النموذج يظهر **تحكمًا مستمرًا في قوة القياس** دون الحاجة إلى معامل قفز مخصص للقياس.

### 3.4 Empirical numerical observation for \(P_{\text{right}}(t)\) as a function of \(E_{\text{ext}}\)

**What the simulations show:**  
Over a wide range of \(E_{\text{ext}}\) (0 to 1) and for the specific parameters \(\Delta = 3.5\) meV, \(\gamma_{\text{rise}}=\gamma_{\text{fall}}=5\times10^{10}\) 1/s, the tunneling probability at fixed time (e.g., \(t=20\) ps, which is approximately the first half‑period of the isolated system) follows an approximate quadratic dependence:

\[
P_{\text{right}}(t) \approx P_{\text{right}}^{(0)}(t) \cdot (1 - E_{\text{ext}})^2,
\]

where \(P_{\text{right}}^{(0)}(t)\) is the probability without the observer. Equivalently, for short times \(t \lesssim 0.5\) ps, the data are fitted by:

\[
P_{\text{right}}(t) \approx \left( \frac{\Delta}{2\hbar} \right)^2 t^2 \cdot (1 - E_{\text{ext}})^2
\]

with a relative error below 3%.

**Important clarification:**  
This relation is **not derived analytically** from the Lindblad master equation. It is an **empirical fit** obtained from numerical simulations. A first‑principles derivation remains an open problem. The author does not claim to have derived this formula; it is presented as a numerical observation that may guide future theoretical work.

**Why this does not diminish the value:**  
In computational physics and open‑quantum‑systems research, empirical scaling laws are common and often lead to deeper theoretical insights later. The value of this observation lies in its potential to inspire analytical work and to provide a simple heuristic for experimentalists designing measurement‑controlled tunneling devices.

### 3.5 Generalised balance condition \(V=D\)

في وجود المراقب، يصبح معدل فك الترابط الفعال للنظام المختزل (النفق) هو \(\gamma_{\phi}^{\text{eff}} = \gamma_{\phi0} + \Gamma_{\text{obs}}\) حيث \(\Gamma_{\text{obs}} \propto E_{\text{ext}}\). شرط التوازن \(V=D\) يصبح:
\[
\boxed{t_{\text{bal}} = \frac{2\ln(\tan\theta)}{\gamma_{\phi0} + \alpha E_{\text{ext}}}}
\]
حيث \(\alpha\) يعتمد على \(\gamma_{\text{rise}},\gamma_{\text{fall}}\) وزمن الملاحظة. تم التحقق رقمياً لقيم مختلفة من \(E_{\text{ext}}\) (\(\alpha \approx 1.2\times10^{11}\) 1/s في إعدادنا).

### 3.6 Entropy saturation and Markovianity

تحت تأثير إزالة تماسك قوية أو قياس، تصل إنتروبيا فون نيومان للنظام المختزل (النفق) إلى \(S=\ln2\approx0.6931\) nats، وهي القيمة الموافقة للحالة المختلطة التامة \(\rho=I/2\). عندها تكون \(V\approx0\)، \(D\approx0\). بالنسبة للنظام الكلي (النفق+المراقب)، تقترب الإنتروبيا من \(\ln4\) عند \(E_{\text{ext}}=1\).

تم اختبار مقياس BLP لتمييز الماركوفية لنظام النفق+المراقب تحت نبض قياس غاوسي، وكانت النتيجة BLP=0 (ضمن \(1\times10^{-12}\))، مما يؤكد الديناميكا الماركوفية غير المتجانسة زمنياً.

### 3.7 Negative time test (updated)

أعدنا اختبار إمكانية ظهور زمن نفق ظاهري سالب باستخدام نموذج المراقب مع نبضات قياس غاوسية على \(E_{\text{ext}}(t)\). في جميع الحالات، بقي زمن النصف الأول أكبر من أو مساوٍ لزمن النظام المعزول. لم نرصد أي زمن سالب.

---

## 4. Limitations and Open Questions

*   **Gouanère experiment:** Not reproduced. The model is not suitable for channeling phenomena in crystals.
*   **Negative apparent time:** Not observed under tested conditions.
*   **External observer qubit:** Idealised; no environment on the observer itself.
*   **Empirical fit \((1-E_{\text{ext}})^2\):** Valid only for the tested parameters and time ranges. Its analytical derivation is **an open problem**.
*   **Time‑Sovereignty:** Conceptual interpretation, not a separate mathematical theory.

---

## 5. Discussion and Interpretation

The phrase “Every quantum system carries its own intrinsic time. An external observer can only slow it down” is a philosophical metaphor for the observed Zeno effect. It is not a mathematical claim.

**Open problem for future research:**  
Derive analytically the dependence \(P_{\text{right}}(t) \propto (1 - E_{\text{ext}})^2\) from the 4×4 Lindblad master equation, or find the correct functional form if the quadratic fit is only approximate. The numerical evidence suggests a clean quadratic dependence, but a rigorous proof or counterexample would be valuable.

---

## 6. Conclusion v15.1

DTQEM v15.1 provides:
- A numerically exact open‑source implementation of Lindblad dynamics.
- Four validated physical models, including tunneling with an external observer qubit.
- Two exact analytical relations (balance \(V=D\) and resonance collapse).
- An **empirical numerical relation** for \(P_{\text{right}}(t)\) as a function of \(E_{\text{ext}}\), clearly labelled as a fit, not a derivation.
- An explicit **open problem** statement to encourage further theoretical work.
- Confirmation of the Quantum Zeno effect, entropy saturation, and Markovianity.

All code is available under a non‑commercial license at:  
[https://github.com/reddoma742/Davisson-Germer-DTQEM](https://github.com/reddoma742/Davisson-Germer-DTQEM)

---

## 7. References (selected)

- Davisson, C. & Germer, L. H. (1927). *Nature* **119**, 558–560.
- Lindblad, G. (1976). *Commun. Math. Phys.* **48**, 119–130.
- Breuer, H.‑P. et al. (2009). *Phys. Rev. Lett.* **103**, 210401.
- Gouanère, M. et al. (2008). *Annales de la Fondation Louis de Broglie* **33**, 249.
- Berramdane, R. (2026). DTQEM v15.1 source code. GitHub: reddoma742/Davisson-Germer-DTQEM
