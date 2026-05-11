# DTQEM – Unified Framework for Open Quantum Systems (v15.1)

**Davisson–Germer | Quantum Tunneling | Schottky Effect | Balance Condition V=D | Resonance Collapse**

[![License: DTQEM Research & Educational](https://img.shields.io/badge/License-DTQEM%20Research%20%26%20Educational-blue)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ⚠️ License Notice
DTQEM v14.0 is released under the **DTQEM Research & Educational License**. 
**Commercial use is strictly prohibited** without prior written authorization. 
Academic and non-commercial research use is encouraged.

---

## 🔬 Core Applications
This framework simulates open quantum systems under the **Time-Sovereignty** hypothesis:
- **Davisson–Germer Experiment:** Numerical validation of electron diffraction.
- **Quantum Tunneling:** Analysis of the Zeno effect and entropy stability at $\ln 2$.
- **Schottky Effect:** Modeling thermionic emission via internal resonance.

## ⚖️ Analytical Breakthroughs (v14.0)

1. **Wave-Particle Balance Condition:**
   $$\gamma_{\phi0}\,t_{obs} = 2\ln(\tan\theta), \quad \theta > 45^\circ$$

2. **Resonance Collapse Time:**
   $$t_{collapse} = -\frac{\ln\varepsilon}{2\gamma}$$

## 🧪 Experimental & Validation Labs
- `experiments/balance_condition.py`: Interactive verification of the $V=D$ threshold.
- `experiments/tunneling_apparent_time.py`: Numerical study on apparent tunneling time (Confirmed Zeno-dominant behavior; no negative time observed in current dephasing limit).
- `experiments/blp_measure.py`: Verification of Markovian dynamics (BLP = 0).

## 📚 Documentation
- **White Paper:** [`docs/WHITEPAPER_v14.0.md`](docs/WHITEPAPER_v14.0.md)
- **Conceptual Philosophy:** [`docs/PEER_DISCUSSION.md`](docs/PEER_DISCUSSION.md)

## 🚀 Installation & Usage
```bash
git clone [https://github.com/reddoma742/Davisson-Germer-DTQEM.git](https://github.com/reddoma742/Davisson-Germer-DTQEM.git)
cd Davisson-Germer-DTQEM
pip install -r requirements.txt
