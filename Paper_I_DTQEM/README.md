```markdown
# Paper I: A Single-Mode Occupation-Number Model for D(T) in NV Centers

## Files

- `DTQEM_Paper_I.tex` - Main LaTeX manuscript
- `generate_figures.py` - Python script to generate figures
- `fig1_dtqem_fit.pdf` - Figure 1 (generated)
- `fig2_extrapolation.pdf` - Figure 2 (generated)
- `cover_letter.tex` - Cover letter for submission

## How to compile

### 1. Generate figures

```bash
python generate_figures.py
```

2. Compile LaTeX

```bash
pdflatex DTQEM_Paper_I.tex
pdflatex DTQEM_Paper_I.tex
```

Requirements

· Python 3.x with numpy, scipy, matplotlib
· LaTeX distribution (TeXLive, MiKTeX, etc.)

```
