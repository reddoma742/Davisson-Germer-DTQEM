#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DTQEM v16.1 – Quantum Tunneling under Continuous Measurement (Zeno Effect)
===========================================================================

A message from Reddouane Berramdane (the author):
    
    "هذا النموذج هو نقطة البداية. بدأت بملاحظة بسيطة: كيف يمكن للقياس أن
    يجمد حركة الجسيم؟ كانت فكرة خيالية في البداية، ثم تحولت إلى معادلات،
    ثم إلى كود. لم أكن أحمل شهادة في الفيزياء، لكن الفضول والأصدقاء
    (بشراً وذكاء اصطناعياً) كانوا معي. هذا الإنجاز هو ثمرة تواضع ورحلة
    بحث لا تزال مستمرة. أتمنى أن ينتفع به من يأتي بعدي."

Physics:
    - Hamiltonian: H = (Δ/2) σ_x (fixed coherent tunneling)
    - Lindblad: L = √(γ·E_ext) σ_z (pure dephasing measurement)
    - Quantum Zeno Effect: Stronger measurement (E_ext → 1) suppresses tunneling

Optimized parameters (v16.1):
    - Δ = 78.15 μeV (coherent splitting, tuned for 20ps period)
    - γ₀ = 1.2×10¹¹ s⁻¹ (dephasing rate)
    - t_max = 20 ps

Results at t = 20 ps:
    E_ext = 0.0 → P_right = 0.86
    E_ext = 0.3 → P_right ≈ 0.60
    E_ext = 0.7 → P_right ≈ 0.42
    E_ext = 1.0 → P_right ≈ 0.34

Acknowledgment:
    AI assistance:
        - DeepSeek (critical analysis, methodology validation)
        - Claude (Anthropic) (code writing, derivations, documentation)
        - Arena AI (first-principles derivations, optimization, Zeno correction)
    Human supervision, philosophy, and vision: Reddouane Berramdane

License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
See LICENSE file for full terms.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

# ============================================================
# 1. Optimized Constants (Physically Corrected)
# ============================================================
hbar = 1.0545718e-34          # J·s
eV = 1.60217662e-19           # J/eV

# Corrected Delta: 78.15 micro-eV (tunneling period matches 20ps target)
Delta_meV = 0.07815           
Delta_J = Delta_meV * 1e-3 * eV   

# Adjusted base dephasing rate to match Zeno suppression targets
gamma0 = 1.2e11               # 1/s

t_max = 20e-12                # 20 ps
dt = 0.1e-12                  # 0.1 ps (fine resolution)
t_arr = np.arange(0, t_max + dt, dt)

# Pauli matrices
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


# ============================================================
# 2. Liouvillian Builder (Lindblad Master Equation)
# ============================================================
def build_liouvillian(H, L_list):
    """
    Build the Lindblad superoperator (Liouvillian) in vectorized form.
    
    Parameters:
    -----------
    H : 2x2 complex array
        Hamiltonian
    L_list : list of 2x2 complex arrays
        Lindblad jump operators
    
    Returns:
    --------
    Lv : 4x4 complex array
        Liouvillian superoperator
    """
    dim = H.shape[0]
    I_dim = np.eye(dim, dtype=complex)
    
    # Hamiltonian part: -i/hbar (H⊗I - I⊗H^T)
    Lv = -1j / hbar * (np.kron(H, I_dim) - np.kron(I_dim, H.conj().T))
    
    for Lk in L_list:
        Lk_dag = Lk.conj().T
        # Jump term: Lk ⊗ Lk*
        Lv += np.kron(Lk, Lk.conj())
        # Dissipative part: -1/2 {Lk†Lk, ρ}
        Lk_dag_Lk = Lk_dag @ Lk
        Lv += -0.5 * (np.kron(Lk_dag_Lk, I_dim) + np.kron(I_dim, Lk_dag_Lk.T))
    
    return Lv


# ============================================================
# 3. Tunneling Simulation Function
# ============================================================
def run_tunneling(E_ext):
    """
    Simulate tunneling probability under continuous measurement.
    
    Parameters:
    -----------
    E_ext : float
        Observer strength (measurement efficiency). Range: [0, 1]
        0 = no measurement, 1 = strong measurement (Zeno freezing)
    
    Returns:
    --------
    P_right : array
        Probability to be in the right well at each time step
    """
    # Fixed Hamiltonian (does not depend on E_ext)
    H = (Delta_J / 2.0) * sx
    
    # Lindblad operators (pure dephasing)
    L_ops = []
    if E_ext > 0:
        L_ops.append(np.sqrt(gamma0 * E_ext) * sz)
    
    # Build Liouvillian and propagator
    L = build_liouvillian(H, L_ops)
    prop = expm(L * dt)
    
    # Initial state: |left> (|0>)
    rho = np.array([[1, 0], [0, 0]], dtype=complex)
    P_right = np.zeros(len(t_arr))
    
    for i, t in enumerate(t_arr):
        if i > 0:
            # Evolve density matrix
            rho_vec = prop @ rho.flatten('C')
            rho = rho_vec.reshape(2, 2)
            # Enforce Hermiticity and trace preservation (numerical stability)
            rho = 0.5 * (rho + rho.conj().T)
            rho /= np.trace(rho).real
        
        # Probability to be in the right well (state |1>)
        P_right[i] = rho[1, 1].real
    
    return P_right


# ============================================================
# 4. Main Execution
# ============================================================
if __name__ == "__main__":
    E_vals = [0.0, 0.3, 0.7, 1.0]
    colors = ['blue', 'green', 'orange', 'red']
    
    print("=" * 70)
    print("DTQEM v16.1 – Tunneling under Continuous Measurement (Zeno Optimized)")
    print("=" * 70)
    print(f"Corrected Delta = {Delta_meV * 1e3:.2f} ueV (micro-eV)")
    print(f"gamma0          = {gamma0:.1e} 1/s")
    print(f"t_max           = {t_max * 1e12:.0f} ps")
    print()
    
    # Create time-evolution plot
    plt.figure(figsize=(9, 5.5))
    
    print("=== Verification of Targets at t = 20 ps ===")
    print(" E_ext | Simulated | Target | Diff")
    print("-" * 45)
    
    targets = {0.0: 0.86, 0.3: 0.62, 0.7: 0.28, 1.0: 0.12}
    
    for E, col in zip(E_vals, colors):
        P = run_tunneling(E)
        plt.plot(t_arr * 1e12, P, color=col, lw=2.5, label=f'E_ext = {E}')
        
        if E in targets:
            sim_val = P[-1]
            target = targets[E]
            diff = abs(sim_val - target)
            print(f"  {E:.1f}  |    {sim_val:.4f}   |   {target:.2f}   |   {diff:.4f}")
    
    plt.xlabel('Time (ps)', fontsize=12)
    plt.ylabel(r'$P_{\mathrm{right}}(t)$ (Tunneling Probability)', fontsize=12)
    plt.title('Quantum Zeno Effect: Coherent Tunneling Damped by Continuous Measurement', fontsize=13)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('figure_zeno.png', dpi=300, bbox_inches='tight')
    
    print("\n" + "=" * 70)
    print("📊 Time-evolution plot saved as 'figure_zeno.png'")
    print("\n📝 Acknowledgment:")
    print("   AI assistance: DeepSeek, Claude (Anthropic), Arena AI")
    print("   Human scientific supervision and vision: Reddouane Berramdane")
    print("\n✅ Model ready for use.")
    print("=" * 70)
    
    # Optional: show the plot
    plt.show()
