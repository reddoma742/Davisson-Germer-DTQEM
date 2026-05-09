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
        - measurement (Zeno): sqrt(measurement_rate) * P_left (projector on left well)
    """
    def __init__(self, Delta_eV=0.001, gamma_phi0=0.0, gamma_relax0=0.0, measurement_rate=0.0):
        # LindbladSolver is a static class (no __init__), but we call super for consistency
        super().__init__()
        
        self.Delta_J = Delta_eV * eV
        self.gamma_phi0 = gamma_phi0
        self.gamma_relax0 = gamma_relax0
        self.measurement_rate = measurement_rate
        
        # Pauli matrices for single qubit
        self.sx = np.array([[0, 1], [1, 0]], dtype=complex)
        self.sz = np.array([[1, 0], [0, -1]], dtype=complex)
        self.sm = np.array([[0, 0], [1, 0]], dtype=complex)
        self.sp = np.array([[0, 1], [0, 0]], dtype=complex)
        self.I = np.eye(2, dtype=complex)
        
    def hamiltonian(self):
        return (self.Delta_J / 2.0) * self.sx
    
    def jump_operators(self, T):
        n_th = self.thermal_occupation(self.Delta_J, T)
        
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
        if self.measurement_rate > 0:
            # QND measurement: projection onto left well |0><0|
            L_meas = np.sqrt(self.measurement_rate) * np.array([[1, 0], [0, 0]], dtype=complex)
            Ls.append(L_meas)
        
        rates = {
            'gamma_phi': gamma_phi,
            'gamma_down': gamma_down,
            'gamma_up': gamma_up,
            'meas_rate': self.measurement_rate
        }
        return Ls, rates
    
    def build_liouvillian(self, T):
        H = self.hamiltonian()
        Ls, _ = self.jump_operators(T)
        return super().build_liouvillian(H, Ls)
    
    def evolve(self, rho0, t_obs, T):
        L = self.build_liouvillian(T)
        return super().evolve(rho0, t_obs, L)
    
    def tunneling_dynamics(self, T, t_max, num_points=500, initial='left'):
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
            # Use the static entropy method from LindbladSolver (which we defined earlier)
            S[i] = LindbladSolver.entropy(rho)
        
        return t_arr, P, V, D, S

    def entanglement_lifetime(self, T):
        """Estimate lifetime from sum of all decoherence rates."""
        _, rates = self.jump_operators(T)
        total_rate = rates.get('gamma_phi', 0.0) + rates.get('gamma_down', 0.0) + rates.get('gamma_up', 0.0) + self.measurement_rate
        return 1.0 / total_rate if total_rate > 1e-15 else np.inf

    def first_tunneling_time(self, t_arr, P, thresh=0.5):
        idx = np.where(P >= thresh)[0]
        return t_arr[idx[0]] if len(idx) > 0 else np.nan

    def effective_gamma_phi(self, t_arr, V):
        mask = V > 0.1
        if np.sum(mask) < 2:
            return 0.0
        logV = np.log(V[mask])
        t_masked = t_arr[mask]
        coeffs = np.polyfit(t_masked, logV, 1)
        return max(-coeffs[0], 0.0)

    @staticmethod
    def isolated_P_right(t, Delta_eV):
        omega = Delta_eV * eV / hbar
        return np.sin(omega * t / 2)**2
