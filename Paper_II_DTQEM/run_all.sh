#!/bin/bash
echo "Running J5 Model Validation..."
python J5_Model_Validation.py
echo "Compiling LaTeX..."
pdflatex paper_II.tex
pdflatex paper_II.tex
echo "Done. See paper_II.pdf and output/ directory."
