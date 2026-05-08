# tests/test_core.py
import sys
sys.path.append('..')
import numpy as np
from core.lindblad_solver import LindbladSolver
from core.tunneling_engine import TunnelingEngine

def test_isolated_tunneling():
    Delta_eV = 1.0  # meV
    t_max_ps = 5.0
    t_max = t_max_ps * 1e-12
    engine = TunnelingEngine(Delta_eV=Delta_eV/1000.0, gamma_phi0=0, gamma_relax0=0)
    t_arr, P, _, _ = engine.tunneling_dynamics(T=0, t_max=t_max)
    P_ana = engine.isolated_P_right(t_arr, Delta_eV/1000.0)
    error = np.max(np.abs(P - P_ana))
    assert error < 1e-12, f"Error {error} too large"
    print("test_isolated_tunneling passed")

if __name__ == "__main__":
    test_isolated_tunneling()
