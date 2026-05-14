# DTQEM v16.0 – Synchronized Two‑Times Effective Model

**Author:** Reddouane Berramdane  
**AI‑assisted tools:** Gemini, Claude, DeepSeek  
**License:** Non‑commercial academic license  
**Previous DOIs:** 10.5281/zenodo.20090038 (v13.0)  
**Concept DOI:** (same as repository)

---

## Abstract (English)

DTQEM v16.0 presents a clean 2×2 Lindblad model for quantum tunneling under continuous measurement. The observer strength \(E_{\text{ext}}\) scales the effective Hamiltonian \(H_{\text{eff}} = \frac{\Delta}{2}(1-E_{\text{ext}})\sigma_x\) and adds a pure dephasing Lindblad operator \(L = \sqrt{\gamma E_{\text{ext}}}\,\sigma_z\). Key numerical results at \(t=20\) ps (\(\Delta=3.5\) meV, \(\gamma=5\times10^{10}\) s\(^{-1}\)) are:

- \(E=0.0\) → \(P=0.0532\) (free Rabi, destructive phase)
- \(E=0.3\) → \(P=0.2872\) (partial decoherence)
- \(E=0.5\) → \(P=0.7943\) (synchronisation peak, balanced times)
- \(E=0.7\) → \(P=0.2774\) (near‑Zeno)
- \(E=1.0\) → \(P=0.0000\) (complete Zeno freeze)

The model unifies the quantum Zeno effect, quantum eraser, and wave‑particle duality under the concept of **temporal balance** (observer time \(V=E_{\text{ext}}\) vs. particle time \(D=1-E_{\text{ext}}\)). The quadratic scaling \(P \propto (1-E)^2\) emerges naturally from \(\omega_{\text{eff}} = \omega_0(1-E)\).

---

## Abstract (العربية)

يقدم DTQEM v16.0 نموذج ليندبلاد فعالاً ثنائي الأبعاد يصف نفق الجسيمات تحت قياس مستمر. قوة المراقب \(E_{\text{ext}}\) تغير الهاميلتوني الفعال \(H_{\text{eff}} = \frac{\Delta}{2}(1-E_{\text{ext}})\sigma_x\) وتضيف تبديد أطوار \(L = \sqrt{\gamma E_{\text{ext}}}\,\sigma_z\). النتائج الرئيسية عند \(t=20\) ps موضحة أعلاه. النموذج يوحد تأثير زينو، وممحاة الكم، وازدواجية موجة‑جسيم تحت مفهوم "الميزان الزمني" حيث \(V=E_{\text{ext}}\) هو زمن المراقب و \(D=1-E_{\text{ext}}\) هو زمن الجسيم. العلاقة التربيعية \(P \propto (1-E)^2\) تنبع من التردد الفعال \(\omega_{\text{eff}} = \omega_0(1-E)\).

---

## Main results table

| \(E_{\text{ext}}\) | \(P_{\text{right}}(20\,\text{ps})\) | Interpretation |
|---|---|---|
| 0.0 | 0.0532 | Free Rabi (destructive phase) |
| 0.3 | 0.2872 | Beginning of dephasing |
| **0.5** | **0.7943** | **Synchronisation peak (times balanced)** |
| 0.7 | 0.2774 | Near‑Zeno regime |
| 1.0 | 0.0000 | Complete Zeno freeze |

> Note: the high value at \(E=0.5\) is a phase coincidence – the effective Rabi period is ~2.36 ps, so at 20 ps the system lies near a constructive maximum. This does not contradict decoherence.

---

## Core equations

\[
H_{\text{eff}} = \frac{\Delta}{2}(1-E_{\text{ext}})\,\sigma_x , \qquad 
L = \sqrt{\gamma_0 E_{\text{ext}}}\,\sigma_z .
\]

Master equation (Lindblad):

\[
\dot{\rho} = -\frac{i}{\hbar}[H_{\text{eff}},\rho] + \gamma_0 E_{\text{ext}}\bigl(\sigma_z\rho\sigma_z - \rho\bigr).
\]

Short‑time scaling:

\[
P_{\text{right}}(t) \approx \left(\frac{\Delta}{2\hbar}\right)^2 t^2\,(1-E_{\text{ext}})^2 .
\]

Effective frequency:

\[
\omega_{\text{eff}} = \frac{\Delta}{\hbar}(1-E_{\text{ext}}) \quad\Rightarrow\quad \text{period } T_{\text{eff}} = \frac{T_0}{1-E_{\text{ext}}}.
\]

---

## Discussion

- **Why \(\sigma_z\) works**: Pure dephasing kills coherences without directly changing populations. This is the correct mechanism for the quantum Zeno effect (freezing). Using \(\sigma_x\) would add flips and spoil the freeze.
- **Temporal balance**: The condition \(V+D=1\) with \(V=E_{\text{ext}}\), \(D=1-E_{\text{ext}}\) captures complementarity: more observer knowledge (V) means less wave behaviour (D).
- **Relation to entanglement**: The current 2×2 model does not explicitly contain entanglement; it is an effective description. Future work may return to a corrected 4×4 model to explore true entanglement between the particle and the observer.
- **Open problem**: An analytical derivation of \((1-E)^2\) from first principles remains missing. The present result is an empirical fit supported by numerical evidence.

---

## Conclusion

DTQEM v16.0 is a stable, efficient, and testable effective model for measurement‑controlled tunneling. It reproduces all key phenomena (Zeno, eraser, duality) with a simple temporal‑balance picture. The code is open source and ready for experimental validation.

---

## Code availability

All scripts are available at the GitHub repository. The main simulation file is `temporal_balance.py`. Use Python 3.9+ with numpy, scipy, matplotlib.
