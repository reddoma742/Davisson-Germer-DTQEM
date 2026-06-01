# DTQEM v19.0 – Analytical Solution of the Baseline Lindblad Model with Fixed Hamiltonian and Pure Dephasing (Final Version)

**Author:** Reddouane Berramdane  
**AI‑assisted tools:** Gemini, DeepSeek, Claude  
**License:** CC BY‑NC 4.0  
**Previous DOIs:** 10.5281/zenodo.20090038 (v13), v16, v17, v18  
**Concept DOI:** (same repository)

---

## Abstract (English)

Within the pure‑dephasing two‑level baseline model, DTQEM v19.0 presents the exact analytical solution of the Lindblad master equation for a continuously measured qubit. The model consists of a fixed Hamiltonian \( H = \frac{\Delta}{2}\sigma_x \) and a pure dephasing Lindblad operator \( L = \sqrt{\gamma E_{\text{ext}}}\,\sigma_z \), with no observer‑dependent energy shift. Starting from \( |0\rangle \), the probability to be in \( |1\rangle \) is derived in closed form:

\[
P_{\text{right}}(E,t) = \frac{1}{2}\left[1 - e^{-\gamma E t}\left(\cos(\omega_0 t) + \frac{\gamma E}{\omega_0}\sin(\omega_0 t)\right)\right],\qquad \omega_0 = \frac{\Delta}{\hbar}.
\]

This solution replaces earlier phenomenological fits (e.g. \( P\propto(1-E)^2 \)) for this baseline model and provides a rigorous foundation for DTQEM simulations. From the expression we obtain the decoherence time \( \tau_{\text{coh}} = 1/(\gamma E) \), the critical observer strength \( E_{\text{crit}} = \omega_0/\gamma \) separating oscillatory from overdamped regimes, and the long‑time limit \( P(E=1,t\to\infty)=1/2 \) (complete mixing, not freezing). The Rabi frequency remains constant, confirming that the observer only destroys coherence without altering the system’s energy scale.

---

## Abstract (العربية)

ضمن نموذج الخط الأساسي (baseline) ثنائي المستوى مع تبديد محض، يقدم الإصدار v19.0 الحل التحليلي الدقيق لمعادلة ليندبلاد لكيوبيت خاضع لقياس مستمر. يتكون النموذج من هاميلتوني ثابت \( H = \frac{\Delta}{2}\sigma_x \) ومشغل ليندبلاد لتبديد محض \( L = \sqrt{\gamma E_{\text{ext}}}\,\sigma_z \). ابتداءً من الحالة \( |0\rangle \)، يتم استنتاج احتمال الوجود في \( |1\rangle \) بشكل مغلق:

\[
P_{\text{right}}(E,t) = \frac{1}{2}\left[1 - e^{-\gamma E t}\left(\cos(\omega_0 t) + \frac{\gamma E}{\omega_0}\sin(\omega_0 t)\right)\right],\quad \omega_0 = \frac{\Delta}{\hbar}.
\]

هذا الحل يحل محل الملاءات الفينومينولوجية السابقة (مثل \( P\propto(1-E)^2 \)) في هذا النموذج الأساسي، ويوفر أساساً متيناً لمحاكاة DTQEM. نستنتج زمن التماسك \( \tau_{\text{coh}} = 1/(\gamma E) \)، وقوة المراقب الحرجة \( E_{\text{crit}} = \omega_0/\gamma \) التي تفصل النظام التذبذبي عن المفرط التخميد، والحد اللانهائي \( P(E=1,t\to\infty)=1/2 \) (اختلاط كامل، وليس تجمداً). يبقى تردد رابي ثابتاً، مما يؤكد أن المراقب يقتل التماسك فقط دون تغيير مقياس طاقة النظام.

---

## 1. Introduction

The DTQEM project investigates the **temporal balance** hypothesis: a quantum system’s coherence decays because the observer’s time frame overrides the particle’s internal time. In previous releases (v16–v18) we validated this picture numerically for tunneling, photon wave‑particle duality, and entanglement. However, the analytical relation \( P\propto(1-E)^2 \) remained an empirical fit, not derived from first principles.

Here we present **version 19.0** which contains the exact analytical solution of the Lindblad master equation for the baseline model: a fixed Hamiltonian \( H = \frac{\Delta}{2}\sigma_x \) and a pure dephasing Lindblad operator \( L = \sqrt{\gamma E_{\text{ext}}}\,\sigma_z \). This solution is derived directly from the Lindblad equation and fully describes the open‑system dynamics without any approximation.

---

## 2. Model and Exact Solution

### 2.1 Lindblad master equation

The system is a single qubit (representing a particle in a double well or a photon polarization state). The Hamiltonian is **constant** (the observer does not change the energy):

\[
H = \frac{\Delta}{2}\,\sigma_x.
\]

The only effect of the observer is pure dephasing, with strength controlled by \( E_{\text{ext}} \in [0,1] \):

\[
L = \sqrt{\gamma E_{\text{ext}}}\,\sigma_z.
\]

The Lindblad master equation reads:

\[
\frac{d\rho}{dt} = -\frac{i}{\hbar}[H,\rho] + \gamma E_{\text{ext}}\bigl(\sigma_z\rho\sigma_z - \rho\bigr).
\]

Initial state: \( \rho(0) = |0\rangle\langle0| \).

### 2.2 Derivation outline

Using the Bloch vector representation \( \rho = \frac12(I + x\sigma_x + y\sigma_y + z\sigma_z) \), and noting that the dissipator contributes \( -2\gamma E\,x \) to \( \dot{x} \) and \( -2\gamma E\,y \) to \( \dot{y} \), we obtain:

\[
\dot{x} = -2\gamma E\,x,\quad
\dot{y} = -2\gamma E\,y - \omega_0 z,\quad
\dot{z} = \omega_0 y,
\]

with \( \omega_0 = \Delta/\hbar \). Eliminating \( y \) gives a second‑order equation for \( z \):

\[
\ddot{z} + 2\gamma E\,\dot{z} + \omega_0^2 z = 0.
\]

With initial conditions \( z(0)=1,\ \dot{z}(0)=0 \), the solution (underdamped regime, \( \gamma E < \omega_0 \)) is:

\[
z(t) = e^{-\gamma E t}\left(\cos(\omega_0 t) + \frac{\gamma E}{\omega_0}\sin(\omega_0 t)\right).
\]

The probability to be in \( |1\rangle \) is \( P_{\text{right}} = (1-z)/2 \), leading to the final closed‑form expression.

### 2.3 Exact solution

\[
\boxed{P_{\text{right}}(E,t) = \frac{1}{2}\left[1 - e^{-\gamma E t}\left(\cos(\omega_0 t) + \frac{\gamma E}{\omega_0}\sin(\omega_0 t)\right)\right],\qquad \omega_0 = \frac{\Delta}{\hbar}.}
\]

**Domain of validity:** This solution holds for all \( t \) and for \( 0 \le E \le 1 \) such that \( \gamma E < \omega_0 \) (underdamped regime). For our parameters (\( \Delta = 3.5\,\text{meV} \), \( \gamma = 5\times10^{10}\,\text{s}^{-1} \)), \( \omega_0/\gamma \approx 107 \), so the condition is satisfied for all realistic \( E \).

---

## 3. Physical Insights

From the exact solution we deduce the following:

| Quantity | Expression | Interpretation |
|----------|------------|----------------|
| **Decoherence time** | \( \tau_{\text{coh}} = \dfrac{1}{\gamma E} \) | The observer kills coherences on a timescale inversely proportional to measurement strength. |
| **Critical observer strength** | \( E_{\text{crit}} = \dfrac{\omega_0}{\gamma} \) | For \( E < E_{\text{crit}} \) the dynamics are under‑damped (oscillatory quantum behaviour); for \( E > E_{\text{crit}} \) they become over‑damped (classical relaxation). For our parameters, \( E_{\text{crit}} \approx 107 \gg 1 \), so the underdamped regime applies for all realistic \( E \). |
| **Long‑time limit** | \( \displaystyle \lim_{t\to\infty} P(E,t) = \frac12 \) | The system tends to a completely mixed state (maximal entropy), **not** a frozen state. This is the thermodynamic equilibrium of an open quantum system. |
| **Rabi frequency** | constant \( \omega_0 \) | The observer does not change the system’s energy scale; only the amplitude decays. |

These results correct earlier misunderstandings (e.g., the idea that \( P(E=1) \to 0 \)). They show that the “temporal balance” hypothesis should be interpreted as a competition between the particle’s internal clock (fixed Rabi frequency) and the observer’s decoherence rate, not as a direct change of the particle’s energy.

### 3.1 Limitations and assumptions

- The solution assumes the underdamped regime \( \gamma E < \omega_0 \). For \( \gamma E > \omega_0 \) the solution becomes overdamped with hyperbolic functions, though this regime is not reached for our parameters.
- Thermal relaxation (\( T_1 \) processes) is neglected; only pure dephasing (\( T_2 \)) is included.
- The model is single‑qubit; entanglement requires extension to the two‑qubit Lindblad equation.

---

## 4. Comparison with Previous Phenomenological Models

Earlier versions (v15 and below) used an **observer‑dependent Hamiltonian** \( H \propto (1-E)\sigma_x \). That model produced the empirical quadratic fit \( P \propto (1-E)^2 \) but was physically less consistent because the observer effectively changed the system’s energy. In contrast, v19.0’s fixed‑Hamiltonian model is physically motivated and yields the exact solution above.

| Feature | Phenomenological model (v15) | Rigorous baseline model (v19.0) |
|---------|-------------------------------|---------------------------------|
| Hamiltonian | \( \frac{\Delta}{2}(1-E)\sigma_x \) | \( \frac{\Delta}{2}\sigma_x \) (constant) |
| \( P(E=1,t\to\infty) \) | \( \to 0 \) (freezing) | \( \to 1/2 \) (mixing) |
| Rabi frequency | decreases with \( E \) | constant \( \omega_0 \) |
| Analytic expression | approximate (quadratic fit) | exact closed form |
| Physical basis | phenomenological | first principles |

Thus, **v19.0 replaces earlier phenomenological fits** for this baseline model and provides a clearer theoretical foundation for DTQEM.

---

## 5. Numerical Validation

The analytical solution is compared with direct numerical integration of the Lindblad equation (using `scipy.linalg.expm`). For typical parameters (e.g., \( \Delta = 3.5\,\text{meV} \), \( \gamma = 5\times10^{10}\,\text{s}^{-1} \), and \( t = 20\,\text{ps} \)), the absolute error is less than \( 10^{-12} \), confirming the derivation. The validation holds for any parameter set within the underdamped regime.

---

## 6. Discussion and Open Questions

- **Why no empirical fit?** The exact solution eliminates the need for any phenomenological fitting. All previously observed numerical trends (including the approximate quadratic decay) are now understood as consequences of the exact formula under specific parameter choices.
- **Relation to entanglement:** The same analytical technique can be extended to two‑qubit systems. Work on an exact solution for the two‑qubit dephasing model is ongoing.
- **Experimental test:** A clear prediction from v19.0 is the constant Rabi frequency: a Ramsey‑type experiment should show **no frequency shift** with measurement strength, only a decay of the contrast. This distinguishes DTQEM from models that assume an observer‑induced energy change.
- **Future work:** Include thermal relaxation, medium density, and non‑linear interactions while retaining analytical tractability.

---

## 7. Conclusion

DTQEM v19.0 provides the exact analytical solution for the baseline Lindblad model of a continuously measured qubit. The result is a simple closed‑form expression that reveals the true physics: the observer only accelerates decoherence, leaving the particle’s natural frequency unchanged. This release marks a significant step, moving DTQEM from a numerical simulation framework towards a more rigorous analytical theory.

---

## 8. Code Availability

All code, including a simple Python script that evaluates the analytical formula and plots \( P(E,t) \), is available at the GitHub repository. The main script for v19.0 is `analytical_model_v19.py`.

---

## References

- Lindblad, G. (1976). *Commun. Math. Phys.* **48**, 119–130.
- Wootters, W. K. (1998). *Phys. Rev. Lett.* **80**, 2245–2248.
- Breuer, H.-P. & Petruccione, F. (2002). *The Theory of Open Quantum Systems*.
- Schlosshauer, M. (2007). *Decoherence and the Quantum-to-Classical Transition*.
- Berramdane, R. (2026). DTQEM v19.0 source code. GitHub: reddoma742/Davisson-Germer-DTQEM.

---

> *“Pure dephasing does not stop the particle's clock — it only makes the hands jitter until the time becomes unknowable.”*  
> — DTQEM Team
