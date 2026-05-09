# core/tunneling_engine.py
import numpy as np
from core.lindblad_solver import LindbladSolver, hbar, eV

class TunnelingEngine(LindbladSolver):
    """
    Simulates a particle in a double-well potential (tunneling qubit) with:
    Hamiltonian: H = (Delta/2) * sigma_x
    Lindblad jump operators: 
        - dephasing: sqrt(gamma_phi) * sigma_z
        - relaxation: sqrt(gamma_down) * sigma_-
        - excitation: sqrt(gamma_up)   * sigma_+
    """
    def __init__(self, Delta_eV=0.001, gamma_phi0=0.0, gamma_relax0=0.0, measurement_rate=0.0):
        """
        Parameters:
        -----------
        Delta_eV : float
            Tunnel splitting in eV (e.g., 0.001 = 1 meV)
        gamma_phi0 : float
            Pure dephasing rate at T=0 (1/s)
        gamma_relax0 : float
            Relaxation rate at T=0 (1/s)
        """
        self.Delta_J = Delta_eV * eV   # convert to Joules
        self.gamma_phi0 = gamma_phi0
        self.gamma_relax0 = gamma_relax0
        
        # Pauli matrices for single qubit
        self.sx = np.array([[0, 1], [1, 0]], dtype=complex)
        self.sz = np.array([[1, 0], [0, -1]], dtype=complex)
        self.sm = np.array([[0, 0], [1, 0]], dtype=complex)   # sigma-
        self.sp = np.array([[0, 1], [0, 0]], dtype=complex)   # sigma+
        self.I = np.eye(2, dtype=complex)
        
    def hamiltonian(self):
        """Return Hamiltonian matrix (2x2)."""
        return (self.Delta_J / 2.0) * self.sx
    
    def jump_operators(self, T):
        """
        Build list of Lindblad jump operators and their effective rates.
        Returns:
            Ls : list of 2x2 arrays
            rates : dict with 'gamma_phi', 'gamma_down', 'gamma_up'
        """
        # Thermal occupation of the environment
        n_th = self.thermal_occupation(self.Delta_J, T)
        # Effective rates
        gamma_phi = self.gamma_phi0 * (2*n_th + 1) / 2.0
        gamma_down = self.gamma_relax0 * (n_th + 1)
        gamma_up   = self.gamma_relax0 * n_th
        
        Ls = []
        if gamma_phi > 0:
            Ls.append(np.sqrt(gamma_phi) * self.sz)
        if gamma_down > 0:
            Ls.append(np.sqrt(gamma_down) * self.sm)
        if gamma_up > 0:
            Ls.append(np.sqrt(gamma_up) * self.sp)
        rates = {'gamma_phi': gamma_phi, 'gamma_down': gamma_down, 'gamma_up': gamma_up}
        return Ls, rates
    
    def build_liouvillian(self, T):
        """Construct Liouvillian superoperator (4x4) at temperature T."""
        H = self.hamiltonian()
        Ls, _ = self.jump_operators(T)
        return super().build_liouvillian(H, Ls)
    
    def evolve(self, rho0, t_obs, T):
        """
        Evolve density matrix from initial state rho0 for time t_obs at temperature T.
        """
        L = self.build_liouvillian(T)
        return super().evolve(rho0, t_obs, L)
    
    def tunneling_dynamics(self, T, t_max, num_points=500, initial='left'):
        """
        Simulate P_right(t), V(t), D(t) from t=0 to t_max.
        
        Parameters:
        -----------
        T : float
            Temperature (K)
        t_max : float
            Maximum time (seconds)
        num_points : int
            Number of time points
        initial : str ('left' or 'right')
            Initial well
        
        Returns:
        --------
        t_arr : np.ndarray (num_points)
            Time array (seconds)
        P_right : np.ndarray
            Probability to be in right well
        V : np.ndarray
            Visibility = 2|rho01|
        D : np.ndarray
            Distinguishability = |rho00 - rho11|
        """
        if initial == 'left':
            rho0 = np.array([[1, 0], [0, 0]], dtype=complex)
        else:
            rho0 = np.array([[0, 0], [0, 1]], dtype=complex)
        
        t_arr = np.linspace(0, t_max, num_points)
        P = np.zeros(num_points)
        V = np.zeros(num_points)
        D = np.zeros(num_points)
        S = np.zeros(num_points)
        
        for i, t in enumerate(t_arr):
            rho = self.evolve(rho0, t, T)
            P[i] = np.real(rho[1, 1])
            V[i] = 2.0 * np.abs(rho[0, 1])    
            D[i] = np.abs(rho[0, 0] - rho[1, 1])
            S[i] = self.entropy(rho)
            
        return t_arr, P, V, D
    
    def first_tunneling_time(self, t_arr, P, thresh=0.5):
        """First time P(t) >= thresh."""
        idx = np.where(P >= thresh)[0]
        return t_arr[idx[0]] if len(idx) > 0 else np.nan
    
    def effective_gamma_phi(self, t_arr, V):
        """
        Estimate effective dephasing rate from exponential decay of V(t).
        Assumes V(t) ~ V0 * exp(-gamma_eff * t).
        """
        mask = V > 0.1
        if np.sum(mask) < 2:
            return 0.0
        logV = np.log(V[mask])
        t_masked = t_arr[mask]
        coeffs = np.polyfit(t_masked, logV, 1)
        gamma_eff = -coeffs[0]
        return max(gamma_eff, 0.0)
    
    @staticmethod
    def isolated_P_right(t, Delta_eV):
        """
        Analytical solution for isolated system (no Lindblad).
        P_right(t) = sin^2( Delta * t / (2 hbar) )
        """
        omega = Delta_eV * eV / hbar
        return np.sin(omega * t / 2)**2
