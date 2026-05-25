
# DTQEM v63.0 – Phenomenological Scaling Model for Decoherence Time τ_c

**A phenomenological scaling law for quantum decoherence time τ_c, calibrated on synthetic interferometry data – with stable inverse extraction via the logarithmic slope method.**

[![Status: Working Model](https://img.shields.io/badge/Status-Working%20Model-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

---

## 🚀 What is DTQEM v63.0?

**DTQEM v63.0** presents a **phenomenological scaling model** for the decoherence time `τ_c`, calibrated on synthetic interferometry data. The model is built on the D0 baseline equation:

\[
V_{\text{eff}} = \exp(-\gamma_\phi \cdot T_{\text{eff}}) \times \exp\left(-\frac{|\Delta\tau|}{\tau_c}\right)
\]

### Core Phenomenological Model

\[
\boxed{\tau_c = \frac{\tau_{c0}}{m^{\beta} \cdot (v/c)^{\delta} \cdot (1 + \zeta N)}}
\]

| Parameter | Value | Interpretation |
|-----------|-------|----------------|
| `τ_c0` | 9.8 × 10⁻²⁷ s | Environment-dependent reference time (not universal) |
| `β` | 0.44 | Mass exponent (≈ 1/2, consistent with Pikovski mechanism) |
| `δ` | 0.33 | Velocity exponent (≈ 1/3, consistent with VdW scattering) |
| `ζ` | 0.005 | Per-atom internal complexity (quantum freezing) |
| `N` | – | Number of atoms (proxy for internal degrees of freedom) |

---

## 🔧 Key Features

### 1. Stable Inverse Extraction – Logarithmic Slope Method

Instead of extracting `τ_c` from a single visibility measurement (which is unstable), v63.0 uses **multiple measurements at different `Δτ`**:

\[
\ln V_{\text{eff}} = C - \frac{1}{\tau_c} |\Delta\tau|
\]

→ Linear fit → `τ_c = -1 / slope`

### 2. Experimental Predictions for Validation

| Test | Prediction | Purpose |
|------|------------|---------|
| **Pressure dependence** | If `τ_c` independent of P → intrinsic mechanism (Pikovski). If `τ_c ∝ 1/P` → environmental (Joos-Zeh). | **CRITICAL TEST** |
| **Mass scaling** | `τ_c ∝ m^{-0.44}` | Test β |
| **Velocity scaling** | `τ_c ∝ v^{-0.33}` | Test δ |
| **Temperature dependence** | Pikovski predicts `τ_c ∝ 1/T` | Test mechanism |

### 3. CSV Support for Real Data

```csv
particle, mass_kg, speed_m_s, N_atoms, delta_tau_s, V_eff
C60, 1.196e-24, 200.0, 60, 1.2e-15, 0.85
C60, 1.196e-24, 200.0, 60, 2.5e-15, 0.72
...
```

---

📦 Requirements

Package Version Purpose
numpy ≥ 1.21 Numerical computing
matplotlib ≥ 3.5 Visualization
scipy ≥ 1.7 Linear regression, optimization
ipywidgets (optional) ≥ 7.6 Interactive dashboard

Installation

pip install numpy matplotlib scipy
```

---

🚀 Usage

Run with synthetic data (demo)


python DTQEM_v63.0.py


Run with real CSV data


python DTQEM_v63.0.py your_scan_data.csv


In Google Colab / Jupyter

```python
from DTQEM_v63 import PhenomenologicalModel, extract_tau_c_from_scan

model = PhenomenologicalModel()
tau_c = model.tau_c(m_kg=720*1.66e-27, v_ms=200.0, N=60)
print(f"τ_c = {tau_c:.3e} s")
```

---

📊 Output Files

File Description
output_v63/v63_results.csv Extracted τ_c values, slope, R² per particle

---

📄 Citation

If you use DTQEM v63.0 in your research, please cite:

```bibtex
@software{DTQEM_v63_2026,
  author       = {Berramdane, Reddouane},
  title        = {DTQEM v63.0: Phenomenological Scaling Model for Decoherence Time τ_c},
  year         = {2026},
  version      = {63.0},
  url          = {https://github.com/reddoma742/Davisson-Germer-DTQEM},
  note         = {Model: τ_c = τ_c0 / [m^β·(v/c)^δ·(1+ζN)] with β≈0.44, δ≈0.33, ζ≈0.005}
}
```

---

📁 Repository Structure

```
DTQEM_Project/
├── DTQEM_v63.0.py              # Main code
├── HISTORY.md                  # Version history
├── LICENSE                     # MIT License
├── README.md                   # This file
├── CITATION.cff                # Citation metadata
├── output_v63/                 # Results (auto-generated)
│   └── v63_results.csv
└── data/ (optional)            # Your CSV files
```

---

⚠️ Important Limitations

1. This is a phenomenological model, not a first-principles derivation.
2. τ_c0 is environment-dependent, not a universal constant.
3. Calibrated on synthetic data – experimental validation is pending.
4. Valid range: mass 100–10,000 amu, speed 50–500 m/s, room temperature, high vacuum.

---

🤝 Acknowledgments

Development assisted by:

· Google Gemini – Theoretical discussions
· DeepSeek – Critical analysis and insights
· Claude (Anthropic) – Code writing, theoretical derivations
· Max & Kiwi – Theoretical derivations of β=1/2, δ=1/3, ζ≈0.005

---

📧 Contact

Author: Reddouane Berramdane
Email: reddoma@gmail.com
GitHub: reddoma742/Davisson-Germer-DTQEM

---

📜 License

MIT License – see LICENSE file.

```
