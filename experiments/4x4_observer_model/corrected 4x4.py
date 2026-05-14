"""
DTQEM v18.0 — Experimental 4x4 Model
Date: 2026-05-14
Folder: experimental/dtqem_v18_4x4.py

Physical model:
  H = (ω0/2) * [(1 - α·E)·σx⊗I + β·E·σz⊗I]
  L1 = sqrt(γ·E) · σz⊗I          (tunnel dephasing — Zeno effect)
  L2 = sqrt(γ·E) · I⊗σ+           (observer rises)
  L3 = sqrt(γ·(1-E)) · I⊗σ-       (observer falls)

Results at t=20 ps:
  E=0.0 -> ~0.86 | E=0.3 -> ~0.62 | E=0.7 -> ~0.28 | E=1.0 -> ~0.12
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

# ============================================================
# 1. Constants — calibrated for P(E=0, 20ps)=0.86
# ============================================================
hbar    = 1.0545718e-34
eV      = 1.60217662e-19
t20     = 20e-12

# omega0 calibrated from condition P(E=0)=0.86
omega0  = 2 * np.arcsin(np.sqrt(0.86)) / t20   # 1.1873e11 rad/s
Delta_J = hbar * omega0                         # 0.0781 meV

# Model parameters (from grid search)
alpha   = 0.5      # H suppression factor with E
beta    = 0.684    # sigma_z coupling in Hamiltonian
gamma0  = 0.145 * omega0   # observer decay rate

print("="*55)
print("  DTQEM v18.0 — 4x4 Experimental Model")
print("="*55)
print(f"  Delta   = {Delta_J/eV*1000:.5f} meV")
print(f"  omega0  = {omega0:.4e} rad/s")
print(f"  gamma0  = {gamma0:.4e} rad/s")
print(f"  alpha   = {alpha}")
print(f"  beta    = {beta}")

# ============================================================
# 2. Pauli matrices
# ============================================================
sx = np.array([[0,1],[1,0]],   dtype=complex)
sz = np.array([[1,0],[0,-1]],  dtype=complex)
sp = np.array([[0,1],[0,0]],   dtype=complex)
sm = np.array([[0,0],[1,0]],   dtype=complex)
I2 = np.eye(2, dtype=complex)

# ============================================================
# 3. Lindblad Liouvillian
# ============================================================
def build_liouvillian(H, L_list):
    dim = H.shape[0]
    Id  = np.eye(dim, dtype=complex)
    Lv  = -1j * (np.kron(H, Id) - np.kron(Id, H.conj().T))
    for Lk in L_list:
        Ld  = Lk.conj().T
        LdL = Ld @ Lk
        Lv += np.kron(Lk, Lk.conj())
        Lv -= 0.5 * (np.kron(LdL, Id) + np.kron(Id, LdL.T))
    return Lv

# ============================================================
# 4. Time setup
# ============================================================
dt = 0.05e-12
t_arr = np.arange(0, t20 + dt, dt)

# ============================================================
# 5. 4x4 simulation
# ============================================================
def run_4x4(E_ext):
    # Hamiltonian (same as v16 but extended to 4x4)
    H4 = (omega0/2) * (
        (1 - alpha * E_ext) * np.kron(sx, I2) +
        beta * E_ext * np.kron(sz, I2)
    )

    L_ops = []
    if E_ext > 0:
        # (1) Dephasing on tunnel (Zeno mechanism)
        L_ops.append(np.sqrt(gamma0 * E_ext) * np.kron(sz, I2))
        # (2) Observer records (rises at high measurement)
        L_ops.append(np.sqrt(gamma0 * E_ext) * np.kron(I2, sp))
    if E_ext < 1:
        # (3) Observer resets (falls at low measurement)
        L_ops.append(np.sqrt(gamma0 * (1 - E_ext)) * np.kron(I2, sm))

    L = build_liouvillian(H4, L_ops)
    prop = expm(L * dt)

    # Initial state: |L, down> = |00>
    rho = np.zeros((4,4), dtype=complex)
    rho[0,0] = 1.0

    P = np.zeros(len(t_arr))
    for i in range(len(t_arr)):
        if i > 0:
            rv = prop @ rho.flatten('C')
            rho = rv.reshape(4,4)
            rho = 0.5 * (rho + rho.conj().T)
            tr = np.trace(rho).real
            if tr > 1e-12:
                rho /= tr

        # Partial trace over observer qubit
        # rho_tunnel[a,b] = sum_k rho[2a+k, 2b+k]
        rho_t = np.zeros((2,2), dtype=complex)
        for a in range(2):
            for b in range(2):
                for k in range(2):
                    rho_t[a,b] += rho[2*a + k, 2*b + k]
        P[i] = rho_t[1,1].real

    return P

# ============================================================
# 6. Run simulations and print results
# ============================================================
E_values = [0.0, 0.3, 0.5, 0.7, 1.0]
targets  = {0.0: 0.86, 0.3: 0.62, 0.7: 0.28, 1.0: 0.12}
colors   = ['#355cde', '#01a982', '#f5a623', '#b23a48', '#333333']

results = {}

print("\n  E_ext | P_right(20ps) | Target | Diff")
print("  " + "-"*40)

for E in E_values:
    P = run_4x4(E)
    results[E] = P
    val = P[-1]
    tgt = targets.get(E)
    if tgt is not None:
        diff = abs(val - tgt)
        print(f"  {E:5.1f} | {val:12.4f} | {tgt:6.2f} | {diff:.4f}")
    else:
        print(f"  {E:5.1f} | {val:12.4f} | {'--':6} | --")

# ============================================================
# 7. Plotting
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Left plot: time evolution
for E, col in zip(E_values, colors):
    axes[0].plot(t_arr * 1e12, results[E], color=col, lw=2.5, label=f'E_ext={E}')
axes[0].axvline(20, color='gray', ls=':', lw=1.5, alpha=0.7)
axes[0].set_xlim(0, 20)
axes[0].set_ylim(0, 1)
axes[0].set_xlabel('Time (ps)', fontsize=12)
axes[0].set_ylabel('P_right(t)', fontsize=12)
axes[0].set_title('DTQEM 4x4 - Evolution 0-20 ps', fontsize=12)
axes[0].legend(fontsize=9)
axes[0].grid(alpha=0.3)

# Right plot: bar chart comparison
E_bar = [0.0, 0.3, 0.7, 1.0]
P_sim = [results[E][-1] for E in E_bar]
P_tgt = [targets[E] for E in E_bar]
x = np.arange(len(E_bar))
w = 0.35

axes[1].bar(x - w/2, P_tgt, w, label='Target', color='#cccccc', edgecolor='k')
axes[1].bar(x + w/2, P_sim, w, label='DTQEM 4x4',
            color=['#355cde', '#01a982', '#b23a48', '#333333'], edgecolor='k')
axes[1].set_xticks(x)
axes[1].set_xticklabels([f'E={e}' for e in E_bar])
axes[1].set_ylim(0, 1)
axes[1].set_ylabel('P_right at t=20 ps', fontsize=12)
axes[1].set_title('Simulation vs Target', fontsize=12)
axes[1].legend(fontsize=9)
axes[1].grid(alpha=0.3, axis='y')

plt.suptitle('DTQEM v18.0 - 4x4 Experimental Model (Tunnel + Observer)', fontsize=14)
plt.tight_layout()
plt.savefig('dtqem_v18_4x4_final.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nChart saved: dtqem_v18_4x4_final.png")
