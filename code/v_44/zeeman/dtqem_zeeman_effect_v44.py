
"""
dtqem_zeeman_effect_v44.py
===========================
DTQEM Zeeman Effect Simulator — V44.0
Interactive dashboard (ipywidgets + matplotlib)

Core Equations:
    omega_L  = (e * B) / (2 * m)          Larmor frequency [rad/s]
    Delta_omega = |omega_L1 - omega_L2|    frequency difference
    delta_tau(t) = Delta_omega * t         proper-time difference [rad -> s via hbar]

    V_eff(t) = exp(-gamma_phi * t) * exp(-|delta_tau(t)| / tau_c)

    where:
        delta_tau = |Delta_E| * t / hbar
        Delta_E   = hbar * Delta_omega = hbar * |omega_L1 - omega_L2|

Physical Interpretation:
    Two Zeeman sub-levels split by magnetic field B.
    The coherence between them decays due to:
        (1) Environmental decoherence  : exp(-gamma_phi * t)
        (2) DTQEM proper-time term     : exp(-|delta_tau| / tau_c)

═══════════════════════════════════════════════════════════════════
CONTRIBUTORS & ACKNOWLEDGMENTS
═══════════════════════════════════════════════════════════════════

Project Creator:
    • Berramdane Reddouane (Morocco)

Core Contributors (AI Assistants):
    • Gemini (Google)          — Theoretical discussions, D3 proposal
    • DeepSeek (深度求索)       — Philosophical insights, critical analysis
    • Claude (Anthropic)       — Code writing (V44.0, V44.0 Qubit, V44.0 Zeeman)

Special Thanks:
    • "Clore" (Anonymous colleague) — Mathematical improvement proposals

Role of Each Contributor:
    — Gemini:   Proposed the stretched exponential (D3) as a physical
                generalization of the decoherence term.
    — DeepSeek: Provided deep philosophical discussions linking proper-time
                difference to the measurement problem.
    — Claude:   Wrote the complete interactive dashboard for Zeeman Effect (V44.0)
                with ipywidgets and zero-overlap layout.

License: MIT
Version: 44.0
Date: 2026-05-22
"""
# ── backend (must be set before any other matplotlib import) ──────────────
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from typing import Tuple, Dict, List

import ipywidgets as widgets
from IPython.display import display, clear_output


# ===========================================================================
# Physical Constants
# ===========================================================================
C_LIGHT  = 299_792_458.0          # speed of light      [m/s]
HBAR     = 1.054_571_817e-34      # reduced Planck       [J·s]
E_CHARGE = 1.602_176_634e-19      # elementary charge    [C]
M_ELEC   = 9.109_383_701e-31      # electron mass        [kg]
MU_B     = 9.274_009_994e-24      # Bohr magneton        [J/T]
LORENTZ_SAFETY = 0.9999


# ===========================================================================
# Visual Theme  (identical to V44.0 series)
# ===========================================================================
STYLE: Dict[str, str] = {
    "bg_main":        "#0d1117",
    "bg_panel":       "#161b22",
    "bg_slider":      "#21262d",
    "bg_band":        "#13181f",
    "accent_blue":    "#58a6ff",
    "accent_cyan":    "#39d0d8",
    "accent_green":   "#3fb950",
    "accent_orange":  "#d29922",
    "accent_red":     "#f85149",
    "accent_purple":  "#bc8cff",
    "accent_yellow":  "#e3b341",
    "accent_pink":    "#f778ba",
    "text_primary":   "#e6edf3",
    "text_secondary": "#8b949e",
    "grid_color":     "#21262d",
}

def C(k: str) -> str:
    return STYLE[k]


# ===========================================================================
# Physics — Zeeman + DTQEM
# ===========================================================================

def larmor_frequency(B: float, mass: float = M_ELEC) -> float:
    """
    Larmor precession frequency:
        omega_L = (e * B) / (2 * m)   [rad/s]
    """
    return (E_CHARGE * B) / (2.0 * mass)


def zeeman_splitting(B: float, m1: int, m2: int,
                     mass: float = M_ELEC) -> float:
    """
    Energy difference between two Zeeman sub-levels m1, m2:
        Delta_E = hbar * omega_L * |m1 - m2|   [J]
    Returns Delta_omega = Delta_E / hbar  [rad/s]
    """
    omega_L     = larmor_frequency(B, mass)
    delta_omega = omega_L * abs(m1 - m2)
    return delta_omega           # [rad/s]


def delta_tau_zeeman(t: np.ndarray, B: float,
                     m1: int, m2: int,
                     mass: float = M_ELEC) -> np.ndarray:
    """
    DTQEM proper-time difference for Zeeman coherence:
        delta_tau(t) = Delta_omega * t
                     = (|Delta_E| / hbar) * t
    Units: [rad]  (dimensionless phase, treated as time-like in D0)
    For dimensional consistency with tau_c [s]:
        delta_tau [s] = (Delta_omega [rad/s]) * t [s]
                      = Delta_E [J] / hbar [J·s] * t [s]
    """
    d_omega = zeeman_splitting(B, m1, m2, mass)
    return d_omega * t           # [rad] = [s^{-1} * s]


def V_env(t: np.ndarray, gamma_phi: float) -> np.ndarray:
    """Environmental decoherence: exp(-gamma_phi * t)"""
    return np.exp(-gamma_phi * t)


def V_dtqem(t: np.ndarray, B: float,
            m1: int, m2: int,
            tau_c: float,
            mass: float = M_ELEC) -> np.ndarray:
    """
    DTQEM Zeeman decoherence (D0 baseline):
        V_dtqem = exp(-|delta_tau(t)| / tau_c)
    """
    dt = delta_tau_zeeman(t, B, m1, m2, mass)
    return np.exp(-np.abs(dt) / tau_c)


def V_eff_zeeman(t: np.ndarray, B: float,
                 m1: int, m2: int,
                 gamma_phi: float,
                 tau_c: float,
                 mass: float = M_ELEC) -> np.ndarray:
    """
    Total coherence:
        V_eff = exp(-gamma_phi * t) * exp(-|delta_tau| / tau_c)
    """
    return V_env(t, gamma_phi) * V_dtqem(t, B, m1, m2, tau_c, mass)


def T2_estimate(B: float, m1: int, m2: int,
                gamma_phi: float, tau_c: float,
                mass: float = M_ELEC) -> float:
    """
    Estimate T2* : time when V_eff = 1/e.
        (gamma_phi + Delta_omega / tau_c) * T2* = 1
    """
    d_omega = zeeman_splitting(B, m1, m2, mass)
    rate    = gamma_phi + d_omega / tau_c
    return 1.0 / rate if rate > 0 else np.inf


def V_vs_B(B_arr: np.ndarray, t_eval: float,
           m1: int, m2: int,
           gamma_phi: float, tau_c: float,
           mass: float = M_ELEC) -> np.ndarray:
    """V_eff at fixed t_eval across a range of B values."""
    return np.array([
        float(V_eff_zeeman(np.array([t_eval]), Bi,
                           m1, m2, gamma_phi, tau_c, mass)[0])
        for Bi in B_arr
    ])


def energy_levels(B_arr: np.ndarray,
                  m_values: List[int],
                  mass: float = M_ELEC) -> Dict[int, np.ndarray]:
    """
    Zeeman energy levels E_m(B) = hbar * omega_L(B) * m   [eV]
    Returns dict {m: E_m_array}
    """
    levels = {}
    for m in m_values:
        omega_L       = (E_CHARGE * B_arr) / (2.0 * mass)
        E_m           = HBAR * omega_L * m / E_CHARGE   # convert J -> eV
        levels[m] = E_m
    return levels


def compute_all(p: dict) -> dict:
    """
    Compute all quantities needed for the dashboard figure.
    """
    B       = p["B"]
    m1      = p["m1"]
    m2      = p["m2"]
    gph     = p["gamma_phi"]
    tc      = p["tau_c"]
    t_eval  = p["t_eval"]
    t_max   = p["t_max"]
    mass    = p["mass"]

    # Time array
    n_t   = 800
    t_arr = np.linspace(0, t_max, n_t)

    # Coherence components vs time
    Veff  = V_eff_zeeman(t_arr, B, m1, m2, gph, tc, mass)
    Venv  = V_env(t_arr, gph)
    Vdtq  = V_dtqem(t_arr, B, m1, m2, tc, mass)
    dt_t  = delta_tau_zeeman(t_arr, B, m1, m2, mass)

    # T2*
    T2 = T2_estimate(B, m1, m2, gph, tc, mass)

    # Point values at t_eval
    V_at_t  = float(V_eff_zeeman(np.array([t_eval]), B,
                                  m1, m2, gph, tc, mass)[0])
    Ve_at_t = float(V_env(np.array([t_eval]), gph)[0])
    Vd_at_t = float(V_dtqem(np.array([t_eval]), B, m1, m2, tc, mass)[0])
    dt_at_t = float(delta_tau_zeeman(np.array([t_eval]),
                                     B, m1, m2, mass)[0])

    # V_eff vs B  (at fixed t_eval)
    B_arr  = np.linspace(0.001, 20.0, 500)
    V_B    = V_vs_B(B_arr, t_eval, m1, m2, gph, tc, mass)

    # Energy levels vs B
    m_vals  = list(range(m1, m2+1)) if m2 > m1 else [m1, m2]
    m_vals  = sorted(set([m1, m2, 0] + m_vals))
    E_levels = energy_levels(B_arr, m_vals, mass)

    # Larmor & splitting
    omega_L   = larmor_frequency(B, mass)
    d_omega   = zeeman_splitting(B, m1, m2, mass)
    delta_E_J = HBAR * d_omega
    delta_E_eV= delta_E_J / E_CHARGE

    # Heatmap: V_eff(B, t) at varying B and t
    n_h   = 60
    B_h   = np.linspace(0.001, 20.0, n_h)
    t_h   = np.linspace(0, t_max, n_h)
    Z     = np.zeros((n_h, n_h))
    for i, Bi in enumerate(B_h):
        for j, tj in enumerate(t_h):
            Z[i, j] = float(V_eff_zeeman(
                np.array([tj]), Bi, m1, m2, gph, tc, mass)[0])

    return dict(
        t_arr=t_arr, Veff=Veff, Venv=Venv, Vdtq=Vdtq, dt_t=dt_t,
        T2=T2,
        V_at_t=V_at_t, Ve_at_t=Ve_at_t, Vd_at_t=Vd_at_t,
        dt_at_t=dt_at_t,
        B_arr=B_arr, V_B=V_B,
        E_levels=E_levels, m_vals=m_vals,
        omega_L=omega_L, d_omega=d_omega,
        delta_E_J=delta_E_J, delta_E_eV=delta_E_eV,
        Z=Z, B_h=B_h, t_h=t_h,
    )


# ===========================================================================
# Figure Drawing
# ===========================================================================

def _apply_theme():
    plt.rcParams.update({
        "figure.facecolor":  C("bg_main"),
        "axes.facecolor":    C("bg_panel"),
        "axes.edgecolor":    C("text_secondary"),
        "axes.labelcolor":   C("text_primary"),
        "axes.titlecolor":   C("text_primary"),
        "xtick.color":       C("text_secondary"),
        "ytick.color":       C("text_secondary"),
        "text.color":        C("text_primary"),
        "grid.color":        C("grid_color"),
        "grid.linewidth":    0.6,
        "font.family":       "monospace",
        "font.size":         9,
    })


def _coherence_color(V: float) -> str:
    if V > 0.80: return C("accent_green")
    if V > 0.50: return C("accent_cyan")
    if V > 0.25: return C("accent_orange")
    if V > 0.05: return C("accent_red")
    return C("text_secondary")


def _quality_str(V: float) -> str:
    if V > 0.80: return "COHERENT"
    if V > 0.50: return "PARTIAL"
    if V > 0.25: return "DEGRADED"
    if V > 0.05: return "LOST"
    return "DECOHERENT"


def draw_figure(p: dict, d: dict, figsize=(17, 12)) -> plt.Figure:
    """
    Seven-panel dashboard figure.

    Row 0 : V_eff(t) main  |  Energy levels vs B
    Row 1 : Components bar |  V_eff vs B
    Row 2 : Info panel     |  delta_tau(t)  |  Heatmap V_eff(B,t)
    """
    _apply_theme()
    fig = plt.figure(figsize=figsize, facecolor=C("bg_main"))
    fig.suptitle(
        "DTQEM  ·  Zeeman Effect Decoherence Simulator  ·  V44.0",
        fontsize=14, fontweight="bold",
        color=C("accent_blue"), y=0.987,
    )

    gs = gridspec.GridSpec(
        3, 1, figure=fig,
        left=0.05, right=0.97,
        top=0.958, bottom=0.048,
        height_ratios=[4.0, 3.5, 3.2],
        hspace=0.50,
    )
    gs0 = gridspec.GridSpecFromSubplotSpec(
        1, 2, subplot_spec=gs[0], wspace=0.30, width_ratios=[2.8, 2.2])
    gs1 = gridspec.GridSpecFromSubplotSpec(
        1, 2, subplot_spec=gs[1], wspace=0.30)
    gs2 = gridspec.GridSpecFromSubplotSpec(
        1, 3, subplot_spec=gs[2], wspace=0.38, width_ratios=[1.4, 1.8, 1.8])

    ax_main  = fig.add_subplot(gs0[0])   # V_eff vs t
    ax_elev  = fig.add_subplot(gs0[1])   # Energy levels vs B
    ax_comp  = fig.add_subplot(gs1[0])   # Component bar
    ax_vB    = fig.add_subplot(gs1[1])   # V_eff vs B
    ax_info  = fig.add_subplot(gs2[0])   # Info
    ax_dtau  = fig.add_subplot(gs2[1])   # delta_tau vs t
    ax_heat  = fig.add_subplot(gs2[2])   # Heatmap

    for ax in [ax_main, ax_elev, ax_comp, ax_vB,
               ax_info, ax_dtau, ax_heat]:
        ax.set_facecolor(C("bg_panel"))

    t       = d["t_arr"]
    V       = d["Veff"]
    t_eval  = p["t_eval"]
    V_at_t  = d["V_at_t"]
    V_c     = _coherence_color(V_at_t)
    T2      = d["T2"]
    B       = p["B"]
    m1, m2  = p["m1"], p["m2"]

    # ─────────────────────────────────────────────────────────────────
    # Panel 1 — V_eff vs time  (main)
    # ─────────────────────────────────────────────────────────────────
    ax = ax_main

    # Gradient fill
    cmap_g = LinearSegmentedColormap.from_list(
        "coh_z", [C("accent_red"), C("accent_orange"),
                  C("accent_cyan"), C("accent_green")])
    for i in range(len(t)-1):
        fc = cmap_g(float(V[i]))
        ax.fill_between(t[i:i+2]*1e9, 0, V[i:i+2],
                        color=fc, alpha=0.18)

    ax.plot(t*1e9, V,
            color=C("accent_blue"), lw=2.0, zorder=4,
            label="V_eff  (total)")
    ax.plot(t*1e9, d["Venv"],
            color=C("accent_orange"), lw=1.2, ls="--", alpha=0.85,
            label="V_env = exp(-γ_φ·t)")
    ax.plot(t*1e9, d["Vdtq"],
            color=C("accent_purple"), lw=1.2, ls=":", alpha=0.85,
            label="V_dtqem = exp(-|Δτ|/τ_c)")
    ax.axhline(1/np.e, color=C("text_secondary"),
               lw=0.8, ls="--", alpha=0.6, label="1/e  (T₂* level)")

    # T2* marker
    if np.isfinite(T2) and T2 < t[-1]:
        ax.axvline(T2*1e9, color=C("accent_yellow"),
                   lw=1.2, ls="--", alpha=0.85)
        ax.text(T2*1e9 + t[-1]*1e9*0.01, 0.06,
                f"T₂*={T2*1e9:.3f} ns",
                fontsize=8, color=C("accent_yellow"))

    # t_eval marker
    ax.axvline(t_eval*1e9, color=V_c, lw=1.5, alpha=0.9)
    ax.plot([t_eval*1e9], [V_at_t], "o",
            color=V_c, ms=9, zorder=6)
    ax.annotate(
        f"  t={t_eval*1e9:.2f} ns\n  V={V_at_t:.4f}",
        xy=(t_eval*1e9, V_at_t),
        xytext=(t_eval*1e9 + t[-1]*1e9*0.06, V_at_t + 0.09),
        fontsize=8, color=V_c,
        arrowprops=dict(arrowstyle="->", color=V_c, lw=1.0),
    )

    ax.set_xlim(0, t[-1]*1e9)
    ax.set_ylim(-0.03, 1.10)
    ax.set_xlabel("Time  t  [ns]", fontsize=10)
    ax.set_ylabel("Coherence  V_eff", fontsize=10)
    ax.set_title(
        f"Zeeman Coherence vs Time  |  B={B:.3f} T  |  "
        f"m₁={m1}, m₂={m2}  |  "
        f"Δω={d['d_omega']:.3e} rad/s  |  "
        f"T₂*={T2*1e9:.3f} ns",
        fontsize=8.5, pad=5,
    )
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, facecolor=C("bg_slider"),
              edgecolor=C("text_secondary"), loc="upper right")

    # ─────────────────────────────────────────────────────────────────
    # Panel 2 — Zeeman Energy Levels vs B
    # ─────────────────────────────────────────────────────────────────
    ax = ax_elev

    B_arr    = d["B_arr"]
    E_levels = d["E_levels"]
    m_vals   = d["m_vals"]

    level_colors = [
        C("accent_blue"),   C("accent_green"),
        C("accent_orange"), C("accent_red"),
        C("accent_purple"), C("accent_cyan"),
        C("accent_pink"),   C("accent_yellow"),
    ]

    for idx, m in enumerate(sorted(m_vals)):
        col = level_colors[idx % len(level_colors)]
        E   = E_levels[m]
        lw  = 2.2 if m in (m1, m2) else 1.2
        ls  = "-"  if m in (m1, m2) else "--"
        ax.plot(B_arr, E * 1e6, color=col, lw=lw, ls=ls,
                label=f"m = {m:+d}" +
                      (" ◀" if m in (m1, m2) else ""))

    # Mark current B
    ax.axvline(B, color="white", lw=1.0, ls=":", alpha=0.7)

    ax.set_xlabel("Magnetic Field  B  [T]", fontsize=10)
    ax.set_ylabel("Energy  E  [µeV]", fontsize=10)
    ax.set_title("Zeeman Energy Levels  vs  B", fontsize=10)
    ax.set_xlim(B_arr[0], B_arr[-1])
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, facecolor=C("bg_slider"),
              edgecolor=C("text_secondary"),
              loc="upper left", ncol=2)

    # Annotate splitting at current B
    if m1 in E_levels and m2 in E_levels:
        E1_cur = float(E_levels[m1][ np.searchsorted(B_arr, B)])
        E2_cur = float(E_levels[m2][ np.searchsorted(B_arr, B)])
        ax.annotate(
            "",
            xy=(B, E2_cur*1e6),
            xytext=(B, E1_cur*1e6),
            arrowprops=dict(arrowstyle="<->",
                            color=C("accent_yellow"), lw=1.5),
        )
        ax.text(B + B_arr[-1]*0.02,
                (E1_cur + E2_cur) * 0.5e6,
                f"ΔE={d['delta_E_eV']*1e6:.3f} µeV",
                fontsize=8, color=C("accent_yellow"))

    # ─────────────────────────────────────────────────────────────────
    # Panel 3 — Component Bar  at t_eval
    # ─────────────────────────────────────────────────────────────────
    ax = ax_comp

    lbls = ["V_env", "V_dtqem", "V_eff"]
    vals = [d["Ve_at_t"], d["Vd_at_t"], d["V_at_t"]]
    cols = [C("accent_orange"), C("accent_purple"), C("accent_blue")]

    bars = ax.bar(lbls, vals, color=cols,
                  edgecolor=C("bg_main"), lw=1.0, width=0.50)
    for bar, v in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            min(v + 0.03, 0.96),
            f"{v:.4f}",
            ha="center", va="bottom",
            fontsize=9, fontweight="bold",
            color=C("text_primary"),
        )

    ax.set_ylim(0, 1.18)
    ax.axhline(1.0, color=C("text_secondary"),
               lw=0.6, ls="--", alpha=0.5)
    ax.axhline(1/np.e, color=C("accent_yellow"),
               lw=0.7, ls=":", alpha=0.7, label="1/e")
    ax.set_title(
        f"Decoherence Components  at  t = {t_eval*1e9:.2f} ns",
        fontsize=10)
    ax.set_ylabel("Factor", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", labelsize=9)
    ax.legend(fontsize=8, facecolor=C("bg_slider"),
              edgecolor=C("text_secondary"))

    # ─────────────────────────────────────────────────────────────────
    # Panel 4 — V_eff vs B  at t_eval
    # ─────────────────────────────────────────────────────────────────
    ax = ax_vB

    ax.plot(B_arr, d["V_B"],
            color=C("accent_cyan"), lw=1.8)
    ax.fill_between(B_arr, d["V_B"],
                    alpha=0.15, color=C("accent_cyan"))
    ax.axvline(B, color=C("accent_orange"),
               lw=1.2, ls="--", alpha=0.9)
    ax.plot([B], [V_at_t], "o",
            color=C("accent_orange"), ms=8, zorder=5)
    ax.text(0.97, 0.91,
            f"B = {B:.3f} T\nV = {V_at_t:.4f}",
            transform=ax.transAxes, ha="right",
            fontsize=8.5, color=C("accent_orange"),
            fontweight="bold")
    ax.axhline(1/np.e, color=C("text_secondary"),
               lw=0.7, ls=":", alpha=0.6, label="1/e")
    ax.set_xlim(B_arr[0], B_arr[-1])
    ax.set_ylim(-0.02, 1.05)
    ax.set_xlabel("Magnetic Field  B  [T]", fontsize=10)
    ax.set_ylabel("V_eff", fontsize=10)
    ax.set_title(
        f"V_eff  vs  B  at  t = {t_eval*1e9:.2f} ns",
        fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, facecolor=C("bg_slider"),
              edgecolor=C("text_secondary"))

    # ─────────────────────────────────────────────────────────────────
    # Panel 5 — Info Panel
    # ─────────────────────────────────────────────────────────────────
    ax = ax_info
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor(C("text_secondary"))
        sp.set_linewidth(0.5)

    qs = _quality_str(V_at_t)
    qc = _coherence_color(V_at_t)

    info_lines = [
        ("━━ ZEEMAN STATE ━━━━━━━━━━━",  C("text_secondary")),
        (f" B        = {B:.4f} T",         C("text_primary")),
        (f" m₁ → m₂  = {m1:+d} → {m2:+d}", C("accent_cyan")),
        (f" ω_L      = {d['omega_L']:.3e} rad/s", C("accent_cyan")),
        (f" Δω       = {d['d_omega']:.3e} rad/s",  C("accent_yellow")),
        (f" ΔE       = {d['delta_E_eV']*1e6:.4f} µeV", C("accent_yellow")),
        ("", C("text_secondary")),
        ("━━ COHERENCE ━━━━━━━━━━━━━", C("text_secondary")),
        (f" V_eff    = {V_at_t:.6f}",      qc),
        (f" Status   = {qs}",              qc),
        (f" T₂*      = {T2*1e9:.4f} ns",   C("accent_yellow")),
        ("", C("text_secondary")),
        ("━━ DTQEM PARAMS ━━━━━━━━━━", C("text_secondary")),
        (f" τ_c      = {p['tau_c']:.3e} s",  C("accent_purple")),
        (f" γ_φ      = {p['gamma_phi']:.3e} Hz", C("accent_orange")),
        (f" |Δτ|(t)  = {d['dt_at_t']:.3e} rad",  C("accent_purple")),
        (f" t_eval   = {t_eval*1e9:.3f} ns",       C("text_primary")),
    ]

    dy = 0.053
    for i, (txt, col) in enumerate(info_lines):
        ax.text(0.04, 0.975 - i*dy, txt,
                transform=ax.transAxes,
                fontsize=7.8, color=col,
                fontfamily="monospace", va="top")

    ax.set_title("Parameters & State", fontsize=10)

    # ─────────────────────────────────────────────────────────────────
    # Panel 6 — |delta_tau(t)| vs time
    # ─────────────────────────────────────────────────────────────────
    ax = ax_dtau

    ax.plot(t*1e9, np.abs(d["dt_t"]),
            color=C("accent_purple"), lw=1.8, label="|Δτ(t)| [rad]")
    ax.fill_between(t*1e9, np.abs(d["dt_t"]),
                    alpha=0.18, color=C("accent_purple"))
    ax.axhline(p["tau_c"], color=C("accent_yellow"),
               lw=1.0, ls="--", alpha=0.8,
               label=f"τ_c = {p['tau_c']:.1e} s")
    ax.axvline(t_eval*1e9, color=C("accent_orange"),
               lw=1.2, ls="--", alpha=0.8)
    ax.plot([t_eval*1e9], [abs(d["dt_at_t"])], "o",
            color=C("accent_orange"), ms=7, zorder=5)

    # Shade region where |delta_tau| > tau_c  (DTQEM dominated)
    mask = np.abs(d["dt_t"]) > p["tau_c"]
    if mask.any():
        ax.fill_between(t[mask]*1e9, 0, np.abs(d["dt_t"])[mask],
                        alpha=0.12, color=C("accent_red"),
                        label="|Δτ| > τ_c")

    ax.set_xlim(0, t[-1]*1e9)
    ax.set_xlabel("Time  t  [ns]", fontsize=9)
    ax.set_ylabel("|Δτ(t)|  [rad / s]", fontsize=9)
    ax.set_title("Proper-Time Difference  |Δτ(t)|", fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, facecolor=C("bg_slider"),
              edgecolor=C("text_secondary"))

    # ─────────────────────────────────────────────────────────────────
    # Panel 7 — Heatmap  V_eff(B, t)
    # ─────────────────────────────────────────────────────────────────
    ax = ax_heat

    cmap_h = LinearSegmentedColormap.from_list(
        "dtqem_z",
        [(0.0, "#f85149"), (0.3, "#d29922"),
         (0.6, "#39d0d8"), (1.0, "#3fb950")],
    )
    im = ax.imshow(
        d["Z"],
        origin="lower", aspect="auto",
        cmap=cmap_h, vmin=0, vmax=1,
        extent=[d["t_h"][0]*1e9, d["t_h"][-1]*1e9,
                d["B_h"][0],     d["B_h"][-1]],
    )
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("V_eff", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    # Mark current operating point
    ax.axhline(B, color="white", lw=1.0, ls="--", alpha=0.7)
    ax.axvline(t_eval*1e9, color="white", lw=1.0, ls="--", alpha=0.7)
    ax.plot([t_eval*1e9], [B], "*",
            color="white", ms=11, zorder=5)

    ax.set_xlabel("Time  t  [ns]", fontsize=9)
    ax.set_ylabel("B  [T]", fontsize=9)
    ax.set_title("Coherence Map  V_eff(B, t)\n"
                 "(white ✦ = current params)", fontsize=9)
    ax.tick_params(labelsize=8)

    plt.close(fig)
    return fig


# ===========================================================================
# ipywidgets Dashboard
# ===========================================================================

class ZeemanDashboard:
    """
    DTQEM Zeeman Effect Dashboard — V44.0
    All sliders are ipywidgets (HTML) placed ABOVE the matplotlib figure.
    Zero overlap guaranteed.
    """

    DEFAULTS = {
        "tau_c":     1e-15,
        "gamma_phi": 1e9,
        "B":         1.0,
        "t_eval":    2e-9,
        "t_max":     20e-9,
        "m1":        -1,
        "m2":         1,
        "mass":      M_ELEC,
    }

    def __init__(self):
        self.p = dict(self.DEFAULTS)
        self._build_widgets()
        self._build_layout()

    # ── Widget factory ────────────────────────────────────────────────

    def _fsl(self, desc, vmin, vmax, val, step,
             fmt=".3f", color="#58a6ff"):
        sl = widgets.FloatSlider(
            value=val, min=vmin, max=vmax, step=step,
            description="",
            continuous_update=False,
            readout=True, readout_format=fmt,
            layout=widgets.Layout(width="100%", height="26px"),
            style={"handle_color": color},
        )
        lb = widgets.Label(
            value=desc,
            layout=widgets.Layout(width="100%"),
            style={"font_size": "11px",
                   "text_color": "#8b949e",
                   "font_family": "monospace"},
        )
        return sl, lb

    def _isl(self, desc, vmin, vmax, val, color="#58a6ff"):
        sl = widgets.IntSlider(
            value=val, min=vmin, max=vmax, step=1,
            description="",
            continuous_update=False,
            readout=True,
            layout=widgets.Layout(width="100%", height="26px"),
            style={"handle_color": color},
        )
        lb = widgets.Label(
            value=desc,
            layout=widgets.Layout(width="100%"),
            style={"font_size": "11px",
                   "text_color": "#8b949e",
                   "font_family": "monospace"},
        )
        return sl, lb

    def _build_widgets(self):
        # ── Row 0 ────────────────────────────────────────────────────
        self.sl_log_tc,  self.lb_log_tc  = self._fsl(
            "log₁₀(τ_c) [s]   DTQEM param",
            -18, -12, np.log10(self.DEFAULTS["tau_c"]),
            0.1, ".2f", "#bc8cff")

        self.sl_log_gph, self.lb_log_gph = self._fsl(
            "log₁₀(γ_φ) [Hz]   env deco rate",
            6, 15, np.log10(self.DEFAULTS["gamma_phi"]),
            0.1, ".1f", "#d29922")

        self.sl_B,       self.lb_B       = self._fsl(
            "B [T]   magnetic field strength",
            0.001, 20.0, self.DEFAULTS["B"],
            0.001, ".4f", "#58a6ff")

        self.sl_t_eval,  self.lb_t_eval  = self._fsl(
            "t_eval [ns]   evaluation time",
            0.0, 20.0, self.DEFAULTS["t_eval"]*1e9,
            0.1, ".2f", "#39d0d8")

        # ── Row 1 ────────────────────────────────────────────────────
        self.sl_t_max,   self.lb_t_max   = self._fsl(
            "t_max [ns]   time window",
            1.0, 100.0, self.DEFAULTS["t_max"]*1e9,
            1.0, ".1f", "#58a6ff")

        self.sl_m1,      self.lb_m1      = self._isl(
            "m₁   lower Zeeman level",
            -5, 0, self.DEFAULTS["m1"], "#f85149")

        self.sl_m2,      self.lb_m2      = self._isl(
            "m₂   upper Zeeman level",
            0,  5, self.DEFAULTS["m2"], "#3fb950")

        # Buttons
        self.btn_reset = widgets.Button(
            description="⟳  Reset",
            button_style="warning",
            layout=widgets.Layout(width="130px", height="32px"),
        )
        self.btn_export = widgets.Button(
            description="↓  Export PNG",
            button_style="success",
            layout=widgets.Layout(width="140px", height="32px"),
        )
        self.btn_reset.on_click(self._reset)
        self.btn_export.on_click(self._export)

        self.out = widgets.Output()

    # ── Layout ────────────────────────────────────────────────────────

    def _cell(self, lb, sl, w="24%"):
        return widgets.VBox(
            [lb, sl],
            layout=widgets.Layout(
                width=w, padding="2px 6px",
                border="1px solid #21262d",
            ),
        )

    def _build_layout(self):

        header = widgets.HTML(value=(
            '<div style="background:#0d1117;padding:8px 14px;'
            'border-bottom:2px solid #21262d;">'
            '<span style="font-size:16px;font-weight:bold;'
            'color:#58a6ff;font-family:monospace;">'
            'DTQEM  ·  Zeeman Effect Decoherence Simulator  ·  V44.0'
            '</span><br>'
            '<span style="font-size:11px;color:#8b949e;font-family:monospace;">'
            'V_eff(t) = exp(-γ_φ·t) × exp(-|Δτ(t)|/τ_c)'
            '&nbsp;&nbsp;|&nbsp;&nbsp;'
            'Δτ = Δω·t = (ΔE/ℏ)·t'
            '&nbsp;&nbsp;|&nbsp;&nbsp;'
            'ω_L = eB/(2m)'
            '</span></div>'
        ), layout=widgets.Layout(width="100%"))

        ctrl_hdr = widgets.HTML(value=(
            '<div style="background:#13181f;padding:3px 10px;">'
            '<span style="font-size:11px;color:#8b949e;font-family:monospace;">'
            '━━  PARAMETER CONTROLS  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            '</span></div>'
        ), layout=widgets.Layout(width="100%"))

        row0 = widgets.HBox([
            self._cell(self.lb_log_tc,  self.sl_log_tc),
            self._cell(self.lb_log_gph, self.sl_log_gph),
            self._cell(self.lb_B,       self.sl_B),
            self._cell(self.lb_t_eval,  self.sl_t_eval),
        ], layout=widgets.Layout(width="100%",
                                 padding="3px 0px"))

        row1 = widgets.HBox([
            self._cell(self.lb_t_max, self.sl_t_max),
            self._cell(self.lb_m1,   self.sl_m1),
            self._cell(self.lb_m2,   self.sl_m2),
            widgets.VBox([
                widgets.HBox(
                    [self.btn_reset, self.btn_export],
                    layout=widgets.Layout(gap="10px",
                                         padding="10px 6px"),
                )
            ], layout=widgets.Layout(width="24%")),
        ], layout=widgets.Layout(width="100%",
                                 padding="3px 0px"))

        sep = widgets.HTML(value=(
            '<hr style="border:none;border-top:1px solid #21262d;margin:4px 0;"/>'
            '<div style="background:#0d1117;padding:2px 10px;">'
            '<span style="font-size:10px;color:#8b949e;font-family:monospace;">'
            '━━  VISUALIZATION  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            '</span></div>'
        ), layout=widgets.Layout(width="100%"))

        self.dashboard = widgets.VBox(
            [header, ctrl_hdr, row0, row1, sep, self.out],
            layout=widgets.Layout(
                width="100%",
                background="#0d1117",
                border="1px solid #21262d",
            ),
        )

        # Wire all sliders
        for sl in [self.sl_log_tc, self.sl_log_gph,
                   self.sl_B, self.sl_t_eval, self.sl_t_max,
                   self.sl_m1, self.sl_m2]:
            sl.observe(self._update, names="value")

        self._update()

    # ── Read ──────────────────────────────────────────────────────────

    def _read(self):
        self.p["tau_c"]     = 10.0 ** self.sl_log_tc.value
        self.p["gamma_phi"] = 10.0 ** self.sl_log_gph.value
        self.p["B"]         = self.sl_B.value
        self.p["t_eval"]    = self.sl_t_eval.value * 1e-9
        self.p["t_max"]     = self.sl_t_max.value  * 1e-9
        self.p["m1"]        = int(self.sl_m1.value)
        self.p["m2"]        = int(self.sl_m2.value)
        # Ensure m1 != m2
        if self.p["m1"] == self.p["m2"]:
            self.p["m2"] = self.p["m1"] + 1
        # Clamp t_eval
        if self.p["t_eval"] > self.p["t_max"]:
            self.p["t_eval"] = self.p["t_max"]

    # ── Update ────────────────────────────────────────────────────────

    def _update(self, change=None):
        self._read()
        d   = compute_all(self.p)
        fig = draw_figure(self.p, d, figsize=(17, 12))
        with self.out:
            clear_output(wait=True)
            display(fig)
            plt.close(fig)

    # ── Reset ─────────────────────────────────────────────────────────

    def _reset(self, _):
        dv = self.DEFAULTS
        self.sl_log_tc.value  = np.log10(dv["tau_c"])
        self.sl_log_gph.value = np.log10(dv["gamma_phi"])
        self.sl_B.value       = dv["B"]
        self.sl_t_eval.value  = dv["t_eval"] * 1e9
        self.sl_t_max.value   = dv["t_max"]  * 1e9
        self.sl_m1.value      = dv["m1"]
        self.sl_m2.value      = dv["m2"]

    # ── Export ────────────────────────────────────────────────────────

    def _export(self, _):
        self._read()
        d   = compute_all(self.p)
        fig = draw_figure(self.p, d, figsize=(19, 13))
        fname = "dtqem_zeeman_v44_export.png"
        fig.savefig(fname, dpi=180,
                    bbox_inches="tight",
                    facecolor=C("bg_main"))
        plt.close(fig)
        print(f"[DTQEM Zeeman V44.0]  Saved → {fname}")

    def show(self):
        display(self.dashboard)


# ===========================================================================
# Entry Point
# ===========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  DTQEM Zeeman Effect Simulator  —  V44.0")
    print("  ipywidgets  |  dark theme  |  zero overlap")
    print("=" * 60)
    print()
    print("  V_eff(t) = exp(-γ_φ·t) × exp(-|Δτ(t)|/τ_c)")
    print("  Δτ(t)   = Δω·t  =  (|ΔE|/ℏ)·t")
    print("  ω_L     = eB/(2m)")
    print()
    dash = ZeemanDashboard()
    dash.show()
