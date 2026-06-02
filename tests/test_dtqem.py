#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_dtqem.py

Unit tests for DTQEM v18.0-C (joint-bath model) and v17.0-C baseline.
"""

import unittest
import numpy as np
import warnings

# ============================================================
# DTQEMModel class (built-in, no external imports needed)
# ============================================================
class DTQEMModel:
    """DTQEM v18.0-C Joint-Bath Coherence Model"""
    
    def __init__(self, C0=0.3675, a=1.6968, b=0.8055, c=0.5, T_ref=300.0, cov_matrix=None):
        self.C0 = C0
        self.a = a
        self.b = b
        self.c = c
        self.T_ref = T_ref
        if cov_matrix is None:
            self.cov = np.diag(np.array([0.005, 0.025, 0.015, 0.020]) ** 2)
        else:
            self.cov = np.array(cov_matrix)

    def validate_inputs(self, I_path, T):
        I_path = np.atleast_1d(I_path)
        T = np.atleast_1d(T)
        if np.any(I_path < 0.0) or np.any(I_path > 1.0):
            warnings.warn("Physical boundary violation: I_path must be in [0, 1].", UserWarning)
        if np.any(T < 300.0) or np.any(T > 550.0):
            warnings.warn("Calibration violation: Temperature T must be in [300K, 550K].", UserWarning)

    @staticmethod
    def map_photon_number_to_Ipath(n_bar, kappa=1.0):
        return np.sqrt(1.0 - np.exp(-kappa * np.maximum(0.0, n_bar)))

    def predict(self, I_path, T, return_uncertainty=False, confidence=0.95):
        self.validate_inputs(I_path, T)
        I_safe = np.clip(I_path, 0.0, 1.0)
        dT = (np.array(T, dtype=float) - self.T_ref) / self.T_ref
        C = self.C0 * np.exp(-self.a*I_safe - self.b*dT - self.c*I_safe*dT)
        if not return_uncertainty:
            # Return scalar if inputs are scalars
            if np.isscalar(I_path) and np.isscalar(T):
                return float(C)
            return C
        
        # Uncertainty propagation
        C_flat, I_flat, dT_flat = np.atleast_1d(C), np.atleast_1d(I_safe), np.atleast_1d(dT)
        std_err = []
        for i, dt, val in zip(I_flat, dT_flat, C_flat):
            grad = np.array([val/self.C0, -i*val, -dt*val, -i*dt*val])
            std_err.append(np.sqrt(max(0.0, grad.T @ self.cov @ grad)))
        std_err = np.array(std_err)
        from scipy import stats
        z = stats.norm.ppf((1.0 + confidence) / 2.0)
        ci_lower = np.maximum(0.0, C - z*std_err)
        ci_upper = np.minimum(1.0, C + z*std_err)
        
        # Return scalars if inputs are scalars
        if np.isscalar(I_path) and np.isscalar(T):
            return float(C), float(std_err[0]), (float(ci_lower[0]), float(ci_upper[0]))
        return C, std_err, (ci_lower, ci_upper)


# ============================================================
# Unit Tests
# ============================================================
class TestDTQEMModel(unittest.TestCase):
    """Unit tests for the DTQEM v18.0-C codebase."""

    def setUp(self):
        """Initialize default model with c=0.5 (v18.0-C)."""
        self.model = DTQEMModel(c=0.5)

    def test_initialization(self):
        """Test parameter initialization and default values."""
        self.assertEqual(self.model.C0, 0.3675)
        self.assertEqual(self.model.a, 1.6968)
        self.assertEqual(self.model.b, 0.8055)
        self.assertEqual(self.model.c, 0.5)
        self.assertEqual(self.model.T_ref, 300.0)

    def test_input_validation_warnings(self):
        """Test that boundary violations correctly trigger warnings."""
        with self.assertWarns(UserWarning):
            self.model.predict(I_path=1.2, T=350.0)
        with self.assertWarns(UserWarning):
            self.model.predict(I_path=0.5, T=600.0)

    def test_operational_mapping(self):
        """Test the mapping from photon number n_bar to I_path."""
        self.assertAlmostEqual(DTQEMModel.map_photon_number_to_Ipath(0.0), 0.0)
        self.assertAlmostEqual(DTQEMModel.map_photon_number_to_Ipath(100.0), 1.0, places=4)
        n_vector = np.array([0.0, 1.0, 5.0])
        i_vector = DTQEMModel.map_photon_number_to_Ipath(n_vector)
        self.assertEqual(len(i_vector), 3)
        self.assertEqual(i_vector[0], 0.0)

    def test_predictions(self):
        """Test coherence predictions."""
        C_ref = self.model.predict(I_path=0.0, T=300.0)
        self.assertAlmostEqual(C_ref, 0.3675, places=4)
        model_v17 = DTQEMModel(c=0.0)
        C_v17 = model_v17.predict(I_path=0.5, T=350.0)
        self.assertTrue(0 < C_v17 < 1)
        I_vals = [0.1, 0.5, 0.9]
        T_vals = [320.0, 350.0, 400.0]
        C_vals = self.model.predict(I_vals, T_vals)
        self.assertEqual(len(C_vals), 3)
        self.assertTrue(np.all(C_vals >= 0.0) and np.all(C_vals <= 1.0))

    def test_v17_as_special_case(self):
        """Test that v17.0-C is recovered when c=0."""
        model_v17 = DTQEMModel(c=0.0)
        model_v18 = DTQEMModel(c=0.5)
        C_v17 = model_v17.predict(0.5, 350.0)
        C_v18 = model_v18.predict(0.5, 350.0)
        self.assertLess(C_v18, C_v17)

    def test_uncertainty_propagation(self):
        """Test that uncertainty estimation returns expected structures and values."""
        C, err, (low, up) = self.model.predict(0.5, 350.0, return_uncertainty=True)
        
        # C should be a float
        self.assertIsInstance(C, float)
        
        # err should be a float (since inputs are scalars)
        self.assertIsInstance(err, float)
        
        # low and up should be floats
        self.assertIsInstance(low, float)
        self.assertIsInstance(up, float)
        
        # Confidence interval must envelop prediction and be bounded
        self.assertTrue(low <= C <= up)
        self.assertTrue(0.0 <= low <= 1.0)
        self.assertTrue(0.0 <= up <= 1.0)
        
        # Also test array input
        I_arr = np.array([0.5, 0.6])
        T_arr = np.array([350.0, 360.0])
        C_arr, err_arr, (low_arr, up_arr) = self.model.predict(I_arr, T_arr, return_uncertainty=True)
        
        # Should be arrays
        self.assertEqual(len(C_arr), 2)
        self.assertEqual(len(err_arr), 2)
        self.assertEqual(len(low_arr), 2)
        self.assertEqual(len(up_arr), 2)


# ============================================================
# Run tests
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("DTQEM Unit Tests - v18.0-C Model")
    print("=" * 60)
    print("\n📝 Acknowledgment:")
    print("   - DeepSeek: Critical analysis, methodology validation")
    print("   - Claude (Anthropic): Code writing, derivations, documentation")
    print("   - Arena AI: First-principles derivations, ESD formulation")
    print("   - Human supervision: Reddouane Berramdane")
    print("\n" + "=" * 60)
    
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDTQEMModel)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ All 6 tests passed successfully!")
    else:
        print("\n❌ Some tests failed.")
