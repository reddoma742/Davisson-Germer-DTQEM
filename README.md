```markdown
# DTQEM – Dual-Threshold Quantum Decoherence Models

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20460770.svg)](https://doi.org/10.5281/zenodo.20460770)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Research](https://img.shields.io/badge/status-research--grade-orange.svg)]()

**A family of calibrated, first‑principles‑derived models for quantum decoherence in path‑interference and massive‑particle interferometry experiments.**

> *"From independent‑bath phenomenology to unified joint‑bath theory — with a strict statistical detection limit at N ≥ 36."*

---

## ⚛️ The Core Equation (v18.0‑C)

\[
C(I,T) = C_0 \cdot \exp\!\left(-a I - b \frac{\Delta T}{T_{\text{ref}}} - c I \frac{\Delta T}{T_{\text{ref}}}\right)
\]

- \( I \in [0,1] \): which‑path information  
- \( T \): environment temperature (K)  
- \( \Delta T = T - T_{\text{ref}} \), \( T_{\text{ref}} = 300\,\text{K} \)

Setting \( c = 0 \) recovers the historical **independent‑bath** model (v17.0‑C).  
The crossover coefficient \( c > 0 \) indicates a **joint bath** (shared environmental modes).

---

## 📦 Model Family Overview

| Version | Output | Inputs | Key Feature | Status |
|---------|--------|--------|-------------|--------|
| **v17.0‑C** | Coherence \( C \) | \( I, T \) | Baseline, 3 params, LOOCV \( R^2=0.9356 \) | ✅ Final baseline |
| **v18.0‑C** | Coherence \( C \) | \( I, T \) | Joint‑bath crossover \( c \), AICc threshold \( N \ge 36 \) | ✅ Stable |
| **v63.1‑C** | Decoherence time \( \tau_c \) | \( m, v, N \) | Scaling exponents from spin‑boson + Debye | ✅ Working |
| **Unified v1.0** | \( \tau_c \) landscape | \( m, v, N, I, T \) | Complete particle + environment coupling | ✅ Research |

---

## 🧠 Quick Start

### Installation

```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
pip install numpy scipy matplotlib
```

Use v17.0‑C (Baseline Coherence)

```python
from models.v17.dtqem_baseline_v17 import coherence

C = coherence(I_path=0.5, T_env=400)
print(f"C = {C:.4f}")   # → 0.1467
```

Use v18.0‑C (Joint‑Bath Coherence with Uncertainty)

```python
from models.v18.DTQEM_v63_1_C import DTQEMModel

model = DTQEMModel(c=0.5)
C, err, (lo, hi) = model.predict(0.5, 400, return_uncertainty=True)
print(f"C = {C:.4f} ± {err:.4f}  [95% CI: {lo:.4f}, {hi:.4f}]")

# Operational mapping: photons → I_path
I = DTQEMModel.map_photon_number_to_Ipath(nbar=2.5, kappa=0.8)
print(f"I_path = {I:.4f}")   # → 0.8647
```

Use v63.1‑C (Coherence Time Scaling)

```python
from models.v63.DTQEM_v63_1_C import DTQEMv63Model

MU = 1.660539e-27   # kg per atomic mass unit
m_C60 = 720 * MU
model = DTQEMv63Model()
tau = model.calculate_tau(m_kg=m_C60, v_ms=200, N=60)
print(f"τ_c (C60) = {tau:.2e} s")   # → ~4.55e-26 s
```

Use Unified Model

```python
from models.unified.dtqem_unified_simulator import UnifiedDecoherenceModel

unified = UnifiedDecoherenceModel()
tau = unified.calculate_tau_c(m_kg=m_C60, v_ms=200, N_atoms=60,
                               I_path=0.5, T_kelvin=400)
```

---

📊 Parameters & Performance

v17.0‑C / v18.0‑C Calibrated Parameters

Parameter Value Std Error Physical Meaning
 C_0  0.3675 ±0.0052 Baseline coherence
 a  1.6968 ±0.0245 Path‑decoherence rate
 b  0.8055 ±0.0148 Thermal dephasing rate
 c  0.5000 ±0.0201 Joint‑bath crossover (v18 only)
 T_{\text{ref}}  300 K — Reference temperature

Statistical Performance

Model  R^2  LOOCV  R^2  RMSE
v17.0‑C (baseline) 0.9679 0.9356 0.0202
v18.0‑C (joint‑bath) 0.9982 0.9814 0.0045

v63.1‑C Scaling Exponents (First‑Principles)

Exponent Value Physical Derivation
 \beta  (mass) 0.44 Debye‑Pikovski: frozen vibrational modes at 300 K
 \delta  (velocity) 1/3 van der Waals + eikonal scattering
 \zeta  (per‑atom) 0.005 Symmetry‑suppressed blackbody emission
 \tau_{c0}   9.8 \times 10^{-27}  s Phenomenological scale

---

🔬 Key Scientific Result: AICc Statistical Threshold

With only  N = 8  data points, the correct joint‑bath model (v18.0‑C) is selected only 11% of the time.
A minimum of  N \ge 36  measurements is required for reliable detection (79%).

Sample Size  N  Selects v17.0‑C Selects v18.0‑C Reliability
8 89% 11% ❌ Low
16 57% 43% ❌ Low
36 21% 79% ✅ Moderate‑High
50 10% 90% ✅ High
80 5% 95% ✅ Very High

---

📁 Repository Structure

```
DTQEM/
├── README.md
├── LICENSE                      ← MIT
├── CITATION.cff                 ← Machine‑readable citation
├── requirements.txt
│
├── models/
│   ├── v17/
│   │   └── dtqem_baseline_v17.py
│   ├── v18/
│   │   ├── DTQEM_v63_1_C.py     ← Core v18.0‑C model
│   │   └── test_dtqem.py
│   ├── v63/
│   │   ├── DTQEM_v63_1_C.py
│   │   └── dtqem_v63_joint.py
│   └── unified/
│       └── dtqem_unified_simulator.py
│
├── figures/
│   ├── generate_figures.py
│   ├── generate_figure3.py
│   ├── figure1.png              ← Lorentzian a(ω_c)
│   └── figure3.png              ← τ_c landscape C60/C700
│
└── paper/
    └── paper.tex                ← Full LaTeX manuscript (Physical Review A)
```

---

🧪 Running Tests

```bash
# Unit tests for v18.0‑C
python models/v18/test_dtqem.py

# Self‑test for v63.1‑C
python models/v63/DTQEM_v63_1_C.py

# Reproduce AICc threshold figure
python figures/generate_figures.py
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
  journal = {arXiv preprint},
  year    = {2026},
  note    = {arXiv:XXXX.XXXXX [quant-ph] (pending endorsement)}
}
```

Software (Zenodo):

```bibtex
@software{berramdane2026dtqem_sw,
  author    = {Berramdane, Reddouane},
  title     = {DTQEM v17.0-C: Final Coherence Model
               for Path-Interference Experiments},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20460770},
  url       = {https://doi.org/10.5281/zenodo.20460770}
}
```

---

🙏 Acknowledgments

· Scientific supervision, model calibration, and all research decisions: Reddouane Berramdane
· AI assistance (code, derivations, documentation): DeepSeek, Claude (Anthropic), Arena AI — used as computational tools under full human oversight.

---

⚠️ Note on arXiv Submission

This work is awaiting endorsement for the quant‑ph section of arXiv.
The full manuscript (paper/paper.tex) is available in this repository.
If you are an established researcher in quantum physics with at least four previous arXiv papers in the field, and you find this work valuable, your endorsement would be greatly appreciated.
Please contact the author directly: reddoma@gmail.com

---

📜 License

MIT License — free to use, modify, and distribute with attribution.

📬 Contact

· Author: Reddouane Berramdane
· Email: reddoma@gmail.com
· GitHub: reddoma742/Davisson-Germer-DTQEM
· Zenodo: 10.5281/zenodo.20460770

---

Last updated: June 2026

```
