# DTQEM v18.0 – Entanglement under Local Dephasing: Concurrence and Inferred Bell Violation

**Author:** Reddouane Berramdane  
**AI‑assisted tools:** Gemini, DeepSeek, Claude  
**License:** CC BY‑NC 4.0  
**Previous DOIs:** 10.5281/zenodo.20090038 (v13), v16, v17  
**Concept DOI:** (same repository)

---

## Abstract (English)

DTQEM v18.0 simulates the decay of bipartite entanglement under continuous local dephasing. Starting from the Bell state \(|\Phi^+\rangle = (|00\rangle+|11\rangle)/\sqrt{2}\), we apply a Lindblad operator \(L = \sqrt{\gamma_0 E_{\mathrm{ext}}}\,(\sigma_z\otimes I)\) on the first qubit (Alice). Concurrence \(C(t)\) is computed numerically. Using the analytical relation \(S(t)=2\sqrt{2}\,C(t)\), we infer the CHSH parameter and show that Bell inequality violation persists as long as \(C(t) > 1/\sqrt{2}\). The measurement strength \(E_{\mathrm{ext}}\) controls the dephasing rate, demonstrating a clear Zeno‑like suppression of entanglement. This release provides a minimal, stable, and analytically interpretable model for measurement‑induced entanglement decay.

---

## Abstract (العربية)

يقدم الإصدار v18.0 محاكاة لاضمحلال التشابك الثنائي تحت تأثير تبديد محلي مستمر. نبدأ من حالة Bell \(|\Phi^+\rangle\) ونطبق مشغل ليندبلاد \(L = \sqrt{\gamma_0 E_{\mathrm{ext}}}\,(\sigma_z\otimes I)\) على الكيوبت الأول (أليس). نحسب Concurrence \(C(t)\) عددياً، ثم نستخدم العلاقة التحليلية \(S(t)=2\sqrt{2}\,C(t)\) لاستنتاج معامل CHSH. يظل النظام منتهكاً لمتراجحة بيل طالما \(C(t) > 1/\sqrt{2}\). تتحكم قوة المراقب \(E_{\mathrm{ext}}\) في معدل التبديد، مما يظهر تأثير زينو على التشابك.

---

## Core equations

**Initial state**:  
\(|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle+|11\rangle)\)

**Lindblad operator** (local dephasing on qubit A):  
\(L = \sqrt{\gamma_0 E_{\mathrm{ext}}}\,(\sigma_z\otimes I)\)

**Master equation** (no Hamiltonian):  
\(\dot{\rho} = \gamma_0 E_{\mathrm{ext}}\bigl((\sigma_z\otimes I)\,\rho\,(\sigma_z\otimes I) - \rho\bigr)\)

**Concurrence** (Wootters 1998):  
\(C(\rho) = \max(0, \lambda_1-\lambda_2-\lambda_3-\lambda_4)\) where \(\lambda_i\) are square roots of eigenvalues of \(\rho(\sigma_y\otimes\sigma_y)\rho^*(\sigma_y\otimes\sigma_y)\).

**Inferred CHSH parameter**:  
\(S(t) = 2\sqrt{2}\;C(t)\)

---

## Numerical results (γ₀=5e10 rad/s, E_ext=0.5)

| t (ps) | Concurrence C(t) | Inferred CHSH S(t) | Bell violation? |
|--------|------------------|--------------------|------------------|
| 0      | 1.0000           | 2.8284             | Yes (S>2)       |
| 20     | ~0.60            | ~1.70              | No (S<2)        |
| 40     | ~0.36            | ~1.02              | No              |
| 60     | ~0.22            | ~0.62              | No              |
| 100    | ~0.08            | ~0.23              | No              |

**Interpretation**: The observer (dephasing) destroys entanglement and non‑locality on a timescale ~1/(γ₀E_ext). This is a manifestation of the quantum Zeno effect on correlations.

---

## Discussion and open questions

- **Why concurrence only?** Concurrence suffices to quantify entanglement. CHSH is inferred analytically, avoiding numerical optimisation of measurement angles.
- **Relation to v16/v17**: v18 extends the framework to two‑qubit systems, while v16 (tunnelling) and v17 (photon) address single‑qubit wave‑particle duality.
- **Future work**: Include dephasing on both qubits, study different Bell states, and explore higher‑dimensional systems.

---

## Conclusion

DTQEM v18.0 provides a clean, numerically stable simulation of entanglement decay under local measurement. It demonstrates how a continuous observer (parameter \(E_{\mathrm{ext}}\)) suppresses quantum correlations in a predictable way, consistent with the “temporal balance” hypothesis.

---

## Code availability

All source code is available at the GitHub repository. The main script for v18.0 is `concurrence_entanglement.py`.
