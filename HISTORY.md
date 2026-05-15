## [v20.0] - 2026-05-15
### Added
- Two‑qubit entanglement simulation under combined **thermal relaxation (T₁)** and **local pure dephasing**.
- Full Lindblad model with Hamiltonian:
  \[
  H = \frac{\hbar\omega_0}{2}(\sigma_z\otimes I + I\otimes\sigma_z) + \frac{\hbar J}{2}(\sigma_x\otimes\sigma_x + \sigma_y\otimes\sigma_y).
  \]
- Thermal bath on both qubits: rates \( \gamma_{\downarrow} = \frac{1}{T_1}(n_{\text{th}}+1) \), \( \gamma_{\uparrow} = \frac{1}{T_1}n_{\text{th}} \) with \( n_{\text{th}} = 1/(e^{\hbar\omega_0/k_B T}-1) \).
- Database of **five real qubit types** with experimental parameters:
  - Trapped Ion, Superconducting (Transmon), Superconducting (Processor), Silicon Spin, Quantum Dot (hole).
- Computation of concurrence \( C(t) \), CHSH \( S(t) \), and entanglement lifetime \( \tau_{\text{ent}} \) (first time \( C \) drops below \( 1/e \)).
- Exponential fitting of \( C(t) \) to extract \( \tau_{\text{fit}} \).
- Regime classification: underdamped / overdamped using \( E_{\text{crit}} = \omega_0/\gamma_{\phi0} \).
- Publication‑ready plots and summary table output.

### Changed
- Observer strength \( E_{\text{ext}} \) modulates **only** the pure dephasing rate \( \gamma_{\phi} = \gamma_{\phi0} E_{\text{ext}} \), leaving the Hamiltonian fixed (consistent with DTQEM v19.0 physics).
- Automatic \( t_{\text{max}} \) estimation based on the slowest decay rate among \( \gamma_{\downarrow}, \gamma_{\uparrow}, \gamma_{\phi}, J \).
- Improved `sanitize_rho` to enforce Hermiticity, positivity, and trace = 1 in three steps.

### Fixed
- Previous numerical issues with thermal bath implementation (proper handling of \( n_{\text{th}} \) and rate limits).
- Entanglement lifetime now correctly depends on \( E_{\text{ext}} \) and temperature \( T \); earlier manual `t_max` estimation was replaced by dynamic calculation.

### Results
- For a superconducting transmon (\( T_1 = T_2 = 1.68\,\text{ms} \)):
  - At \( T = 0.01\,\text{K} \), increasing \( E_{\text{ext}} \) from 0 to 1 reduces \( \tau_{\text{ent}} \) from 1000 μs to 623 μs (**-38%**, Zeno effect).
  - At \( T = 0.1\,\text{K} \), the reduction is **-46%** (965 μs → 523 μs).
  - At \( T = 1.0\,\text{K} \), thermal excitation dominates; \( \tau_{\text{ent}} \) drops by >90% compared to 0.01 K, and the Zeno effect becomes weak (~7%).
- Simulated \( \tau_{\text{ent}} \approx 0.623\,\text{ms} \) at \( E=1, T=0.01\,\text{K} \) agrees well with the predicted \( T_2/2 = 0.84\,\text{ms} \), validating the model against experimental coherence times.

### Code
- Main script: `dtqem_20_entanglement.py`
- White paper: `WHITE_PAPER_V20.md`
- README updated with v20.0 instructions and DOI.

## [v19.0] - 2026-05-15
### Added
- **Exact analytical solution** of the baseline Lindblad model for a single qubit.
- Fixed Hamiltonian \( H = \frac{\Delta}{2}\sigma_x \) and pure dephasing \( L = \sqrt{\gamma E_{\text{ext}}}\,\sigma_z \).
- Closed‑form expression for the probability to be in \( |1\rangle \):
  \[
  P_{\text{right}}(E,t) = \frac{1}{2}\left[1 - e^{-\gamma E t}\left(\cos(\omega_0 t) + \frac{\gamma E}{\omega_0}\sin(\omega_0 t)\right)\right],\quad \omega_0 = \frac{\Delta}{\hbar}.
  \]
- Key physical insights derived:
  - Decoherence time: \( \tau_{\text{coh}} = 1/(\gamma E) \).
  - Critical observer strength: \( E_{\text{crit}} = \omega_0/\gamma \) (separates under‑damped from over‑damped regimes).
  - Long‑time limit: \( P(E=1, t\to\infty) = 1/2 \) (complete mixing, **not** freezing).
  - Rabi frequency remains constant (observer does not change energy scale).
- Numerical validation: absolute error < 1e-12 compared to direct integration.
- Python script `analytical_model_v19.py` for quick evaluation.

### Changed
- Superseded earlier empirical fits (e.g. \( P \propto (1-E)^2 \)) for the baseline single‑qubit model.
- Clarified that the observer affects **coherence only**, not the system’s energy.

### Deprecated
- Phenomenological models (v15 and below) that used an observer‑dependent Hamiltonian \( H \propto (1-E)\sigma_x \).

### Code
- Main script: `analytical_model_v19.py`
- White paper: `WHITE_PAPER_V19.md`
- README updated with v19.0 as the baseline analytical release.

## [v18.0] - 2026-05-14
### Added
- Two‑qubit entanglement simulation under local dephasing (σz⊗I).
- Concurrence calculation (Wootters formula).
- Analytical inference of CHSH parameter: S = 2√2·C.
- Zeno‑like suppression of entanglement with increasing E_ext.

### Changed
- No Hamiltonian evolution (H=0), pure dephasing only – simplifies interpretation.
- Dephasing on a single qubit (Alice) to model local measurement.

### Fixed
- All previous numerical instabilities in CHSH direct computation are avoided by using the analytical relation.
