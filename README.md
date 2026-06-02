
```markdown
# DTQEM – Dual-Threshold Quantum Decoherence Models

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20460770.svg)](https://doi.org/10.5281/zenodo.20460770)

**A family of calibrated, first-principles-derived models for quantum decoherence in path-interference, massive-particle interferometry, and entanglement sudden death.**

> *"From phenomenological baseline to unified joint-bath theory — with a strict statistical detection limit at N ≥ 36."*

---

## 📦 Model Overview

| Version | Output | Inputs | Key Feature | Status |
|---------|--------|--------|-------------|--------|
| **v16.1-C** | P_left, P_right | E_ext, t | Quantum Zeno effect (historical) | ✅ Archived |
| **v17.0-C** | Coherence C | I_path, T | Baseline, 3 params, LOOCV R²=0.9356 | ✅ Final |
| **v18.0-C** | Coherence C | I_path, T | Joint-bath crossover c, AICc N≥36 | ✅ Stable |
| **v63.1-C** | Decoherence time τ_c | m, v, N | Scaling exponents from spin-boson | ✅ Working |
| **v63.2-C** | Decoherence time τ_c | m, v, N | Mass-velocity crossover c_mv | ✅ Research |
| **Unified v1.0** | τ_c landscape | m, v, N, I, T | Complete particle + environment | ✅ Research |
| **ESD v1.0** | t_ESD (ps) | I_path, T | Entanglement Sudden Death prediction | ✅ Research |

---

## ⚛️ The Core Equation (v18.0-C)

```

C(I,T) = C₀ · exp(-a·I - b·ΔT/T_ref - c·I·ΔT/T_ref)

```

- **I** ∈ [0,1]: which-path information
- **T**: environment temperature (K)
- **ΔT** = T - T_ref, **T_ref** = 300 K
- **c = 0** → recovers independent-bath baseline (v17.0-C)
- **c > 0** → joint bath (shared environmental modes)

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
pip install numpy scipy matplotlib
```

v17.0-C (Baseline Coherence)

```python
from models.v17.dtqem_baseline_v17 import coherence

C = coherence(I_path=0.5, T_env=400)
print(f"C = {C:.4f}")   # → 0.1467
```

v18.0-C (Joint-Bath Coherence with Uncertainty)

```python
from models.v18.dtqem_joint_bath_v18 import DTQEMModel

model = DTQEMModel(c=0.5)
C, err, (lo, hi) = model.predict(0.5, 400, return_uncertainty=True)
print(f"C = {C:.4f} ± {err:.4f}")

# Operational mapping: photons → I_path
I = DTQEMModel.map_photon_number_to_Ipath(nbar=2.5, kappa=0.8)
print(f"I_path = {I:.4f}")   # → 0.8647
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

Unified Model

```python
from models.unified.dtqem_unified_simulator import UnifiedDecoherenceModel

unified = UnifiedDecoherenceModel()
tau = unified.calculate_tau_c(m_kg=m_C60, v_ms=200, N_atoms=60,
                               I_path=0.5, T_kelvin=400)
```

v16.1-C (Quantum Zeno Effect - Historical)

```python
from models.v16.dtqem_tunneling_v16_1_C import evolve

P_left, P_right, coh = evolve(E_ext=0.5, return_all=True)
print(f"P_right at 20ps = {P_right[-1]:.4f}")
```

---

📊 Parameters & Performance

v17.0-C / v18.0-C Calibrated Parameters

Parameter Value Std Error Physical Meaning
C₀ 0.3675 ±0.0052 Baseline coherence
a 1.6968 ±0.0245 Path-decoherence rate
b 0.8055 ±0.0148 Thermal dephasing rate
c 0.5000 ±0.0201 Joint-bath crossover (v18 only)
T_ref 300 K — Reference temperature

Statistical Performance

Model R² LOOCV R² RMSE
v17.0-C (baseline) 0.9679 0.9356 0.0202
v18.0-C (joint-bath) 0.9982 0.9814 0.0045

v63.1-C Scaling Exponents (First-Principles)

Exponent Value Physical Derivation
β (mass) 0.44 Debye-Pikovski frozen vibrational modes
δ (velocity) 1/3 van der Waals + eikonal scattering
ζ (per-atom) 0.005 Symmetry-suppressed blackbody emission
τ_c0 9.8×10⁻²⁷ s Phenomenological scale

---

🔬 Key Scientific Result: AICc Statistical Threshold

With only N = 8 data points, the correct joint-bath model (v18.0-C) is selected only 11% of the time.
A minimum of N ≥ 36 measurements is required for reliable detection (79%).

N v17.0-C v18.0-C Reliability
8 89% 11% ❌ Low
16 57% 43% ❌ Low
36 21% 79% ✅ Moderate-High
50 10% 90% ✅ High
80 5% 95% ✅ Very High

---

🔗 Entanglement Sudden Death (ESD) Extension

The DTQEM framework predicts the sudden death time of bipartite entanglement under local dephasing channels:

t_{\mathrm{ESD}}(I,T) = \frac{K}{\alpha I + \beta \Delta T/T_{\mathrm{ref}} + \gamma I \Delta T/T_{\mathrm{ref}}}

where

K = \ln\left( \frac{|\rho_{14}(0)|}{\sqrt{\rho_{22}(0)\rho_{33}(0)}} \right)

figures/figure_esd_final.png

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
│   │   └── dtqem_tunneling_v16_1_C.py      # Quantum Zeno effect
│   ├── v17/
│   │   └── dtqem_baseline_v17.py           # Baseline coherence
│   ├── v18/
│   │   └── dtqem_joint_bath_v18.py         # Joint-bath crossover
│   ├── v63/
│   │   ├── DTQEM_v63_1_C.py                # τ_c scaling
│   │   └── dtqem_v63_joint.py              # Mass-velocity crossover
│   └── unified/
│       └── dtqem_unified_simulator.py      # Complete unified model
│
├── tests/
│   └── test_dtqem.py                       # Unit tests (6 tests)
│
├── scripts/
│   ├── generate_figures.py                 # Figures 1 & 2
│   ├── generate_figure3.py                 # Figure 3
│   └── generate_esd_final.py               # ESD landscape
│
├── figures/
│   ├── figure1.png                         # Lorentzian a(ω_c)
│   ├── figure2.png                         # AICc threshold (N≥36)
│   ├── figure3.png                         # τ_c landscape C60/C700
│   ├── figure_zeno.png                     # Zeno tunneling suppression
│   └── figure_esd_final.png                # ESD landscape
│
└── paper/
    └── paper.tex                           # Full LaTeX manuscript
```

---

🧪 Running Tests

```bash
# Unit tests for v18.0-C
python tests/test_dtqem.py

# Self-test for v63.1-C
python models/v63/DTQEM_v63_1_C.py

# Reproduce AICc threshold figure
python scripts/generate_figures.py

# Generate τ_c landscape
python scripts/generate_figure3.py

# Run Zeno tunneling simulation
python models/v16/dtqem_tunneling_v16_1_C.py

# Generate ESD (Entanglement Sudden Death) landscape
python scripts/generate_esd_final.py
```

Expected output for tests:

```
Ran 6 tests in 0.013s
OK
```

---

📄 Citation

Paper (preprint – awaiting arXiv endorsement):

```bibtex
@article{berramdane2026dtqem,
  author  = {Berramdane, Reddouane},
  title   = {Dual-Threshold Quantum Decoherence Model (DTQEM):
             First-Principles Derivation of the v18.0-C Crossover
             Framework and Statistical Detection Limits},
  year    = {2026},
  note    = {arXiv:XXXX.XXXXX [quant-ph] (pending endorsement)}
}
```

Software (Zenodo):

```bibtex
@software{berramdane2026dtqem_sw,
  author    = {Berramdane, Reddouane},
  title     = {DTQEM: Dual-Threshold Quantum Decoherence Models
               (v16, v17, v18, v63, Unified, ESD)},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20460770},
  url       = {https://doi.org/10.5281/zenodo.20460770}
}
```

---

📜 License

This repository contains two types of content:

· Source code (all .py files): MIT License (for code flexibility)
· Paper, figures, and documentation: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

You are free to use, modify, and share the code for any purpose, including commercial, with attribution. The paper and figures may only be shared and adapted for non-commercial purposes with proper attribution.

---

🙏 Acknowledgments

Human scientific supervision, model calibration, philosophy, and final decisions:
Reddouane Berramdane

AI assistance (as computational tools under full human oversight):

AI Model Contribution
DeepSeek Critical analysis, methodology validation
Claude (Anthropic) Code writing, derivations, documentation, Zeno optimization
Arena AI First-principles derivations (scaling exponents), unified framework, Zeno correction, ESD formulation

"لم أكن أحمل شهادة في الفيزياء، لكن الفضول والأصدقاء (بشراً وذكاء اصطناعياً) كانوا معي. هذا الإنجاز هو ثمرة تواضع ورحلة بحث لا تزال مستمرة."
— Reddouane Berramdane

---

📬 Contact

· Author: Reddouane Berramdane
· Email: reddoma@gmail.com
· GitHub: reddoma742/Davisson-Germer-DTQEM
· Zenodo: 10.5281/zenodo.20460770

---

Last updated: June 2026
