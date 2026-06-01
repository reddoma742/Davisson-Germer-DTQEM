# DTQEM v17.0 – Unified Wave‑Particle Simulator

**From Temporal Balance to Photon‑Level Quantum Simulations**

[![License: DTQEM Research & Educational](https://img.shields.io/badge/License-DTQEM%20Research%20%26%20Educational-blue)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20159679.svg)](https://doi.org/10.5281/zenodo.20159679)


## What is DTQEM v17.0?

DTQEM v17.0 is an open‑source numerical framework for simulating **wave‑particle duality** under continuous measurement.  
It implements a **2×2 effective Lindblad model** where the **observer strength** \(E_{\mathrm{ext}}\) (0 → 1) controls only the **pure dephasing rate** (\(L = \sqrt{\gamma E}\,\sigma_z\)) without altering the system’s natural Hamiltonian.  
This is the correct physical description: the observer does not change the particle’s energy, only destroys coherence.

## Key features

- **Unified description** of quantum tunnelling (matter particles) and light (photons).
- **Accurate Zeno freeze**: at \(E=1\) the system reaches a maximally mixed state (\(P_{\mathrm{right}}=0.5\)) with zero coherence.
- **Frequency extraction** via FFT to recover the natural frequency of the system from the time‑dependent probability \(P(t)\).
- **High numerical stability** (error < 1% compared to analytical Rabi oscillations).

## Two simulation models

| File | Description |
|------|-------------|
| `temporal_balance.py` | Original model for massive particles (e.g. electrons in a double well). Uses \(H = \frac{\Delta}{2}\sigma_x\). |
| `photon_wave_particle.py` | New model for photons. Uses \(H = \frac{\hbar\omega_0}{2}\sigma_x\) (fixed energy). Observers only add dephasing. |

## Example results (photon model, ν₀ = 461 THz)

| \(E_{\mathrm{ext}}\) | \(P_{\mathrm{right}}(t_{\mathrm{final}})\) | Extracted ν (THz) |
|---------------------|--------------------------------------------|--------------------|
| 0.0                 | 0.1090                                     | 458.17             |
| 0.3                 | 0.4963                                     | 318.73             |
| 0.5                 | 0.5004                                     | 239.04             |
| 0.7                 | 0.5000                                     | 139.44             |
| 1.0                 | 0.5000 (mixed state)                       | (no coherent peak) |

> The extracted frequency follows the theoretical Rabi frequency \(\nu_0\) until decoherence dominates.

## Installation and usage

```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
pip install -r requirements.txt
python photon_wave_particle.py   # or temporal_balance.py
