# experiments/observer_tunneling.py
"""
DTQEM - Temporal Observer Model (Experimental)
Adds an auxiliary qubit representing the particle's "time state" (|W> wave, |P> particle)
with Lindblad jumps controlled by an external factor E_ext (observer strength).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

# Constants
hbar = 1.0545718e-34
eV = 1.60217662e-19

# ----------------------------------------------------------------------
# Base Lindblad solver (simplified, without external dependencies)
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# Temporal Observer Model
# ----------------------------------------------------------------------
class TemporalObserver:
    def __init__(self, gamma_rise=1e10, gamma_fall=1e10):
        self.gamma_rise = gamma_rise
        self.gamma_fall = gamma_fall
        # Pauli for observer qubit
        self.sx = np.array([[0,1],[1,0]], dtype=complex)
        self.sz = np.array([[1,0],[0,-1]], dtype=complex)
        self.sp = np.array([[0,1],[0,0]], dtype=complex)  # |P><W|
        self.sm = np.array([[0,0],[1,0]], dtype=complex)  # |W><P|
        self.I = np.eye(2, dtype=complex)
        # Initial state: |W> (wave)
        self.rho_obs = np.array([[1,0],[0,0]], dtype=complex)

    def jump_operators(self, E_ext):
        """Returns Lindblad operators for observer transitions based on E_ext."""
        Ls = []
        if E_ext > 0:
            L_rise = np.sqrt(self.gamma_rise * E_ext) * self.sp
            Ls.append(L_rise)
        if (1 - E_ext) > 0:
            L_fall = np.sqrt(self.gamma_fall * (1 - E_ext)) * self.sm
            Ls.append(L_fall)
        return Ls

    def evolve(self, dt, E_ext):
        H_obs = np.zeros((2,2), dtype=complex)  # no internal Hamiltonian
        Ls = self.jump_operators(E_ext)
        L = SimpleLindblad.build_liouvillian(H_obs, Ls)
        self.rho_obs = SimpleLindblad.evolve(self.rho_obs, dt, L)
        t_p = np.real(self.rho_obs[1,1])  # probability of |P> (particle state)
        return t_p

# ----------------------------------------------------------------------
# Example: Test the observer response to a square pulse of E_ext
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("Temporal Observer Test (E_ext as external observer strength)")
    observer = TemporalObserver(gamma_rise=1e11, gamma_fall=1e11)
    
    dt = 1e-12       # 1 ps step
    total_steps = 500
    time = np.arange(total_steps) * dt * 1e12  # ps
    
    # Define E_ext as a square pulse: 0 -> 1 -> 0
    E_ext = np.zeros(total_steps)
    E_ext[100:300] = 1.0   # active between 100 and 300 ps
    
    t_p = np.zeros(total_steps)
    for i, E in enumerate(E_ext):
        t_p[i] = observer.evolve(dt, E)
    
    plt.figure(figsize=(10,4))
    plt.plot(time, E_ext, 'r--', label='E_ext (observer strength)')
    plt.plot(time, t_p, 'b-', label='t_p (particle probability)')
    plt.xlabel('Time (ps)')
    plt.ylabel('Probability / Strength')
    plt.title('Temporal Observer: t_p follows observer activity')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()
    print("\nObservation: When E_ext=1, t_p rises (particle dominates). When E_ext=0, t_p decays (wave returns).")
    print("This mimics the Quantum Eraser effect: erasing observer information restores wave behaviour.")
