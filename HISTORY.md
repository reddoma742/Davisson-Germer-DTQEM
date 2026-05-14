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
