# tests/test_lindblad_accuracy.py
import sys
import numpy as np
sys.path.append('..')
from core.lindblad_solver import LindbladSolver, hbar, eV

def test_isolated_rabi_oscillation():
    """
    Test: isolated qubit with H = (Delta/2) sigma_x, starting from |0>.
    Analytical: P_right(t) = sin^2(Delta t / (2 hbar))
    """
    Delta_eV = 0.001  # 1 meV
    Delta_J = Delta_eV * eV
    H = (Delta_J / 2.0) * np.array([[0, 1], [1, 0]], dtype=complex)
    rho0 = np.array([[1, 0], [0, 0]], dtype=complex)
    t_obs = 1e-12  # 1 ps
    L = LindbladSolver.build_liouvillian(H, [])
    rho_t = LindbladSolver.evolve(rho0, t_obs, L)
    P_num = np.real(rho_t[1, 1])
    
    omega = Delta_J / hbar
    P_ana = np.sin(omega * t_obs / 2) ** 2
    error = abs(P_num - P_ana)
    assert error < 1e-12, f"Rabi error too large: {error:.2e}"
    print("✓ test_isolated_rabi_oscillation passed (error = {:.2e})".format(error))

def test_pure_dephasing_decay():
    """
    Test: pure dephasing (L = sqrt(gamma) sigma_z) starting from |+> = (|0>+|1>)/√2.
    Analytical: rho01(t) = 0.5 * exp(-2*gamma*t). Visibility V = 2|rho01| = exp(-2*gamma*t)
    """
    gamma = 1000.0  # 1/s
    t_obs = 0.001   # 1 ms
    H = np.zeros((2,2), dtype=complex)
    Ls = [np.sqrt(gamma) * np.array([[1,0],[0,-1]], dtype=complex)]
    rho0 = 0.5 * np.array([[1,1],[1,1]], dtype=complex)
    L = LindbladSolver.build_liouvillian(H, Ls)
    rho_t = LindbladSolver.evolve(rho0, t_obs, L)
    V_num = 2.0 * np.abs(rho_t[0,1])
    V_ana = np.exp(-2.0 * gamma * t_obs)
    error = abs(V_num - V_ana)
    assert error < 1e-12, f"Pure dephasing error too large: {error:.2e}"
    print("✓ test_pure_dephasing_decay passed (error = {:.2e})".format(error))

if __name__ == "__main__":
    test_isolated_rabi_oscillation()
    test_pure_dephasing_decay()
