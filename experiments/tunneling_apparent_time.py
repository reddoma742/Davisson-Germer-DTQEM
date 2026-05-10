# experiments/tunneling_apparent_time.py
"""
DTQEM Test for Apparent Negative Tunneling Time
Based on the discussion with colleagues (May 2026).
Result: No negative time found; t_half >= tau_isolated for all tested amplitudes.
"""

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

def gaussian_pulse(t, t0=8e-12, width=2e-12, amplitude=1e13):
    return amplitude * np.exp(-((t - t0)**2) / (2*width**2))

def find_half_time(t_arr, P, thresh=0.5):
    idx = np.where(P >= thresh)[0]
    if len(idx) == 0:
        return np.nan
    i = idx[0]
    if i == 0:
        return t_arr[0]
    t1, t2 = t_arr[i-1], t_arr[i]
    P1, P2 = P[i-1], P[i]
    return t1 + (t2 - t1)*(thresh - P1)/(P2 - P1)

def simulate_tunneling_pulse(Delta_eV, gamma_phi0, gamma_relax0, pulse_func, t_max_ps=20.0, num_steps=1000):
    Delta_J = Delta_eV/1000.0 * eV
    t_max = t_max_ps * 1e-12
    t_arr = np.linspace(0, t_max, num_steps)
    dt = t_arr[1] - t_arr[0]

    sx = np.array([[0,1],[1,0]], dtype=complex)
    sz = np.array([[1,0],[0,-1]], dtype=complex)
    sm = np.array([[0,0],[1,0]], dtype=complex)

    rho = np.array([[1,0],[0,0]], dtype=complex)
    H = (Delta_J/2.0) * sx

    P = np.zeros(num_steps)
    for i, t in enumerate(t_arr):
        gamma_meas = pulse_func(t)
        Ls = []
        if gamma_phi0 > 0:
            Ls.append(np.sqrt(gamma_phi0) * sz)
        if gamma_relax0 > 0:
            Ls.append(np.sqrt(gamma_relax0) * sm)
        if gamma_meas > 0:
            L_meas = np.sqrt(gamma_meas) * np.array([[1,0],[0,0]], dtype=complex)
            Ls.append(L_meas)
        L = SimpleLindblad.build_liouvillian(H, Ls)
        rho = SimpleLindblad.evolve(rho, dt, L)
        P[i] = np.real(rho[1,1])

    return t_arr, P

if __name__ == "__main__":
    print("DTQEM Test: Apparent Negative Tunneling Time?")
    print("==============================================")
    Delta_eV = 3.5   # meV
    gamma_phi = 0.0
    gamma_relax = 0.0
    t_max_ps = 20.0

    # Isolated reference
    t_arr_iso, P_iso = simulate_tunneling_pulse(Delta_eV, gamma_phi, gamma_relax, lambda t: 0.0, t_max_ps)
    tau_isolated = find_half_time(t_arr_iso, P_iso)
    print(f"tau_isolated = {tau_isolated*1e12:.3f} ps")

    # Test Gaussian pulses with increasing amplitude
    amplitudes = [1e11, 1e12, 5e12, 1e13, 2e13, 5e13]
    results = []
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(12,5))

    for A in amplitudes:
        pulse = lambda t: gaussian_pulse(t, t0=8e-12, width=2e-12, amplitude=A)
        t_arr, P = simulate_tunneling_pulse(Delta_eV, gamma_phi, gamma_relax, pulse, t_max_ps)
        t_half = find_half_time(t_arr, P)
        results.append((A, t_half*1e12 if not np.isnan(t_half) else np.nan))
        ax1.plot(t_arr*1e12, P, label=f'A={A:.1e}')
        print(f"Amplitude {A:.1e} -> t_half = {t_half*1e12:.3f} ps, ratio = {t_half/tau_isolated:.3f}")

    ax1.axhline(0.5, color='k', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Time (ps)')
    ax1.set_ylabel('P_right(t)')
    ax1.set_title('Tunneling under Gaussian pulse (varying amplitude)')
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)

    # Plot ratio vs amplitude
    amps = [r[0] for r in results]
    ratios = [r[1]/tau_isolated for r in results]
    ax2.semilogx(amps, ratios, 'bo-')
    ax2.axhline(1, color='r', linestyle='--', label='Isolated ratio = 1')
    ax2.set_xlabel('Pulse amplitude (1/s)')
    ax2.set_ylabel('t_half / τ_isolated')
    ax2.set_title('Apparent time ratio vs measurement strength')
    ax2.legend()
    ax2.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    if any(r < 1.0 for r in ratios if not np.isnan(r)):
        print("\n⚠️ Observation: t_half < τ_isolated for some amplitudes.")
    else:
        print("\n✅ t_half >= τ_isolated for all tested amplitudes → no negative apparent time in DTQEM.")
