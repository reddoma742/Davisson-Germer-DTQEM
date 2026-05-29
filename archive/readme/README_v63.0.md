# DTQEM v63.0 â€“ Phenomenological Scaling Model for Decoherence Time \(\tau_c\)

A phenomenological scaling law for quantum decoherence time \(\tau_c\), calibrated on synthetic interferometry data, with stable inverse extraction via the logarithmic slope method.

[![Status: Working Model](https://img.shields.io/badge/Status-Working%20Model-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

## What is DTQEM v63.0?

DTQEM v63.0 presents a phenomenological scaling model for the decoherence time \(\tau_c\), calibrated on synthetic interferometry data. The model is built on the D0 baseline equation:

\[
V_{\text{eff}} = \exp(-\gamma_\phi T_{\text{eff}})\times \exp\left(-\frac{|\Delta\tau|}{\tau_c}\right)
\]

### Core phenomenological model

\[
\boxed{\tau_c = \frac{\tau_{c0}}{m^{\beta}\,(v/c)^{\delta}\,(1+\zeta N)}}
\]

| Parameter | Value | Interpretation |
|-----------|-------|----------------|
| `Ï„_c0` | 9.8 Ã— 10â»Â²â· s | Environment-dependent reference time (not universal) |
| `Î²` | 0.44 | Mass exponent (â‰ˆ 1/2, effective scaling) |
| `Î´` | 0.33 | Velocity exponent (effective transport scaling) |
| `Î¶` | 0.005 | Per-atom internal complexity correction |
| `N` | â€“ | Number of atoms, proxy for internal degrees of freedom |

## Key features

### 1. Stable inverse extraction

Instead of extracting \(\tau_c\) from a single visibility measurement, v63.0 uses multiple measurements at different \(\Delta\tau\):

\[
\ln V_{\text{eff}} = C - \frac{1}{\tau_c}|\Delta\tau|
\]

A linear fit gives \(\tau_c = -1/\text{slope}\).

### 2. Experimental predictions

| Test | Prediction | Purpose |
|------|------------|---------|
| Pressure dependence | If \(\tau_c\) independent of P â†’ intrinsic mechanism. If \(\tau_c \propto 1/P\) â†’ environmental decoherence. | Critical test |
| Mass scaling | \(\tau_c \propto m^{-0.44}\) | Test \(\beta\) |
| Velocity scaling | \(\tau_c \propto v^{-0.33}\) | Test \(\delta\) |
| Temperature dependence | \(\tau_c \propto 1/T\) in the simplest thermal scenario | Test mechanism |

### 3. CSV support for real data

```csv
particle,mass_kg,speed_m_s,N_atoms,delta_tau_s,V_eff
C60,1.196e-24,200.0,60,1.2e-15,0.85
C60,1.196e-24,200.0,60,2.5e-15,0.72
```

## Requirements

- numpy â‰¥ 1.21
- matplotlib â‰¥ 3.5
- scipy â‰¥ 1.7
- ipywidgets (optional) â‰¥ 7.6

Install:

```bash
pip install numpy matplotlib scipy
```

## Usage

### Synthetic demo

```bash
python DTQEM_v63.0.py
```

### Real CSV data

```bash
python DTQEM_v63.0.py your_scan_data.csv
```

### In Google Colab / Jupyter

```python
from DTQEM_v63 import PhenomenologicalModel, extract_tau_c_from_scan

model = PhenomenologicalModel()
tau_c = model.tau_c(m_kg=720*1.66e-27, v_ms=200.0, N=60)
print(f"Ï„_c = {tau_c:.3e} s")
```

## Output files

| File | Description |
|------|-------------|
| `output_v63/v63_results.csv` | Extracted \(\tau_c\), slope, RÂ² per particle |

## Citation

If you use DTQEM v63.0 in your research, please cite:

```bibtex
@software{DTQEM_v63_2026,
  author  = {Berramdane, Reddouane},
  title   = {DTQEM v63.0: Phenomenological Scaling Model for Decoherence Time \(\tau_c\)},
  year    = {2026},
  version = {63.0},
  url     = {https://github.com/reddoma742/Davisson-Germer-DTQEM},
  note    = {Model: Ï„_c = Ï„_c0 / [m^Î²Â·(v/c)^Î´Â·(1+Î¶N)] with Î²â‰ˆ0.44, Î´â‰ˆ0.33, Î¶â‰ˆ0.005}
}
```

## Repository structure

```text
DTQEM_Project/
â”œâ”€â”€ DTQEM_v63.0.py
â”œâ”€â”€ HISTORY.md
â”œâ”€â”€ LICENSE
â”œâ”€â”€ README.md
â”œâ”€â”€ CITATION.cff
â”œâ”€â”€ output_v63/
â”‚   â””â”€â”€ v63_results.csv
â””â”€â”€ data/
```

## Important limitations

1. This is a phenomenological model, not a first-principles derivation.
2. \(\tau_{c0}\) is environment-dependent, not universal.
3. The calibration is synthetic; experimental validation is pending.
4. Valid range: mass 100â€“10,000 amu, speed 50â€“500 m/s, room temperature, high vacuum.

## Acknowledgments

Development assisted by:

- Google Gemini â€” theoretical discussions
- DeepSeek â€” critical analysis and insights
- Claude (Anthropic) â€” code writing and derivations
- Max & Kiwi â€” discussions of \(\beta\approx 1/2\), \(\delta\approx 1/3\), and \(\zeta\approx 0.005\)

## Contact

- Author: Reddouane Berramdane
- Email: reddoma@gmail.com
- GitHub: reddoma742/Davisson-Germer-DTQEM

## License

MIT License â€” see `LICENSE`.
