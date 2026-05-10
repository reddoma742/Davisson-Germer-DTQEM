![Berramdane Model Result](images/Davisson_Germer_DTQEM.jpg)

# DTQEM – Unified Framework for Open Quantum Systems (v14.0)

**Davisson–Germer | Quantum Tunneling | Schottky Effect | Balance Condition V=D | Resonance Collapse**

[![License: DTQEM Research & Educational](https://img.shields.io/badge/License-DTQEM%20Research%20%26%20Educational-blue)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20090038.svg)](https://doi.org/10.5281/zenodo.20090038)

## ⚠️ License Change Notice (v13.0+)

Starting from version 13.0, DTQEM is released under the **DTQEM Research & Educational License** (see [`LICENSE`](LICENSE)).  

**Commercial use is not permitted** without explicit written permission.  
Academic, educational, and non‑commercial research use is free and encouraged.

For commercial licensing inquiries, contact: reddouane.berramdane@example.com

---

This repository provides a full numerical framework for simulating **open quantum systems** under the **Time‑Sovereignty** hypothesis (DTQEM). Version 14.0 introduces two novel analytical results validated to machine precision.

---

## 🔬 Core Applications

### 1. Davisson–Germer Experiment (Electron Diffraction)
- Computes Bragg angles, visibility `V`, distinguishability `D`, and complementarity `V²+D²`.
- Auto‑calibrates the decoherence rate `γ_t` from the diffraction peak width.
- **Location:** `examples/davisson_germer/`

### 2. Quantum Tunneling in a Double Well
- Particle in a symmetric double well (`H = (Δ/2)σₓ`) with Lindblad dissipation:
  - Pure dephasing: `L_φ = √γφ₀ σ_z`
  - Thermal relaxation: `L_± = √γ_rel σ_∓` (temperature dependent)
- Computes tunneling probability `P_right(t)`, `V(t)`, `D(t)` and first tunneling time.
- **Location:** `examples/tunneling/`

### 3. Schottky Effect (Field‑Enhanced Thermionic Emission)
- Two‑level system (metal |M⟩, vacuum |V⟩) with escape rate from Richardson‑Dushman formula.
- **Location:** `examples/schottky/`

---

## ⚖️ New Analytical Results (v14.0)

### Exact wave‑particle balance (pure dephasing)
From the Lindblad master equation with `σ_z⊗I` dephasing:
\[
\boxed{\gamma_{\phi0}\;t_{\text{obs}} = 2\ln(\tan\theta)},\qquad \theta > 45^\circ
\]
- Corrects the “magic angle” misconception – the balance angle depends on the product `γφ₀·t_obs`.
- Verified numerically with errors < 1e‑12.

### Resonance collapse from the maximally coherent state
Starting from `|+⟩ = (|0⟩+|1⟩)/√2` under pure dephasing `γ`:
\[
\boxed{t_{\text{collapse}} = -\frac{\ln\varepsilon}{2\gamma}},\qquad \gamma\,t_{\text{collapse}} = -\frac{\ln\varepsilon}{2}
\]
- For `ε = 0.05`, `γ·t_collapse ≈ 1.498` (expected 1.498).
- Confirmed for thresholds `0.05, 0.1, 0.01` within < 1.2% numerical error.

---

## 🧪 Experimental / Hypothetical Add‑ons

The folder `experiments/` contains exploratory codes. These are **not yet experimentally validated** but are shared to stimulate discussion.

- `balance_condition.py` – interactive verification of `V = D`.
- `negative_tunnel_time.py` – toy model for apparent negative tunneling time (hypothetical).
- `blp_measure.py` – BLP test for non‑Markovianity (result: BLP = 0 → Markovian).
- `tunneling_apparent_time.py` – **New**: test for negative apparent time with Gaussian pulses.  
  Result: `t_half ≥ τ_isolated` for all amplitudes → no negative time in current model.

All experimental files contain a clear disclaimer.

---

## 📁 Repository Structure
