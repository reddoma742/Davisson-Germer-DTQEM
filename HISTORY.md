```markdown
## [v18.0-C-paper] – 2026-06-15  ← FINAL PAPERS RELEASE

### 🎯 Summary
Completion of the three‑paper DTQEM series: phenomenological model (Paper I), microscopic derivation (Paper II), and vibronic‑mediated temperature‑dependent dephasing (Paper III). The series transitions from empirical fitting to first‑principles theory with falsifiable predictions.

### ✨ Added – Papers

#### Paper I (Phenomenological Joint‑Bath Model)
- `papers/DTQEM_PaperI_Phenomenological_v1.0.tex`
- Bilinear cross‑coupling term `c·I_path·ΔT/T_ref`
- Calibration: R² = 0.9982 (synthetic), LOOCV R² = 0.9814
- Validation on Hornberger (2003): R² = 0.936 (N=8)
- AICc threshold: N ≥ 36 for reliable detection

#### Paper II (Microscopic Derivation)
- `papers/DTQEM_PaperII_Microscopic_v1.0.tex`
- Canonical transformation → cross‑spectral density `J₁₂(ω)`
- Cauchy–Schwarz bound: `|J₁₂|² ≤ J₁₁·J₂₂`
- Correlation coefficient `ρ ≈ 0.855`, optimal coupling `λ_opt ≈ 0.095`

#### Paper III (Vibronic‑Mediated Dephasing)
- `papers/DTQEM_PaperIII_Vibronic_Mediated_Decoherence_v1.0.tex`
- Effective dephasing coefficient: `a_eff(T) = a₀ + 2S·coth(ħω_v/2k_BT)`
- Huang–Rhys factor `S = g²/ω_v²` – measurable independently
- Predictions: low‑T saturation, high‑T linear growth, isotope‑dependent crossover `T*`
- Isotope shift: `ΔT*/T* ≈ -3.9%` for ¹²C → ¹³C in C₇₀

### ✨ Added – Documentation & Metadata
- **Acknowledgments** in all three papers explicitly mention AI models (DeepSeek, Claude, Qwen) as analytical tools under human supervision.
- `papers/README.md` – overview of all three papers with compilation instructions.
- Updated `CITATION.cff` with entries for Papers I, II, III.
- Updated main `README.md` with Paper III in the model table and citation section.

### 🔧 Changed
- Repository structure: `papers/` folder now contains all three `.tex` and `.pdf` files.
- `.gitignore` updated to keep final PDFs of all three papers.
- `HISTORY.md` restructured to separate paper releases from code releases.

### 📊 Performance summary (Paper III)

| Regime | Behavior | Formula |
|--------|----------|---------|
| Low T | Saturation | `a_eff → a₀ + 2S` |
| High T | Linear growth | `a_eff ≈ a₀ + 4Sk_BT/(ħω_v)` |
| Crossover | `T* ≈ ħω_v/2k_B` | Example: C₇₀ → `T* ≈ 195 K` |

### 🔮 Testable predictions
- **Isotope effect**: `T*'/T* = √(μ/μ')`, `S'/S = μ'/μ`
- **Low‑T saturation** – measurable in superconducting qubits or cryogenic interferometry
- **High‑T linear slope** – directly related to `S` and `ω_v`

### 📁 Files added/updated

```

papers/DTQEM_PaperI_Phenomenological_v1.0.tex
papers/DTQEM_PaperI_Phenomenological_v1.0.pdf
papers/DTQEM_PaperII_Microscopic_v1.0.tex
papers/DTQEM_PaperII_Microscopic_v1.0.pdf
papers/DTQEM_PaperIII_Vibronic_Mediated_Decoherence_v1.0.tex
papers/DTQEM_PaperIII_Vibronic_Mediated_Decoherence_v1.0.pdf
papers/README.md
README.md (updated)
CITATION.cff (updated)
.gitignore (updated)
HISTORY.md (updated)

```

### 🔗 DOI
> **Current release DOI (for all three papers together):**  
> *To be assigned after Zenodo upload – use tag `v18.0-C-paper`.*

### 🧪 Next steps
- Upload to Zenodo (DOI will be issued)
- Submit Papers I, II, III to arXiv (quant-ph)
- Contact experimental groups (e.g., Arndt lab, Vienna) for isotope effect test
```

## [v18.0-C-paper] – 2026-06-11  ← PAPER RELEASE

### 🎯 Summary
Publication-ready release of DTQEM v18.0-C. Complete LaTeX manuscript (Paper I) 
submitted to arXiv, including full calibration, validation on Hornberger (2003) data, 
and exploratory temperature scan predicting T* ≈ 3.82 K.

### ✨ Added (this release)

#### Paper (LaTeX)
- `paper/paper1_final.tex` – complete manuscript ready for arXiv
- Abstract includes: R²=0.9679 (c=0), R²=0.9982 (full), LOOCV R²=0.9814
- Validation on Hornberger et al. (2003): R²=0.936 (N=8)
- Appendix: cumulant derivation of cross-coupling term
- Acknowledgments: explicit mention of AI models (DeepSeek, Claude, Qwen)

#### Figure
- `figures/figure_b_eff.png` – effective thermal coefficient b_eff(T)
  - Classical regime: T > T* (b ∝ T)
  - Saturation regime: T < T* (b_sat ≈ 0.0103)
  - Crossover: T* ≈ 3.82 K (marked as exploratory)

#### Code improvements
- Custom `\coth` command (removed physics package dependency)
- Suppressed LaTeX warnings (siunitx compatibility)

### 📊 New validation result

| Dataset | R² | Notes |
|---------|-----|-------|
| Hornberger 2003 (N=8) | 0.936 | Independent experimental validation |

### 📁 New files
paper/paper1_final.tex figures/figure_b_eff.png scripts/generate_figure_beff.py (optional) .gitignore (updated)

```markdown
# DTQEM – Project History & Changelog

All notable changes to the DTQEM project are documented in this file.  
Format inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

### 🔗 DOI
> Zenodo (to be updated after upload):  
> Current: [10.5281/zenodo.20516742](https://doi.org/10.5281/zenodo.20516742)  
> New DOI will be shared after final archive submission.

### ⚠️ Updated limitations
- Hornberger validation (N=8) demonstrates compatibility, not universality
- T* ≈ 3.82 K is exploratory – requires low-temperature experimental confirmation
---

## [ESD v1.0] – 2026-06-02  ← LATEST ADDITION

### 🎯 Summary
Extension of the DTQEM framework to predict Entanglement Sudden Death (ESD) 
in bipartite quantum systems under local dephasing channels.

### ✨ Added
- **ESD time equation**: $t_{\text{ESD}}(I,T) = K / (\alpha I + \beta \Delta T/T_{\text{ref}} + \gamma I \Delta T/T_{\text{ref}})$
- **Concurrence-based derivation** for X-state initial conditions
- **Publication-ready heatmap** (`figure_esd_final.png`) with logarithmic scaling
- **Complete Python implementation** (`scripts/generate_esd_final.py`)
- **Metadata JSON** for figure archival

### Parameters
- $\alpha = 1.0$, $\beta = 0.85$, $\gamma = 0.5$
- $T_{\text{ref}} = 300$ K
- $\rho_{14}(0) = 0.35$, $\rho_{22}(0) = \rho_{33}(0) = 0.10$

### Files
- `scripts/generate_esd_final.py`
- `figures/figure_esd_final.png`
- `figures/figure_esd_final.png.meta.json`

---

## [v18.0-C] – 2026-06-01  ← CURRENT RELEASE

### 🎯 Summary
Major theoretical upgrade: transition from independent‑bath approximation to a unified joint‑bath framework with a first‑principles‑derived crossover coupling coefficient `c`.  
This release also integrates the `v63.x` particle‑scaling models and the **Unified DTQEM** equation.

### ✨ Added

#### Core model (v18.0‑C)
- **Joint‑bath crossover term** `c · I_path · ΔT/T_ref` in the coherence equation.
- **First‑principles derivation** of all coefficients:
  - `a(ω_c, T)` from Lorentzian spectral density + Fermi’s Golden Rule.
  - `b(T)` from high‑temperature Ohmic bath (linear in T, R²=0.998).
- **Operational bridge**: mapping `I_path ← n̄` via Englert‑Greenberger distinguishability →  
  `I_path(n̄) = √(1 − e^{−κ n̄})`.
- **AICc statistical threshold**: at least **N ≥ 36** samples required to reliably detect `c > 0`.

#### Unified model (particle + environment)
- **Unified DTQEM equation** combining v18.0‑C (environmental) with v63.1‑C (particle structure):
  
```

τ_c(m, v, N, I, T) = τ_c0 / [ A·(m/μ)^β·(v/c)^δ·I + B·(1+ζN)·ΔT/T_ref + C_joint·(m/μ)^β·(v/c)^δ·I·(1+ζN)·ΔT/T_ref ]

```
  
- **First‑principles scaling exponents** (β, δ, ζ) derived with assistance from Arena AI.

#### Code & documentation
- **Delta‑method uncertainty propagation** for all predictions.
- **Input validation** with physical boundary warnings.
- **Unit test suite** (`test_dtqem.py`) covering 5 test classes.
- **Full LaTeX manuscript** (`paper.tex`) ready for arXiv submission.
- **Figures**:
  - Figure 1 : Lorentzian spectral line shape `a(ω_c)` (peak at 5.0 GHz).
  - Figure 2 : AICc model selection probability vs. sample size (threshold at N=36).
  - Figure 3 : Coherence time landscape `τ_c` for C60 (N=60) and C700 (N=700).

### 🔧 Changed
- Model equation extended from 3 to 4 parameters (added `c = 0.5000 ± 0.0201`).
- `predict()` now supports optional `return_uncertainty=True`.
- Repository structure reorganised into `models/`, `figures/`, `paper/`.

### 📊 Performance vs v17.0‑C

| Metric     | v17.0‑C  | v18.0‑C   | Improvement |
|------------|----------|-----------|-------------|
| R²         | 0.9679   | **0.9982**| +3.1%       |
| LOOCV R²   | 0.9356   | **0.9814**| +4.9%       |
| RMSE       | 0.0202   | **0.0045**| ×4.5 better |

### 📁 Files in this release

```

models/v17/dtqem_baseline_v17.py
models/v18/dtqem_joint_bath_v18.py
models/v63/DTQEM_v63_1_C.py
models/v63/dtqem_v63_joint.py
models/unified/dtqem_unified_simulator.py
tests/test_dtqem.py
scripts/generate_figures.py
scripts/generate_figure3.py
figures/figure1.png
figures/figure2.png
figures/figure3.png
paper/paper.tex
README.md
LICENSE
CITATION.cff

```

### 🔗 DOI
> Zenodo (main release): [10.5281/zenodo.20460770](https://doi.org/10.5281/zenodo.20460770)

### ⚠️ Known Limitations
- Calibrated on synthetic data (N=8 for baseline); experimental validation (N≥36) pending.
- Valid range: `I_path ∈ [0, 1]`, `T ∈ [300, 550] K`.
- Assumes Markovian dynamics (no non‑Markovian revivals).
- Pure‑dephasing model only (T₂*); T₁ relaxation not included.

---

## [v17.0-C] – 2026-05-30

### 🎯 Summary
Final calibrated baseline coherence model. Independent‑bath approximation (`c = 0`).  
Three‑parameter model validated by LOOCV.

### Equation
```

C = C₀ · exp(−a_path · I_path − a_temp · ΔT/T_ref)

```

### Parameters

| Parameter | Value  | Std Error |
|-----------|--------|-----------|
| C₀        | 0.3675 | ±0.0052   |
| a_path    | 1.6968 | ±0.0245   |
| a_temp    | 0.8055 | ±0.0148   |
| T_ref     | 300 K  | fixed     |

### Performance

| Metric   | Value  |
|----------|--------|
| R²       | 0.9679 |
| LOOCV R² | 0.9356 |
| RMSE     | 0.0202 |

### 🔗 DOI
> Zenodo: [10.5281/zenodo.20460770](https://doi.org/10.5281/zenodo.20460770)

### Files
- `models/v17/dtqem_baseline_v17.py`
- `LICENSE`
- `README.md`

---

## [v16.1-C] – 2026-06-02 (Historical - Zeno Effect)

### 🎯 Summary
Quantum tunneling under continuous dephasing (Quantum Zeno effect prototype).  
Lindblad master equation simulation for a two-level system.

### Added
- **Quantum tunneling under continuous dephasing** (Lindblad master equation)
- Hamiltonian: H = (Δ/2) σ_x (fixed coherent tunneling)
- Lindblad operator: L = √(γ·E_ext) σ_z (pure dephasing)
- Calculation of P_left, P_right, and coherence
- Metadata JSON for figure_zeno.png

### Parameters (Optimized)
- Δ = 78.15 μeV (coherent splitting)
- γ₀ = 1.2×10¹¹ s⁻¹ (dephasing rate)
- t_max = 20 ps

### Results at t = 20 ps
| E_ext | P_left | P_right |
|-------|--------|---------|
| 0.0   | 0.14   | 0.86    |
| 0.3   | 0.40   | 0.60    |
| 0.7   | 0.58   | 0.42    |
| 1.0   | 0.66   | 0.34    |

### Files
- `models/v16/dtqem_tunneling_v16_1_C.py`
- `figures/figure_zeno.png`
- `figures/figure_zeno.png.meta.json`

---

## [v63.1‑C] – 2026-05 (Integrated)

### 🎯 Summary
Coherence **time** τ_c scaling model for massive composite particles.  
Inverse problem solver with Delta‑method uncertainty propagation.

### Equation
```

τ_c = τ_c0 / [ (m/μ)^β · (v/c)^δ · (1 + ζN) ]

```

### Exponents (first‑principles derived)

| Exponent | Value | Origin |
|----------|-------|--------|
| β        | 0.44  | Debye‑Pikovski frozen modes |
| δ        | 1/3   | van der Waals + eikonal scattering |
| ζ        | 0.005 | Symmetry‑suppressed blackbody emission |
| τ_c0     | 9.8×10⁻²⁷ s | Phenomenological scale |

### Files
- `models/v63/DTQEM_v63_1_C.py`

---

## [v63.0] – Legacy (historical reference only)

- Original empirical τ_c scaling (no derivations).
- Superseded by v63.1‑C.

---

## 🗺️ Roadmap

| Version   | Target    | Description |
|-----------|-----------|-------------|
| v18.1‑C   | Q3 2026   | Experimental validation (N≥36 real data points) |
| v19.0‑C   | Q4 2026   | Non‑Markovian extension (HEOM framework) |
| v20.0‑C   | 2027      | T₁ relaxation integration |

---

*Maintained by: Reddouane Berramdane*  
*License: CC BY‑NC‑SA 4.0*  
*Contact: reddoma@gmail.com*
```

## [v16.1-C] – 2026-06-02 (Historical - Zeno Effect)

### Added
- **Quantum tunneling under continuous dephasing** (Lindblad master equation)
- Hamiltonian: H = (Δ/2) σ_x (fixed coherent tunneling)
- Lindblad operator: L = √(γ·E_ext) σ_z (pure dephasing)
- Calculation of P_left, P_right, and coherence
- Metadata JSON for figure_zeno.png

### Parameters (Optimized)
- Δ = 78.15 μeV (coherent splitting)
- γ₀ = 1.2×10¹¹ s⁻¹ (dephasing rate)
- t_max = 20 ps

### Results at t = 20 ps
- E_ext = 0.0 → P_right = 0.86
- E_ext = 0.3 → P_right = 0.60
- E_ext = 0.7 → P_right = 0.42
- E_ext = 1.0 → P_right = 0.34

### Files
- `models/v16/dtqem_tunneling_v16_1_C.py`
- `figures/figure_zeno.png`
- `figures/figure_zeno.png.meta.json`

```markdown
# DTQEM – Project History & Changelog

All notable changes to the DTQEM project are documented in this file.  
Format inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [v18.0-C] – 2026-06-01  ← CURRENT RELEASE

### 🎯 Summary
Major theoretical upgrade: transition from independent‑bath approximation to a unified joint‑bath framework with a first‑principles‑derived crossover coupling coefficient `c`.  
This release also integrates the `v63.x` particle‑scaling models and the **Unified DTQEM** equation.

### ✨ Added

#### Core model (v18.0‑C)
- **Joint‑bath crossover term** `c · I_path · ΔT/T_ref` in the coherence equation.
- **First‑principles derivation** of all coefficients:
  - `a(ω_c, T)` from Lorentzian spectral density + Fermi’s Golden Rule.
  - `b(T)` from high‑temperature Ohmic bath (linear in T, R²=0.998).
- **Operational bridge**: mapping `I_path ← n̄` via Englert‑Greenberger distinguishability →  
  `I_path(n̄) = √(1 − e^{−κ n̄})`.
- **AICc statistical threshold**: at least **N ≥ 36** samples required to reliably detect `c > 0`.

#### Unified model (particle + environment)
- **Unified DTQEM equation** combining v18.0‑C (environmental) with v63.1‑C (particle structure):
```

τ_c(m, v, N, I, T) = τ_c0 / [ A·(m/μ)^β·(v/c)^δ·I + B·(1+ζN)·ΔT/T_ref + C_joint·(m/μ)^β·(v/c)^δ·I·(1+ζN)·ΔT/T_ref ]

```
- **First‑principles scaling exponents** (β, δ, ζ) derived with assistance from Arena AI.

#### Code & documentation
- **Delta‑method uncertainty propagation** for all predictions.
- **Input validation** with physical boundary warnings.
- **Unit test suite** (`test_dtqem.py`) covering 5 test classes.
- **Full LaTeX manuscript** (`paper.tex`) ready for arXiv submission.
- **Figures**:
  - Figure 1 : Lorentzian spectral line shape `a(ω_c)` (peak at 5.0 GHz).
  - Figure 2 : AICc model selection probability vs. sample size (threshold at N=36).
  - Figure 3 : Coherence time landscape `τ_c` for C60 (N=60) and C700 (N=700).

### 🔧 Changed
- Model equation extended from 3 to 4 parameters (added `c = 0.5000 ± 0.0201`).
- `predict()` now supports optional `return_uncertainty=True`.
- Repository structure reorganised into `models/`, `figures/`, `paper/`.

### 📊 Performance vs v17.0‑C

| Metric     | v17.0‑C  | v18.0‑C   | Improvement |
|------------|----------|-----------|-------------|
| R²         | 0.9679   | **0.9982**| +3.1%       |
| LOOCV R²   | 0.9356   | **0.9814**| +4.9%       |
| RMSE       | 0.0202   | **0.0045**| ×4.5 better |

### 📁 Files in this release

```

models/v17/dtqem_baseline_v17.py
models/v18/DTQEM_v63_1_C.py          ← Core v18.0‑C model + uncertainty
models/v63/DTQEM_v63_1_C.py          ← τ_c scaling model
models/v63/dtqem_v63_joint.py        ← Joint‑bath (mass‑velocity crossover)
models/unified/dtqem_unified_simulator.py
tests/test_dtqem.py
scripts/generate_figures.py
scripts/generate_figure3.py
figures/figure1.png
figures/figure2.png
figures/figure3.png
paper/paper.tex
README.md
LICENSE
CITATION.cff

```

### 🔗 DOI
> Zenodo (main release): [10.5281/zenodo.20460770](https://doi.org/10.5281/zenodo.20460770)  
> *This DOI points to the v17.0‑C baseline; after upload of the full v18.0‑C archive, a new DOI will be issued and updated here.*

### ⚠️ Known Limitations
- Calibrated on synthetic data (N=8 for baseline); experimental validation (N≥36) pending.
- Valid range: `I_path ∈ [0, 1]`, `T ∈ [300, 550] K`.
- Assumes Markovian dynamics (no non‑Markovian revivals).
- Pure‑dephasing model only (T₂*); T₁ relaxation not included.

---

## [v17.0‑C] – 2026-05-30  ← PREVIOUS RELEASE

### 🎯 Summary
Final calibrated baseline coherence model. Independent‑bath approximation (`c = 0`).  
Three‑parameter model validated by LOOCV.

### Equation
```

C = C₀ · exp(−a_path · I_path − a_temp · ΔT/T_ref)

```

### Parameters

| Parameter | Value  | Std Error |
|-----------|--------|-----------|
| C₀        | 0.3675 | ±0.0052   |
| a_path    | 1.6968 | ±0.0245   |
| a_temp    | 0.8055 | ±0.0148   |
| T_ref     | 300 K  | fixed     |

### Performance

| Metric   | Value  |
|----------|--------|
| R²       | 0.9679 |
| LOOCV R² | 0.9356 |
| RMSE     | 0.0202 |

### 🔗 DOI
> Zenodo: [10.5281/zenodo.20460770](https://doi.org/10.5281/zenodo.20460770)

### Files
```

dtqem_v17.0-C_coherence.py   ← Standalone coherence function
LICENSE
README_v17.md

```

---

## [v63.1‑C] – 2026-05 (parallel branch, now integrated)

### 🎯 Summary
Coherence **time** τ_c scaling model for massive composite particles.  
Inverse problem solver with Delta‑method uncertainty propagation.

### Equation
```

τ_c = τ_c0 / [ (m/μ)^β · (v/c)^δ · (1 + ζN) ]

```

### Exponents (first‑principles derived)

| Exponent | Value | Origin |
|----------|-------|--------|
| β        | 0.44  | Debye‑Pikovski frozen modes |
| δ        | 1/3   | van der Waals + eikonal scattering |
| ζ        | 0.005 | Symmetry‑suppressed blackbody emission |
| τ_c0     | 9.8×10⁻²⁷ s | Phenomenological scale |

---

## [v63.0] – Legacy (historical reference only)

- Original empirical τ_c scaling (no derivations).
- Superseded by v63.1‑C.

---

## 🗺️ Roadmap

| Version   | Target    | Description |
|-----------|-----------|-------------|
| v18.1‑C   | Q3 2026   | Experimental validation (N≥36 real data points) |
| v19.0‑C   | Q4 2026   | Non‑Markovian extension (HEOM framework) |
| v20.0‑C   | 2027      | T₁ relaxation integration |

---

*Maintained by: Reddouane Berramdane*  
*License: CC BY‑NC‑SA 4.0*  
*Contact: reddoma@gmail.com*
```

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
- `README_v17.0-C.md`
- `whitepaper_v17.0-C.md`

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
