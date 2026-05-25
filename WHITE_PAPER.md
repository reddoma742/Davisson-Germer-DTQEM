# DTQEM v63.1: Phenomenological Scaling Model for Decoherence Time \(\tau_c\)

**White Paper â€” Improved Draft**  
**Author:** Berramdane Reddouane (Morocco)  
**Date:** May 2026  
**Repository:** [Davisson-Germer-DTQEM](https://github.com/reddoma742/Davisson-Germer-DTQEM)  
**DOI:** To be assigned

## Abstract

We present a phenomenological scaling model for the decoherence time \(\tau_c\) within the DTQEM framework. The baseline visibility law is

\[
V_{\mathrm{eff}} = \exp(-\gamma_\phi T_{\mathrm{eff}})\,\exp\!\left(-\frac{|\Delta\tau|}{\tau_c}\right).
\]

The extracted scaling law is

\[
\tau_c = \frac{\tau_{c0}}{m^{\beta}\,(v/c)^{\delta}\,(1+\zeta N)}.
\]

The current coefficients are obtained from synthetic calibration and should be interpreted as effective parameters, not universal constants. The main purpose of this white paper is to document the model, its inverse-extraction procedure, its testable predictions, and its present limitations.

## 1. Motivation

The DTQEM idea is that an interferometric visibility loss can be described by two conceptually distinct contributions. The first is ordinary environmental decoherence, summarized by \(\gamma_\phi\) and \(T_{\mathrm{eff}}\). The second is an intrinsic proper-time mismatch term controlled by \(\tau_c\). This separation is useful because it allows one to study whether the observed loss of coherence comes from the environment, internal structure, or an additional effective relativistic scale.

The model is intentionally phenomenological. It does not claim that \(\tau_c\) is a fundamental constant. Rather, \(\tau_c\) is treated as an effective coherence scale that may depend on mass, speed, and internal complexity.

## 2. Baseline model

For a Machâ€“Zehnder-type geometry, we define

\[
V_{\mathrm{eff}} = V_{\mathrm{env}}\,V_{\mathrm{dtqem}},
\qquad
V_{\mathrm{env}} = \exp(-\gamma_\phi T_{\mathrm{eff}}),
\qquad
V_{\mathrm{dtqem}} = \exp\!\left(-\frac{|\Delta\tau|}{\tau_c}\right).
\]

Here \(|\Delta\tau|\) is the proper-time mismatch between the two arms of the interferometer, and \(T_{\mathrm{eff}}\) is the effective interaction time. The key advantage of this form is that it remains simple enough for inversion from visibility scans, yet flexible enough to accommodate different particle classes.

## 3. Scaling law

The calibrated phenomenological law is

\[
\tau_c = \frac{\tau_{c0}}{m^{\beta}\,(v/c)^{\delta}\,(1+\zeta N)}.
\]

In the current version, the best-fit values are approximately

- \(\tau_{c0} \approx 9.8 \times 10^{-27}\,\mathrm{s}\)
- \(\beta \approx 0.44\)
- \(\delta \approx 0.33\)
- \(\zeta \approx 0.005\)

These values should be read as *effective scaling exponents* over the explored domain, not as exact theoretical identities.

## 4. Physical interpretation

### 4.1 Mass dependence

The exponent \(\beta\) is close to \(1/2\), which is consistent with many coarse-grained mechanisms where the relevant scale depends on a fluctuation amplitude, a width, or a diffusion-like quantity. We therefore interpret the mass dependence as a sublinear suppression of coherence time with increasing inertial scale.

### 4.2 Velocity dependence

The exponent \(\delta\) is close to \(1/3\). In the present formulation this should be treated as an effective transport exponent. It may reflect the way proper-time mismatch, dwell time, or scattering-related transport effects map velocity into a decoherence rate.

### 4.3 Internal complexity

The factor \((1+\zeta N)\) encodes the idea that more internal structure offers more channels for phase information to leak away from the center-of-mass coherence. Here \(N\) is used as a proxy for internal degrees of freedom. The small value of \(\zeta\) indicates that each additional atom contributes only a weak correction, but the correction becomes relevant for large clusters.

## 5. Interpretation of \(\tau_{c0}\)

The parameter \(\tau_{c0}\) is best understood as a reference scale determined by experimental conditions and the chosen coarse-graining. It may absorb the influence of background pressure, temperature, device geometry, residual gas scattering, and internal mode coupling.

At the current stage, it is not justified to claim that \(\tau_{c0}\) is derivable from fundamental constants alone. A more conservative statement is that \(\tau_{c0}\) is an effective calibration constant.

## 6. Inverse extraction method

A single visibility point is generally insufficient to separate environmental damping from the proper-time term. For that reason, the model uses a logarithmic-slope inversion.

If one measures \(V_{\mathrm{eff}}\) at multiple values of \(|\Delta\tau|\), then

\[
\ln V_{\mathrm{eff}} = A - \frac{|\Delta\tau|}{\tau_c},
\]

where \(A\) is a constant offset. A linear regression of \(\ln V_{\mathrm{eff}}\) against \(|\Delta\tau|\) yields a slope equal to \(-1/\tau_c\). This is numerically stable and substantially reduces the inversion ambiguity present in single-point measurements.

## 7. Testable predictions

The model becomes scientifically valuable when it produces clear discriminating tests.

- **Pressure dependence:** If \(\tau_c\) is independent of pressure, the effect is more likely intrinsic; if it scales as \(1/P\), environmental decoherence is dominant.
- **Mass scaling:** The model predicts \(\tau_c \propto m^{-0.44}\) over the current calibration range.
- **Velocity scaling:** The model predicts \(\tau_c \propto v^{-0.33}\) over the current calibration range.
- **Temperature dependence:** A systematic temperature scan can reveal whether the extracted coherence scale is dominated by internal excitations or environmental coupling.
- **Complexity dependence:** Replacing \(N\) by a more refined internal descriptor should improve future fits if internal structure truly matters.

## 8. Domain of validity

The present law is expected to hold only under restricted conditions:

1. The particles are effectively neutral, or charge effects are negligible.
2. Velocities remain non-relativistic or weakly relativistic.
3. The environment is approximately stationary during the scan.
4. The internal structure can be summarized by a single complexity proxy.
5. Decoherence contributions are weak enough to be approximated by an effective exponential law.

Outside these conditions, the model may need additional terms, such as charge dependence, non-Markovian corrections, or explicit environmental cross sections.

## 9. Limitations

This version is still limited in several important ways.

- The calibration is synthetic, not yet based on a broad experimental dataset.
- The proposed interpretations of the exponents are plausible but not uniquely derived.
- The proxy \(N\) is coarse and may be replaced by vibrational-mode counts, internal entropy, or spectral density measures.
- The parameter \(\tau_{c0}\) currently lacks a first-principles derivation.
- The model should be compared against established collisional-decoherence and collapse-model predictions before any strong claims are made.

## 10. Relation to existing decoherence ideas

The strength of the present work is not that it replaces all existing decoherence models, but that it offers a compact scaling form that can be checked experimentally. In particular, it should be contrasted with environmental collisional decoherence, internal-state decoherence, and collapse-model-inspired scaling laws. Such comparisons will help determine whether the proper-time term is genuinely new or merely a reparameterization of known effects.

## 11. Implementation summary

The associated codebase includes:

- synthetic data generation,
- logarithmic-slope extraction of \(\tau_c\),
- calibration of \(\beta\), \(\delta\), and \(\zeta\),
- CSV output for post-processing,
- and comparison plots for model selection.

The code is useful because it makes the model reproducible and allows future replacement of synthetic inputs with real measurements.

## 12. Conclusion

DTQEM v63.1 should be read as a carefully constrained phenomenological framework. Its main contribution is a simple and testable scaling law for the decoherence time,

\[
\tau_c = \frac{\tau_{c0}}{m^{\beta}\,(v/c)^{\delta}\,(1+\zeta N)},
\]

together with an inversion method that stabilizes parameter extraction from interferometric visibility scans.

The next critical step is experimental validation. The most decisive tests are pressure dependence, controlled velocity scans, and comparisons across particles with different internal complexity.

---

*This draft is intended as an improved working white paper. It should be revised again once real experimental data become available.*
