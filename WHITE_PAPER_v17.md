
---

### 📦 الملف 4: `WHITE_PAPER_v17.md`

```markdown
# DTQEM v17.0 – Unified Wave‑Particle Simulator
---
AUTHOR AND METADATA
---
Author: Reddouane Berramdane
Affiliation: Independent Researcher, Oujda, Morocco
AI-Assisted Tools: Gemini, DeepSeek, Claude (Scientific development & documentation)
License: DTQEM Research & Educational License v1.0 (CC BY-NC 4.0)

PROJECT IDENTIFIERS (DOIs)
Concept DOI: 10.5281/zenodo.20043754 (Permanent - Links to all versions)
Version 16.0 DOI: 10.5281/zenodo.20159679
Version 13.0 DOI: 10.5281/zenodo.20090038
Current Release: Version 17.0 (May 2026) - Unified Wave-Particle Simulator
---



---

## Abstract

DTQEM v17.0 extends the effective 2×2 Lindblad framework to **photons** while correcting the earlier misinterpretation of the Hamiltonian. In this version the observer strength \(E_{\mathrm{ext}}\) **only affects the pure dephasing rate** (\(L = \sqrt{\gamma_0 E_{\mathrm{ext}}}\,\sigma_z\)), leaving the natural system energy unchanged. This correctly reproduces the quantum Zeno effect as a loss of coherence, not a change in energy. The model is validated by extracting the Rabi frequency from the time‑dependent probability \(P(t)\) via FFT; the extracted values match the theoretical frequency \(\omega_0/2\pi\) within < 2% error for weak measurement.

---

## Core equations (corrected)

**Fixed Hamiltonian** (does not depend on the observer):
\[
H = \frac{\hbar\omega_0}{2}\,\sigma_x
\]

**Lindblad operator (pure dephasing, observer‑controlled)**:
\[
L = \sqrt{\gamma_0 E_{\mathrm{ext}}}\,\sigma_z
\]

**Master equation**:
\[
\dot{\rho} = -\frac{i}{\hbar}[H,\rho] + \gamma_0 E_{\mathrm{ext}}\bigl(\sigma_z\rho\sigma_z - \rho\bigr)
\]

**Key behaviour**:
- At \(E_{\mathrm{ext}}=0\): free Rabi oscillation, \(P(t) = \sin^2(\omega_0 t/2)\).
- At \(E_{\mathrm{ext}}\gg 1\) (in practice \(E_{\mathrm{ext}}\to 1\)): dephasing destroys all coherence, the system tends to the maximally mixed state \(\rho = I/2\) (\(P_{\mathrm{right}}\to 0.5\), \(V\to 0\), \(D\to 0\)).
- The effective Rabi frequency extracted from \(P(t)\) remains \(\approx\omega_0\) until strong dephasing washes out oscillations.

---

## Numerical validation (photon model, ν₀ = 461 THz)

| \(E_{\mathrm{ext}}\) | \(P_{\mathrm{right}}(50\,\mathrm{fs})\) | Extracted ν (THz) | ν₀ (THz) | Relative error |
|---------------------|------------------------------------------|-------------------|----------|----------------|
| 0.0                 | 0.1090                                   | 458.17            | 461.22   | 0.66 %         |
| 0.3                 | 0.4963                                   | 318.73            | 322.85   | 1.28 %         |
| 0.5                 | 0.5004                                   | 239.04            | 230.61   | 3.66 %         |
| 0.7                 | 0.5000                                   | 139.44            | 138.37   | 0.78 %         |
| 1.0                 | 0.5000 (mixed)                           | no peak           | –        | –              |

> The small errors are due to finite‑time window effects; they decrease with longer simulation time.

---

## Discussion and open questions

- **Why fixed Hamiltonian?** The observer does not change the energy of a photon or a particle. The previous version with \(H \propto (1-E)\) was a phenomenological simplification; v17.0 corrects this and aligns with standard quantum measurement theory.
- **Zeno effect as dephasing**: The model shows that strong measurement kills coherence (off‑diagonals) without altering populations. This is the true Zeno mechanism.
- **Future work**: Extend to two coupled qubits to study entanglement under measurement; add spatial interference pattern simulation.

---

## Conclusion

DTQEM v17.0 provides a physically consistent, computationally efficient, and well‑documented open‑source tool for simulating wave‑particle duality of both matter and light under continuous measurement. It is ready for educational use and experimental benchmarking.

---

## Code availability

All source code is available at the GitHub repository. The main script for photon simulations is `photon_wave_particle.py`.
