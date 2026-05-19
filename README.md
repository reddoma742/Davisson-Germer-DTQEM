# DTQEM v38.2 – Hydrogen Balmer‑alpha Zeeman Inversion

**An open‑source framework for extracting magnetic fields from Hα spectra – with multi‑start bootstrap and 100% success rate under standard validation.**

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20260168.svg)](https://doi.org/10.5281/zenodo.20260168) <!-- to be updated -->

---

## 🚀 Latest stable release – v38.2 (Zeeman triplet inversion)

**Robust inversion of the hydrogen Balmer‑alpha line** (656.28 nm) to recover the magnetic field strength \(B\) (Tesla).  
The model assumes a symmetric Gaussian triplet (\(\pi, \sigma^+, \sigma^-\)) with a fixed intensity ratio, a linear background (measured independently), and Poisson statistics.  

From a single unpolarised spectrum, the code extracts:

- **Magnetic field \(B\)** (Tesla) – the key physical parameter.
- **Peak intensity \(I_0\)** – with bootstrap uncertainties.
- **Line width \(\sigma\)** – instrumental + thermal broadening.

AICc automatically selects between a single‑peak model (no field) and the triplet.  
The multi‑start bootstrap (30 samples, 10 restarts, 20% fully random starts) achieves **100% success** in all validation tests and provides realistic 95% confidence intervals.

---

## 🔬 What makes v38.2 special?

| Feature | Description |
|---------|-------------|
| **Physically correct model** | \(I(\lambda) = I_0\,G(\lambda,\lambda_0,\sigma) + I_0\,f\,G(\lambda,\lambda_0+\Delta\lambda,\sigma) + I_0\,f\,G(\lambda,\lambda_0-\Delta\lambda,\sigma) + \text{BG}\)<br>\(\Delta\lambda = \frac{\lambda_0^2}{c}\,\frac{\mu_B}{h}\,g_{\text{eff}}\,|B|\) with \(g_{\text{eff}}=1.0\) (normal Zeeman for Hα). |
| **Fixed linear background** | Measured independently (with the laser off) – eliminates correlation with line parameters. |
| **Poisson likelihood** | Full negative log‑likelihood including Stirling’s term – correct for photon‑counting data. |
| **Global optimisation** | Differential evolution (40 generations) followed by L‑BFGS‑B guarantees the true minimum. |
| **Automatic model selection** | AICc with SNR‑dependent threshold + physical rejections (spread ratio < 0.5 or \(B/\sigma_B < 2\)). |
| **Multi‑start bootstrap** | 30 Poisson samples, 10 local restarts each (20% fully random), physics‑based acceptance → **100% success**. |
| **Complete diagnostics** | Residual analysis, normalised residuals, bootstrap distribution histogram, recovery curve. |

---

## 📊 Performance on synthetic data (Poisson noise)

| True \(B\) (T) | Recovered \(B\) (MAP) (T) | Bootstrap std (T) | 95% CI (T) | Relative error |
|----------------|----------------------------|--------------------|--------------|----------------|
| 0.5            | 0.506                      | 0.120              | [0.284, 0.713] | 1.2 % |
| 1.0            | 0.985                      | 0.082              | [0.860, 1.139] | 1.5 % |
| 1.5            | 1.502                      | 0.103              | [1.293, 1.667] | 0.2 % |
| 2.0            | 1.995                      | 0.102              | [1.853, 2.185] | 0.25 % |
| 1.0 (low SNR ~172) | 0.993                  | 0.100              | [0.847, 1.213] | 0.7 % |

- **Bootstrap success rate:** 100% (30/30 samples) in all tests.
- **Detection limit:** ~0.15 T (below that the model correctly returns a single peak).
- **Runtime:** 8–13 s per spectrum (standard CPU).

**Additional validations:**  
✔ Phase shift, quadratic background, high noise, low SNR, stress tests (Monte Carlo) – all passed.

---

## 📌 Evolution of the framework

| Version | Focus | Key result | File |
|---------|-------|------------|------|
| **v38.2** | **Hα Zeeman inversion** | Recover \(B\) with 100% bootstrap success, realistic CIs | `dtqem_v38_2.py` / `dtqem_v38_2_full.py` |
| v34.2 | Double‑slit inversion | Observer strength \(E\), slit separation \(d\) | `dtqem_v34_2.py` |
| v22.0 | Self‑calibrating spectral inversion (hydrogen) | Recover \(T, \alpha, E\) from Balmer linewidths | `dtqem_v22_inversion.py` |
| v20.0 | Two‑qubit entanglement with temperature | Entanglement lifetimes for real qubits | `dtqem_20_entanglement.py` |

All versions share the same foundational hypothesis:  
*The observer does not change the system’s energy; it only destroys coherence via pure dephasing (\(\sigma_z\) Lindblad operator).*  
The dimensionless observer strength \(E\) controls the dephasing rate: \(\gamma_{\phi} = \gamma_0\,E\).

---

## 🚀 Quick start (v38.2 – Zeeman inversion)

### 1. Clone the repository

```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
