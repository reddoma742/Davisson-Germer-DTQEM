```markdown
# Paper I: A Single-Mode Occupation-Number Model for Temperature-Dependent Zero-Field Splitting in NV Centers

**Author:** Reddouane BERRAMDANE  
**Affiliation:** Independent Researcher  
**Date:** June 21, 2026  
**License:** [To be added]

---

## Overview

This repository contains the complete source code, figures, and manuscript for **Paper I** of the DTQEM (Dynamic Temperature-Quantum Effective Model) project. The paper presents a physically motivated single-mode occupation-number model for the temperature-dependent zero-field splitting \(D(T)\) in nitrogen-vacancy (NV) centers in diamond.

### Key Results
- **Model:** \(D(T) = D_0 + A \cdot n(\omega, T)\) — 3 parameters, Bose-Einstein occupation
- **Calibration:** \(R^2 = 0.999946\) on Ouyang et al. data (298–383 K)
- **Effective phonon frequency:** \(\omega = 711 \pm 48\) cm⁻¹ (88 meV)
- **Extrapolation to 1000 K:** \(R^2 = 0.998185\) — validated against Liu et al.
- **Power law failure:** Deviations > 70 MHz outside calibration window

---

## Repository Structure

```

Paper_I_DTQEM/
├── main.tex                       # LaTeX manuscript (complete)
├── DTQEM_figures_COLAB.py         # Python script to generate figures
├── cover_letter.tex               # Cover letter for journal submission
├── README.md                      # This file
├── fig1_dtqem_fit_final.png       # Figure 1 — PNG format
├── fig1_dtqem_fit_final.pdf       # Figure 1 — PDF format (high resolution)
├── fig2_MC_bands_final.png        # Figure 2 — PNG format
├── fig2_MC_bands_final.pdf        # Figure 2 — PDF format (high resolution)
└── paper_I_final.pdf              # Compiled manuscript (for quick reading)

```

---

## How to Compile the Manuscript

### Option 1: Using the pre-compiled PDF
Simply open `paper_I_final.pdf` to read the manuscript.

### Option 2: Compile from source
```bash
pdflatex main.tex
pdflatex main.tex
```

Option 3: Online (Overleaf)

1. Create a new project on Overleaf.
2. Upload all files from this repository.
3. Set the compiler to pdfLaTeX.
4. Click Recompile.

---

How to Generate the Figures

In Google Colab

1. Upload DTQEM_figures_COLAB.py to Google Colab.
2. Run the entire script in a single cell.
3. Figures will be saved in ./output/ and downloaded automatically.

Local Machine

```bash
python DTQEM_figures_COLAB.py
```

Requirements: Python 3.x with numpy, scipy, matplotlib.

---

Data Sources

Data Source Reference
Ouyang et al. (calibration) Table 1, Phys. Rev. Research 6, 023078 (2024) ouyang2024
Liu et al. (validation) Digitized from Fig. 2(c), Nat. Commun. 10, 1344 (2019) liu2019

---

Citation

If you use this work, please cite:

```bibtex
@article{berramdane2026,
  title  = {A Single-Mode Occupation-Number Model for Temperature-Dependent
            Zero-Field Splitting in NV Centers},
  author = {Reddouane Berramdane},
  year   = {2026},
  doi    = {[TO BE PROVIDED]}
}
```

---

Acknowledgments

The author thanks colleagues and collaborators for valuable discussions and methodological feedback. The DeepSeek and Claude (Anthropic) AI systems are acknowledged for assistance with code development, data extraction, literature survey, LaTeX manuscript preparation, and scientific discussion.

---

Related Work

This is Paper I of the DTQEM series. Future papers will address:

· Paper II: Transport integral description of T_1(T) relaxation
· Paper III: Dephasing time T_2(T) and multi-channel decoherence

---

Contact

For questions or collaboration inquiries, please contact the author.

---

```
