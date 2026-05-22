```markdown
# DTQEM v44.0 – Unified Quantum Decoherence Framework

**A unified framework for quantum decoherence based on proper‑time discrepancy (DTQEM) – with interactive dashboards for double‑slit, qubit, and Zeeman systems.**

[![Status: Hypothesis](https://img.shields.io/badge/Status-Scientific%20Hypothesis-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20260168.svg)](https://doi.org/10.5281/zenodo.20260168) <!-- to be updated -->

---

## 🚀 What is DTQEM?

**DTQEM (Decoherence from Time‑scale Quantum Effective Mismatch)** proposes a new physical mechanism for quantum decoherence:

> *The coherence between quantum states decays when there is a discrepancy between the proper time of the particle and the reference time of the measuring device.*

The core equation (D0 – baseline model) is:

\[
\boxed{V_{\text{eff}} = V_{\text{source}}(d) \times e^{-\gamma_\phi \tau} \times e^{-|\Delta\tau|/\tau_c}}
\]

where:
- \(V_{\text{source}}(d)\) – source coherence (Van Cittert‑Zernike)
- \(e^{-\gamma_\phi \tau}\) – environmental decoherence (Lindblad)
- \(e^{-|\Delta\tau|/\tau_c}\) – **DTQEM hypothesis** (proper‑time decoherence)
- \(\Delta\tau = \tau \times (1 - 1/\gamma)\), \(\tau = a/v\), \(\gamma = 1/\sqrt{1-v^2/c^2}\)
- \(\tau_c\) – the only free parameter (proper‑time coherence constant)

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
```

---

🔬 What makes v44.0 special?

Feature Description
Unified framework Same equation applied to double‑slit, qubit, and Zeeman systems
Interactive dashboards ipywidgets + matplotlib – zero overlap between sliders and plots
Dark theme Professional GitHub‑style dark interface
Real‑time updates All plots update instantly when parameters change
Export & reset Save figures as PNG, restore default values
Colab ready Works in Google Colab and Jupyter notebooks
D0 baseline Simple exponential decoherence (no β, no τ_sat, no τ_c(γ))
---

📊 The codes of v44.0

```
📁 codes/
│
├── 📁 double_slit/
│   ├── dtqem_double_slit_forward_v44.py      # Forward model (interactive)
│   ├── dtqem_double_slit_forward_v44.ipynb   # Notebook version
│   ├── dtqem_double_slit_inverse_v44.py      # Inverse model (parameter extraction)
│   └── dtqem_double_slit_inverse_v44.ipynb   # Notebook version
│
├── 📁 qubit/
│   ├── dtqem_qubit_decoherence_v44.py        # Qubit decoherence simulator
│   └── dtqem_qubit_decoherence_v44.ipynb     # Notebook version
│
├── 📁 zeeman/
│   ├── dtqem_zeeman_effect_v44.py            # Zeeman effect simulator
│   └── dtqem_zeeman_effect_v44.ipynb         # Notebook version
│
├── 📁 wave/
│   └── dtqem_wave_code_v44.py                # Core wave functions
│
└── dtqem_all_v44.py                          # Optional: all-in-one collector
```

# File Description
1 dtqem_double_slit_forward_v44.py Double‑slit interference – forward model (interactive)
2 dtqem_double_slit_inverse_v44.py Double‑slit – inverse model (parameter extraction)
3 dtqem_qubit_decoherence_v44.py Qubit decoherence simulator
4 dtqem_zeeman_effect_v44.py Zeeman effect simulator
5 dtqem_wave_code_v44.py Core wave functions and propagation

All codes share:

· The same core equation (D0)
· ipywidgets sliders (outside the figure)
· Zero overlap layout
· Dark theme styling
· Reset & Export buttons

---

🖥️ Interactive dashboards – what you can explore

1. Double‑slit interference (dtqem_double_slit_forward_v44.py)

· Adjust slit separation, wavelength, screen distance, source size
· Change particle velocity, τ_c, γ_φ
· See the interference pattern evolve in real time
· Watch V_eff decompose into V_source, V_env, V_dtqem

2. Qubit decoherence (dtqem_qubit_decoherence_v44.py)

· Watch coherence decay as V_eff(t) = exp(-γ_φ·t) × exp(-|Δτ(t)|/τ_c)
· See the Bloch sphere projection (xy plane)
· Explore V_eff vs velocity at fixed time
· Heatmap of coherence in (τ_c, β) space

3. Zeeman effect (dtqem_zeeman_effect_v44.py)

· Zeeman splitting between sub‑levels m₁ and m₂
· Δτ(t) = Δω·t = (|ΔE|/ħ)·t
· See energy levels vs magnetic field B
· V_eff vs B at fixed time
· Coherence heatmap V_eff(B, t)

---

📈 Predictions (testable)

Prediction Description Status
P1 Increasing particle velocity reduces V_eff ✅ Testable
P2 τ_c (if exists) ≤ 10⁻¹⁵ s ✅ Testable
P3 Detector material may affect V_eff ✅ Testable
P4 Different velocities → faster entanglement loss ✅ Proposed

---

🚀 Quick start

1. Clone the repository

```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
```

2. Install dependencies

```bash
pip install numpy matplotlib ipywidgets scipy
```

3. Run any dashboard (in Jupyter or Colab)

```python
# For double‑slit forward model
run codes/double_slit/dtqem_double_slit_forward_v44.py

# For qubit decoherence
run codes/qubit/dtqem_qubit_decoherence_v44.py

# For Zeeman effect
run codes/zeeman/dtqem_zeeman_effect_v44.py
```

Or open the .ipynb files directly in Google Colab (upload first).

---

📌 Version history

Version Focus Key result File
v44.0 Unified DTQEM framework Double‑slit + Qubit + Zeeman with D0 equation All codes in codes/
v38.2 Hα Zeeman inversion Extract B with 100% bootstrap success dtqem_v38_2.py
v34.2 Double‑slit inversion Observer strength E, slit separation d dtqem_v34_2.py
v22.0 Self‑calibrating spectral inversion Recover T, α, E from Balmer linewidths dtqem_v22_inversion.py

All versions share the same foundational hypothesis:
The observer does not change the system’s energy; it only destroys coherence via proper‑time discrepancy.

---

👥 Contributors & Acknowledgments

Project Creator:

· Berramdane Reddouane (Morocco)

Core Contributors (AI Assistants):

· Gemini (Google) – Theoretical discussions, D3 proposal
· DeepSeek (深度求索) – Philosophical insights, critical analysis
· Claude (Anthropic) – Code writing (V44.0 series)

Special Thanks:

· "Clore" (Anonymous colleague) – Mathematical improvement proposals (D1–D6 models)

---

📝 License

This project is licensed under the MIT License – see the LICENSE file for details.

---

📖 Citation

If you use DTQEM in your research, please cite:

```bibtex
@software{berramdane2026dtqem,
  title = {DTQEM: A Physical Hypothesis Linking Quantum Decoherence to Proper-Time Discrepancy},
  author = {Berramdane, Reddouane},
  contributors = {Gemini, DeepSeek, Claude},
  year = {2026},
  month = {05},
  version = {44.0},
  publisher = {GitHub},
  url = {https://github.com/reddoma742/Davisson-Germer-DTQEM.git}
}
```

---

🙏 Final word

From philosophy to equations.
From equations to code.
From code to interactive dashboards.
From dashboards to a stable release.

DTQEM v44.0 is ready for testing, criticism, and future expansion.
