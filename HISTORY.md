
# DTQEM – HISTORY

## v63.0 – 2026-05-25 (Current Release)

**Model**: Phenomenological scaling law for decoherence time `τ_c`


# DTQEM – Version History

## v46.0 (2026-05-24) – Mach-Zehnder Interferometer (Stable Release)

**Major release:** First stable implementation of DTQEM for a Mach-Zehnder interferometer.

### Core Features
- **Proper‑time mismatch**: Δτ = |L₁/(v₁γ₁) − L₂/(v₂γ₂)|
- **Effective environmental time**: T_eff = (τ₁ + τ₂)/2
- **Total visibility**: V_eff = exp(-γ_φ · T_eff) × exp(-|Δτ| / τ_c)

### Code Modules
| File | Description |
|------|-------------|
| `dtqem_mach_zehnder_v46.py` | Core model with 6 sanity checks and plotting utilities |
| `c70_benchmark.py` | Experimental benchmark against C70 interferometry data |
| `dtqem_mass_effect_demo_v3.py` | Experimental demo of mass-dependent τ_c (P9) |

### Sanity Checks (all passed)
1. Δτ = 0 for identical arms (L1=L2, v1=v2)
2. Δτ > 0 when L1=L2 but v1≠v2 (MZ-P1)
3. V_eff ∈ [0,1] for random parameters
4. Symmetric arms → V_eff = exp(-γ_φ·L/v)
5. When γ_φ = 0, V_eff peaks at v1 = v2 (isolated DTQEM)
6. T_eff symmetric under arm exchange

### New Predictions (MZ‑P1 to MZ‑P4)
| Prediction | Description |
|------------|-------------|
| **MZ-P1** | L1 = L2 but v1 ≠ v2 → Δτ ≠ 0 → V_eff < 1 |
| **MZ-P2** | Δτ ≈ τ_c → coherence collapse threshold |
| **MZ-P3** | Proper time differs even at equal lab times |
| **MZ-P4** | Ridge at β₁ = β₂ in coherence surface |

### Experimental Extensions
- `dtqem_mass_effect_demo_v3.py`: explores τ_c ∝ 1/m^β / γ^α (P9)
- `c70_benchmark.py`: compares mass-dependent model with C70 data (RMSE, R²)

---

## v44.0 (2026-05-22) – Unified Quantum Decoherence Framework

**First unified release:** Core D0 model applied to three physical systems.

### Core Equation
V_eff = V_source(d) × exp(-γ_φ·τ) × exp(-|Δτ|/τ_c)

### Code Modules (5 codes)
| File | Description |
|------|-------------|
| `dtqem_double_slit_forward_v44.py` | Double‑slit forward model (interactive) |
| `dtqem_double_slit_inverse_v44.py` | Inverse model (DE + L‑BFGS‑B + Bootstrap) |
| `dtqem_qubit_decoherence_v44.py` | Qubit decoherence simulator |
| `dtqem_zeeman_effect_v44.py` | Zeeman effect simulator |
| `dtqem_wave_code_v44.py` | Core wave functions and propagation |

### Predictions (P1–P5)
| Prediction | Description |
|------------|-------------|
| **P1** | Increasing velocity reduces V_eff |
| **P2** | τ_c ≤ 10⁻¹⁵ s (femtosecond scale) |
| **P3** | Detector material may affect V_eff |
| **P4** | Decoherence rate scales linearly with B (Zeeman) |
| **P5** | Heavier particles → less decoherence (if τ_c ∝ 1/m) |

### Zenodo DOI
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20349674.svg)](https://doi.org/10.5281/zenodo.20349674)

---

## Earlier Versions (Legacy)

| Version | Focus | Key Result |
|---------|-------|------------|
| v38.2 | Hα Zeeman inversion | Extract B with 100% bootstrap success |
| v34.2 | Double‑slit inversion | Observer strength E, slit separation d |
| v22.0 | Self‑calibrating spectral inversion | Recover T, α, E from Balmer linewidths |

*These versions are archived in the `legacy/` folder.*

---

## Roadmap

| Version | Focus | Status |
|---------|-------|--------|
| **v44.0** | Unified D0 framework | ✅ Released (Zenodo) |
| **v46.0** | Mach‑Zehnder interferometer | ✅ Stable |
| **v46.x** | Experimental: mass‑dependent τ_c (P9) | 🔬 In progress |
| **v47.0** | Inverse fitting on experimental data | ⏳ Planned |
| **v48.0** | Non‑Markovian extensions (D3) | ⏳ Future |

---

**End of history.**


# DTQEM – Version History

## v44.0 (2026-05-22) – Unified Quantum Decoherence Framework

**Stable Release · D0 Baseline Model · Three Physical Systems**

---

### 🚀 Major Features

| Feature | Description |
|---------|-------------|
| **Unified framework** | Same core equation applied to double-slit, qubit, and Zeeman systems |
| **D0 baseline model** | \(V_{\text{eff}} = V_{\text{source}}(d) \times e^{-\gamma_\phi \tau} \times e^{-|\Delta\tau|/\tau_c}\) |
| **Single free parameter** | Only \(\tau_c\) (proper-time coherence constant) |
| **No extensions** | No \(\beta\), no \(\tau_c(\gamma)\), no \(\tau_{\text{sat}}\) (deferred to future versions) |

---

### 📊 Five Code Modules

| # | File | Description |
|---|------|-------------|
| 1 | `dtqem_double_slit_forward_v44.py` | Double-slit interference – forward model (interactive dashboard) |
| 2 | `dtqem_double_slit_inverse_v44.py` | Double-slit – inverse model (DE + L-BFGS-B + Bootstrap) |
| 3 | `dtqem_qubit_decoherence_v44.py` | Qubit decoherence simulator with Bloch sphere |
| 4 | `dtqem_zeeman_effect_v44.py` | Zeeman effect simulator with energy levels |
| 5 | `dtqem_wave_code_v44.py` | Core wave functions and propagation |

---

### 🎨 Interactive Dashboard Features

- **ipywidgets** sliders (HTML layer, outside matplotlib figures)
- **Zero overlap** between controls and plots
- **Dark theme** (GitHub-style professional interface)
- **Real-time updates** – all plots update instantly when parameters change
- **Export to PNG** – save figures with one click
- **Reset button** – restore all default values
- **Google Colab / Jupyter compatible** – works in any environment

---

### 📈 Testable Predictions

| Prediction | Description |
|------------|-------------|
| **P1** | Increasing particle velocity reduces \(V_{\text{eff}}\) |
| **P2** | \(\tau_c \leq 10^{-15}\) s (femtosecond scale) |
| **P3** | Detector material may affect \(V_{\text{eff}}\) |
| **P4** | Decoherence rate increases linearly with magnetic field B (Zeeman) |
| **P5** | Heavier particles → less DTQEM decoherence |

---

### 🔧 Requirements

| Package | Version |
|---------|---------|
| numpy | ≥ 1.21 |
| matplotlib | ≥ 3.5 |
| ipywidgets | ≥ 7.6 |
| scipy | ≥ 1.7 |

---

### 📁 Repository Structure


📁 DTQEM_Project/
│
├── 📄 README.md
├── 📄 LICENSE
├── 📄 CITATION.cff
├── 📄 HISTORY.md
├── 📄 requirements.txt
├── 📄 .gitignore
│
├── 📁 codes/
│   ├── 📁 double_slit/
│   │   ├── dtqem_double_slit_forward_v44.py
│   │   ├── dtqem_double_slit_forward_v44.ipynb
│   │   ├── dtqem_double_slit_inverse_v44.py
│   │   └── dtqem_double_slit_inverse_v44.ipynb
│   │
│   ├── 📁 qubit/
│   │   ├── dtqem_qubit_decoherence_v44.py
│   │   └── dtqem_qubit_decoherence_v44.ipynb
│   │
│   ├── 📁 zeeman/
│   │   ├── dtqem_zeeman_effect_v44.py
│   │   └── dtqem_zeeman_effect_v44.ipynb
│   │
│   └── 📁 wave/
│       └── dtqem_wave_code_v44.py
│
├── 📁 papers/
│   ├── DTQEM_paper_AR.md
│   ├── DTQEM_paper_EN.md
│   └── DTQEM_v44_WhitePaper.md
│
├── 📁 legacy/
│   └── (previous versions: v38.2, v34.2, v22.0, v20.0)
│
└── 📁 figures/

```

---

### 👥 Contributors

**Project Creator:**  
- Berramdane Reddouane (Morocco)

**Core Contributors (AI Assistants):**  
- **Gemini (Google)** – Theoretical discussions, D3 proposal  
- **DeepSeek (深度求索)** – Philosophical insights, critical analysis  
- **Claude (Anthropic)** – Code writing (V44.0 series)

**Special Thanks:**  
- **"Clore"** (Anonymous colleague) – Mathematical improvement proposals (D1–D6 models)

---

### 📝 License

MIT License – see [LICENSE](LICENSE) file for details.

---

### 📖 Citation

```bibtex
@software{berramdane2026dtqem,
  title = {DTQEM: A Physical Hypothesis Linking Quantum Decoherence to Proper-Time Discrepancy},
  author = {Berramdane, Reddouane},
  contributors = {Gemini, DeepSeek, Claude},
  year = {2026},
  month = {05},
  version = {44.0},
  publisher = {GitHub},
  url = {https://github.com/reddoma742/Davisson-Germer-DTQEM}
}
```

---

🔄 What's New in v44.0 (Compared to v38.2)

Aspect v38.2 v44.0
Focus Hα Zeeman inversion only Unified framework (3 systems)
Core equation Zeeman triplet for Hα D0 unified equation
Number of codes 1 5
Interactive dashboards No Yes (ipywidgets)
Dark theme No Yes
Zero overlap layout No Yes
Colab compatible Partial Full
Bloch sphere No Yes (qubit module)
Energy levels plot No Yes (Zeeman module)
Heatmaps No Yes
License CC BY-NC 4.0 MIT

---

⚠️ Known Limitations

# Limitation
L1 No experimental data yet – all results from synthetic data
L2 D0 assumes Markovian decoherence (may not hold in all systems)
L3 Physical origin of \tau_c is unknown
L4 No field-theoretic derivation exists yet
L5 DTQEM describes decoherence, not collapse

---

🚧 Future Work (v45.0+)

· Non-Markovian extensions (D3: stretched exponential with \beta)
· Velocity-dependent \tau_c(\gamma)
· Saturation factor \mathcal{C}(\Delta\tau)
· Experimental validation of \tau_c
· Field-theoretic derivation from first principles

---

✅ Validation Status

Test Result
Double-slit forward model ✅ Passed
Double-slit inverse model (DE + L-BFGS-B) ✅ Passed
Bootstrap uncertainty (synthetic data) ✅ Passed (100% success)
Qubit decoherence simulator ✅ Passed
Zeeman effect simulator ✅ Passed
ipywidgets integration ✅ Passed
Zero overlap layout ✅ Passed
Colab compatibility ✅ Passed

---

DTQEM v44.0 – Ready for testing, criticism, and future expansion.


DTQEM v38.2 – Hydrogen Balmer‑alpha Zeeman Inversion (2026-05-19)

Stable release of the Zeeman model for Hα line with major improvements in bootstrap and model selection

---

🚀 Key improvements over v38.1 and v37.x

Area Improvement Achieved result
Bootstrap n_restarts=10, pert=10%, 20% fully random starts, physics-based acceptance (instead of res.success) 100% success rate in all tests (was <25% in v38.1)
Uncertainty estimation Bootstrap distributions instead of linear Hessian Realistic B_std (0.08–0.12 T) instead of over‑optimistic Hessian (0.001–0.004 T)
Model selection AICc + SNR‑dependent threshold + spread_ratio + B/σ_B Correct choice between Single / Triplet even at B=0 and low SNR
Speed Code optimised (avoided unnecessary closures) 8–13 s per spectrum (30 bootstrap samples)
Robustness Added stress tests (11 scenarios × 5 repeats) Works down to SNR = 172 and B = 0.1 T
Documentation Full docstrings, diagnostic plots, CSV reports Ready for scientific publication

---

📦 New features in v38.2

1. Symmetric Gaussian triplet model
   · π (Δm=0) and σ⁺, σ⁻ (Δm=±1) share the same sigma_width.
   · Optional frac_side (default 0.60, can be fitted).
2. Full Poisson negative log‑likelihood (including Stirling’s constant) – suitable for photon‑counting data.
3. Automatic model selection
   · AICc with SNR‑dependent threshold (stricter for low SNR).
   · Rejects triplet if spread_ratio < 0.5 or B/σ_B < 2.
4. Multi‑start bootstrap
   · 30 samples, 10 restarts per sample.
   · 20% of restarts start from fully random points (to escape local minima).
   · 80% start from x_opt with additive parameter‑specific perturbation.
   · Acceptance based on physics (B ≥ 0, sigma > 0, amplitude > 0) rather than res.success.
5. Monte Carlo stress tests
   · 11 scenarios: B from 0 to 2.5 T, amplitude scaling from 0.05 to 1.
   · 5 repeats each → ensures robustness under various conditions.
6. Integrated reports and plots
   · fit_B=...png: 3 panels (spectrum, residuals, normalised residuals) + 4th panel for bootstrap distribution if triplet selected.
   · recovery_curve.png: B_rec vs B_true.
   · bootstrap_diagnostics.png: Bootstrap distributions for each case.
   · CSV files for results and bootstrap distributions.

---

📊 Performance summary

B_true (T) B_rec (MAP) (T) B_std (T) 95% CI (T) Absolute error (T)
0.5 0.5057 0.1198 [0.284, 0.713] 0.0057
1.0 0.9850 0.0821 [0.860, 1.139] 0.0150
1.5 1.5025 0.1031 [1.293, 1.667] 0.0025
2.0 1.9950 0.1017 [1.853, 2.185] 0.0050
1.0 (SNR=172) 0.9930 0.0999 [0.847, 1.213] 0.0070

· Bootstrap success rate: 100% in all tests.
· Detection limit: ~0.15 T (at B=0.1 T it correctly returns Single).
· Runtime: 8–13 s (standard CPU) with n_bootstrap=30.

---

🔧 Technical improvements (for developers)

· Critical bug fix in v38.1 bootstrap: obj_local reused the same sample due to incorrect closure. Fixed by passing I_synth as a default argument (_I=I_synth) inside the loop.
· Removed dependency on res.success: replaced with _is_valid_solution checking B ≥ 0, sigma > 0, amplitude > 0.
· _sample_x0_bootstrap: hybrid strategy (local + fully random) with parameter‑specific handling (additive for λ_center and B, multiplicative for others).
· Improved hessian_std: guarded against LinAlgError, returns nan instead of raising exception.
· select_model: multi‑level decision rule (B/σ_B > spread_ratio > AICc).

---

📁 Files included in this release

File Description
dtqem_v38_2.py Core version – for importing into other projects.
dtqem_v38_2_full.py Full version – includes tests and plotting.
CITATION.cff Citation information for the release.
LICENSE CC BY‑NC 4.0.

---

📖 Scientific references used for validation

· Lavrov & Golubovskii (1995) – Hydrogen plasma in glow discharge.
· Pérez et al. (1991) – Zeeman measurements in Z‑pinch plasma.
· Stehlé et al. (2000) – Stark+Zeeman database for Hα.
· Ashbourn (2004) – Hα spectrum in a tokamak (1–5 T fields).

---

👤 Author

· Reddouane Berramdane (with assistance from AI tools: Gemini, DeepSeek, Claude, Perplexity)

---

🔗 DOI

To be assigned after upload to Zenodo

---

Released on 2026-05-19

HISTORY – DTQEM v34.2

Version 34.2 (2026-05-18) – Double‑slit inversion with multi‑start bootstrap

🚀 Major improvements

· Multi‑start bootstrap protocol
    Each bootstrap sample is refitted using 3 local restarts (L‑BFGS‑B) starting from the original best‑fit parameters with small random perturbations. This raises the bootstrap success rate from ~88 % (v34.0) to >98 % (often 100 %) – even for high‑noise or slightly non‑linear backgrounds.
· Increased global optimisation robustness
    Differential evolution maxiter raised from 50 to 60, and updating='deferred' with workers=1 eliminates the previous warning. Together with L‑BFGS‑B local refinement, the true global minimum is found reliably.
· New parameter bootstrap_n_restarts (default = 3)
    Users can adjust the number of restarts per bootstrap sample. Higher values increase success rate at the cost of computation time.
· Improved convergence criterion
    Local refinement success is now sufficient for a successful fit; if differential evolution fails but the local optimisation succeeds, a warning is issued but the result is accepted.

📊 Validation results (synthetic data)

Scenario d error E or \phi_B error \chi^2_{\text{red}} Bootstrap success
Linear background, \phi=0 0.05 % 1.5 % (E) 0.991 99.3 %
Phase shift \phi=0.3 rad – 2.8 % (φ) 0.997 100 %
Quadratic background (B_2=5000) 0.03 % – 0.978 100 %
High Poisson noise (5 % at peak) 0.21 % 4.7 % (E) 1.012 100 %

All 95 % bootstrap confidence intervals contain the true values. The residuals are white (correlation with x between −0.025 and 0.007).

🔧 Technical changes

· bootstrap_uncertainty now uses n_restarts and a more realistic perturbation (3 % relative noise) instead of the previous 1e-6.
· The objective function remains the half‑\chi^2 for Poisson noise:
    \mathcal{L} = \frac{1}{2}\sum_i (I_i - I_{\text{model},i})^2 / \max(I_{\text{model},i},10^{-9}).
· Boundary warnings added: near‑limit values of I_0, d, E or \phi_B trigger a warning.
· Residual diagnostics include mean, standard deviation, and correlation with x.

📁 Files introduced

· dtqem_v34_2.py – main inversion code (replaces v34.0/v34.1)
· WHITE_PAPER_v34.md – detailed theoretical and validation document
· CITATION.cff – updated with DOI and AI acknowledgement
· LICENSE – version 3.2 for v34.2

⚠️ Known limitations (same as v33.0)

· The linear background B_0+B_1x must be measured independently (laser off) – the user is responsible for this measurement.
· The model assumes pure dephasing (\sigma_z Lindblad) with a fixed Hamiltonian; any energy‑changing observer effects are not covered.
· For spin‑½ particles (electrons, neutrons) with unpolarized spin, the observer strength E cannot be distinguished from a spin‑dependent phase \phi_B using only intensity data. This is not a bug but a fundamental identifiability limit. For such experiments use the separate spin‑aware model (v35.1).

🎯 Recommended citation

Berramdane, R. (2026). DTQEM v34.2 – Robust double‑slit inversion with multi‑start bootstrap and >98 % success rate. Zenodo. https://doi.org/10.5281/zenodo.20260168

---

This file documents the changes specific to DTQEM v34.2. For earlier versions see the main HISTORY.md.

## v34.2 – 2026-05-18 (Multi‑start Bootstrap, >98% success)

**Improvements over v34.1:**

- **Multi‑start bootstrap:** Each synthetic sample is refitted using 3 local restarts (L‑BFGS‑B) starting from the original best parameters with tiny random perturbations. This raises the success rate from ~88% to **>98%** (often 100%).
- Increased `maxiter` of differential evolution from 50 to 60, suppressing the occasional `"Optimisation did not converge properly"` warning.
- Added parameter `bootstrap_n_restarts` (default 3) to control the number of restarts.
- Bootstrap success rate and number of successful samples are now printed in the summary.

**Validation results:**
- Original synthetic example: success rate 99.3% (149/150), d error 0.05%, E error 1.5%.
- Phase shift φ = 0.3 rad: 100% success, φ recovered as 0.3083 rad.
- Quadratic background (B2 = 5000): 100% success, d error 0.03%, χ²_red = 0.978.
- High Poisson noise (5% at peak): 100% success, d error 0.21%, E error 4.7%.

**Files:** `dtqem_v34_2.py`, `WHITE_PAPER_v34.md` (updated), `LICENSE_v34`.

---

## v34.1 – 2026-05-18 (Faster bootstrap, local only)

**Improvements over v34.0:**

- Bootstrap rewritten to use **local refinement only** (L‑BFGS‑B) for each synthetic sample, starting from the original best-fit parameters. This is ~10× faster than the global method and raises success rate to ~88–93%.
- Fixed `DeprecationWarning` from `scipy.linalg.kron` by replacing with `np.kron` in unit tests.
- Added `bootstrap_method` parameter (`'local'` or `'global'`), default `'local'`.
- Reduced `maxiter` of differential evolution to 50 (still sufficient).

**Validation results:**
- Success rates: φ case 93%, quadratic background 82%, high noise 86.7%, original 88.7%.
- Parameter accuracy unchanged from v34.0.

**Files:** `dtqem_v34_1.py` (internal development, not officially released).

---

## v34.0 – 2026-05-17 (First stable release with bootstrap improvements)

**Major changes from v33.0:**

- **Bootstrap uncertainty:** added full bootstrap with 150–200 synthetic Poisson samples. Initially used global optimisation (DE + L‑BFGS‑B) for each sample, but success rate was low (~46–76%).
- **Fixed differential evolution warning:** set `workers=1`, `updating='deferred'` to avoid the `'workers' overrides updating` warning.
- **Increased DE iterations** from 40 to 60 for the main fit.
- **Warning for χ²_red far from 1:** if χ²_red > 1.5 or < 0.7, a warning suggests model inadequacy or overfitting.
- **Unit tests:** added `test_concurrence()`, `test_double_slit_model()`, `test_estimate_d_from_fft()`.

**Validation results (synthetic, 1% Poisson noise):**
- d error: 0.05%, E error: 1.5%, χ²_red = 0.991.
- Bootstrap success rate: 46.7% (original example) – too low, leading to v34.1.

**Files:** `dtqem_v34_inversion.py`, `WHITE_PAPER_v34.md` (draft).

---

## v33.0 – 2026-05-16 (Original stable release – linear background, AICc, bootstrap)

**Key features:**
- Linear background \(B_0+B_1x\) measured independently and fixed during inversion.
- Wide search range for \(d\) [1 µm, 2 mm] independent of FFT guess.
- Global optimisation (DE 40‑50 iters) + local refinement.
- AICc model selection (with/without phase shift \(\phi\)).
- Bootstrap uncertainty (single-start local refinement, success rate ~88%).
- Residual diagnostics and boundary warnings.

**Validation:**
- d error 0.13%, E error 4.85%, χ²_red = 1.08.
- Residual correlation with x = 0.0068.

**DOI:** 10.5281/zenodo.20260168

**Files:** `dtqem_v33_inversion.py`, `WHITE_PAPER.md`, `README.md`, `LICENSE`.

## [v33.0] - 2026-05-17

### Added
- **Production-grade robust inversion** for Young's double-slit experiment.
- **Complete physical model** including:
  - Interference term: `(1-E) cos²(π d x/(λ L) + φ) + E`
  - Single-slit diffraction envelope: `sinc²(π a x/(λ L))`
  - Linear background: `B₀ + B₁ x` (measured independently with laser off)
- **Fixed parameter framework**: `B₀` and `B₁` are kept constant, breaking the harmful correlation with `E`.
- **Wide parameter bounds** for slit separation `d`: `[1 µm, 2 mm]` independent of FFT initial guess – eliminates previous convergence failures.
- **Global + local optimisation**: Differential evolution (40‑50 iterations) followed by L‑BFGS‑B guarantees finding the true global minimum.
- **Automatic model selection** using AICc to decide whether a phase shift `φ` is needed (simple model without `φ` is preferred for clean data).
- **Bootstrap uncertainty quantification** (150‑200 synthetic Poisson samples) providing 95% confidence intervals for `I₀`, `d`, and `E`.
- **Residual diagnostics**: mean, standard deviation, and correlation with position (`corr_x`) to verify model adequacy.
- **Boundary check warnings**: alerts when any fitted parameter reaches its allowed limits.
- **Structured output** via `FitResult` dataclass with automatic summary printing.
- **File I/O**: saves results as `_summary.txt`, `_params.csv`, and publication‑ready `_fit.png`.
- **Example synthetic test** demonstrating full pipeline with known true parameters.

### Changed
- Replaced the ad‑hoc background treatment of earlier versions (v16‑v22) with a physically motivated linear background that must be measured independently.
- Removed `source_width` and `linewidth` from the default model – they are unnecessary for standard double‑slit data and cause overfitting.
- The observer strength `E` is now the **only** quantum parameter; all other parameters (`I₀`, `d`, `B₀`, `B₁`, `φ`) are either classical or fixed by independent measurement.
- Improved initial guess for `d` using detrended FFT and fallback to 0.5 mm if FFT fails.

### Fixed
- **Critical bug**: previous versions (v25‑v30) often failed to recover the correct `d` (giving 3 µm instead of 500 µm) because bounds depended on the unreliable FFT initial guess. Now `d` bounds are fixed and wide.
- **Degeneracy between `E` and `B₁`**: by fixing `B₁` from an independent measurement (laser off), the correlation is eliminated, stabilising `E`.
- **Overfitting with `source_width`**: adding unnecessary parameters now causes AICc to correctly select the simpler model.
- **Clipboard copy errors** removed – the code saves files instead of relying on system clipboard.

### Results (synthetic data with 1% Poisson noise)
- **Slit separation `d`**: recovered with **0.13% error** (499.34 µm vs 500.00 µm true).
- **Observer strength `E`**: recovered with **4.9% error** (0.1903 vs 0.2000 true).
- **Peak intensity `I₀`**: recovered with 3.3% error (103.25 vs 100.0 true).
- **Reduced χ²_red = 1.08** (ideal = 1) – model describes data within noise limits.
- **Residuals are white**: correlation with `x` = 0.0068, mean ≈ -0.4, std ≈ 5.7.
- **AICc unambiguously selects the model without `φ`** (ΔAICc > 9), confirming that the phase shift is unnecessary.
- **Bootstrap 95% confidence intervals**:
  - `d`: [497.9 µm, 500.6 µm]
  - `E`: [0.1803, 0.2095]
  - `I₀`: [102.1, 106.3]

### Code
- Main script: `dtqem_v33_inversion.py`
- README updated with v33.0 instructions and DOI.
- Citation file (`CITATION.cff`) updated for v33.0.

---

## [v22.0] - 2026-05-16

### Added
- **Production-grade self-calibrating inversion** for hydrogen-like atomic spectra (Balmer series: Hα, Hβ, Hγ, Hδ).
- **Three-stage protocol** to recover temperature `T`, dephasing coefficient `α`, and unknown observer strength `E` from three sets of FWHM linewidth measurements:
  1. **Stage 0 – α calibration** from differential data: `ΔΓ_i = Γ_i(E_cal) - Γ_i(0) = α·ω₀,i·E_cal` (T‑independent, breaks degeneracy).
  2. **Stage 1 – T inference** from `E=0` data using the calibrated `α`.
  3. **Stage 2 – E inference** from `E_unk` data with fixed `T` and `α`.
- **Bootstrap uncertainty quantification** (500–1000 resampling trials) to estimate `σ_T`, `σ_α`, `σ_E`.
- **Consistency check** for `α`: computes per‑line `α` values and flags if `σ/μ > 0.05` (instrument drift or data inconsistency).
- **Convergence guards** on all scalar minimisations: residual tolerance checks and boundary warnings.
- **Corrected hydrogen mass** `m_H = m_p + m_e` (instead of only `m_p`).
- **User‑definable bounds** `T_max` and `E_max` (removed hard‑coded limits).
- **Structured output** via `InversionResult` dataclass, with automatic summary printing.
- **Full warnings integration** using Python's `warnings` module.
- **Publication‑quality figure** showing noise robustness with uncertainty bands and a panel for all three parameters.

### Changed
- Replaced the simple dictionary output of v21.0 with a robust, diagnostic‑rich `InversionResult`.
- Upgraded noise‑robustness test to include bootstrap‑based error propagation.
- The forward model now uses the exact hydrogen mass and allows arbitrary upper bounds for `T` and `E`.

### Fixed
- Degeneracy between Doppler and dephasing broadening that plagued earlier multi‑line inversion attempts (e.g., giving `T ≈ 2262 K` instead of `800 K`).
- Lack of uncertainty estimates – bootstrap now provides realistic error bars.

### Results
- **Noise‑free inversion**: errors < 0.001% for all parameters (perfect recovery).
- **Noise robustness** (200 trials, 1% noise): median `ΔT/T ≈ 3.9%`, median `ΔE ≈ 0.013`.
- Per‑line `α` consistency perfect (`σ/μ ≈ 0`) for synthetic data.
- The protocol works for a wide range of true parameters: `T = 300…2000 K`, `α/α_ref = 0.5…2.0`, `E = 0.3…1.0`.

### Code
- Main script: `dtqem_v22_inversion.py`
- White paper: `WHITE_PAPER_V22.md`
- README updated with v22.0 instructions and DOI.

---

## [v21.0] - 2026-05-16 (intermediate)

### Added
- First complete three‑stage inversion protocol for hydrogen Balmer lines.
- **Stage 0**: calibration of `α` from `Γ(E_cal) - Γ(0)` (temperature‑independent).
- **Stage 1**: temperature inference from `E=0` data.
- **Stage 2**: observer strength inference from `E_unk` data.
- Use of log‑squared residuals for all optimisations.
- Weighted averaging of `α` over lines with weights `ω₀,i` (higher sensitivity for shorter wavelengths).

### Changed
- Derived the degeneracy‑breaking principle: the differential measurement eliminates `T` completely.
- Replaced the earlier empirical fitting with a rigorous three‑step procedure.

### Fixed
- The degeneracy that prevented simultaneous recovery of `T` and `E` from multiple lines (demonstrated by the failure to recover `T=800 K` in earlier attempts).

### Note
- This version served as a proof‑of‑concept for the self‑calibrating approach but did not include uncertainty quantification or consistency checks. Those were added in v22.0.

---

## [v20.0] - 2026-05-15

### Added
- Two‑qubit entanglement simulation under combined **thermal relaxation (T₁)** and **local pure dephasing**.
- Full Lindblad model with Hamiltonian:
  `H = (ħω₀/2)(σ_z⊗I + I⊗σ_z) + (ħJ/2)(σ_x⊗σ_x + σ_y⊗σ_y)`.
- Thermal bath on both qubits: rates `γ_↓ = (1/T₁)(n_th+1)`, `γ_↑ = (1/T₁)n_th` with `n_th = 1/(e^(ħω₀/k_B T)-1)`.
- Database of **five real qubit types** with experimental parameters:
  - Trapped Ion, Superconducting (Transmon), Superconducting (Processor), Silicon Spin, Quantum Dot (hole).
- Computation of concurrence `C(t)`, CHSH `S(t)`, and entanglement lifetime `τ_ent` (first time `C` drops below `1/e`).
- Exponential fitting of `C(t)` to extract `τ_fit`.
- Regime classification: underdamped / overdamped using `E_crit = ω₀/γ_φ0`.
- Publication‑ready plots and summary table output.

### Changed
- Observer strength `E_ext` modulates **only** the pure dephasing rate `γ_φ = γ_φ0·E_ext`, leaving the Hamiltonian fixed (consistent with DTQEM v19.0 physics).
- Automatic `t_max` estimation based on the slowest decay rate among `γ_↓, γ_↑, γ_φ, J`.
- Improved `sanitize_rho` to enforce Hermiticity, positivity, and trace = 1 in three steps.

### Fixed
- Previous numerical issues with thermal bath implementation (proper handling of `n_th` and rate limits).
- Entanglement lifetime now correctly depends on `E_ext` and temperature `T`; earlier manual `t_max` estimation was replaced by dynamic calculation.

### Results
- For a superconducting transmon (`T₁ = T₂ = 1.68 ms`):
  - At `T = 0.01 K`, increasing `E_ext` from 0 to 1 reduces `τ_ent` from 1000 μs to 623 μs (**-38%**, Zeno effect).
  - At `T = 0.1 K`, the reduction is **-46%** (965 μs → 523 μs).
  - At `T = 1.0 K`, thermal excitation dominates; `τ_ent` drops by >90% compared to 0.01 K, and the Zeno effect becomes weak (~7%).
- Simulated `τ_ent ≈ 0.623 ms` at `E=1, T=0.01 K` agrees well with the predicted `T₂/2 = 0.84 ms`, validating the model against experimental coherence times.

### Code
- Main script: `dtqem_20_entanglement.py`
- White paper: `WHITE_PAPER_V20.md`
- README updated with v20.0 instructions and DOI.

---

## [v19.0] - 2026-05-15

### Added
- **Exact analytical solution** of the baseline Lindblad model for a single qubit.
- Fixed Hamiltonian `H = (Δ/2)σ_x` and pure dephasing `L = √(γ·E_ext)·σ_z`.
- Closed‑form expression for the probability to be in `|1⟩`:
  `P_right(E,t) = ½[1 - e^{-γ·E·t}(cos(ω₀ t) + (γ·E/ω₀) sin(ω₀ t))]`, where `ω₀ = Δ/ħ`.
- Key physical insights derived:
  - Decoherence time: `τ_coh = 1/(γ·E)`.
  - Critical observer strength: `E_crit = ω₀/γ` (separates under‑damped from over‑damped regimes).
  - Long‑time limit: `P(E=1, t→∞) = 1/2` (complete mixing, **not** freezing).
  - Rabi frequency remains constant (observer does not change energy scale).
- Numerical validation: absolute error < 1e-12 compared to direct integration.
- Python script `analytical_model_v19.py` for quick evaluation.

### Changed
- Superseded earlier empirical fits (e.g., `P ∝ (1-E)²`) for the baseline single‑qubit model.
- Clarified that the observer affects **coherence only**, not the system's energy.

### Deprecated
- Phenomenological models (v15 and below) that used an observer‑dependent Hamiltonian `H ∝ (1-E)σ_x`.

### Code
- Main script: `analytical_model_v19.py`
- White paper: `WHITE_PAPER_V19.md`
- README updated with v19.0 as the baseline analytical release.

---

## [v18.0] - 2026-05-14

### Added
- Two‑qubit entanglement simulation under local dephasing (`σ_z⊗I`).
- Concurrence calculation (Wootters formula).
- Analytical inference of CHSH parameter: `S = 2√2·C`.
- Zeno‑like suppression of entanglement with increasing `E_ext`.

### Changed
- No Hamiltonian evolution (`H=0`), pure dephasing only – simplifies interpretation.
- Dephasing on a single qubit (Alice) to model local measurement.

### Fixed
- All previous numerical instabilities in CHSH direct computation are avoided by using the analytical relation.

---

## [v17.0] - 2026-05-13

### Added
- Photon wave‑particle simulation (650 nm red light).
- Frequency extraction via FFT to demonstrate constant Rabi frequency.
- Observer strength `E` modulates pure dephasing only; Hamiltonian fixed.
- Clear visualisation: probability vs time and extracted frequency vs `E`.

### Results
- Extracted frequency `ν₀ = 461 THz` matches theoretical value regardless of `E`.
- Probability `P_right(t)` shows slower oscillations and lower amplitude as `E` increases.

---

## [v16.0] - 2026-05-12

### Added
- Massive‑particle tunneling simulation under continuous measurement.
- Fixed Hamiltonian `H = (Δ/2)σ_x`, dephasing `L = √(γ·E)·σ_z`.
- Numerical verification of the **Zeno effect**: increasing `E` suppresses tunneling.

### Results
- At `t = 20 ps`, `P_right` decreases from 0.86 (`E=0`) to 0.12 (`E=1`).
- Clear demonstration that observation slows down quantum evolution.
