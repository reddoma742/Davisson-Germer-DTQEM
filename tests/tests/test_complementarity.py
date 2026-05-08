# tests/test_complementarity.py
import sys
import numpy as np
sys.path.append('..')
from core.tunneling_engine import TunnelingEngine

def test_complementarity_isolated():
    """For isolated system, V² + D² should be 1 (within numerical precision)."""
    Delta_eV = 1.0  # 1 meV
    engine = TunnelingEngine(Delta_eV=Delta_eV/1000.0, gamma_phi0=0.0, gamma_relax0=0.0)
    t_max = 5e-12
    t_arr, _, V, D = engine.tunneling_dynamics(T=0, t_max=t_max, num_points=200)
    comp = V**2 + D**2
    # Allow tiny numerical errors (should be close to 1)
    assert np.all(comp <= 1.0 + 1e-12), "V²+D² > 1 found in isolated case"
    assert np.all(comp >= 1.0 - 1e-12), "V²+D² < 1 found in isolated case"
    print("✓ test_complementarity_isolated passed")

def test_complementarity_with_dephasing():
    """With dephasing, V²+D² should be ≤ 1, and can drop significantly."""
    Delta_eV = 4.4  # meV
    gamma_phi0 = 5.24e12
    engine = TunnelingEngine(Delta_eV=Delta_eV/1000.0, gamma_phi0=gamma_phi0, gamma_relax0=0.0)
    t_max = 1e-12
    t_arr, _, V, D = engine.tunneling_dynamics(T=0, t_max=t_max, num_points=200)
    comp = V**2 + D**2
    assert np.all(comp <= 1.0 + 1e-12), "V²+D² > 1 with dephasing"
    # The minimum can be very low (e.g., 0.15) – we just assert it's not above 1.
    print("✓ test_complementarity_with_dephasing passed (min comp = {:.4f})".format(np.min(comp)))

if __name__ == "__main__":
    test_complementarity_isolated()
    test_complementarity_with_dephasing()
