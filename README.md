DTQEM v34.2 – Dual‑Time Quantum Entanglement Model

An open‑source framework for simulating open quantum systems under measurement – from wave‑particle duality to double‑slit inversion with robust bootstrap uncertainty.

https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey
https://img.shields.io/badge/python-3.8+-blue.svg
https://zenodo.org/badge/DOI/10.5281/zenodo.20260168.svg

---

🚀 Latest stable release – v34.2 (double‑slit inversion with multi‑start bootstrap)

Robust inversion of Young’s double‑slit experiment with linear background, AICc model selection and bootstrap confidence intervals that succeed in >98 % of cases – even under high Poisson noise or slightly non‑linear backgrounds.

From a single interference pattern, the code extracts:

· Observer strength E – the quantum parameter that quantifies measurement‑induced decoherence (pure dephasing).
· Slit separation d – the classical geometry, recovered with error < 0.2 %.
· Peak intensity I_0 – together with full bootstrap uncertainties (standard deviation and 95 % CI).

---

🔬 What makes v34.2 special?

Feature Description
Physically correct model I(x)=I_0\bigl[(1-E)\cos^2\bigl(\frac{\pi d x}{\lambda L}+\phi\bigr)+E\bigr]\,\operatorname{sinc}^2\bigl(\frac{\pi a x}{\lambda L}\bigr)+B_0+B_1x
Fixed linear background B_0 and B_1 are measured independently (laser off) – this breaks the harmful correlation with E.
Global optimisation Differential evolution (60 generations) followed by L‑BFGS‑B guarantees the true global minimum.
Automatic model selection AICc decides whether a phase shift \phi is needed. For clean data the simple model (no \phi) is always preferred.
Multi‑start bootstrap 3 local restarts per synthetic sample, starting from the original best fit. Success rate >98 % (often 100 %).
Complete diagnostics Residual analysis (mean, std, correlation with x) and boundary‑check warnings.

---

📊 Performance on synthetic data (Poisson noise)

Parameter True value Recovered value 95 % confidence interval Relative error
d 500.00 μm 499.76 μm [497.9 μm, 500.6 μm] 0.05 %
E 0.2000 0.2029 [0.1974, 0.2290] 1.5 %
I_0 100.0 100.12 [98.5, 101.7] 0.12 %

· Reduced \chi^2_{\text{red}} = 0.991 (ideal = 1)
· Residuals are white (correlation with x = −0.0248)
· Bootstrap success rate: 99.3 % (149/150 samples)
· AICc unambiguously selects the model without an ad‑hoc phase shift.

Additional validation experiments (all with 100 % bootstrap success):

· Phase shift \phi = 0.3 rad → recovered \phi = 0.3083 rad, model with \phi correctly chosen.
· Quadratic background (B_2=5000) → d error = 0.03 %, \chi^2_{\text{red}}=0.978.
· High Poisson noise (5 % at peak) → d error = 0.21 %, E error = 4.7 %, CI contains true value.

Conclusion: The double‑slit inversion is now numerically robust, physically faithful and ready for real experimental data – with uncertainty estimates you can trust.

---

📌 Evolution of the framework

Version Focus Key result File
v34.2 Double‑slit inversion with multi‑start bootstrap Recover E, d, I_0 with >98 % bootstrap success dtqem_v34_2.py
v34.0 Double‑slit inversion (linear background) Bootstrap success improved to ~88 % dtqem_v34_inversion.py
v33.0 Double‑slit inversion (linear background) First stable inversion with AICc dtqem_v33_inversion.py
v22.0 Self‑calibrating spectral inversion (hydrogen) Recover T, \alpha, E from Balmer linewidths dtqem_v22_inversion.py
v20.0 Two‑qubit entanglement with temperature Entanglement lifetimes for real qubits dtqem_20_entanglement.py
v19.0 Baseline analytical model Exact closed‑form solution for P(E,t) analytical_model_v19.py
v18.0 Two‑qubit entanglement under local dephasing Concurrence decay + inferred CHSH concurrence_entanglement.py
v17.0 Photon wave‑particle duality (650 nm) Frequency extraction via FFT, \nu_0 = 461\ \mathrm{THz} photon_wave_particle.py
v16.0 Massive‑particle tunneling Numerical verification of Zeno effect tunneling.py

All versions share the same foundational hypothesis:

· The observer does not change the system’s energy; it only destroys coherence via pure dephasing (\sigma_z Lindblad operator).
· The dimensionless observer strength E controls the dephasing rate: \gamma_{\phi} = \gamma_0\;E.

---

🚀 Quick start (v34.2 double‑slit inversion)

1. Clone the repository

```bash
git clone https://github.com/reddoma742/Davisson-Germer-DTQEM.git
cd Davisson-Germer-DTQEM
```

2. Install dependencies

```bash
pip install numpy scipy matplotlib
```

3. Prepare your experimental data

Create a CSV file with two columns: x (m), I (a.u.)

4. Run the inversion script

Edit dtqem_v34_2.py or use it as a module:

```python
from dtqem_v34_2 import run_v34
import numpy as np

# Load your data
x = np.loadtxt("my_data.csv", delimiter=",")[:, 0]
I = np.loadtxt("my_data.csv", delimiter=",")[:, 1]

# Fixed experimental parameters (measure background with laser off!)
result = run_v34(
    x, I,
    lam=650e-9,           # laser wavelength (m)
    L=1.0,                # screen distance (m)
    a=80e-6,              # single‑slit width (m) – optional, set None to disable envelope
    fixed_B0=4.8,         # constant background (a.u.)
    fixed_B1=185.0,       # linear background slope (a.u./m)
    use_global=True,      # enable differential evolution (recommended)
    n_bootstrap=150,      # number of bootstrap samples
    bootstrap_n_restarts=3,   # local restarts per sample (default 3)
    output_prefix="my_experiment"
)

print(f"d = {result.d_um:.2f} µm ± {result.d_std:.3f} µm")
print(f"E = {result.E:.5f} ± {result.E_std:.5f}")
print(f"95% CI for E: {result.E_ci95}")
```

The script will:

· Automatically select the best model (with/without \phi),
· Compute bootstrap confidence intervals (with >98 % success),
· Generate a summary table, a CSV file, and a publication‑ready plot.

---

🧪 Physical interpretation of E

In the DTQEM picture, the observer strength E \in [0,1] quantifies how strongly the measurement process destroys coherence:

· E = 0 → no observer, full quantum coherence (visibility V = 1).
· E = 1 → maximal measurement, total loss of interference (visibility V = 0).

The dephasing rate is \gamma_{\phi} = \gamma_0\;E, where \gamma_0 is a fixed material/geometry constant.
Because the Hamiltonian itself is independent of E, the model cleanly separates unitary evolution from the effect of observation – an essential requirement for any consistent quantum‑measurement theory.

---

📄 Citation

If you use DTQEM in your research, please cite:

R. Berramdane, DTQEM v34.2: A robust double‑slit inversion framework with multi‑start bootstrap, Zenodo (2026).
DOI: 10.5281/zenodo.20260168

---

📜 License

This project is licensed under the Creative Commons Attribution‑NonCommercial 4.0 International license – see the LICENSE file for details.

---

Enjoy exploring quantum interference – reliably!
Reddouane Berramdane (DTQEM Team)
