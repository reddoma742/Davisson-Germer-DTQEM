#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exploratory model for apparent negative tunneling time due to time sovereignty mismatch.
This is a HYPOTHETICAL model, not validated experimentally.

We introduce a two-qubit system: particle (qubit 1) + barrier (qubit 2).
The coupling strength depends on the ratio tau_ratio = tau_particle / tau_barrier.
The effective tunneling time can become 'negative' (i.e., earlier than expected)
when tau_ratio > 1 (barrier clock runs faster).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

hbar = 1.0545718e-34
eV = 1.60217662e-19

class NegativeTimeTunnel:
    def __init__(self, Delta_eV=0.001, gamma_coupling=1e12):
        self.Delta = Delta_eV * eV
        self.gc = gamma_coupling
        self.sx = np.array([[0,1],[1,0]], dtype=complex)
        self.sz = np.array([[1,0],[0,-1]], dtype=complex)
        self.I = np.eye(2, dtype=complex)
    
    def hamiltonian(self, tau_ratio):
        H_tunnel = (self.Delta/2.0) * np.kron(self.sx, self.I)
        # Coupling that depends on the clock ratio
        H_coup = self.gc * hbar * tau_ratio * np.kron(self.sz, self.sx)
        return H_tunnel + H_coup
    
    def tunneling_dynamics(self, tau_ratio, t_max, num_points=500):
        H = self.hamiltonian(tau_ratio)
        psi0 = np.kron(np.array([1,0]), np.array([1,0]))  # particle left, barrier ground
        t_arr = np.linspace(0, t_max, num_points)
        P_right = np.zeros(num_points)
        for i, t in enumerate(t_arr):
            U = expm(-1j * H * t / hbar)
            psi_t = U @ psi0
            rho_t = np.outer(psi_t, psi_t.conj())
            # Partial trace over barrier gives particle's reduced density matrix
            rho_particle = np.array([[rho_t[0,0]+rho_t[1,1], rho_t[0,2]+rho_t[1,3]],
                                     [rho_t[2,0]+rho_t[3,1], rho_t[2,2]+rho_t[3,3]]])
            P_right[i] = np.real(rho_particle[1,1])
        return t_arr, P_right
    
    def first_crossing_time(self, tau_ratio, t_max=5e-12, thresh=0.5):
        t_arr, P = self.tunneling_dynamics(tau_ratio, t_max)
        idx = np.where(P >= thresh)[0]
        if len(idx) > 0:
            return t_arr[idx[0]]
        # If never reaches threshold, return negative as an indicator
        return -t_arr[-1] if P[-1] < thresh else np.nan

# ----------------------------------------------------------------------
# Scan over tau_ratio
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("Exploratory negative tunneling time model (hypothetical)")
    tau_ratios = np.linspace(0.2, 3.0, 50)
    times = []
    model = NegativeTimeTunnel(Delta_eV=1.0, gamma_coupling=5e12)
    for tr in tau_ratios:
        t_cross = model.first_crossing_time(tr, t_max=4e-12)
        times.append(t_cross * 1e12)  # to ps
    
    plt.figure(figsize=(8,5))
    plt.plot(tau_ratios, times, 'bo-', linewidth=2)
    plt.axhline(0, color='k', linestyle='--', alpha=0.5)
    plt.xlabel('τ_particle / τ_barrier (clock ratio)')
    plt.ylabel('First crossing time (ps)')
    plt.title('Apparent tunneling time can become "negative" for τ_ratio > 1?')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    print("Note: Negative values here indicate that the threshold was not reached")
    print("within the simulation time; this is not physical negativity but a numerical indicator.")
