
```markdown
# DTQEM Papers – Overview

This directory contains the three core papers of the DTQEM project, documenting the development from a phenomenological model to a full microscopic theory of joint-bath decoherence.

---

## Paper I: Phenomenological Joint-Bath Decoherence Model (v18.0‑C)

**File:** `DTQEM_PaperI_Phenomenological_v1.0.tex`  
**Compiled PDF:** `DTQEM_PaperI_Phenomenological_v1.0.pdf`

| Field | Information |
|-------|-------------|
| **Title** | DTQEM: A Phenomenological Model for Correlated Path‑Information and Thermal Decoherence (v18.0‑C) |
| **Status** | ✅ Published (Zenodo) |
| **DOI** | [10.5281/zenodo.20670032](https://doi.org/10.5281/zenodo.20670032) |
| **Abstract** | We present a phenomenological model for quantum decoherence in systems simultaneously subject to path‑information extraction and thermal dephasing. The coherence function extends the independent‑bath baseline by a bilinear cross‑coupling term, capturing the synergistic action of correlated environmental modes. |

**Compilation:**
```bash
pdflatex DTQEM_PaperI_Phenomenological_v1.0.tex
bibtex DTQEM_PaperI_Phenomenological_v1.0
pdflatex DTQEM_PaperI_Phenomenological_v1.0.tex
pdflatex DTQEM_PaperI_Phenomenological_v1.0.tex
```

---

Paper II: Microscopic Derivation of Joint‑Bath Decoherence

File: DTQEM_PaperII_Microscopic_v1.0.tex
Compiled PDF: DTQEM_PaperII_Microscopic_v1.0.pdf

Field Information
Title Microscopic Derivation of Joint‑Bath Decoherence: Cross‑Spectral Density and Inter‑Bath Correlation in Coupled Bosonic Reservoirs
Status ✅ Published (Zenodo, companion to Paper I)
DOI 10.5281/zenodo.20670032 (same DOI – companion paper)
Abstract Starting from a generalized Caldeira–Leggett model with mutually coupled bosonic baths, we perform a canonical transformation that yields an explicit cross‑spectral density $J_{12}(\omega)$ and prove the Cauchy–Schwarz bound $

Compilation:

```bash
pdflatex DTQEM_PaperII_Microscopic_v1.0.tex
bibtex DTQEM_PaperII_Microscopic_v1.0
pdflatex DTQEM_PaperII_Microscopic_v1.0.tex
pdflatex DTQEM_PaperII_Microscopic_v1.0.tex
```

---

Paper III: Vibronic‑Mediated Temperature‑Dependent Dephasing

File: DTQEM_PaperIII_Vibronic_Mediated_Decoherence_v1.0.tex
Compiled PDF: DTQEM_PaperIII_Vibronic_Mediated_Decoherence_v1.0.pdf

Field Information
Title Vibronic‑Mediated Decoherence: A Microscopic Foundation for Temperature‑Dependent Dephasing in DTQEM
Status 🔜 Complete, ready for submission (arXiv & Zenodo pending)
DOI (to be assigned after Zenodo upload)
Abstract We derive the temperature dependence of the path‑dephasing coefficient from a shared vibronic mode using the exact independent‑boson solution. The effective coefficient $a_{\text{eff}}(T)=a_0+2S\coth(\hbar\omega_v/2k_BT)$ replaces the earlier bilinear term, predicts low‑$T$ saturation, high‑$T$ linear growth, and an isotope‑dependent crossover $T^*$. The Huang–Rhys factor $S=g^2/\omega_v^2$ links the model to independently measurable optical spectroscopy.

Compilation:

```bash
pdflatex DTQEM_PaperIII_Vibronic_Mediated_Decoherence_v1.0.tex
bibtex DTQEM_PaperIII_Vibronic_Mediated_Decoherence_v1.0
pdflatex DTQEM_PaperIII_Vibronic_Mediated_Decoherence_v1.0.tex
pdflatex DTQEM_PaperIII_Vibronic_Mediated_Decoherence_v1.0.tex
```

---

Notes for users

· Papers I and II share the same Zenodo DOI because they are two parts of the same foundational work (phenomenological + microscopic derivation).
· Paper III is the new, independent work that generalises the bilinear term to a temperature‑dependent vibronic coefficient. It should be cited separately after its own DOI is obtained.
· All papers use the revtex4‑2 document class (APS, PRL style). Compilation requires a standard LaTeX distribution with bibtex.

---

Last updated: June 2026
Maintainer: Reddouane Berramdane

```
