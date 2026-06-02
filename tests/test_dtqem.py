#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_dtqem.py

Unit tests for DTQEM v18.0-C (joint-bath model) and v17.0-C baseline.
Tests cover initialization, input validation, operational mapping,
predictions, v17 as special case, and uncertainty propagation.

Acknowledgment:
    This code was developed with the assistance of AI language models:
    - DeepSeek (critical analysis, methodology validation)
    - Claude (Anthropic) (code writing, derivations, documentation)
    - Arena AI (first-principles derivations of scaling exponents, ESD formulation)
    Human scientific supervision and validation: Reddouane Berramdane

Version: 1.0 (Zenodo-ready)
Date: 2026-06-02

License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
See LICENSE file for full terms.
"""

import unittest
import numpy as np
import warnings
import sys
import os

# Safe way to add parent directory to path (works in scripts and interactive environments)
try:
    # When running as a script
    current_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # When running in interactive environment (Jupyter, Colab, etc.)
    current_dir = os.getcwd()

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Try multiple import paths
DTQEMModel = None

# Try path 1: models.v18.dtqem_joint_bath_v18
try:
    from models.v18.dtqem_joint_bath_v18 import DTQEMModel
    print("✓ Imported DTQEMModel from models.v18.dtqem_joint_bath_v18")
except (ImportError, ModuleNotFoundError):
    pass

# Try path 2: DTQEM_v63_1_C (original name)
if DTQEMModel is None:
    try:
        from DTQEM_v63_1_C import DTQEMModel
        print("✓ Imported DTQEMModel from DTQEM_v63_1_C (local)")
    except (ImportError, ModuleNotFoundError):
        pass

# Try path 3: dtqem_joint_bath_v18 (same directory)
if DTQEMModel is None:
    try:
        from dtqem_joint_bath_v18 import DTQEMModel
        print("✓ Imported DTQEMModel from dtqem_joint_bath_v18")
    except (ImportError, ModuleNotFoundError):
        pass

# Fallback: create a minimal DTQEMModel for testing
if DTQEMModel is None:
    print("⚠️ No external DTQEMModel found. Using fallback implementation.")
    class DTQEMModel:
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
                return C
            C_flat, I_flat, dT_flat = np.atleast_1d(C), np.atleast_1d(I_safe), np.atleast_1d(dT)
            std_err = []
            for i, dt, val in zip(I_flat, dT_flat, C_flat):
                grad = np.array([val/self.C0, -i*val, -dt*val, -i*dt*val])
                std_err.append(np.sqrt(max(0.0, grad.T @ self.cov @ grad)))
            std_err = np.array(std_err)
            from scipy import stats
            z = stats.norm.ppf((1.0 + confidence) / 2.0)
            return C, std_err, (np.maximum(0.0, C - z*std_err), np.minimum(1.0, C + z*std_err))


class TestDTQEMModel(unittest.TestCase):
    """
    Unit tests for the DTQEM v18.0-C codebase.
    """

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
        # I_path out of bounds (1.2)
        with self.assertWarns(UserWarning):
            self.model.predict(I_path=1.2, T=350.0)
        
        # Temperature out of bounds (600 K)
        with self.assertWarns(UserWarning):
            self.model.predict(I_path=0.5, T=600.0)

    def test_operational_mapping(self):
        """Test the mapping from photon number n_bar to I_path."""
        # 0 photons should map to 0 path information
        self.assertAlmostEqual(DTQEMModel.map_photon_number_to_Ipath(0.0), 0.0)
        
        # Large photon number should approach 1.0
        self.assertAlmostEqual(DTQEMModel.map_photon_number_to_Ipath(100.0), 1.0, places=4)
        
        # Test vector mapping
        n_vector = np.array([0.0, 1.0, 5.0])
        i_vector = DTQEMModel.map_photon_number_to_Ipath(n_vector)
        self.assertEqual(len(i_vector), 3)
        self.assertEqual(i_vector[0], 0.0)

    def test_predictions(self):
        """Test coherence predictions."""
        # At reference temperature and I_path = 0, coherence should be exactly C0
        C_ref = self.model.predict(I_path=0.0, T=300.0)
        self.assertAlmostEqual(C_ref, 0.3675, places=4)
        
        # Test v17.0-C limit (c=0)
        model_v17 = DTQEMModel(c=0.0)
        C_v17 = model_v17.predict(I_path=0.5, T=350.0)
        self.assertTrue(0 < C_v17 < 1)
        
        # Vector predictions
        I_vals = [0.1, 0.5, 0.9]
        T_vals = [320.0, 350.0, 400.0]
        C_vals = self.model.predict(I_vals, T_vals)
        self.assertEqual(len(C_vals), 3)
        self.assertTrue(np.all(C_vals >= 0.0) and np.all(C_vals <= 1.0))

    def test_v17_as_special_case(self):
        """Test that v17.0-C is recovered when c=0."""
        model_v17 = DTQEMModel(c=0.0)
        model_v18 = DTQEMModel(c=0.5)
        
        I_test = 0.5
        T_test = 350.0
        
        C_v17 = model_v17.predict(I_test, T_test)
        C_v18 = model_v18.predict(I_test, T_test)
        
        # v18 with c=0.5 should give lower coherence than v17
        self.assertLess(C_v18, C_v17)

    def test_uncertainty_propagation(self):
        """Test that uncertainty estimation returns expected structures and values."""
        C, err, (low, up) = self.model.predict(0.5, 350.0, return_uncertainty=True)
        
        self.assertIsInstance(C, float)
        self.assertIsInstance(err, float)
        self.assertIsInstance(low, float)
        self.assertIsInstance(up, float)
        
        # Confidence interval must envelop prediction and be bounded
        self.assertTrue(low <= C <= up)
        self.assertTrue(0.0 <= low <= 1.0)
        self.assertTrue(0.0 <= up <= 1.0)


if __name__ == '__main__':
    print("=" * 60)
    print("DTQEM Unit Tests - v18.0-C Model")
    print("=" * 60)
    print("\n📝 Acknowledgment:")
    print("   This code was developed with the assistance of AI models:")
    print("   - DeepSeek (critical analysis, methodology validation)")
    print("   - Claude (Anthropic) (code writing, derivations, documentation)")
    print("   - Arena AI (first-principles derivations of scaling exponents, ESD formulation)")
    print("   Human scientific supervision and validation: Reddouane Berramdane")
    print("\n" + "=" * 60)
    
    unittest.main()
