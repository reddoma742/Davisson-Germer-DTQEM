# core/schottky_engine.py
import numpy as np
from core.lindblad_solver import LindbladSolver, hbar, eV, k_B

class SchottkyEngine(LindbladSolver):
    """
    Simulates Schottky effect (field-enhanced thermionic emission) as a two-level system:
        |M> : electron trapped in metal
        |V> : electron in vacuum (emitted)
    Hamiltonian: zero (no coherent coupling)
    Lindblad jump operator: L_emit = sqrt(gamma_emit) * |V><M|
    The emission rate gamma_emit follows the Richardson-Dushman formula modified by
    Schottky barrier lowering: Δφ = sqrt(e^3 E / (4π ε₀))
    """
    def __init__(self, work_function_eV=4.5, A_richardson=1.2e6, epsilon_r=1.0):
        """
        Parameters:
        -----------
        work_function_eV : float
            Material work function (eV), typical for metals: 4.5 eV for W, 4.3 for Ni, etc.
        A_richardson : float
            Richardson constant (A/m²/K²). Typical 1.2e6 for metals.
        epsilon_r : float
            Relative permittivity (for barrier lowering, usually 1 for vacuum).
        """
        self.phi0 = work_function_eV * eV          # Joules
        self.A = A_richardson                      # A/m²/K²
        self.epsilon_r = epsilon_r
        
        # Two-level system states
        self.M = np.array([[1,0],[0,0]], dtype=complex)   # |M><M|
        self.V = np.array([[0,0],[0,1]], dtype=complex)   # |V><V|
        self.sigma_plus = np.array([[0,1],[0,0]], dtype=complex)  # |V><M|
        self.sigma_minus = np.array([[0,0],[1,0]], dtype=complex) # |M><V|
        
    def schottky_barrier_lowering(self, E_field):
        """
        Compute Schottky barrier reduction Δφ (Joules) for given electric field E (V/m).
        Formula: Δφ = sqrt( e^3 E / (4π ε₀ ε_r) )
        Returns: Delta in Joules.
        """
        if E_field <= 0:
            return 0.0
        e = 1.60217662e-19
        eps0 = 8.8541878128e-12
        epsilon = eps0 * self.epsilon_r
        Delta_phi_J = np.sqrt(e**3 * E_field / (4 * np.pi * epsilon))
        return Delta_phi_J
    
    def emission_rate(self, T, E_field):
        """
        Compute effective escape rate γ_emit (1/s) using Richardson-Dushman formula
        with Schottky barrier lowering.
        J = A T^2 exp( - (φ - Δφ) / (k_B T) )   (A/m²)
        To get a rate (1/s), we multiply by emission area (assumed 1 nm² typical).
        But here we return gamma proportional to J.
        For two-level model, we set gamma = γ0 * exp( - (φ-Δφ)/(k_B T) )
        with γ0 chosen to match typical timescales (e.g., 1e12 1/s).
        """
        if T <= 0:
            return 0.0
        Delta_phi = self.schottky_barrier_lowering(E_field)
        phi_eff = self.phi0 - Delta_phi
        if phi_eff < 0:
            phi_eff = 0.0
        # Richardson-Dushman current density (A/m²)
        J = self.A * T**2 * np.exp(-phi_eff / (k_B * T))
        # Convert current density to a rate: gamma = J * Area / e, with Area = 1 nm² = 1e-18 m²
        area = 1e-18   # m² (typical emission area for nanoscale emitter)
        gamma = J * area / eV   # electrons per second (since J*area gives Amps = C/s, divide by e to get 1/s)
        # Ensure gamma is not too high (capped at 1e15 1/s for numerical stability)
        return min(gamma, 1e15)
    
    def jump_operators(self, T, E_field):
        """
        Return list of Lindblad operators. For Schottky effect, only one jump:
        L_emit = sqrt(gamma_emit) * sigma_plus = |V><M|
        This transfers population from |M> to |V>.
        """
        gamma = self.emission_rate(T, E_field)
        Ls = []
        if gamma > 0:
            Ls.append(np.sqrt(gamma) * self.sigma_plus)
        # Optionally add dephasing or relaxation, but not essential.
        return Ls, {'gamma_emit': gamma}
    
    def build_liouvillian(self, T, E_field):
        H = np.zeros((2,2), dtype=complex)   # zero Hamiltonian
        Ls, _ = self.jump_operators(T, E_field)
        return super().build_liouvillian(H, Ls)
    
    def evolve(self, rho0, t_obs, T, E_field):
        L = self.build_liouvillian(T, E_field)
        return super().evolve(rho0, t_obs, L)
    
    def emission_dynamics(self, T, E_field, t_max, num_points=500):
        """
        Start with electron in metal state |M>, compute probability in vacuum P_v(t)
        and also visibility V(t)=2|rho_{01}|, D(t)=|rho00-rho11|.
        """
        rho0 = np.diag([1,0], dtype=complex)   # |M><M|
        t_arr = np.linspace(0, t_max, num_points)
        P_v = np.zeros(num_points)
        V = np.zeros(num_points)
        D = np.zeros(num_points)
        for i, t in enumerate(t_arr):
            rho = self.evolve(rho0, t, T, E_field)
            P_v[i] = np.real(rho[1,1])
            V[i] = 2.0 * np.abs(rho[0,1])
            D[i] = np.abs(rho[0,0] - rho[1,1])
        return t_arr, P_v, V, D
    
    def steady_state_current(self, T, E_field):
        """Analytical steady-state current (rate) from rate equation: dP_v/dt = gamma * P_M."""
        gamma = self.emission_rate(T, E_field)
        # Steady state: P_M = gamma / (gamma + ...), but no return. Actually pure exponential.
        # For two-level without return, current = gamma * exp(-gamma t) integrated? Better:
        # The emission rate itself is a measure of current.
        return gamma
