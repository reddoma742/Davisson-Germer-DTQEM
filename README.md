# DTQEM – Dual-Time Quantum Entanglement Model

**A unified open‑source framework for simulating open quantum systems under measurement – from wave‑particle duality to analytical dynamics.**

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI (v19.0)](https://zenodo.org/badge/DOI/10.5281/zenodo.20184654.svg)](https://zenodo.org/record/20184654)

---

## 🚀 Latest stable release – v19.0 (2026-05-15)

**Analytical solution of the baseline DTQEM model**  
Fixed Hamiltonian \( H = \frac{\Delta}{2}\sigma_x \) · Pure dephasing \( L = \sqrt{\gamma E_{\text{ext}}}\,\sigma_z \)

The probability to find the particle in the right well (or in state `|1⟩`) is:

\[
\boxed{P(E,t) = \frac{1}{2}\left[1 - e^{-\gamma E t}\left(\cos(\omega_0 t) + \frac{\gamma E}{\omega_0}\sin(\omega_0 t)\right)\right],\qquad \omega_0 = \frac{\Delta}{\hbar}.}
\]

This closed‑form solution supersedes earlier empirical fits (e.g. \(P\propto(1-E)^2\)) and provides a rigorous foundation for all DTQEM simulations.  
👉 [White Paper v19.0](WHITE_PAPER_v19.md)  
👉 [Python implementation](analytical_model_v19.py)

---

## 📌 Overview

DTQEM is an open‑source numerical and theoretical framework for **open quantum systems** under the **temporal balance** hypothesis: the observer does not change the system’s energy, it only destroys coherence via **pure dephasing** (`σ_z` Lindblad operators).

| Version | Focus | Key result | File |
|---------|-------|------------|------|
| **v19.0** | Baseline analytical model | Exact closed‑form solution for \(P(E,t)\) | `analytical_model_v19.py` |
| **v18.0** | Two‑qubit entanglement under local dephasing | Concurrence decay + inferred CHSH | `concurrence_entanglement.py` |
| **v17.0** | Photon wave‑particle duality (650 nm) | Frequency extraction via FFT, ν₀ = 461 THz | `photon_wave_particle.py` |
| **v16.0** | Massive‑particle tunneling | Numerical verification of Zeno effect | `tunneling.py` |

All versions use a **fixed Hamiltonian** and a **pure dephasing Lindblad operator** \(L = \sqrt{\gamma_0 E_{\text{ext}}}\,\sigma_z\).  
Earlier phenomenological versions (v15 and below) that used a Hamiltonian depending on \(E_{\text{ext}}\) are now **deprecated** – v19.0 provides the correct physics.

---

## 🧪 Key physical insights from v19.0

- **Decoherence time:** \( \tau_{\text{coh}} = 1/(\gamma E) \)
- **Critical observer strength:** \( E_{\text{crit}} = \omega_0 / \gamma \) (separates under‑damped from over‑damped regime)
- **Long‑time limit:** \( P(E=1, t\to\infty) = 1/2 \) (complete mixing, **not** freezing)
- **Rabi frequency remains constant** (observer does not change the energy scale)

These results are derived directly from the Lindblad master equation and exactly match numerical simulations.

---

## 🚀 Quick start (v19.0)

### 1. Clone the repository
```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
