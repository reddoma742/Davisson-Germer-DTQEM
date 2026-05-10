# DTQEM White Paper – v14.0 (May 2026)

## Dual‑Time Quantum Entanglement Model: From Pure Dephasing to Resonance Collapse and Zeno Effect

**Authors:** Reddouane Berramdane & DTQEM Team (Gemini, Claude, DeepSeek, Plecity)  
**DOI:** this version (to be assigned on Zenodo)  
**Previous DOI:** 10.5281/zenodo.20090038 (v13.0)  
**License:** DTQEM Research & Educational License (non‑commercial, academic use free)

---

## Abstract (English)

This work presents an open‑source numerical framework for simulating open quantum systems under the **Time‑Sovereignty** hypothesis. The model is based on the Lindblad master equation, solved via exact Liouvillian exponentiation (`expm`) with machine precision (errors `< 1e‑12`).

**Three validated building blocks** are provided:
1. **Davisson–Germer experiment** – electron diffraction on a crystal (two‑qubit dephasing).
2. **Quantum tunneling** – particle in a double well with pure dephasing, thermal relaxation, and measurement.
3. **Schottky effect** – field‑enhanced thermionic emission (two‑level system).

**New analytical results from pure dephasing dynamics:**
- Exact wave‑particle balance condition:  
  \(\boxed{\gamma_{\phi0}\,t_{\text{obs}} = 2\ln(\tan\theta)},\qquad \theta>45^\circ\).
- Resonance collapse from the maximally coherent state \(|+\rangle\):  
  \(\boxed{t_{\text{collapse}} = -\frac{\ln\varepsilon}{2\gamma}}\) or \(\gamma\,t_{\text{collapse}} = -\frac{\ln\varepsilon}{2}\).

**Numerical validations:**  
- Quantum Zeno effect: tuning \(\Gamma_{\text{meas}}\) increases the tunneling time by a factor up to 9.  
- Entropy saturation at \(S=\ln2\) (maximally mixed state).  
- Markovianity test (BLP measure) yields BLP = 0 → time‑inhomogeneous Markovian dynamics.  
- No “negative apparent time” was found under Gaussian measurement pulses.  
- The model does **not** reproduce the Gouanère silicon‑channeling resonance (80.874 MeV), defining its clear domain of validity.

All codes, interactive GUIs, and documentation are open source, available under a non‑commercial academic license.

---

## Abstract (العربية)

يقدم هذا العمل إطاراً رقمياً مفتوح المصدر لمحاكاة الأنظمة الكمومية المفتوحة تحت فرضية **سيادة الزمن**، عبر معادلة ليندبلاد المُحلولة بالدقة الآلية. يقدّم النموذج:

- ثلاث وحدات قاعدة (دافيسون-جيرمر، النفقية، شوتكي).  
- علاقتين تحليليتين جديدتين: التوازن \(V=D\) وانهيار الرنين \(t_{\text{collapse}} = -\ln\varepsilon/(2\gamma)\).  
- التحقق العددي من تأثير زينو، ثبات الإنتروبيا عند \(\ln2\)، وكون النموذج ماركوفياً (BLP = 0).  
- بيان حدوده: عدم إعادة إنتاج تجربة غونييه، وغياب الزمن الظاهري السالب تحت نبضات غاوسية.  

الكود مفتوح المصدر، مع ترخيص أكاديمي غير تجاري.

---

## 1. Introduction

The Time‑Sovereignty hypothesis states that a quantum system remains coherent as long as its internal clock dominates. Interaction with the environment imposes an external “camera clock” that drives the system toward classical behaviour. DTQEM implements this via the Lindblad master equation.

This document summarises the core results obtained up to v14.0. The emphasis is placed on **analytical predictions** that are numerically verified and experimentally testable.

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

### 2.4 Exact analytical results for pure dephasing

**Balance condition \(V=D\):**  
For \(\gamma_{\text{rel}}=0\), \(T=0\), the initial entangled state evolves as \(\rho_{03}(t)=\frac12\sin\theta\,e^{-\gamma_{\phi0}t/2}\). Hence  
\[
V = \sin\theta\,e^{-\gamma_{\phi0}t/2},\qquad D = |\cos\theta|.
\]  
Setting \(V=D\) gives  
\[
\boxed{\gamma_{\phi0}\,t = 2\ln(\tan\theta)},\qquad \theta>45^\circ.
\]

**Resonance collapse from \(|+\rangle\):**  
Start from \(|+\rangle = (|0\rangle+|1\rangle)/\sqrt{2}\). Under pure dephasing (\(\gamma\)), \(V(t)=e^{-2\gamma t}\). The time to reach a threshold \(\varepsilon\) is  
\[
\boxed{t_{\text{collapse}} = \frac{-\ln\varepsilon}{2\gamma},\qquad\text{or}\qquad \gamma\,t_{\text{collapse}} = -\frac{\ln\varepsilon}{2}.}
\]

---

## 3. Numerical Validations

### 3.1 Verification of the balance condition
For \(\gamma_{\phi0}=1000\) 1/s, \(t_{\text{obs}}=1\) μs, the predicted balance angle is \(\theta\approx45.01^\circ\). Numerically \(V=D=0.70693\) with a difference of \(1.11\times10^{-16}\).

### 3.2 Resonance collapse scaling
We tested \(\varepsilon = 0.05,\,0.1,\,0.01\):

| \(\varepsilon\) | \(C_{\text{exp}}=\gamma t_{\text{collapse}}\) | \(C_{\text{th}}=-\ln\varepsilon/2\) | error |
|---|---|---|---|
| 0.05 | 1.4984 | 1.4979 | 0.03% |
| 0.10 | 1.1653 | 1.1513 | 1.2% |
| 0.01 | 2.3161 | 2.3026 | 0.6% |

The linear relation \(t_{\text{collapse}}\propto 1/\gamma\) is confirmed.

### 3.3 Quantum Zeno effect
Adding a measurement jump operator \(L_{\text{meas}}=\sqrt{\Gamma_{\text{meas}}}\,|0\rangle\langle0|\) increases the first tunneling time. Example: \(\Delta=3.5\) meV, isolated \(\tau=0.30\) ps; at \(\Gamma_{\text{meas}}\approx 8.5\times10^{12}\) 1/s, \(\tau\approx 2.77\) ps (factor ≈9).

### 3.4 Entropy saturation at \(\ln2\)
Under strong dephasing or measurement, the von Neumann entropy reaches \(S=\ln2\approx0.6931\) nats, corresponding to the maximally mixed state \(\rho=I/2\). At this point \(V\approx0\), \(D\approx0\).

### 3.5 Markovianity test (BLP measure)
We computed the Breuer‑Laine‑Piilo distinguishability measure for two initial states (\(|0\rangle\) and \(|+\rangle\)) under a Gaussian measurement pulse. Result: BLP = 0 (within \(1\times10^{-12}\)), confirming time‑inhomogeneous Markovian dynamics.

### 3.6 Apparent negative time? (Test)
We modified the scheme to search for a “negative apparent tunneling time” (\(t_{\text{half}} < \tau_{\text{isolated}}\)). Under Gaussian measurement pulses with amplitudes from \(10^{11}\) 1/s to \(5\times10^{13}\) 1/s, we observed \(t_{\text{half}} \ge \tau_{\text{isolated}}\) for all cases. At the highest amplitudes a tiny Zeno delay appears (\(0.276\) ps vs. \(0.275\) ps). No negative time was found.

---

## 4. Limitations and Domain of Validity

### 4.1 Attempt to simulate the Gouanère experiment (2008)
We modelled the silicon‑channeling resonance at 80.874 MeV using a two‑level picture with pure dephasing and \(\gamma_{\phi0}\) set to twice the de Broglie frequency. The simulation **did not produce any transmission dip** (depth ≈0%). This failure shows that the present DTQEM version (designed for two‑level systems with pure dephasing) cannot capture the detailed channeling dynamics of high‑energy electrons in a crystal lattice. The model remains valid for double‑well tunneling, two‑path interference, and emission‑type processes.

### 4.2 No “negative apparent time” within tested parameters
As reported in §3.6, the model did not produce an apparent tunneling time shorter than the isolated one. Therefore, any claim about “negative time” should not be attributed to DTQEM without a different implementation (e.g., a different measurement operator or a continuous‑space potential barrier).

### 4.3 Time‑Sovereignty as a conceptual framework
The philosophical interpretation in terms of an “internal clock” competing with an external environment is not a mathematically separate theory; it is a **retrospective interpretation** of the Lindblad dynamics already coded. The model does not add new physical mechanisms beyond those of a time‑inhomogeneous Markovian master equation.

---

## 5. Conclusion

DTQEM v14.0 provides:
- A numerically exact, open‑source implementation of Lindblad dynamics with machine precision.
- Two exact analytical relations governing wave‑particle transition and coherence collapse under pure dephasing.
- Successful simulation of the quantum Zeno effect, entropy saturation at \(\ln2\), and Markovianity (BLP = 0).
- A clear statement of its limits: it does not reproduce the Gouanère resonance, nor does it show “negative apparent time” under the tested measurement pulses.

All code, documentation, and interactive examples are freely available under a non‑commercial license.

---

## 6. References (selected)

- Davisson, C. & Germer, L. H. (1927). *Nature* **119**, 558–560.
- Lindblad, G. (1976). *Commun. Math. Phys.* **48**, 119–130.
- Breuer, H.‑P. et al. (2009). *Phys. Rev. Lett.* **103**, 210401.
- Gouanère, M. et al. (2008). *Annales de la Fondation Louis de Broglie* **33**, 249.
- Berramdane, R. (2026). DTQEM v13.0. Zenodo. DOI: 10.5281/zenodo.20090038

---

**“Every quantum system carries its own intrinsic time.”**
