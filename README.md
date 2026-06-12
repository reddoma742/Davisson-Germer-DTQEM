```markdown
# DTQEM – Dual-Threshold Quantum Decoherence Models

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-v18.0--C--paper-blue.svg)](https://github.com/reddoma742/Davisson-Germer-DTQEM/releases/tag/v18.0-C-paper)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20670032.svg)](https://doi.org/10.5281/zenodo.20670032)

**A family of calibrated, first-principles-derived models for quantum decoherence in path-interference, massive-particle interferometry, and entanglement sudden death.**

> *Version v18.0-C-paper – The official release accompanying Paper I (Phenomenological Model)*
> *"From phenomenological baseline to unified joint-bath theory — with a strict statistical detection limit at N ≥ 36."*

---

## 🏷️ Version Information

| Field | Value |
|-------|-------|
| **Version** | `v18.0-C-paper` |
| **Release Date** | June 2026 |
| **Associated Paper** | Paper I: Phenomenological Joint-Bath Model |
| **DOI** | 10.5281/zenodo.XXXXXXX (to be updated) |
| **Status** | ✅ Stable / Published |

---

## 📦 Model Overview

| Version | Output | Inputs | Key Feature | Status |
|---------|--------|--------|-------------|--------|
| **v16.1-C** | P_left, P_right | E_ext, t | Quantum Zeno effect (historical) | ✅ Archived |
| **v17.0-C** | Coherence C | I_path, T | Baseline, 3 params, LOOCV R²=0.9356 | ✅ Final |
| **v18.0-C-paper** | Coherence C | I_path, T | Joint-bath crossover c, AICc N≥36 | ✅ **Current** |
| **v63.1-C** | Decoherence time τ_c | m, v, N | Scaling exponents from spin-boson | ✅ Working |
| **v63.2-C** | Decoherence time τ_c | m, v, N | Mass-velocity crossover c_mv | 🔜 Research |
| **Unified v1.0** | τ_c landscape | m, v, N, I, T | Complete particle + environment | 🔜 Research |
| **ESD v1.0** | t_ESD (ps) | I_path, T | Entanglement Sudden Death prediction | 🔜 Research |
| **Paper II** | Derivation | I, T | Microscopic √(uv) form | 🔜 In preparation |

---

## ⚛️ The Core Equation (v18.0-C-paper)

```math
C(I,T) = C_0 \cdot \exp\left(-a \cdot I - b \cdot \frac{\Delta T}{T_{\mathrm{ref}}} - c \cdot I \cdot \frac{\Delta T}{T_{\mathrm{ref}}}\right)
```

Symbol Meaning Value
C Coherence (visibility) Output
I Which-path information ∈ [0, 1]
T Environment temperature Kelvin
\Delta T T - T_{\mathrm{ref}} —
T_{\mathrm{ref}} Reference temperature 300 K (fixed)
C_0 Baseline coherence 0.3675 ± 0.0052
a Path-dephasing rate 1.6968 ± 0.0245
b Thermal-dephasing rate 0.8055 ± 0.0148
c Joint-bath crossover 0.5000 ± 0.0201

Note: Setting c = 0 recovers the independent-bath baseline (v17.0-C).

---

🚀 Quick Start

Installation

```bash
git clone https://github.com/reddoma742/Davisson-Ger
cd Davisson-Germer-DTQEM
pip install numpy scipy matplotlib
```

v18.0-C-paper (Joint-Bath Coherence)

```python
from models.v18.dtqem_joint_bath_v18 import DTQEMModel

# Create model with calibrated parameters
model = DTQEMModel(c=0.5)

# Predict coherence
C, err, (lo, hi) = model.predict(I_path=0.5, T_kelvin=400, return_uncertainty=True)
print(f"C = {C:.4f} ± {err:.4f}")   # → 0.1467 ± 0.0021

# Operational mapping: photons → I_path
I = DTQEMModel.map_photon_number_to_Ipath(nbar=2.5, kappa=0.8)
print(f"I_path = {I:.4f}")          # → 0.8647
```

v17.0-C (Baseline Coherence)

```python
from models.v17.dtqem_baseline_v17 import coherence

C = coherence(I_path=0.5, T_env=400)
print(f"C = {C:.4f}")               # → 0.1467
```

v63.1-C (Coherence Time Scaling)

```python
from models.v63.DTQEM_v63_1_C import DTQEM_v63_Model

M_U = 1.660539e-27
m_C60 = 720 * M_U
model = DTQEM_v63_Model()
tau = model.calculate_tau_c(m_C60, v=200, N=60)
print(f"τ_c (C60) = {tau:.2e} s")   # → 4.55e-26 s
```

v16.1-C (Quantum Zeno Effect - Historical)

```python
from models.v16.dtqem_tunneling_v16_1_C import evolve

P_left, P_right, coh = evolve(E_ext=0.5, return_all=True)
print(f"P_right at 20ps = {P_right[-1]:.4f}")
```

---

📊 Performance & Validation

Statistical Performance (v18.0-C-paper)

Model R² LOOCV R² RMSE
v17.0-C (baseline, c=0) 0.9679 0.9356 0.0202
v18.0-C-paper (full) 0.9982 0.9814 0.0045

Hornberger (2003) Validation

· Dataset: 8 experimental points (C₇₀ fullerene interferometry)
· Re-fitted R²: 0.936
· Conclusion: The functional form is compatible with independent experimental data

Key Scientific Result: AICc Statistical Threshold

With only N = 8 data points, the correct joint-bath model is selected only 11% of the time.
A minimum of N ≥ 36 measurements is required for reliable detection (79%).

N v17.0-C v18.0-C-paper Reliability
8 89% 11% ❌ Low
16 57% 43% ❌ Low
36 21% 79% ✅ Moderate-High
50 10% 90% ✅ High
80 5% 95% ✅ Very High

---

📁 Repository Structure

```
DTQEM/
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── .gitignore
│
├── models/
│   ├── v16/
│   │   └── dtqem_tunneling_v16_1_C.py
│   ├── v17/
│   │   └── dtqem_baseline_v17.py
│   ├── v18/
│   │   └── dtqem_joint_bath_v18.py          # ⭐ Main model
│   ├── v63/
│   │   ├── DTQEM_v63_1_C.py
│   │   └── dtqem_v63_joint.py
│   └── unified/
│       └── dtqem_unified_simulator.py
│
├── tests/
│   └── test_dtqem.py
│
├── scripts/
│   ├── 01_generate_synthetic_data.py
│   ├── 02_loocv_validation.py
│   ├── 03_hornberger_fit.py
│   ├── 04_temperature_scan_Tstar.py
│   └── 05_cauchy_schwarz_lambda_sweep.py
│
├── data/
│   ├── calibration/
│   │   ├── synthetic_grid.csv
│   │   └── fitted_parameters.json
│   └── validation/
│       └── hornberger_2003.csv
│
├── figures/
│   ├── figure_b_eff.png
│   ├── cauchy_schwarz_lambda_sweep.png
│   ├── hornberger_validation.png
│   └── ...
│
└── papers/
    └── DTQEM_PaperI_Phenomenological_v1.0.tex
```

---

🧪 Running Validation Scripts

```bash
# Generate synthetic calibration data
python scripts/01_generate_synthetic_data.py

# Run LOOCV validation (reproduces Table II)
python scripts/02_loocv_validation.py

# Fit Hornberger (2003) data (R² = 0.936)
python scripts/03_hornberger_fit.py

# Compute T* ≈ 3.82 K
python scripts/04_temperature_scan_Tstar.py

# Cauchy-Schwarz validation & λ sweep
python scripts/05_cauchy_schwarz_lambda_sweep.py

# Unit tests
python tests/test_dtqem.py
```

Expected output for tests:

```
Ran 6 tests in 0.013s
OK
```

---

📄 Citation

Paper I (Phenomenological Model)

```bibtex
@article{berramdane2026dtqem_paperI,
  author    = {Berramdane, Reddouane},
  title     = {DTQEM: A Phenomenological Model for Joint-Bath Quantum Decoherence},
  year      = {2026},
  note      = {arXiv:XXXX.XXXXX [quant-ph] (submitted)},
  version   = {v18.0-C-paper}
}
```

Software (Zenodo)

```bibtex
@software{berramdane2026dtqem_sw,
  author       = {Berramdane, Reddouane},
  title        = {DTQEM: Dual-Threshold Quantum Decoherence Models},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {v18.0-C-paper},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

---

📜 License

Content License
Source code (.py files) MIT License
Paper, figures, documentation CC BY-NC-SA 4.0

---

🙏 Acknowledgments

Human scientific supervision, model calibration, philosophy, and final decisions:
Reddouane Berramdane

AI assistance (as computational tools under full human oversight):

AI Model Contribution
DeepSeek Critical analysis, methodology validation
Claude (Anthropic) Code writing, derivations, documentation, Zeno optimization
Qwen Editorial assistance, manuscript formatting, LaTeX optimization
Arena AI First-principles derivations (scaling exponents), unified framework, ESD formulation

"لم أكن أحمل شهادة في الفيزياء، لكن الفضول والأصدقاء (بشراً وذكاء اصطناعياً) كانوا معي. هذا الإنجاز هو ثمرة تواضع ورحلة بحث لا تزال مستمرة."
— Reddouane Berramdane

---

📬 Contact

 
Author Reddouane Berramdane
Email reddoma@gmail.com
GitHub reddoma742/Davisson-Germer-DTQEM
Zenodo 10.5281/zenodo.XXXXXXX (to be updated)

---

Last updated: June 2026
Version: v18.0-C-paper

```
