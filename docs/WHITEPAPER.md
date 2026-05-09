# DTQEM White Paper – v13.0 (May 2026)

## Dual‑Time Quantum Entanglement Model: From Electron Diffraction to Tunneling & Schottky Effect

**Authors:** Redouane Berramdane & DTQEM Team (Gemini, Claude, DeepSeek, Plecity)  
**DOI:** pending (previous DOI: 10.5281/zenodo.20043754)  
**License:** MIT (with non‑commercial recommendation)

---

## Abstract (English)

This work presents an open‑source numerical framework for simulating open quantum systems under the **Time‑Sovereignty** hypothesis. Three validated applications are provided:

1. **Davisson–Germer experiment** – electron diffraction on a nickel crystal, where visibility V and distinguishability D are computed from the Lindblad master equation (two‑qubit dephasing).
2. **Quantum tunneling** – particle in a double well with thermal relaxation and pure dephasing, illustrating the transition from coherent tunneling to incoherent hopping.
3. **Schottky effect** – field‑enhanced thermionic emission from a metal into vacuum, using a two‑level system with a Richardson‑Dushman escape rate.

All simulations use exact Liouvillian exponentiation (`expm`), achieving machine precision (errors < 1e‑12). Complementarity V² + D² ≤ 1 is always satisfied. An exact analytical balance condition `V = D` is derived for pure dephasing:

\[
\boxed{\gamma_{\phi0}\,t_{\text{obs}} = 2\ln(\tan\theta)},\qquad \theta>45^\circ
\]

This equation corrects the earlier misconception of a fixed “magic angle” and provides a design tool for experiments. Exploratory codes for apparent negative tunneling times and observer‑frequency effects are also included (hypothetical, not yet validated).

---

## Abstract (العربية)

يقدم هذا العمل إطاراً رقمياً مفتوح المصدر لمحاكاة الأنظمة الكمومية المفتوحة تحت فرضية **سيادة الزمن**. يتضمن ثلاثة تطبيقات موثَّقة:

1. **تجربة دافيسون-جيرمر** – حيود الإلكترونات على بلورة نيكل، مع حساب الوضوح V وقابلية التمييز D عبر معادلة ليندبلاد (كيوبتان، تبديد صرف).
2. **النفقية الكمومية** – جسيم في بئر مزدوج مع استرخاء حراري وتبديد صرف، يظهر الانتقال من النفقية المتماسكة إلى القفز غير المتماسك.
3. **تأثير شوتكي** – انبعاث حراري معزز بالمجال من معدن إلى الفراغ، كنظام مستويين مع معدل هروب ريتشاردسون-دوشمان.

تعتمد المحاكاة على الأسي المصفوفي للمُشغِّل الليوفيلياني (`expm`) بدقة آلية (خطأ < 1e-12). علاقة التكاملية V² + D² ≤ 1 محققة دائماً. تم اشتقاق شرط توازن تحليلي دقيق لـ `V = D` في حالة التبديد الصرف:

\[
\boxed{\gamma_{\phi0}\,t_{\text{obs}} = 2\ln(\tan\theta)},\qquad \theta>45^\circ
\]

هذه المعادلة تصحح الفكرة الخاطئة عن "زاوية سحرية" ثابتة وتقدّم أداة لتصميم التجارب. كما نضمّن أكواداً استكشافية للظواهر الافتراضية (الزمن السلبي، ترددات المراقب) مع إخلاء مسؤولية واضح.

---

## 1. Introduction

The Time‑Sovereignty hypothesis states that a quantum system remains coherent as long as its internal clock dominates. Interaction with the environment (measurement, dephasing, thermal baths) imposes an external “camera clock”, driving the system toward classical behaviour. DTQEM implements this via the Lindblad master equation.

Three paradigmatic cases are simulated:
- **Davisson–Germer:** an electron scatters from a crystal, entangling its path with crystal modes.
- **Tunneling:** a particle in a double well tunnels between left and right.
- **Schottky effect:** an electron escapes from a metal under the combined action of heat and electric field.

Additionally, we present an **exact analytical balance condition** `V = D` for pure dephasing, which provides a quantitative answer to the question “when does a quantum system behave equally as wave and particle?”. This condition is derived in Section 2.4 and verified numerically in the accompanying code.

---

## 2. Core Physics & Mathematical Framework

### 2.1 Lindblad Master Equation

\[
\frac{d\rho}{dt} = -i[H,\rho] + \sum_k \left( L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k,\rho\} \right)
\]

Solved via Liouvillian superoperator exponentiation:  
\[
\vec{\rho}(t) = \exp(\mathcal{L} t) \,\vec{\rho}(0),\qquad \mathcal{L} = -i(H\otimes I - I\otimes H^T) + \sum_k \left( L_k\otimes L_k^* - \frac12 (L_k^\dagger L_k\otimes I + I\otimes (L_k^\dagger L_k)^T ) \right)
\]

### 2.2 Davisson–Germer (Two‑qubit)

- Qubit A: electron path (|0⟩ reflected, |1⟩ diffracted)
- Qubit B: crystal mode (|0⟩ ground, |1⟩ excited)
- Hamiltonian: \(H = 0\) (no internal evolution)
- Jump operator: \(L = \sqrt{\gamma_{\phi0}}\; \sigma_z \otimes I\) (pure dephasing)
- Initial entangled state:  
  \[
  |\psi(\theta)\rangle = \cos\frac{\theta}{2}|00\rangle + \sin\frac{\theta}{2}|11\rangle,\qquad \theta = 180^\circ - 2\phi_{\text{Bragg}}
  \]
- Visibility: \(V = 2|\rho_{03}|\), Distinguishability: \(D = |\rho_{00} - \rho_{33}|\)

### 2.3 Quantum Tunneling (Single qubit)

- Hamiltonian: \(H = \frac{\Delta}{2} \sigma_x\) (Δ = tunnel splitting)
- Jump operators:
  - Dephasing: \(L_\phi = \sqrt{\gamma_{\phi}(T)}\;\sigma_z\) with \(\gamma_{\phi}(T) = \frac{\gamma_{\phi0}}{2}(2n_{\text{th}}+1)\)
  - Relaxation: \(L_- = \sqrt{\gamma_{\text{rel}}(n_{\text{th}}+1)}\;\sigma_-,\; L_+ = \sqrt{\gamma_{\text{rel}} n_{\text{th}}}\;\sigma_+\)
- Thermal occupation: \(n_{\text{th}} = 1/(\exp(\Delta/k_B T)-1)\)
- Start from left well: \(\rho_0 = |0\rangle\langle0|\), compute \(P_{\text{right}}(t) = \rho_{11}(t)\), \(V(t)=2|\rho_{01}|\), \(D(t)=|\rho_{00}-\rho_{11}|\)

### 2.4 Schottky Effect (Two‑level system)

- States: |M⟩ (electron in metal), |V⟩ (electron in vacuum)
- Hamiltonian: \(H = 0\) (no coherent coupling)
- Lindblad jump operator: \(L_{\text{emit}} = \sqrt{\gamma_{\text{emit}}}\; |V\rangle\langle M|\)
- Escape rate follows Richardson‑Dushman with Schottky barrier lowering:
  \[
  \gamma_{\text{emit}} = A \, T^2 \exp\!\left(-\frac{\phi - \Delta\phi}{k_B T}\right),\quad \Delta\phi = \sqrt{\frac{e^3 E}{4\pi\varepsilon_0}}
  \]
- Emission probability \(P_v(t) = 1 - e^{-\gamma_{\text{emit}} t}\) (for low occupation).

### 2.5 Complementarity & Exact Balance Condition for Pure Dephasing

For pure dephasing only (\(\gamma_{\text{rel}}=0\), \(T=0\), \(B=0\)), the entangled state evolves as:

\[
\rho_{03}(t) = \frac{1}{2}\sin\theta\;\exp\!\left(-\frac{\gamma_{\phi0}}{2}t\right)
\]

Thus:
\[
V = 2|\rho_{03}| = \sin\theta\; e^{-\gamma_{\phi0} t/2},\qquad D = |\rho_{00} - \rho_{33}| = |\cos\theta|
\]

Setting \(V = D\) gives:

\[
\sin\theta\; e^{-\gamma_{\phi0} t/2} = \cos\theta \quad\Rightarrow\quad e^{-\gamma_{\phi0} t/2} = \cot\theta \quad\Rightarrow\quad \frac{\gamma_{\phi0}}{2}t = \ln(\tan\theta)
\]

Therefore, the exact analytical condition for wave‑particle balance is:

\[
\boxed{\gamma_{\phi0}\,t = 2\ln(\tan\theta)},\qquad \theta>45^\circ
\]

**Key implications:**
- The control parameter is the product \(\gamma_{\phi0} t\) (the total dephasing dose), not \(\gamma_{\phi0}\) alone.
- For \(\theta = 90^\circ\) (maximally entangled initial state), \(\tan 90^\circ \to \infty\) → the balance can only be approached asymptotically (requires infinite dephasing or infinite time).
- The previously observed “magic angle” around 65° was an artifact of fixing \(t_{\text{obs}}\); changing \(t_{\text{obs}}\) shifts the balance angle according to \(\ln(\tan\theta)\).

**Note on code convention:** In DTQEM, the user‑supplied \(\gamma_{\phi0}\) is related to the physical dephasing rate by \(\gamma_{\text{phys}} = \gamma_{\phi0}/2\). The formula above uses the code convention. If one prefers the physical rate, the equation becomes \(\gamma_{\text{phys}} t = \ln(\tan\theta)\).

---

## 3. Numerical Implementation

- **Language:** Python 3.8+
- **Libraries:** NumPy, SciPy (expm), Matplotlib, ipywidgets, pandas
- **Structure:**
