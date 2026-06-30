# Paper II: A Unified DTQEM Framework

## Overview
This directory contains the second paper of the DTQEM series, which extends 
the single-mode model (Paper I) to spin-lattice relaxation T₁(T) using a 
Debye-Raman transport integral J₅.

## Contents
- `paper_II.tex` — LaTeX manuscript (final version)
- `paper_II.pdf` — Compiled PDF
- `J5_Model_Validation.py` — Python script to reproduce Figures 1 & 2
- `fig1_J5_fit_Jarmola_final.png/pdf` — Figure 1: J₅ fits for Jarmola samples
- `fig2_model_comparison_final.png/pdf` — Figure 2: Model comparison on S2

## Key Results
- Θ_eff = 596 ± 88 K across three Jarmola ensemble samples
- The coth(x) = 2n(x)+1 identity unifies static shifts, dephasing, and relaxation
- The single-mode Raman factor n(n+1) has a T² ceiling, requiring continuum J₅

## Dependencies
- Python 3.x with numpy, scipy, matplotlib

## Author
Reddouane BERRAMDANE — reddoma@gmail.com
