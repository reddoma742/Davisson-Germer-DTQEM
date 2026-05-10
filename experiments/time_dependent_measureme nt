# experiments/time_dependent_measurement.py
# Non‑Markovian stress test: time‑dependent measurement rate Γ_meas(t)

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

hbar = 1.0545718e-34
eV = 1.60217662e-19

class SimpleLindblad:
    @staticmethod
    def build_liouvillian(H, Ls):
        dim = H.shape[0]
        size = dim * dim
        L = -1j / hbar * (np.kron(H, np.eye(dim)) - np.kron(np.eye(dim), H.T))
        for Lj in Ls:
            Lj_dag = Lj.conj().T
            term1 = np.kron(Lj, Lj.conj())
            LjLj = Lj_dag @ Lj
            term2 = -0.5 * (np.kron(LjLj, np.eye(dim)) + np.kron(np.eye(dim), LjLj.T))
            L += term1 + term2
        return L

    @staticmethod
    def evolve(rho0, t_obs, L):
        rho_vec = rho0.flatten('C')
        rho_vec_t = expm(L * t_obs) @ rho_vec
        rho_t = rho_vec_t.reshape(rho0.shape)
        rho_t = 0.5 * (rho_t + rho_t.conj().T)
        evals, evecs = np.linalg.eigh(rho_t)
        evals = np.maximum(evals, 1e-15)
        rho_t = evecs @ np.diag(evals) @ evecs.conj().T
        tr = np.real(np.trace(rho_t))
        if tr > 0:
            rho_t /= tr
        return rho_t

def measurement_rate_gaussian(t, t0=5e-12, width=1e-12, amplitude=1e13):
    """Γ_meas(t) = amplitude * exp(-(t-t0)²/(2*width²))"""
    return amplitude * np.exp(-((t - t0)**2) / (2 * width**2))

def simulate_tunneling_time_dependent(Delta_eV, gamma_phi0, gamma_relax0, measurement_rate_func,
                                      t_max, num_steps=1000, initial='left'):
    """
    Evolve step by step, recomputing Liouvillian at each time step
    because measurement rate changes with time.
    """
    Delta_J = Delta_eV * eV

    # Pauli matrices
    sx = np.array([[0,1],[1,0]], dtype=complex)
    sz = np.array([[1,0],[0,-1]], dtype=complex)
    sm = np.array([[0,0],[1,0]], dtype=complex)
    sp = np.array([[0,1],[0,0]], dtype=complex)

    # Initial state
    if initial == 'left':
        rho = np.array([[1,0],[0,0]], dtype=complex)
    else:
        rho = np.array([[0,0],[0,1]], dtype=complex)

    t_arr = np.linspace(0, t_max, num_steps)
    dt = t_arr[1] - t_arr[0]
    P_right = np.zeros(num_steps)
    V_arr = np.zeros(num_steps)
    D_arr = np.zeros(num_steps)

    for i, t in enumerate(t_arr):
        gamma_meas = measurement_rate_func(t)

        # Hamiltonian
        H = (Delta_J / 2.0) * sx

        # Jump operators
        Ls = []
        if gamma_phi0 > 0:
            Ls.append(np.sqrt(gamma_phi0) * sz)
        if gamma_relax0 > 0:
            Ls.append(np.sqrt(gamma_relax0) * sm)
        # For pure Zeno test: add measurement jump
        if gamma_meas > 0:
            L_meas = np.sqrt(gamma_meas) * np.array([[1,0],[0,0]], dtype=complex)
            Ls.append(L_meas)

        L = SimpleLindblad.build_liouvillian(H, Ls)
        rho = SimpleLindblad.evolve(rho, dt, L)

        P_right[i] = np.real(rho[1,1])
        V_arr[i] = 2.0 * np.abs(rho[0,1])
        D_arr[i] = np.abs(rho[0,0] - rho[1,1])

    return t_arr, P_right, V_arr, D_arr

if __name__ == "__main__":
    Delta = 3.5          # meV
    gamma_phi = 0.0
    gamma_relax = 0.0
    t_max_ps = 20.0
    t_max = t_max_ps * 1e-12

    # Constant rate (for comparison)
    def const_rate(t):
        return 1e13 if 5e-12 < t < 15e-12 else 0.0   # gate pulse

    # Gaussian pulse centered at 10 ps
    def gauss_rate(t):
        return 1e13 * np.exp(-((t - 10e-12)**2) / (2*(2e-12)**2))

    print("Running constant‑rate simulation...")
    t_c, P_c, V_c, D_c = simulate_tunneling_time_dependent(Delta, gamma_phi, gamma_relax, const_rate, t_max)

    print("Running Gaussian‑pulse simulation...")
    t_g, P_g, V_g, D_g = simulate_tunneling_time_dependent(Delta, gamma_phi, gamma_relax, gauss_rate, t_max)

    # Plot comparison
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    axes[0,0].plot(t_c*1e12, P_c, 'r-', label='constant gate')
    axes[0,0].plot(t_g*1e12, P_g, 'b--', label='Gaussian pulse')
    axes[0,0].set_xlabel('Time (ps)')
    axes[0,0].set_ylabel('P_right(t)')
    axes[0,0].set_title('Tunneling probability')
    axes[0,0].legend()
    axes[0,0].grid(alpha=0.3)

    axes[0,1].plot(t_c*1e12, V_c, 'r-', label='const V')
    axes[0,1].plot(t_g*1e12, V_g, 'b--', label='Gaussian V')
    axes[0,1].set_xlabel('Time (ps)')
    axes[0,1].set_ylabel('Visibility V')
    axes[0,1].set_title('Coherence')
    axes[0,1].legend()
    axes[0,1].grid(alpha=0.3)

    axes[1,0].plot(t_c*1e12, D_c, 'r-', label='const D')
    axes[1,0].plot(t_g*1e12, D_g, 'b--', label='Gaussian D')
    axes[1,0].set_xlabel('Time (ps)')
    axes[1,0].set_ylabel('Distinguishability D')
    axes[1,0].legend()
    axes[1,0].grid(alpha=0.3)

    # Show the measurement rate shape
    t_plot = np.linspace(0, t_max, 500)
    gamma_const = [const_rate(t) for t in t_plot]
    gamma_gauss = [gauss_rate(t) for t in t_plot]
    axes[1,1].plot(t_plot*1e12, gamma_const, 'r-', label='const rate')
    axes[1,1].plot(t_plot*1e12, gamma_gauss, 'b--', label='Gaussian rate')
    axes[1,1].set_xlabel('Time (ps)')
    axes[1,1].set_ylabel('Γ_meas (1/s)')
    axes[1,1].set_title('Measurement rate profile')
    axes[1,1].legend()
    axes[1,1].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()

    print("\nObservation: If the Gaussian pulse shows revival of V(t) after the pulse ends,")
    print("while the constant gate does not, that indicates non‑Markovian memory and supports Time‑Sovereignty.")
