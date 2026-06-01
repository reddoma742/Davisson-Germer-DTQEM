# DTQEM v46.0 – Mach-Zehnder Interferometer & Unified Framework

**A unified framework for quantum decoherence based on proper‑time discrepancy (DTQEM) – with interactive dashboards for double‑slit, qubit, Zeeman, and Mach-Zehnder systems.**

[![Status: Hypothesis](https://img.shields.io/badge/Status-Scientific%20Hypothesis-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20349674.svg)](https://doi.org/10.5281/zenodo.20349674)

---

## 🚀 What is DTQEM?

**DTQEM (Decoherence from Time‑scale Quantum Effective Mismatch)** proposes a new physical mechanism for quantum decoherence:

> *The coherence between quantum states decays when there is a discrepancy between the proper time of the particle and the reference time of the measuring device.*

### Core Equation (D0 – Baseline Model)

For the **Mach-Zehnder interferometer** (v46.0):

\[
\boxed{V_{\text{eff}} = \exp(-\gamma_\phi \cdot T_{\text{eff}}) \times \exp\left(-\frac{|\Delta\tau|}{\tau_c}\right)}
\]

where:
- \(T_{\text{eff}} = \frac{\tau_1 + \tau_2}{2}\) – effective environmental interaction time
- \(\Delta\tau = \left| \frac{L_1}{v_1 \gamma_1} - \frac{L_2}{v_2 \gamma_2} \right|\) – proper-time mismatch
- \(\tau_i = L_i / v_i\) – lab-frame transit time
- \(\gamma_i = 1 / \sqrt{1 - v_i^2/c^2}\) – Lorentz factor
- \(\tau_c\) – the only free parameter (proper‑time coherence constant)

For **double‑slit, qubit, and Zeeman** systems (v44.0), the equation includes a source coherence term \(V_{\text{source}}(d)\).

---

## 🔧 Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | ≥ 1.21 | Numerical computing |
| matplotlib | ≥ 3.5 | Visualization |
| ipywidgets | ≥ 7.6 | Interactive sliders |
| scipy | ≥ 1.7 | Inverse model (DE) |

### Installation

```bash
pip install numpy matplotlib ipywidgets scipy
