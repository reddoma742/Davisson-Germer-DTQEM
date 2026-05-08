# tests/test_isolated_tunneling.py
import sys
import numpy as np
sys.path.append('..')
from core.tunneling_engine import TunnelingEngine

def test_isolated_tunneling_accuracy():
    Delta_eV = 1.0  # 1 meV
    t_max_ps = 5.0
    t_max = t_max_ps * 1e-12
    engine = TunnelingEngine(Delta_eV=Delta_eV/1000.0, gamma_phi0=0.0, gamma_relax0=0.0)
    t_arr, P_num, _, _ = engine.tunneling_dynamics(T=0, t_max=t_max, num_points=100)
    P_ana = engine.isolated_P_right(t_arr, Delta_eV/1000.0)
    max_error = np.max(np.abs(P_num - P_ana))
    assert max_error < 1e-12, f"Max error in tunneling: {max_error:.2e}"
    print("✓ test_isolated_tunneling_accuracy passed (max error = {:.2e})".format(max_error))

if __name__ == "__main__":
    test_isolated_tunneling_accuracy()
