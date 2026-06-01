# core/dg_engine.py
import numpy as np
from core.lindblad_solver import LindbladSolver, hbar, eV

class DavissonGermerEngine(LindbladSolver):
    """
    Simulates electron diffraction from a crystal (Davisson–Germer experiment)
    as an entanglement between the electron and the crystal (treated as environment).
    The system is modeled as two qubits: 
        - qubit A: electron path (|0⟩ = reflected, |1⟩ = diffracted)
        - qubit B: crystal mode (|0⟩ = ground, |1⟩ = excited)
    The Hamiltonian is zero (no internal evolution, only interaction via environment).
    Lindblad jump operator: L = sqrt(gamma_phi) * (sigma_z ⊗ I)
    This induces pure dephasing of the electron relative to the crystal.
    """
    def __init__(self, gamma_phi0=1000.0, t_obs=1e-6):
        """
        Parameters:
        -----------
        gamma_phi0 : float
            Pure dephasing rate (1/s) coupling electron and crystal.
        t_obs : float
            Observation time (seconds) – the time electron interacts with crystal.
        """
        self.gamma_phi0 = gamma_phi0
        self.t_obs = t_obs
        # Pauli matrices for two qubits
        self.I2 = np.eye(2, dtype=complex)
        self.sz = np.array([[1, 0], [0, -1]], dtype=complex)
    
    def hamiltonian(self):
        """No internal Hamiltonian for the system (free evolution)."""
        return np.zeros((4, 4), dtype=complex)
    
    def jump_operators(self):
        """
        Only one jump operator: L = sqrt(gamma_phi0) * (sigma_z ⊗ I).
        This describes pure dephasing of the electron qubit due to the crystal.
        """
        L = np.sqrt(self.gamma_phi0) * np.kron(self.sz, self.I2)
        return [L]
    
    def build_liouvillian(self):
        """Liouvillian superoperator (16x16 for 2 qubits)."""
        H = self.hamiltonian()
        Ls = self.jump_operators()
        # Use base class method (which works for any dimension)
        return super().build_liouvillian(H, Ls)
    
    def evolve(self, rho0):
        """
        Evolve from initial state rho0 for t_obs seconds.
        """
        L = self.build_liouvillian()
        return super().evolve(rho0, self.t_obs, L)
    
    @staticmethod
    def bragg_angles(d_nm, wavelength_m, n=1):
        """
        Calculate Bragg angle(s) for a given crystal spacing and de Broglie wavelength.
        Returns a list of angles (degrees). Empty if no solution.
        """
        d_m = d_nm * 1e-9
        sin_theta = n * wavelength_m / (2 * d_m)
        if sin_theta > 1:
            return []
        return [np.degrees(np.arcsin(sin_theta))]
    
    @staticmethod
    def de_broglie_wavelength(energy_eV):
        """Compute de Broglie wavelength (m) for an electron with kinetic energy in eV."""
        E_J = energy_eV * eV
        p = np.sqrt(2 * 9.109e-31 * E_J)
        return 6.626e-34 / p
    
    def visibility_distinguishability_from_theta(self, theta_deg):
        """
        For a given initial superposition angle θ (in degrees), create the initial
        entangled state |ψ(θ)⟩ = cos(θ/2)|00⟩ + sin(θ/2)|11⟩, evolve under dephasing,
        and compute V = 2|ρ_{03}| and D = |ρ_{00} - ρ_{33}|.
        """
        theta_rad = np.radians(theta_deg)
        c = np.cos(theta_rad/2)
        s = np.sin(theta_rad/2)
        psi0 = np.array([c, 0, 0, s], dtype=complex)
        rho0 = np.outer(psi0, psi0.conj())
        rho_f = self.evolve(rho0)
        V = 2.0 * np.abs(rho_f[0, 3])
        D = np.abs(rho_f[0, 0] - rho_f[3, 3])
        return V, D
    
    @staticmethod
    def intensity_profile(phi_deg, phi_peak_deg, sigma_deg=1.0):
        """Gaussian peak shape for diffraction intensity."""
        return np.exp(-((phi_deg - phi_peak_deg)**2) / (2 * sigma_deg**2))
    
    def analyze_crystal(self, d_nm, energy_eV, n=1):
        """
        Full analysis: compute Bragg angle, then V and D for that angle.
        Assumes that the initial state corresponds to the electron being in a superposition
        of two paths with angle θ related to φ? 
        Actually, from earlier derivation: θ = 180° - 2φ, and α = cos φ.
        But here we skip the θ = 180 - 2φ and directly use φ_peak as the parameter
        that defines the initial state? Need to be consistent with earlier code.
        For now, we use the experimental φ to compute θ and then use that to get V, D.
        """
        lam = self.de_broglie_wavelength(energy_eV)
        phi_list = self.bragg_angles(d_nm, lam, n)
        if not phi_list:
            return None
        phi_peak = phi_list[0]
        theta_deg = 180 - 2 * phi_peak
        V, D = self.visibility_distinguishability_from_theta(theta_deg)
        return {
            'phi_peak_deg': phi_peak,
            'theta_deg': theta_deg,
            'V': V,
            'D': D,
            'complementarity': V*V + D*D,
            'lambda_A': lam * 1e10  # Angstroms
        }
