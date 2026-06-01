# core/lindblad_solver.py
import numpy as np
from scipy.linalg import expm

# ======================================================================
# Physical constants
# ======================================================================
hbar = 1.0545718e-34   # J·s
eV = 1.60217662e-19     # J/eV
k_B = 1.380649e-23      # J/K

class LindbladSolver:
    """
    Base class for solving Lindblad master equation for a general quantum system.
    Provides methods to build Liouvillian superoperator and evolve density matrix.
    """
    @staticmethod
    def thermal_occupation(Delta_J, T):
        """
        Mean thermal occupation number for a given energy gap (in Joules).
        """
        if T <= 0 or Delta_J <= 0:
            return 0.0
        x = Delta_J / (k_B * T)
        if x > 700:   # avoid overflow
            return 0.0
        return 1.0 / (np.exp(x) - 1.0)

    @staticmethod
    def build_liouvillian(H, jump_operators):
        """
        Construct the Liouvillian superoperator L (size dim² × dim²) such that
        dρ/dt = L vec(ρ).

        Parameters:
        -----------
        H : np.ndarray (dim, dim)
            Hamiltonian matrix.
        jump_operators : list of np.ndarray
            List of Lindblad jump operators L_k.

        Returns:
        --------
        L : np.ndarray (dim², dim²)
            Liouvillian superoperator.
        """
        dim = H.shape[0]
        size = dim * dim
        # Hamiltonian part: -i ( H ⊗ I - I ⊗ H^T )
        L = -1j / hbar * (np.kron(H, np.eye(dim)) - np.kron(np.eye(dim), H.T))
        # Dissipative part
        for Lj in jump_operators:
            Lj_dag = Lj.conj().T
            term1 = np.kron(Lj, Lj.conj())
            LjLj = Lj_dag @ Lj
            term2 = -0.5 * (np.kron(LjLj, np.eye(dim)) + np.kron(np.eye(dim), LjLj.T))
            L += term1 + term2
        return L

    @staticmethod
    def evolve(rho0, t_obs, L):
        """
        Evolve density matrix under a constant Liouvillian superoperator.

        Parameters:
        -----------
        rho0 : np.ndarray (dim, dim)
            Initial density matrix.
        t_obs : float
            Evolution time (seconds).
        L : np.ndarray (dim², dim²)
            Liouvillian superoperator.

        Returns:
        --------
        rho_t : np.ndarray (dim, dim)
            Density matrix after time t_obs.
        """
        rho_vec = rho0.flatten('C')
        rho_vec_t = expm(L * t_obs) @ rho_vec
        rho_t = rho_vec_t.reshape(rho0.shape)
        # Enforce hermiticity and positivity
        rho_t = 0.5 * (rho_t + rho_t.conj().T)
        evals, evecs = np.linalg.eigh(rho_t)
        evals = np.maximum(evals, 1e-15)
        rho_t = evecs @ np.diag(evals) @ evecs.conj().T
        trace = np.real(np.trace(rho_t))
        if trace > 0:
            rho_t /= trace
        return rho_t
            # زيد هاد الدالة في آخر ملف core/lindblad_solver.py تحت دالة evolve
    @staticmethod
    def entropy(rho):
        """
        Calculate Von Neumann entropy: S = -Tr(rho * ln(rho))
        """
        # حساب القيم الذاتية (Eigenvalues)
        evals = np.linalg.eigvalsh(rho)
        # كنختارو غير القيم اللي كبر من الصفر باش نتفاداو خطأ log(0)
        evals = evals[evals > 1e-15]
        return -np.sum(evals * np.log(evals))
