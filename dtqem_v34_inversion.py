Running DTQEM v34.2 unit tests...
✓ test_concurrence passed
✓ test_double_slit_model passed
✓ test_estimate_d_from_fft passed
All tests passed.

======================================================================
DTQEM v34.2 – Validation experiments
======================================================================

--- Experiment 1: Phase shift φ = 0.3 rad ---
/tmp/ipykernel_3915/2632212167.py:314: UserWarning: Optimisation did not converge properly.
  warnings.warn("Optimisation did not converge properly.")
Recovered φ = 0.3083 rad (true = 0.3)
Model with phi selected: True (expected True)
Bootstrap success rate: 100.0% (expected >98%)

--- Experiment 2: Quadratic background (B2=5000) ---
d error = 0.029% (<0.5% expected)
χ²_red = 0.978
Bootstrap success rate: 100.0%

--- Experiment 3: High Poisson noise (std ~10 at peak) ---
d error = 0.213%, E error = 4.692%
Bootstrap CI for E: (np.float64(0.20701996752336585), np.float64(0.23297989651692724))
Bootstrap success rate: 100.0%

======================================================================
Original synthetic example (no phi, linear background)
======================================================================

============================================================
DTQEM v34.2 – Inversion results
============================================================
d = 499.76 µm
E = 0.20296 ± 0.00807 (95% CI: (np.float64(0.19744611200571427), np.float64(0.2289551088375872)))
I0 = 100.12 ± 0.78
χ²_red = 0.9911
AICc = 498.62 (model with phi = False)
Residuals: mean=-0.220, std=5.108, corr(x)=-0.0248
Bootstrap success rate: 99.3% (149/150)
Plot saved as v34_original_v34_fit.png

=== True parameters ===
d = 500.00 µm, E = 0.20, I0 = 100.0
