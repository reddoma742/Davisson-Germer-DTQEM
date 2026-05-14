# DTQEM – Dual-Time Quantum Entanglement Model

**A unified open‑source framework for simulating wave‑particle duality, measurement‑controlled tunneling, and entanglement decay under local dephasing.**

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI (v18.0)](https://zenodo.org/badge/DOI/10.5281/zenodo.20162958.svg)](https://zenodo.org/record/20162958)

---

## 📌 Overview

DTQEM provides numerically exact simulations of **open quantum systems** under the **“temporal balance”** hypothesis: the observer (measurement) does not change the system’s energy – it only destroys coherence via **pure dephasing** (`σ_z` Lindblad operators). Three stable versions are available:

| Version | Focus | Key result | File |
|---------|-------|------------|------|
| **v16.0** | Massive‑particle tunneling (double well) | `P_right(t) ∝ (1-E_ext)²` , Zeno freeze | `tunneling.py` |
| **v17.0** | Photon wave‑particle duality (red light, 650 nm) | Frequency extraction via FFT, ν₀ = 461 THz | `photon_wave_particle.py` |
| **v18.0** | Two‑qubit entanglement under local dephasing | Concurrence decay + inferred CHSH (`S = 2√2·C`) | `concurrence_entanglement.py` |

All models use a **fixed Hamiltonian** and a **pure dephasing Lindblad operator** `L = √(γ₀·E_ext)·σ_z` (on one or both qubits). This corrects earlier phenomenological versions where the Hamiltonian was wrongly made observer‑dependent.

---

## 🚀 Quick start

### 1. Clone the repository
```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
