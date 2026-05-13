# DTQEM – Dual‑Time Quantum Entanglement Model

**From Dephasing to Temporal Balance: A Unified Open‑Quantum‑System Framework**

[![License: DTQEM Research & Educational](https://img.shields.io/badge/License-DTQEM%20Research%20%26%20Educational-blue)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI (latest)](https://zenodo.org/badge/DOI/10.5281/zenodo.20090038.svg)](https://zenodo.org/record/20090038)

---

## ⚠️ License Notice
DTQEM is released under the **DTQEM Research & Educational License**.  
**Commercial use is strictly prohibited** without prior written authorization.  
Academic and non‑commercial research use is encouraged.

---

## 🧭 Which version should I use?

| Version | Status | Recommended for |
|---------|--------|----------------|
| **v16.0** | **Current stable** | All new users, teaching, experimental validation |
| v15.1 | Historical reference | Understanding earlier attempts and 4×4 Lindblad model |
| v14.0 – v13.0 | Archive | Insight into model evolution |

👉 **For new work, please use v16.0 (this version).** It contains a simplified 2×2 effective Lindblad model that reproduces all key phenomena with high numerical stability.

---

## 🔬 Core ideas (v16.0)

DTQEM v16.0 implements the **"temporal balance"** hypothesis: a quantum system’s behaviour (wave‑like vs. particle‑like) is governed by the competition between an **internal particle time** and the **observer’s time** (measurement strength). The external parameter \(E_{\text{ext}}\) (0 ≤ E ≤ 1) controls this balance.

- **Effective Hamiltonian**  
  \[
  H_{\text{eff}} = \frac{\Delta}{2}(1-E_{\text{ext}})\,\sigma_x
  \]
  → reduces Rabi frequency linearly with observer strength.

- **Pure dephasing Lindblad operator**  
  \[
  L = \sqrt{\gamma_0 E_{\text{ext}}}\,\sigma_z
  \]
  → kills coherences without directly flipping populations (true Zeno effect).

- **Resulting scaling**  
  \[
  P_{\text{right}}(t) \approx \left(\frac{\Delta}{2\hbar}\right)^2 t^2\,(1-E_{\text{ext}})^2
  \]

### Key numerical results (t = 20 ps, Δ = 3.5 meV, γ₀ = 5×10¹⁰ s⁻¹)

| \(E_{\text{ext}}\) | \(P_{\text{right}}\) | Physical interpretation |
|-------------------|---------------------|--------------------------|
| 0.0 | 0.0532 | Free Rabi oscillation (destructive phase) |
| 0.3 | 0.2872 | Beginning of decoherence |
| **0.5** | **0.7943** | **Synchronisation peak (times balanced)** |
| 0.7 | 0.2774 | Near‑Zeno regime |
| 1.0 | 0.0000 | Complete Zeno freeze (particle time stops) |

> The elevated value at \(E=0.5\) is a phase coincidence: the effective Rabi period at that point is ≈ 2.36 ps, so at 20 ps the system lies near a constructive maximum. This does not contradict decoherence.

---

## 📦 Installation & quick start

**Requirements:** Python 3.8+, numpy, scipy, matplotlib.

```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
pip install -r requirements.txt
python temporal_balance.py
