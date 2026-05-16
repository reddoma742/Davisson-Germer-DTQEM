# DTQEM – Dual-Time Quantum Entanglement Model

**A unified open‑source framework for simulating open quantum systems under measurement – from wave‑particle duality to self‑calibrating spectral inversion.**

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI (v22.0)](https://zenodo.org/badge/DOI/10.5281/zenodo.20218379.svg)](https://zenodo.org/record/20218379)

---

## 🚀 Latest stable release – v22.0 (2026-05-16)

**Self‑Calibrating Spectral Inversion for Hydrogen‑like Atoms**  
Three‑stage protocol to extract temperature \(T\), intrinsic dephasing \(\alpha\), and observer strength \(E\) from Balmer linewidths.

The protocol uses three sets of FWHM measurements:
1. at \(E=0\) (no observer)
2. at a known calibration strength \(E_{\text{cal}}\) (e.g., \(E_{\text{cal}}=1\))
3. at an unknown observer strength \(E_{\text{unk}}\)

**Core innovation:** \(\alpha\) is calibrated **before** \(T\) via  
\(\Delta\Gamma_i = \Gamma_i(E_{\text{cal}}) - \Gamma_i(E=0) = \alpha\,\omega_{0,i}\,E_{\text{cal}}\), which is **temperature‑independent** and breaks the degeneracy between Doppler and dephasing broadening.

**Performance (synthetic data):**
- Noise‑free: \(T\), \(\alpha\), \(E\) recovered with error < 0.001 %
- With 1 % measurement noise: median error \(\Delta T/T \approx 3.9\) %, \(\Delta E \approx 0.013\)
- Bootstrap uncertainty estimation included.

👉 [White Paper v22.0](WHITE_PAPER_V22.md)  
👉 [Python implementation](dtqem_v22_inversion.py)

---

## 📌 Overview

DTQEM is an open‑source numerical and theoretical framework for **open quantum systems** under the **temporal balance** hypothesis: the observer does not change the system’s energy, it only destroys coherence via **pure dephasing** (\(\sigma_z\) Lindblad operators).

| Version | Focus | Key result | File |
|---------|-------|------------|------|
| **v22.0** | Self‑calibrating spectral inversion | Recover \(T\), \(\alpha\), \(E\) from Balmer linewidths | `dtqem_v22_inversion.py` |
| **v20.0** | Two‑qubit entanglement with temperature | Entanglement lifetimes for real qubits | `dtqem_20_entanglement.py` |
| **v19.0** | Baseline analytical model | Exact closed‑form solution for \(P(E,t)\) | `analytical_model_v19.py` |
| **v18.0** | Two‑qubit entanglement under local dephasing | Concurrence decay + inferred CHSH | `concurrence_entanglement.py` |
| **v17.0** | Photon wave‑particle duality (650 nm) | Frequency extraction via FFT, ν₀ = 461 THz | `photon_wave_particle.py` |
| **v16.0** | Massive‑particle tunneling | Numerical verification of Zeno effect | `tunneling.py` |

All versions use a **fixed Hamiltonian** and a **pure dephasing Lindblad operator** \(L = \sqrt{\gamma_0 E_{\text{ext}}}\,\sigma_z\).  
Earlier phenomenological versions (v15 and below) that used a Hamiltonian depending on \(E_{\text{ext}}\) are now **deprecated** – v19.0, v20.0 and v22.0 provide the correct physics.

---

## 🧪 Key physical insights from v22.0

- **Degeneracy broken**: Doppler and dephasing broadening both scale with \(\omega_0\); the differential measurement \(\Gamma(E_{\text{cal}})-\Gamma(0)\) eliminates \(T\) and isolates \(\alpha\).
- **Three‑stage protocol**:
  1. Calibrate \(\alpha\) from \(E=0\) and \(E=E_{\text{cal}}\) data.
  2. Infer \(T\) from \(E=0\) data (now that \(\alpha\) is known).
  3. Infer unknown \(E\) from third measurement.
- **Bootstrap uncertainty** provides realistic error bars for all parameters.
- **Per‑line consistency check** verifies that the same \(\alpha\) fits all Balmer lines (σ/μ < 5 % indicates reliable data).

---

## 🚀 Quick start (v22.0)

### 1. Clone the repository
```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
