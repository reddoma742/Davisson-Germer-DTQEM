## v17.0-C (2026-05-29) â€“ Final Coherence Model

**Final simplified release:** compact exponential model for the quantum coherence factor C (equivalent to visibility V) in path-interference experiments.

### Core equation
\[
C = C_0 \, \exp\!\left(-a_{\mathrm{path}} I_{\mathrm{path}} - a_{\mathrm{temp}}\, \frac{\max(0, T_{\mathrm{env}}-T_{\mathrm{ref}})}{T_{\mathrm{ref}}}\right)
\]

### Calibrated parameters
- \(C_0 = 0.3675\)
- \(a_{\mathrm{path}} = 1.6968\)
- \(a_{\mathrm{temp}} = 0.8055\)
- \(T_{\mathrm{ref}} = 300\,\mathrm{K}\)

### Performance
- In-sample: RÂ² = 0.9679, RMSE = 0.0202
- LOOCV: RÂ² = 0.9356, RMSE = 0.0286
- Number of data points: 8
- Number of free parameters: 3

### Key points
- The model was selected as the final recommended baseline because it gives the best balance between predictive accuracy and parsimony.
- Earlier more complex variants were tested, including a nonlinear exponent extension, but they did not improve the out-of-sample trade-off enough to replace the simpler form.
- The model remains physically interpretable and easy to reproduce.
- The code is Zenodo-ready and suitable for archival release.

### Physical interpretation
- Increasing which-path information suppresses coherence exponentially.
- Thermal excess above the reference temperature further suppresses coherence.
- The model is consistent with the general complementarity picture where coherence decreases as path distinguishability increases.

### Intended files
- `dtqem_v17.0-C_coherence.py`
- `README_v17_0C.md`
- `whitepaper_v17_0C.md`

### Note
This version is a phenomenological baseline, not a first-principles derivation.

# DTQEM â€“ HISTORY

## v63.1 (2026-05-29) â€“ Phenomenological Scaling Model for Decoherence Time \(\tau_c\)

**White paper draft update:** clarified the phenomenological scaling law for the decoherence time \(\tau_c\), the logarithmic-slope inverse extraction method, and the current interpretation limits.

### Core model
\[
V_{\mathrm{eff}} = \exp(-\gamma_\phi T_{\mathrm{eff}})\,\exp\!\left(-\frac{|\Delta\tau|}{\tau_c}\right)
\]
\[
\tau_c = \frac{\tau_{c0}}{m^{\beta}\,(v/c)^{\delta}\,(1+\zeta N)}
\]

### Main points
- \(\tau_c\) is treated as an **effective phenomenological scale**, not a universal constant.
- Inverse extraction uses multiple \(|\Delta\tau|\) points and a linear fit of \(\ln V_{\mathrm{eff}}\) versus \(|\Delta\tau|\).
- Synthetic calibration yields effective values such as \(\beta \approx 0.44\), \(\delta \approx 0.33\), and \(\zeta \approx 0.005\).
- The draft explicitly states limitations and the need for real experimental validation.

### Intended files
- `DTQEM_v63.1.py`
- `WHITE_PAPER_v63_1.md`
- `CITATION.cff`

---

## v63.0 (2026-05-25) â€“ Phenomenological Scaling Model for Decoherence Time \(\tau_c\)

**Working model:** phenomenological scaling law for decoherence time \(\tau_c\) calibrated on synthetic interferometry data.

### Core model
\[
V_{\mathrm{eff}} = \exp(-\gamma_\phi T_{\mathrm{eff}})\times \exp\left(-\frac{|\Delta\tau|}{\tau_c}\right)
\]
\[
\tau_c = \frac{\tau_{c0}}{m^{\beta}\,(v/c)^{\delta}\,(1+\zeta N)}
\]

### Key features
- Stable inverse extraction by logarithmic slope.
- Pressure, mass, velocity, temperature, and complexity dependence proposed as testable predictions.
- CSV-based support for synthetic and real data.

### Limitations
- Phenomenological, not first-principles.
- Calibration synthetic, experimental validation pending.
- \(\tau_{c0}\) is environment-dependent.

---

## v46.0 (2026-05-24) â€“ Mach-Zehnder Interferometer (Stable Release)

**Major release:** first stable implementation of DTQEM for a Mach-Zehnder interferometer.

### Core equation
\[
\Delta\tau = \left|\frac{L_1}{v_1\gamma_1} - \frac{L_2}{v_2\gamma_2}\right|,\qquad
T_{\mathrm{eff}} = \frac{\tau_1+\tau_2}{2},\qquad
V_{\mathrm{eff}} = e^{-\gamma_\phi T_{\mathrm{eff}}}e^{-|\Delta\tau|/\tau_c}
\]

### Main features
- Proper-time mismatch.
- Symmetry checks.
- Stable visibility bounds.
- Mass-dependent extensions explored in demos.

### Code modules
| File | Description |
|------|-------------|
| `dtqem_mach_zehnder_v46.py` | Core model with 6 sanity checks and plotting utilities |
| `c70_benchmark.py` | Benchmark against C70 interferometry data |
| `dtqem_mass_effect_demo_v3.py` | Mass-dependent \(\tau_c\) demo |

---

## v44.0 (2026-05-22) â€“ Unified Quantum Decoherence Framework

**First unified release:** core D0 model applied to three physical systems.

### Core equation
\[
V_{\mathrm{eff}} = V_{\mathrm{source}}(d)\times e^{-\gamma_\phi\tau}\times e^{-|\Delta\tau|/\tau_c}
\]

### Code modules
| File | Description |
|------|-------------|
| `dtqem_double_slit_forward_v44.py` | Double-slit forward model (interactive) |
| `dtqem_double_slit_inverse_v44.py` | Inverse model (DE + L-BFGS-B + Bootstrap) |
| `dtqem_qubit_decoherence_v44.py` | Qubit decoherence simulator |
| `dtqem_zeeman_effect_v44.py` | Zeeman effect simulator |
| `dtqem_wave_code_v44.py` | Core wave functions and propagation |

### Predictions
- Increasing velocity reduces \(V_{\mathrm{eff}}\).
- \(\tau_c\) on femtosecond scale in the synthetic regime.
- Detector material may affect visibility.
- Decoherence rate scales linearly with magnetic field in the Zeeman module.

### Notes
- Unified D0 framework.
- MIT license for the released codebase.
- Zenodo DOI assigned for the release.

---

## v38.2 (2026-05-19) â€“ Hydrogen Balmer-alpha Zeeman Inversion

**Stable release:** major improvements in bootstrap and model selection for H\(\alpha\) Zeeman inversion.

### Key improvements
- Multi-start bootstrap with robust acceptance criteria.
- Realistic uncertainty estimation from bootstrap distributions.
- Automatic model selection between single and triplet profiles.
- Monte Carlo stress tests across multiple synthetic scenarios.

### Results
- Bootstrap success rate reached 100% in several tests.
- Reliable recovery of magnetic field strength across tested scenarios.
- Detection limit approximately 0.15 T in the synthetic benchmark.

### Files
- `dtqem_v38_2.py`
- `dtqem_v38_2_full.py`
- `CITATION.cff`
- `LICENSE`

---

## v34.2 (2026-05-18) â€“ Double-slit inversion with multi-start bootstrap

**Major improvements over v34.1:**
- Multi-start bootstrap per synthetic sample.
- Higher success rate for difficult inversions.
- Improved convergence handling and more realistic perturbations.

### Validation highlights
- Strong recovery of slit separation and observer strength under noise.
- Robustness improved substantially compared with v34.0.

### Files
- `dtqem_v34_2.py`
- `WHITE_PAPER_v34.md`
- `CITATION.cff`
- `LICENSE`

---

## v33.0 (2026-05-17) â€“ Production-grade robust inversion for Youngâ€™s double slit

### Major additions
- Physical interference + diffraction model.
- Fixed linear background measured independently.
- Wide parameter bounds for slit separation.
- Global + local optimisation.
- AICc-based selection for optional phase shift.
- Bootstrap uncertainty quantification.
- Residual diagnostics and boundary warnings.

### Results
- Accurate recovery of slit separation.
- Stable estimation of observer strength.
- Residuals close to white.

---

## v22.0 (2026-05-16) â€“ Self-calibrating spectral inversion

### Major additions
- Three-stage inversion for Balmer-series linewidths.
- Recovery of temperature, dephasing coefficient, and observer strength.
- Bootstrap-based uncertainty quantification.
- Consistency checks for calibrated \(\alpha\).

---

## v20.0 (2026-05-15) â€“ Two-qubit entanglement under thermal relaxation and dephasing

### Major additions
- Full Lindblad model with thermal bath.
- Concurrence, CHSH, entanglement lifetime.
- Multiple qubit platform database.
- Regime classification and publication-ready plots.

---

## v19.0 (2026-05-15) â€“ Exact analytical single-qubit decoherence model

### Major additions
- Closed-form solution for the probability dynamics.
- Decoherence time \(\tau_{\mathrm{coh}} = 1/(\gamma E)\).
- Critical observer strength \(E_{\mathrm{crit}}\).
- Numerical validation against direct integration.

---

## v18.0 (2026-05-14) â€“ Two-qubit local dephasing and entanglement

### Major additions
- Local dephasing on one qubit.
- Concurrence calculation.
- Analytical CHSH inference.
- Zeno-like entanglement suppression with observer strength.

---

## v17.0 (2026-05-13) â€“ Photon wave-particle simulation

### Major additions
- 650 nm photon simulation.
- FFT-based frequency extraction.
- Observer strength modulating pure dephasing only.
- Clear probability-vs-time visualization.

---

## v16.0 (2026-05-12) â€“ Massive-particle tunneling under continuous measurement

### Major additions
- Fixed Hamiltonian with dephasing.
- Numerical verification of the quantum Zeno effect.
- Observation suppresses tunneling.

---

## Legacy versions

| Version | Focus | Key result |
|---------|-------|------------|
| v46.0 | Mach-Zehnder interferometer | Stable proper-time model |
| v44.0 | Unified decoherence framework | Three-system baseline |
| v38.2 | H\(\alpha\) Zeeman inversion | Robust bootstrap and selection |
| v34.2 | Double-slit inversion | Multi-start bootstrap |
| v33.0 | Double-slit robust inversion | AICc + bootstrap + diagnostics |
| v22.0 | Spectral inversion | Three-stage calibration |
| v20.0 | Two-qubit entanglement | Thermal + dephasing model |
| v19.0 | Analytical single-qubit model | Closed-form solution |
| v18.0 | Local dephasing entanglement | CHSH and concurrence |
| v17.0 | Photon wave-particle model | FFT and observer dephasing |
| v16.0 | Continuous-measurement tunneling | Zeno-effect demonstration |

*Earlier draft histories and intermediate notebooks are archived in the repository history and legacy folders.*

---

## Roadmap

| Version | Focus | Status |
|---------|-------|--------|
| v63.1 | Phenomenological scaling model for \(\tau_c\) | Working draft |
| v63.0 | Decoherence-time scaling law | Working model |
| v46.x | Experimental mass-dependent \(\tau_c\) | In progress |
| v47.0 | Inverse fitting on experimental data | Planned |
| v48.0 | Non-Markovian extensions | Future |

---

**End of history.**
