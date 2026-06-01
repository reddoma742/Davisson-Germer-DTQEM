# core/schottky_engine.py
import numpy as np
from core.lindblad_solver import LindbladSolver, hbar, eV, k_B

class SchottkyEngine(LindbladSolver):
    """
    Simulates Schottky effect (field-enhanced thermionic emission) as a two-level system.
    """
    def __init__(self, work_function_eV=4.5, A_richardson=1.2e6, epsilon_r=1.0):
        # استدعاء LindbladSolver لربط الدوال الأساسية (مثل الإنتروبيا)
        super().__init__()
        
        self.phi0 = work_function_eV * eV          # Joules
        self.A = A_richardson                      # A/m²/K²
        self.epsilon_r = epsilon_r
        
        # Two-level system states
        self.M = np.array([[1,0],[0,0]], dtype=complex)   # |M><M|
        self.V = np.array([[0,0],[0,1]], dtype=complex)   # |V><V|
        self.sigma_plus = np.array([[0,1],[0,0]], dtype=complex)  # |V><M|
        self.sigma_minus = np.array([[0,0],[1,0]], dtype=complex) # |M><V|
        
    def schottky_barrier_lowering(self, E_field):
        """Compute Schottky barrier reduction Δφ (Joules)."""
        if E_field <= 0:
            return 0.0
        e = 1.60217662e-19
        eps0 = 8.8541878128e-12
        epsilon = eps0 * self.epsilon_r
        Delta_phi_J = np.sqrt(e**3 * E_field / (4 * np.pi * epsilon))
        return Delta_phi_J
    
    def emission_rate(self, T, E_field):
        """Compute effective escape rate γ_emit (1/s)."""
        if T <= 0:
            return 0.0
        Delta_phi = self.schottky_barrier_lowering(E_field)
        phi_eff = self.phi0 - Delta_phi
        if phi_eff < 0:
            phi_eff = 0.0
        
        J = self.A * T**2 * np.exp(-phi_eff / (k_B * T))
        area = 1e-18   # m²
        gamma = J * area / eV   
        return min(gamma, 1e15)
    
    def jump_operators(self, T, E_field):
        gamma = self.emission_rate(T, E_field)
        Ls = []
        if gamma > 0:
            Ls.append(np.sqrt(gamma) * self.sigma_plus)
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
        Returns: t_arr, P_v, V, D, S
        """
        rho0 = np.diag([1,0], dtype=complex)   # |M><M|
        t_arr = np.linspace(0, t_max, num_points)
        P_v = np.zeros(num_points)
        V = np.zeros(num_points)
        D = np.zeros(num_points)
        S = np.zeros(num_points) # مصفوفة الإنتروبيا
        
        for i, t in enumerate(t_arr):
            rho = self.evolve(rho0, t, T, E_field)
            P_v[i] = np.real(rho[1,1])
            V[i] = 2.0 * np.abs(rho[0,1])
            D[i] = np.abs(rho[0,0] - rho[1,1])
            # استدعاء الإنتروبيا من الكلاس الأم لتفادي AttributeError
            S[i] = LindbladSolver.entropy(rho)
            
        return t_arr, P_v, V, D, S # إرجاع 5 قيم
    
    def steady_state_current(self, T, E_field):
        return self.emission_rate(T, E_field)
