DTQEM – Dual‑Time Quantum Entanglement Model

A unified open‑source framework for simulating open quantum systems under measurement – from wave‑particle duality to self‑calibrating spectral inversion and robust double‑slit inversion.

https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey
https://img.shields.io/badge/python-3.8+-blue.svg
https://zenodo.org/badge/DOI/10.5281/zenodo.20218379.svg

---

🚀 Latest stable release – v23.0 (2026‑05‑17)

Robust double‑slit inversion with linear background & bootstrap uncertainty

This release completes the systematic development of a production‑grade inverse model for the Young double‑slit experiment.
From the raw interference pattern, the code extracts:

· Observer strength E – the quantum parameter that quantifies how strongly the measurement destroys coherence.
· Slit separation d – the classical geometric parameter, recovered with < 0.2 % error.
· Peak intensity I_0 – together with realistic bootstrap confidence intervals.

🔬 What is new in v23.0?

Feature Description
Physically correct model I(x)=I_0\bigl[(1-E)\cos^2\bigl(\frac{\pi d x}{\lambda L}+\phi\bigr)+E\bigr]\,\text{sinc}^2\bigl(\frac{\pi a x}{\lambda L}\bigr)+B_0+B_1x
Fixed background The linear background B_0+B_1x is now measured independently (laser‑off) and kept fixed – this breaks the detrimental correlation with E.
Wide parameter bounds The slit distance d is always searched in [1\ \mu\mathrm{m},\;2\ \mathrm{mm}], independent of the FFT initial guess.
Global + local optimisation Differential evolution (40 iterations) followed by L‑BFGS‑B guarantees that the true global minimum is found.
Automatic model selection AICc decides whether a phase shift \phi is needed. For clean data the simple model (without \phi) is always preferred.
Bootstrap uncertainty 150‑200 synthetic Poisson samples provide 95 % confidence intervals for I_0, d and E.
Complete diagnostics Residual analysis (mean, standard deviation, correlation with x) and boundary‑check warnings.

📊 Performance summary (synthetic data with 1 % Poisson noise)

Parameter True value Recovered value 95 % confidence interval Relative error
d 500.00 μm 499.34 μm [497.9 μm, 500.6 μm] 0.13 %
E 0.200 0.1903 [0.1803, 0.2095] 4.9 %
I_0 100.0 103.25 [102.1, 106.3] 3.3 %

· Reduced \chi^2_{\text{red}} = 1.08 (ideal value = 1)
· Residuals are white (correlation with x = 0.0068)
· AICc unambiguously selects the model without an ad‑hoc phase shift

Conclusion: The double‑slit inversion is now numerically robust, physically faithful and ready for real experimental data.

---

📌 Evolution of the framework

Version Focus Key result File
v23.0 Double‑slit inversion with linear background Recover E, d, I_0 with bootstrap CIs dtqem_v33_inversion.py
v22.0 Self‑calibrating spectral inversion Recover T, \alpha, E from Balmer linewidths dtqem_v22_inversion.py
v20.0 Two‑qubit entanglement with temperature Entanglement lifetimes for real qubits dtqem_20_entanglement.py
v19.0 Baseline analytical model Exact closed‑form solution for P(E,t) analytical_model_v19.py
v18.0 Two‑qubit entanglement under local dephasing Concurrence decay + inferred CHSH concurrence_entanglement.py
v17.0 Photon wave‑particle duality (650 nm) Frequency extraction via FFT, \nu_0 = 461\ \mathrm{THz} photon_wave_particle.py
v16.0 Massive‑particle tunneling Numerical verification of Zeno effect tunneling.py

All versions share the same foundational hypothesis:

The observer does not change the system’s energy; it only destroys coherence via pure dephasing (\sigma_z Lindblad operator).
The dimensionless observer strength E controls the dephasing rate: \gamma_{\phi} = \gamma_0\;E.

---

🚀 Quick start (v23.0 double‑slit inversion)

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

Create a CSV file with two columns:
x (m), I (a.u.)

4. Run the inversion script

Edit dtqem_v33_inversion.py to point to your data and set the fixed parameters:

```python
result = run_v33(
    x, I_meas,
    lam=650e-9,        # laser wavelength (m)
    L=1.0,             # screen distance (m)
    a=80e-6,           # single‑slit width (m), optional
    fixed_B0=4.8,      # background measured with laser off
    fixed_B1=185.0,    # linear background slope (a.u./m)
    output_prefix="my_experiment"
)
```

The script will:

· automatically select the best model (with/without \phi),
· compute bootstrap confidence intervals,
· generate a summary text, a CSV table and a publication‑ready plot.

---

🧪 Physical interpretation of E

In the DTQEM picture, the observer strength E ( ∈ [0,1]) quantifies how strongly the measurement process destroys coherence:

· E = 0 → no observer, full quantum coherence (visibility V = 1).
· E = 1 → maximal measurement, total loss of interference (visibility V = 0).

The dephasing rate is \gamma_{\phi} = \gamma_0\;E, where \gamma_0 is a fixed material/geometry constant.
Because the Hamiltonian itself is independent of E, the model cleanly separates unitary evolution from the effect of observation – an essential requirement for any consistent quantum‑measurement theory.
