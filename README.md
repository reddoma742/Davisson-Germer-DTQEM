# Paper I: A Single-Mode Occupation-Number Model for D(T) in NV Centers

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20819966.svg)](https://doi.org/10.5281/zenodo.20819966) 

**Part of the DTQEM (Decoherence-Temperature Quantum Effective Model) project.**

> *A physically motivated single-mode occupation-number model for the temperature-dependent zero-field splitting in NV centers.*

---

## 📊 Key Results

| Metric | Value |
|:---|:---|
| **Model** | D(T) = D₀ + A·n(ν̃,T) — 3 parameters |
| **Calibration R²** | 0.999946 (Ouyang et al., 298–383 K) |
| **Effective phonon wavenumber** | ν̃ = 711 ± 48 cm⁻¹ (≈ 88 meV) |
| **Extrapolation R² (to 1000 K)** | 0.998185 (Liu et al. benchmark) |
| **Max deviation at 1000 K** | < 2 MHz |
| **Power-law failure at 1000 K** | Deviation > 70 MHz |

---

## 📁 Repository Structure
Paper_I_DTQEM/
├── main.tex # Final manuscript (LaTeX)
├── DTQEM_figures_COLAB.py # Figure generation code
├── cover_letter.tex # Cover letter for submission
├── README.md # This file
├── HISTORY.md # Development history
├── LICENSE # CC BY-NC-SA 4.0
├── CITATION.cff # Citation metadata
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore rules
├── fig1_dtqem_fit_final.png/pdf # Figure 1
├── fig2_MC_bands_final.png/pdf # Figure 2
├── paper_I_final.pdf # Compiled manuscript
└── archive/ # Previous versions

text

---

## 🚀 Quick Start

### Generate figures

```bash
python DTQEM_figures_COLAB.py
Compile manuscript
bash
pdflatex main.tex
pdflatex main.tex
Requirements
Python 3.8+ with numpy, scipy, matplotlib

LaTeX distribution (TeXLive, MiKTeX)

📄 Citation
bibtex
@article{berramdane2026dtqem_paperI,
  author  = {Berramdane, Reddouane},
  title   = {A Single-Mode Occupation-Number Model for Temperature-Dependent
             Zero-Field Splitting in NV Centers},
  year    = {2026},
  note    = {arXiv:XXXX.XXXXX (submitted)}
}
🙏 Acknowledgments
Human scientific supervision: Reddouane Berramdane

AI assistance (as computational tools):

DeepSeek — code development, data extraction, critical analysis

Claude (Anthropic) — code polishing, LaTeX manuscript, philosophical discussions

Grok (xAI) — scientific review, transport integral framework

Perplexity AI — literature survey, methodological feedback

📬 Contact
Author: Reddouane Berramdane

Email: reddoma@gmail.com

Part of: DTQEM Project

text

---


