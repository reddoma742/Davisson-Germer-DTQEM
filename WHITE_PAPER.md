# DTQEM v17.0-C: Phenomenological Coherence Model

## White Paper — Final Version

**Author:** Berramdane Reddouane (Morocco)  
**Date:** May 2026  
**Repository:** [Davisson-Germer-DTQEM](https://github.com/reddoma742/Davisson-Germer-DTQEM)  
**DOI:** To be assigned  

---

## Abstract

We present DTQEM v17.0-C, a compact phenomenological model for the quantum coherence factor C in path-interference experiments. The model is calibrated on 8 experimental points and selected as the final recommended baseline because it achieves strong predictive performance with only 3 free parameters. The core law is  

\[
C = C_0 \, \exp\!\left(-a_{\mathrm{path}} I_{\mathrm{path}} - a_{\mathrm{temp}}\, \frac{\max(0, T_{\mathrm{env}}-T_{\mathrm{ref}})}{T_{\mathrm{ref}}}\right).
\]

The present white paper documents the physical meaning of the model, the calibration strategy, the validation metrics, and the reasons for preferring this compact form over more elaborate alternatives.

---

## 1. Motivation

The DTQEM project aims to describe coherence loss in a way that is both physically interpretable and numerically stable. Earlier versions explored several candidate mechanisms, including additional recovery terms, duality constraints, and nonlinear extensions. The final conclusion from this exploration is that a minimal model already captures the main structure of the data.

This version is therefore not a reduction in scientific value; it is a reduction in unnecessary complexity. In model building, a simpler model is preferred when it performs comparably to a larger one and remains easier to interpret, validate, and reproduce.

---

## 2. Baseline model

For the present path-interference setting, the coherence factor is modeled as  

\[
C = C_0 \, \exp\!\left(-a_{\mathrm{path}} I_{\mathrm{path}} - a_{\mathrm{temp}}\, \Delta T_{+}/T_{\mathrm{ref}}\right), \qquad \Delta T_{+} = \max(0, T_{\mathrm{env}}-T_{\mathrm{ref}}).
\]

Here:  

- \(C_0\) is the maximum coherence at zero which-path information and reference temperature.  
- \(I_{\mathrm{path}}\) is the normalized path-information variable.  
- \(a_{\mathrm{path}}\) controls the decoherence due to which-path information.  
- \(a_{\mathrm{temp}}\) controls thermal suppression above the reference temperature.  
- \(T_{\mathrm{ref}} = 300\,\mathrm{K}\) is the reference temperature.  

The use of the positive temperature excess \(\Delta T_{+}\) ensures that temperatures below the reference do not introduce an artificial negative thermal gain.

---

## 3. Calibrated parameters

The final fitted values are:  

- \(C_0 = 0.3675\)  
- \(a_{\mathrm{path}} = 1.6968\)  
- \(a_{\mathrm{temp}} = 0.8055\)  

These values were obtained from a small experimental dataset and should be interpreted as effective calibration constants rather than universal physical constants.  

The calibration dataset consists of **8 experimental measurements** (visibility values) obtained under controlled conditions:  
\(I_{\mathrm{path}}\) in \([0, 1]\) and \(T_{\mathrm{env}}\) in \([300\,\mathrm{K}, 550\,\mathrm{K}]\).

---

## 4. Model performance

The v17.0-C model performs strongly on the calibration data and remains stable under leave-one-out validation.

| Metric | Value |
|--------|-------|
| In-sample R² | 0.9679 |
| In-sample RMSE | 0.0202 |
| LOOCV R² | 0.9356 |
| LOOCV RMSE | 0.0286 |
| Number of data points | 8 |
| Number of free parameters | 3 |

The LOOCV result is especially important because it indicates that the model is not merely fitting noise; it generalizes reasonably well for such a small dataset.

---

## 5. Physical interpretation

The model can be read as the product of two suppressing effects:  

1. **Path-information suppression**: as which-path information increases, coherence decays exponentially.  
2. **Thermal suppression**: as the environment becomes hotter than the reference state, coherence is further reduced.  

This is consistent with the general complementarity picture in which visibility decreases when distinguishability increases. In this sense, the model is not trying to replace the duality principle; it is trying to encode it in a simple empirical form.

---

## 6. Why this version is final

The project explored more elaborate variants, including nonlinear path exponents (v17.1) and additional correction terms. Those variants sometimes improved the fit on the same data, but they did not improve the overall balance between predictive power, simplicity, and interpretability.  

For this reason, v17.0-C is the preferred baseline:  

- It has fewer parameters.  
- It is easier to explain physically.  
- It is easier to reproduce.  
- It is less sensitive to overfitting.  

This makes it the most suitable version for documentation, citation, and future extension.

---

## 7. Implementation summary

The associated codebase provides:  

- a vectorized coherence function,  
- fixed calibrated parameters,  
- a self-test reproducing representative values,  
- and a short, readable implementation suitable for archiving.  

The public function is:  

```python
coherence(I_path, T_env)
It returns a value in the interval [0, 1] and can handle scalar or array inputs.

The complete Python code is available in the repository under the filename dtqem_v17_0_C_coherence.py.

---

8. Limitations

This white paper describes a phenomenological model, not a first-principles derivation. The parameters were calibrated on a limited dataset, so the present values should not be overgeneralized.

With only 8 calibration points, the model is intended as a baseline for this specific dataset. Future work should re-calibrate with larger datasets to confirm parameter stability.

The model also assumes that coherence and visibility are interchangeable in this specific experimental context. If future experiments involve additional channels of decoherence, the model may need to be extended.

---

9. Relation to other versions

Compared with earlier DTQEM variants, v17.0-C is intentionally simpler. Compared with the later exploratory v17.1 nonlinear extension, it sacrifices some internal flexibility in exchange for better parsimony and stronger overall stability as a baseline model. That is why it is recommended as the final coherence model for the current stage of the project.

---

10. Conclusion

DTQEM v17.0-C provides a compact and reproducible phenomenological description of coherence loss in path-interference experiments. With only three parameters, it captures the main experimental trend while preserving a clear physical interpretation.

The model is archived as dtqem_v17_0_C_coherence.py and this white paper documents its final recommended state. It is well suited as the final baseline version for the project, pending any future dataset that may justify a deeper extension.

---

Acknowledgments

This white paper and the associated code were developed with the assistance of AI language models:

· DeepSeek — critical analysis, methodology validation, and discussion.
· Claude (Anthropic) — code writing, derivations, and documentation.

Human scientific supervision, experimental design, and validation: Reddouane Berramdane.

---

References

No external references are cited, as this work is self-contained and based on original experimental data and model calibration.

---

End of white paper — version v17.0-C, final.
