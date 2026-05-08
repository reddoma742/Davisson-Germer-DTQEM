markdown
![Berramdane Model Result](images/Davisson_Germer_DTQEM.jpg)


# Davisson-Germer-DTQEM
Simulation of electron crystal diffraction (Davisson–Germer) linked to the DTQEM decoherence model. Computes Bragg angles, visibility V, distinguishability D, complementarity V²+D², and temperature‑dependent γ_t. A bridge between classical wave interference and quantum self‑consistent temporal dynamics.
# Davisson–Germer + DTQEM: Decoherence, Temperature, Bragg Peaks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/Davisson-Germer-DTQEM/blob/main/Davisson_Germer_DTQEM.ipynb)

**Full simulation of electron diffraction on a crystal (Davisson–Germer) linked to the DTQEM model.**  
Computes Bragg angles, visibility V, distinguishability D, complementarity V²+D², and decoherence rate γ_t auto‑calibrated from peak width. Includes temperature‑dependent peak broadening and γ_t. Fully vectorized, interactive, with export to CSV.

## ✨ Features

- ✅ **Davisson–Germer diffraction** – Bragg peaks for a nickel crystal (or any d‑spacing)
- ✅ **DTQEM linkage** – maps scattering angle φ to launch angle θ, then computes V and D
- ✅ **Auto‑calibration of γ_t** – from the width of the main diffraction peak
- ✅ **Temperature effect** – peak width increases with T, which increases γ_t and reduces V
- ✅ **Visualisation** – intensity pattern, V(φ), D(φ), complementarity circle, θ(φ)
- ✅ **Widgets & CSV export** – interactive sliders, save results

## ⚙️ Requirements

- Python 3.8+
- `numpy`, `matplotlib`, `scipy`, `ipywidgets` (optional for GUI)

Install with:
```bash
pip install numpy matplotlib scipy ipywidgets pandas
