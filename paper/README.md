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
