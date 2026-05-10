# DTQEM – Unified Framework for Open Quantum Systems (v14.0)

**Davisson–Germer | Quantum Tunneling | Schottky Effect | Balance Condition V=D | Resonance Collapse**

[![License: DTQEM Research & Educational](https://img.shields.io/badge/License-DTQEM%20Research%20%26%20Educational-blue)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20090038.svg)](https://doi.org/10.5281/zenodo.20090038)

## ⚠️ License Change Notice (v13.0+)

Starting from version 13.0, DTQEM is released under the **DTQEM Research & Educational License** (see [`LICENSE`](LICENSE)).  

**Commercial use is not permitted** without explicit written permission.  
Academic, educational, and non‑commercial research use is free and encouraged.

---

This repository provides a full numerical framework for simulating **open quantum systems** under the **Time‑Sovereignty** hypothesis.

## 🔬 Core Applications

- **Davisson–Germer experiment** → `examples/davisson_germer/`
- **Quantum tunneling** with Zeno effect and entropy → `examples/tunneling/`
- **Schottky effect** (thermionic emission) → `examples/schottky/`

## ⚖️ New Analytical Results (v14.0)

1.  **Wave‑particle balance (pure dephasing)**  
    \(\boxed{\gamma_{\phi0}\,t_{\text{obs}} = 2\ln(\tan\theta)},\qquad \theta>45^\circ\)

2.  **Resonance collapse from |+⟩**  
    \(\boxed{t_{\text{collapse}} = -\frac{\ln\varepsilon}{2\gamma}}\) or \(\boxed{\gamma\,t_{\text{collapse}} = -\frac{\ln\varepsilon}{2}}\)

## 🧪 Experimental Codes (Hypothetical / Exploratory)

- `experiments/balance_condition.py` – interactive verification of `V=D`
- `experiments/tunneling_apparent_time.py` – test for negative time (result: none found)
- `experiments/blp_measure.py` – Markovianity test (BLP = 0)

## 📚 Documentation

- Full white paper: [`docs/WHITEPAPER_v14.0.md`](docs/WHITEPAPER_v14.0.md)
- Peer discussion notes: [`docs/PEER_DISCUSSION.md`](docs/PEER_DISCUSSION.md)

## 🚀 Getting Started

```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
pip install -r requirements.txt
