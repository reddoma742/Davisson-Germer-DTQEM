# DTQEM White Paper – v13.0 (May 2026)

## Dual‑Time Quantum Entanglement Model: From Electron Diffraction to Tunneling

**Authors:** Redouane Berramdane & DTQEM Team (Gemini, Claude, DeepSeek, Plecity)  
**DOI:** pending (previous DOI: 10.5281/zenodo.20043754)  
**License:** MIT

---

## Abstract (English)

This work presents an open‑source numerical framework for simulating open quantum systems under the **Time‑Sovereignty** hypothesis. Two validated applications are provided:

1. **Davisson–Germer experiment** – electron diffraction on a nickel crystal, where the visibility V and distinguishability D are computed from Lindblad master equation (two‑qubit dephasing).
2. **Quantum tunneling** – particle in a double well with thermal relaxation and pure dephasing, illustrating the transition from coherent tunneling to incoherent hopping.

All simulations use exact Liouvillian exponentiation (`expm`) reaching machine precision (errors < 1e‑12). Complementarity V² + D² ≤ 1 is always satisfied, and an analytical balance condition V = D is derived for pure dephasing.

---

## Abstract (العربية)

يقدم هذا العمل إطاراً رقمياً مفتوح المصدر لمحاكاة الأنظمة الكمومية المفتوحة في ضوء فرضية **سيادة الزمن**. يتضمن تطبيقين موثَّقين:

1. **تجربة دافيسون-جيرمر** – حيود الإلكترونات على بلورة نيكل، حيث يُحسب الوضوح V وقابلية التمييز D من معادلة ليندبلاد (كيوبتان، تبديد صرف).
2. **النفقية الكمومية** – جسيم في بئر مزدوج مع استرخاء حراري وتبديد صرف، مما يظهر الانتقال من النفقية المتماسكة إلى القفز غير المتماسك.

تعتمد المحاكاة على الأسي المصفوفي للمُشغِّل الليوفيلياني (`expm`) وتصل دقتها إلى حد الآلة (خطأ < 1e-12). علاقة التكاملية V² + D² ≤ 1 محققة دائماً، ويُشتق شرط توازن تحليلي V = D لحالة التبديد الصرف.

---

## 1. Introduction

The Time‑Sovereignty hypothesis states that a quantum system remains coherent as long as its internal clock dominates. Interaction with the environment (measurement, dephasing, thermal baths) imposes an external “camera clock”, driving the system toward classical behaviour. DTQEM implements this via the Lindblad master equation.

Two paradigmatic cases are simulated:
- **Davisson–Germer:** an electron scatters from a crystal, entangling its path with crystal modes.
- **Tunneling:** a particle in a double well tunnels between left and right.

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

### 2.4 Complementarity & Balance Condition

\[
V^2 + D^2 \le 1
\]

For pure dephasing only (\(\gamma_{\text{rel}}=0\), \(T=0\)):
\[
V(t) = \sin\theta\; e^{-\gamma_{\phi0} t/2},\quad D(t) = |\cos\theta|
\]
Setting \(V = D\) gives the exact analytical condition:
\[
\boxed{\gamma_{\phi0}\,t = 2\ln(\tan\theta)},\qquad \theta>45^\circ
\]

---

## 3. Numerical Implementation

- **Language:** Python 3.8+
- **Libraries:** NumPy, SciPy (expm), Matplotlib, ipywidgets
- **Structure:**
