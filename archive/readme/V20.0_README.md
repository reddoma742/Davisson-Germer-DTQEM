DTQEM – Dual-Time Quantum Entanglement Model

A unified open‑source framework for simulating open quantum systems under measurement – from wave‑particle duality to entanglement decay under temperature and local dephasing.

https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey
https://img.shields.io/badge/python-3.8+-blue.svg
https://zenodo.org/badge/DOI/10.5281/zenodo.20208753.svg

---

🚀 Latest stable release – v20.0 (2026-05-15)

Two‑qubit entanglement decay under temperature and local dephasing
Fixed Hamiltonian · Pure dephasing  L = \sqrt{\gamma_{\phi0} E_{\text{ext}}}\,(\sigma_z \otimes I)  · Thermal relaxation (T₁)

The simulation starts from the Bell state |\Phi^+\rangle and computes the concurrence C(t) and CHSH parameter S(t) as functions of time for a given qubit technology, temperature, and observer strength. Using experimental parameters for a superconducting transmon, we obtain the entanglement lifetime \tau_{\text{ent}}.

Key results (Superconducting Transmon, T_1 = T_2 = 1.68 ms):

T (K) E_{\text{ext}} \tau_{\text{ent}} (μs) Effect
0.01 0 → 1 1000 → 623 -38% (Zeno)
0.1 0 → 1 965 → 523 -46% (Zeno)
1.0 0 → 1 95 → 88 -7%  (thermal dominates)

Experimental validation
For a single qubit, T_2 sets the scale: \tau_{\text{ent}} \approx T_2/2 for maximal measurement. Our simulated value at E=1 and 0.01 K is 0.623 ms, close to the predicted 0.84 ms.

👉 White Paper v20.0
👉 Python implementation

---

📌 Overview

DTQEM is an open‑source numerical and theoretical framework for open quantum systems under the temporal balance hypothesis: the observer does not change the system’s energy, it only destroys coherence via pure dephasing (σ_z Lindblad operators). Version 20.0 adds a full two‑qubit Lindblad model with thermal relaxation (T₁) and a database of five qubit types.

Version Focus Key result File
v20.0 Two‑qubit entanglement with temperature Entanglement lifetimes for real qubits dtqem_20_entanglement.py
v19.0 Baseline analytical model Exact closed‑form solution for P(E,t) analytical_model_v19.py
v18.0 Two‑qubit entanglement under local dephasing Concurrence decay + inferred CHSH concurrence_entanglement.py
v17.0 Photon wave‑particle duality (650 nm) Frequency extraction via FFT, ν₀ = 461 THz photon_wave_particle.py
v16.0 Massive‑particle tunneling Numerical verification of Zeno effect tunneling.py

All versions use a fixed Hamiltonian and a pure dephasing Lindblad operator L = \sqrt{\gamma_0 E_{\text{ext}}}\,\sigma_z.
Earlier phenomenological versions (v15 and below) that used a Hamiltonian depending on E_{\text{ext}} are now deprecated – v19.0 and v20.0 provide the correct physics.

---

🧪 Key physical insights from v20.0

· Entanglement lifetime \tau_{\text{ent}} decreases with increasing observer strength E_{\text{ext}} (Zeno effect)
· Temperature dramatically reduces entanglement: at 1 K the lifetime drops by >90% compared to 10 mK
· The simulated \tau_{\text{ent}} agrees well with experimental T_2 values, providing direct validation
· Exponential decay of concurrence is confirmed (\tau_{\text{fit}} from exponential fit matches \tau_{\text{ent}})

---

🚀 Quick start (v20.0)

1. Clone the repository

```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
```

2. Install dependencies

```bash
pip install numpy scipy matplotlib pandas
```

3. Run the simulation

```bash
python dtqem_20_entanglement.py
```

This will produce a summary table and a publication‑ready plot of concurrence vs time for three temperatures and four observer strengths.

4. Explore other qubit types

Edit the line qubit = 'Superconducting (Transmon)' in the script to try:

· 'Trapped Ion'
· 'Silicon Spin'
· 'Quantum Dot (hole)'

---
