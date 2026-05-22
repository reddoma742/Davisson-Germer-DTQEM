
"""
dtqem_qubit_decoherence_v44.py
==============================
DTQEM Qubit Decoherence Simulator — V44.0
Interactive dashboard (ipywidgets + matplotlib)

Core Equation:
    V_eff(t) = exp(-gamma_phi * t) * exp(-|delta_tau(t)| / tau_c)

    delta_tau(t) = t * (1 - 1/gamma_rel)
    gamma_rel    = 1 / sqrt(1 - v^2/c^2)

Physical Interpretation:
    V_eff -> coherence between |0> and |1> states of the qubit
    V_eff = 1 : perfect coherence
    V_eff = 0 : complete decoherence

═══════════════════════════════════════════════════════════════════
CONTRIBUTORS & ACKNOWLEDGMENTS
═══════════════════════════════════════════════════════════════════

Project Creator:
    • Berramdane Reddouane (Morocco)

Core Contributors (AI Assistants):
    • Gemini (Google)          — Theoretical discussions, D3 proposal
    • DeepSeek (深度求索)       — Philosophical insights, critical analysis
    • Claude (Anthropic)       — Code writing (V44.0, V1.0, V1.0 Zeeman)

Special Thanks:
    • "Clore" (Anonymous colleague) — Mathematical improvement proposals

Role of Each Contributor:
    — Gemini:   Proposed the stretched exponential (D3) as a physical
                generalization of the decoherence term.
    — DeepSeek: Provided deep philosophical discussions linking proper-time
                difference to the measurement problem.
    — Claude:   Wrote the complete interactive dashboard for Qubit (V1.0)
                with ipywidgets and zero-overlap layout.

License: MIT
Version: 1.0
Date: 2026-05-22
"""

# ── backend ───────────────────────────────────────────────────────────────
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
C_LIGHT        = 299_792_458.0   # m/s
LORENTZ_SAFETY = 0.9999


# ===========================================================================
# Visual Theme
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
    "text_primary":   "#e6edf3",
    "text_secondary": "#8b949e",
    "grid_color":     "#21262d",
}

def C(k: str) -> str:
    return STYLE[k]


# ===========================================================================
# Physics
# ===========================================================================

def gamma_rel(v: float) -> float:
    """Lorentz factor with safety clipping."""
    beta = np.clip(abs(v) / C_LIGHT, 0.0, LORENTZ_SAFETY)
    return 1.0 / np.sqrt(1.0 - beta * beta)


def delta_tau_fn(t: np.ndarray, v: float) -> np.ndarray:
    """
    Relativistic proper-time difference:
        delta_tau(t) = t * (1 - 1/gamma_rel)
    """
    g = gamma_rel(v)
    return t * (1.0 - 1.0 / g)


def V_env_fn(t: np.ndarray, gamma_phi: float) -> np.ndarray:
    """Environmental decoherence: exp(-gamma_phi * t)"""
    return np.exp(-gamma_phi * t)


def V_dtqem_fn(t: np.ndarray, v: float, tau_c: float) -> np.ndarray:
    """DTQEM proper-time decoherence: exp(-|delta_tau| / tau_c)"""
    dt = delta_tau_fn(t, v)
    return np.exp(-np.abs(dt) / tau_c)


def V_eff_fn(t: np.ndarray, v: float,
             gamma_phi: float, tau_c: float) -> np.ndarray:
    """
    Total effective coherence:
        V_eff = exp(-gamma_phi*t) * exp(-|delta_tau|/tau_c)
    """
    return V_env_fn(t, gamma_phi) * V_dtqem_fn(t, v, tau_c)


def coherence_time_estimate(v: float,
                             gamma_phi: float,
                             tau_c: float) -> float:
    """
    Estimate T2* (time when V_eff drops to 1/e).
    Solved analytically for the D0 model:
        gamma_phi*t + |delta_tau(t)|/tau_c = 1
        (gamma_phi + (1-1/g)/tau_c) * t = 1
    """
    g   = gamma_rel(v)
    k   = gamma_phi + abs(1.0 - 1.0/g) / tau_c
    return 1.0 / k if k > 0 else np.inf


def bloch_coords(V: np.ndarray,
                 phi: float = 0.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Map coherence V_eff to Bloch sphere trajectory.
    Assumes initial state |+> = (|0>+|1>)/sqrt(2)
        rho_01 = 0.5 * V_eff * exp(i*phi)
    Returns (x, y, z) with z=0 for equatorial state.
    """
    x = V * np.cos(phi)
    y = V * np.sin(phi)
    z = np.zeros_like(V)
    return x, y, z


def velocity_sweep(v_arr: np.ndarray,
                   t_eval: float,
                   gamma_phi: float,
                   tau_c: float) -> np.ndarray:
    """Compute V_eff at fixed time t_eval across a range of velocities."""
    return np.array([
        float(V_eff_fn(np.array([t_eval]), vi, gamma_phi, tau_c)[0])
        for vi in v_arr
    ])


def compute_all(p: dict) -> dict:
    """
    Compute all quantities needed for the dashboard.

    Returns a dict with:
        t_arr, V_eff, V_env, V_dtqem, delta_tau
        v_arr, V_vs_v
        T2_star, gamma_val, beta_val
        bloch_x, bloch_y
    """
    t_max = p["t_max"]
    n_t   = 800
    t_arr = np.linspace(0, t_max, n_t)

    v         = p["velocity"]
    gph       = p["gamma_phi"]
    tc        = p["tau_c"]
    t_eval    = p["t_eval"]

    g_val     = gamma_rel(v)
    beta_val  = v / C_LIGHT

    V_eff     = V_eff_fn(t_arr, v, gph, tc)
    V_env     = V_env_fn(t_arr, gph)
    V_dtq     = V_dtqem_fn(t_arr, v, tc)
    dt_arr    = delta_tau_fn(t_arr, v)
    T2        = coherence_time_estimate(v, gph, tc)

    # Velocity sweep at fixed t_eval
    v_arr  = np.linspace(1e3, 0.9999 * C_LIGHT, 600)
    V_vs_v = velocity_sweep(v_arr, t_eval, gph, tc)

    # Bloch trajectory
    bx, by, _ = bloch_coords(V_eff, phi=0.0)

    # Point values at t_eval
    V_at_t = float(V_eff_fn(np.array([t_eval]), v, gph, tc)[0])

    return dict(
        t_arr=t_arr,
        V_eff=V_eff, V_env=V_env, V_dtq=V_dtq,
        dt_arr=dt_arr,
        v_arr=v_arr, V_vs_v=V_vs_v,
        T2=T2,
        gamma_val=g_val, beta_val=beta_val,
        bx=bx, by=by,
        t_eval=t_eval, V_at_t=V_at_t,
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
    """Map coherence value to a status color."""
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


def draw_figure(p: dict, d: dict, figsize=(16, 11)) -> plt.Figure:
    """
    Draw the complete qubit decoherence dashboard figure.

    Layout (3 rows):
        Row 0 : V_eff(t) main plot  +  Bloch sphere projection
        Row 1 : Component breakdown  +  V_eff vs velocity
        Row 2 : Info panel  +  delta_tau(t)  +  Coherence heatmap
    """
    _apply_theme()
    fig = plt.figure(figsize=figsize, facecolor=C("bg_main"))

    fig.suptitle(
        "DTQEM  ·  Qubit Decoherence Simulator  ·  V44.0",
        fontsize=14, fontweight="bold",
        color=C("accent_blue"), y=0.985,
    )

    gs = gridspec.GridSpec(
        3, 1,
        figure=fig,
        left=0.05, right=0.97,
        top=0.955, bottom=0.05,
        height_ratios=[4.2, 3.5, 3.0],
        hspace=0.48,
    )

    # ── Row 0 ────────────────────────────────────────────────────────
    gs0 = gridspec.GridSpecFromSubplotSpec(
        1, 2, subplot_spec=gs[0], wspace=0.30, width_ratios=[3, 1.4])

    # ── Row 1 ────────────────────────────────────────────────────────
    gs1 = gridspec.GridSpecFromSubplotSpec(
        1, 2, subplot_spec=gs[1], wspace=0.30)

    # ── Row 2 ────────────────────────────────────────────────────────
    gs2 = gridspec.GridSpecFromSubplotSpec(
        1, 3, subplot_spec=gs[2], wspace=0.38, width_ratios=[1.4, 1.8, 1.8])

    ax_main  = fig.add_subplot(gs0[0])   # V_eff vs t
    ax_bloch = fig.add_subplot(gs0[1])   # Bloch projection
    ax_comp  = fig.add_subplot(gs1[0])   # Components
    ax_vvel  = fig.add_subplot(gs1[1])   # V_eff vs velocity
    ax_info  = fig.add_subplot(gs2[0])   # Info panel
    ax_dtau  = fig.add_subplot(gs2[1])   # delta_tau(t)
    ax_heat  = fig.add_subplot(gs2[2])   # Coherence heatmap

    for ax in [ax_main, ax_bloch, ax_comp, ax_vvel,
               ax_info, ax_dtau, ax_heat]:
        ax.set_facecolor(C("bg_panel"))

    t   = d["t_arr"]
    V   = d["V_eff"]
    V_c = _coherence_color(d["V_at_t"])
    t_s = d["t_eval"]

    # =================================================================
    # Panel 1: V_eff vs time  (main)
    # =================================================================
    ax = ax_main

    # Gradient fill using a custom colormap
    cmap_g = LinearSegmentedColormap.from_list(
        "coh", [C("accent_red"), C("accent_orange"),
                C("accent_cyan"), C("accent_green")])

    # Fill with segments coloured by V value
    for i in range(len(t)-1):
        fc = cmap_g(V[i])
        ax.fill_between(t[i:i+2]*1e9, 0, V[i:i+2], color=fc, alpha=0.18)

    ax.plot(t*1e9, V,  color=C("accent_blue"),   lw=2.0, label="V_eff (total)",  zorder=4)
    ax.plot(t*1e9, d["V_env"], color=C("accent_orange"),
            lw=1.2, ls="--", alpha=0.8, label="V_env = exp(-γφ·t)",   zorder=3)
    ax.plot(t*1e9, d["V_dtq"], color=C("accent_purple"),
            lw=1.2, ls=":",  alpha=0.8, label="V_dtqem = exp(-|Δτ|/τc)", zorder=3)

    # 1/e reference
    ax.axhline(1/np.e, color=C("text_secondary"),
               lw=0.8, ls="--", alpha=0.6, label="1/e  (T₂* level)")

    # T2* marker
    T2 = d["T2"]
    if T2 < t[-1]:
        ax.axvline(T2*1e9, color=C("accent_yellow"),
                   lw=1.2, ls="--", alpha=0.8)
        ax.text(T2*1e9 + t[-1]*1e9*0.01, 0.05,
                f"T₂*={T2*1e9:.2f} ns",
                fontsize=8, color=C("accent_yellow"))

    # t_eval marker
    V_te = d["V_at_t"]
    ax.axvline(t_s*1e9, color=V_c, lw=1.5, alpha=0.9)
    ax.plot([t_s*1e9], [V_te], "o", color=V_c, ms=9, zorder=6)
    ax.annotate(
        f"  t={t_s*1e9:.1f}ns\n  V={V_te:.4f}",
        xy=(t_s*1e9, V_te),
        xytext=(t_s*1e9 + t[-1]*1e9*0.05, V_te + 0.08),
        fontsize=8, color=V_c,
        arrowprops=dict(arrowstyle="->", color=V_c, lw=1.0),
    )

    ax.set_xlim(0, t[-1]*1e9)
    ax.set_ylim(-0.03, 1.08)
    ax.set_xlabel("Time  t  [ns]", fontsize=10)
    ax.set_ylabel("Coherence  V_eff", fontsize=10)
    ax.set_title(
        f"Qubit Coherence vs Time  "
        f"|  β={d['beta_val']:.5f}  |  γ={d['gamma_val']:.5f}  "
        f"|  T₂*={T2*1e9:.3f} ns",
        fontsize=9, pad=5,
    )
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, facecolor=C("bg_slider"),
              edgecolor=C("text_secondary"), loc="upper right")

    # =================================================================
    # Panel 2: Bloch Sphere Projection  (xy plane)
    # =================================================================
    ax = ax_bloch

    # Unit circle
    th = np.linspace(0, 2*np.pi, 300)
    ax.plot(np.cos(th), np.sin(th),
            color=C("text_secondary"), lw=0.8, alpha=0.5)

    # Trajectory
    bx_arr, by_arr = d["bx"], d["by"]
    ax.plot(bx_arr, by_arr, color=C("accent_blue"),
            lw=1.5, alpha=0.7, label="Bloch trajectory")

    # Current point
    idx_te = np.searchsorted(t, t_s)
    idx_te = min(idx_te, len(bx_arr)-1)
    ax.plot([bx_arr[idx_te]], [by_arr[idx_te]], "o",
            color=V_c, ms=10, zorder=5, label=f"t={t_s*1e9:.1f} ns")

    # Axes labels
    ax.axhline(0, color=C("text_secondary"), lw=0.5, alpha=0.4)
    ax.axvline(0, color=C("text_secondary"), lw=0.5, alpha=0.4)
    ax.text(1.05,  0.0, "|+⟩",   fontsize=9, color=C("text_secondary"), va="center")
    ax.text(-1.15, 0.0, "|-⟩",   fontsize=9, color=C("text_secondary"), va="center")
    ax.text(0.0,  1.08, "|i+⟩",  fontsize=9, color=C("text_secondary"), ha="center")
    ax.text(0.0, -1.12, "|i-⟩",  fontsize=9, color=C("text_secondary"), ha="center")

    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal")
    ax.set_title("Bloch Sphere  (xy projection)", fontsize=10)
    ax.set_xlabel("⟨σ_x⟩", fontsize=9)
    ax.set_ylabel("⟨σ_y⟩", fontsize=9)
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, facecolor=C("bg_slider"),
              edgecolor=C("text_secondary"))

    # =================================================================
    # Panel 3: Component Breakdown Bar
    # =================================================================
    ax = ax_comp

    # At t_eval
    Ve_te  = float(V_env_fn(np.array([t_s]), p["gamma_phi"])[0])
    Vd_te  = float(V_dtqem_fn(np.array([t_s]), p["velocity"], p["tau_c"])[0])

    lbls  = ["V_env", "V_dtqem", "V_eff"]
    vals  = [Ve_te, Vd_te, V_te]
    cols  = [C("accent_orange"), C("accent_purple"), C("accent_blue")]

    bars = ax.bar(lbls, vals, color=cols,
                  edgecolor=C("bg_main"), lw=1.0, width=0.5)
    for bar, v in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            min(v + 0.03, 0.96),
            f"{v:.4f}",
            ha="center", va="bottom",
            fontsize=9, fontweight="bold",
            color=C("text_primary"),
        )

    ax.set_ylim(0, 1.15)
    ax.axhline(1.0, color=C("text_secondary"), lw=0.6, ls="--", alpha=0.5)
    ax.axhline(1/np.e, color=C("accent_yellow"), lw=0.6, ls=":", alpha=0.7)
    ax.set_title(f"Decoherence Components  at  t = {t_s*1e9:.2f} ns",
                 fontsize=10)
    ax.set_ylabel("Factor value", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", labelsize=9)

    # =================================================================
    # Panel 4: V_eff vs Velocity
    # =================================================================
    ax = ax_vvel

    v_arr  = d["v_arr"]
    V_vs_v = d["V_vs_v"]
    beta_arr = v_arr / C_LIGHT

    ax.plot(beta_arr, V_vs_v, color=C("accent_cyan"), lw=1.8)
    ax.fill_between(beta_arr, V_vs_v,
                    alpha=0.15, color=C("accent_cyan"))

    # Mark current velocity
    ax.axvline(d["beta_val"], color=C("accent_orange"),
               lw=1.2, ls="--", alpha=0.9)
    ax.plot([d["beta_val"]], [V_te], "o",
            color=C("accent_orange"), ms=8, zorder=5)
    ax.text(0.97, 0.92, f"β = {d['beta_val']:.5f}\nV = {V_te:.4f}",
            transform=ax.transAxes, ha="right", fontsize=8.5,
            color=C("accent_orange"), fontweight="bold")

    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.02, 1.05)
    ax.axhline(1/np.e, color=C("text_secondary"),
               lw=0.7, ls=":", alpha=0.6, label="1/e")
    ax.set_xlabel("β = v/c", fontsize=10)
    ax.set_ylabel("V_eff", fontsize=10)
    ax.set_title(f"V_eff  vs  Velocity  at  t = {t_s*1e9:.2f} ns",
                 fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, facecolor=C("bg_slider"),
              edgecolor=C("text_secondary"))

    # =================================================================
    # Panel 5: Info Panel
    # =================================================================
    ax = ax_info
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor(C("text_secondary"))
        sp.set_linewidth(0.5)

    qs = _quality_str(V_te)
    qc = _coherence_color(V_te)

    info_lines = [
        ("━━ QUBIT STATE ━━━━━━━━━━━",   C("text_secondary")),
        (f" V_eff    = {V_te:.6f}",        qc),
        (f" Status   = {qs}",              qc),
        ("", C("text_secondary")),
        ("━━ PARTICLE ━━━━━━━━━━━━━",    C("text_secondary")),
        (f" v        = {p['velocity']:.3e} m/s", C("text_primary")),
        (f" β        = {d['beta_val']:.6f}",      C("accent_cyan")),
        (f" γ        = {d['gamma_val']:.6f}",      C("accent_cyan")),
        ("", C("text_secondary")),
        ("━━ TIME SCALES ━━━━━━━━━━",    C("text_secondary")),
        (f" t_eval   = {t_s*1e9:.3f} ns",          C("text_primary")),
        (f" T₂*      = {T2*1e9:.3f} ns",            C("accent_yellow")),
        (f" τ_c      = {p['tau_c']:.3e} s",         C("accent_purple")),
        (f" Δτ(t)    = {float(delta_tau_fn(np.array([t_s]),p['velocity'])[0]):.3e} s",
                                                     C("accent_purple")),
        ("", C("text_secondary")),
        ("━━ RATES ━━━━━━━━━━━━━━━━",   C("text_secondary")),
        (f" γ_φ      = {p['gamma_phi']:.3e} Hz",    C("accent_orange")),
        (f" 1/τ_c    = {1/p['tau_c']:.3e} Hz",      C("accent_purple")),
    ]

    dy = 0.054
    for i, (txt, col) in enumerate(info_lines):
        ax.text(0.04, 0.97 - i*dy, txt,
                transform=ax.transAxes,
                fontsize=7.8, color=col,
                fontfamily="monospace", va="top")

    ax.set_title("Parameters & State", fontsize=10)

    # =================================================================
    # Panel 6: delta_tau vs time
    # =================================================================
    ax = ax_dtau

    ax.plot(t*1e9, d["dt_arr"]*1e15,
            color=C("accent_purple"), lw=1.8, label="|Δτ(t)|")
    ax.fill_between(t*1e9, d["dt_arr"]*1e15,
                    alpha=0.18, color=C("accent_purple"))

    # tau_c reference line
    ax.axhline(p["tau_c"]*1e15, color=C("accent_yellow"),
               lw=1.0, ls="--", alpha=0.8,
               label=f"τ_c = {p['tau_c']:.1e} s")

    # t_eval marker
    dtau_te = float(delta_tau_fn(np.array([t_s]), p["velocity"])[0])
    ax.axvline(t_s*1e9, color=C("accent_orange"),
               lw=1.2, ls="--", alpha=0.8)
    ax.plot([t_s*1e9], [dtau_te*1e15], "o",
            color=C("accent_orange"), ms=7, zorder=5)

    ax.set_xlim(0, t[-1]*1e9)
    ax.set_xlabel("Time  t  [ns]", fontsize=9)
    ax.set_ylabel("|Δτ|  [fs]", fontsize=9)
    ax.set_title("Proper-Time Difference  |Δτ(t)|", fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(fontsize=8, facecolor=C("bg_slider"),
              edgecolor=C("text_secondary"))

    # =================================================================
    # Panel 7: Coherence Heatmap  (tau_c vs velocity)
    # =================================================================
    ax = ax_heat

    n_h     = 60
    v_h     = np.linspace(1e4, 0.999*C_LIGHT, n_h)
    tc_h    = np.logspace(-18, -12, n_h)
    beta_h  = v_h / C_LIGHT

    Z = np.zeros((n_h, n_h))
    for i, vi in enumerate(v_h):
        for j, tci in enumerate(tc_h):
            Z[i, j] = float(
                V_eff_fn(np.array([t_s]), vi, p["gamma_phi"], tci)[0]
            )

    # Custom colormap: red(0) -> yellow -> green(1)
    cmap_h = LinearSegmentedColormap.from_list(
        "dtqem_heat",
        [(0.0, "#f85149"),
         (0.3, "#d29922"),
         (0.6, "#39d0d8"),
         (1.0, "#3fb950")],
    )

    im = ax.imshow(
        Z, origin="lower", aspect="auto",
        cmap=cmap_h, vmin=0, vmax=1,
        extent=[np.log10(tc_h[0]), np.log10(tc_h[-1]),
                beta_h[0], beta_h[-1]],
    )
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
                 label="V_eff").ax.tick_params(labelsize=7)

    # Mark current params
    ax.axhline(d["beta_val"],
               color="white", lw=1.0, ls="--", alpha=0.7)
    ax.axvline(np.log10(p["tau_c"]),
               color="white", lw=1.0, ls="--", alpha=0.7)
    ax.plot([np.log10(p["tau_c"])], [d["beta_val"]],
            "*", color="white", ms=10, zorder=5)

    ax.set_xlabel("log₁₀(τ_c)  [s]", fontsize=9)
    ax.set_ylabel("β = v/c", fontsize=9)
    ax.set_title(f"Coherence Map  at  t = {t_s*1e9:.2f} ns\n"
                 f"(white ✦ = current params)", fontsize=9)
    ax.tick_params(labelsize=8)

    plt.close(fig)
    return fig


# ===========================================================================
# ipywidgets Dashboard
# ===========================================================================

class QubitDashboard:
    """
    DTQEM Qubit Decoherence Dashboard — V44.0
    ipywidgets sliders ABOVE matplotlib figure. Zero overlap.
    """

    DEFAULTS = {
        "tau_c":     1e-15,
        "velocity":  1e6,
        "gamma_phi": 1e9,
        "t_eval":    2e-9,
        "t_max":     20e-9,
        "a_m":       50e-6,
    }

    def __init__(self):
        self.p = dict(self.DEFAULTS)
        self._build_widgets()
        self._build_layout()

    # ── Widget factory ────────────────────────────────────────────────

    def _fsl(self, desc, vmin, vmax, val, step,
             fmt=".3f", color="#58a6ff"):
        """Styled FloatSlider."""
        sl = widgets.FloatSlider(
            value=val, min=vmin, max=vmax, step=step,
            description="",
            continuous_update=False,
            readout=True,
            readout_format=fmt,
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
            -18, -12,
            np.log10(self.DEFAULTS["tau_c"]),
            0.1, ".2f", "#bc8cff")

        self.sl_log_v,   self.lb_log_v   = self._fsl(
            "log₁₀(v) [m/s]   velocity",
            3, np.log10(0.9999 * C_LIGHT),
            np.log10(self.DEFAULTS["velocity"]),
            0.05, ".3f", "#f85149")

        self.sl_log_gph, self.lb_log_gph = self._fsl(
            "log₁₀(γ_φ) [Hz]   env deco rate",
            6, 15,
            np.log10(self.DEFAULTS["gamma_phi"]),
            0.1, ".1f", "#d29922")

        self.sl_t_eval,  self.lb_t_eval  = self._fsl(
            "t_eval [ns]   evaluation time",
            0.0, 20.0,
            self.DEFAULTS["t_eval"] * 1e9,
            0.1, ".2f", "#39d0d8")

        # ── Row 1 ────────────────────────────────────────────────────
        self.sl_t_max,   self.lb_t_max   = self._fsl(
            "t_max [ns]   time window",
            1.0, 100.0,
            self.DEFAULTS["t_max"] * 1e9,
            1.0, ".1f", "#58a6ff")

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

        # Output widget for the figure
        self.out = widgets.Output()

    # ── Layout ────────────────────────────────────────────────────────

    def _cell(self, lb, sl):
        return widgets.VBox(
            [lb, sl],
            layout=widgets.Layout(
                width="24%",
                padding="2px 6px",
                border="1px solid #21262d",
            ),
        )

    def _build_layout(self):

        header = widgets.HTML(value=(
            '<div style="background:#0d1117;padding:8px 14px;'
            'border-bottom:2px solid #21262d;">'
            '<span style="font-size:16px;font-weight:bold;'
            'color:#58a6ff;font-family:monospace;">'
            'DTQEM  ·  Qubit Decoherence Simulator  ·  V44.0'
            '</span><br>'
            '<span style="font-size:11px;color:#8b949e;font-family:monospace;">'
            'V_eff(t) = exp(-γφ·t) × exp(-|Δτ(t)|/τ_c)'
            '&nbsp;&nbsp;|&nbsp;&nbsp;'
            'Δτ = t·(1 - 1/γ)&nbsp;&nbsp;|&nbsp;&nbsp;'
            'γ = 1/√(1-β²)'
            '</span></div>'
        ), layout=widgets.Layout(width="100%"))

        ctrl_hdr = widgets.HTML(value=(
            '<div style="background:#13181f;padding:3px 10px;">'
            '<span style="font-size:11px;color:#8b949e;font-family:monospace;">'
            '━━  PARAMETER CONTROLS  '
            '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
            '</span></div>'
        ), layout=widgets.Layout(width="100%"))

        row0 = widgets.HBox([
            self._cell(self.lb_log_tc,  self.sl_log_tc),
            self._cell(self.lb_log_v,   self.sl_log_v),
            self._cell(self.lb_log_gph, self.sl_log_gph),
            self._cell(self.lb_t_eval,  self.sl_t_eval),
        ], layout=widgets.Layout(width="100%", background="#13181f",
                                 padding="3px 0px"))

        row1 = widgets.HBox([
            self._cell(self.lb_t_max, self.sl_t_max),
            widgets.VBox(
                [widgets.HBox(
                    [self.btn_reset, self.btn_export],
                    layout=widgets.Layout(gap="10px", padding="12px 6px"),
                )],
                layout=widgets.Layout(width="74%"),
            ),
        ], layout=widgets.Layout(width="100%", background="#13181f",
                                 padding="3px 0px"))

        sep = widgets.HTML(value=(
            '<hr style="border:none;border-top:1px solid #21262d;margin:4px 0;"/>'
            '<div style="background:#0d1117;padding:2px 10px;">'
            '<span style="font-size:10px;color:#8b949e;font-family:monospace;">'
            '━━  VISUALIZATION  '
            '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
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

        # Wire sliders
        for sl in [self.sl_log_tc, self.sl_log_v,
                   self.sl_log_gph, self.sl_t_eval, self.sl_t_max]:
            sl.observe(self._update, names="value")

        # Initial draw
        self._update()

    # ── Read ──────────────────────────────────────────────────────────

    def _read(self):
        self.p["tau_c"]     = 10.0 ** self.sl_log_tc.value
        self.p["velocity"]  = 10.0 ** self.sl_log_v.value
        self.p["gamma_phi"] = 10.0 ** self.sl_log_gph.value
        self.p["t_eval"]    = self.sl_t_eval.value * 1e-9
        self.p["t_max"]     = self.sl_t_max.value  * 1e-9
        # Clamp t_eval to t_max
        if self.p["t_eval"] > self.p["t_max"]:
            self.p["t_eval"] = self.p["t_max"]

    # ── Update ────────────────────────────────────────────────────────

    def _update(self, change=None):
        self._read()
        d   = compute_all(self.p)
        fig = draw_figure(self.p, d, figsize=(16, 11))
        with self.out:
            clear_output(wait=True)
            display(fig)
            plt.close(fig)

    # ── Reset ─────────────────────────────────────────────────────────

    def _reset(self, _):
        dv = self.DEFAULTS
        self.sl_log_tc.value  = np.log10(dv["tau_c"])
        self.sl_log_v.value   = np.log10(dv["velocity"])
        self.sl_log_gph.value = np.log10(dv["gamma_phi"])
        self.sl_t_eval.value  = dv["t_eval"] * 1e9
        self.sl_t_max.value   = dv["t_max"]  * 1e9

    # ── Export ────────────────────────────────────────────────────────

    def _export(self, _):
        self._read()
        d   = compute_all(self.p)
        fig = draw_figure(self.p, d, figsize=(18, 12))
        fname = "dtqem_qubit_v1_export.png"
        fig.savefig(fname, dpi=180,
                    bbox_inches="tight",
                    facecolor=C("bg_main"))
        plt.close(fig)
        print(f"[DTQEM Qubit V1.0]  Saved → {fname}")

    # ── Show ──────────────────────────────────────────────────────────

    def show(self):
        display(self.dashboard)


# ===========================================================================
# Entry Point
# ===========================================================================

if __name__ == "__main__":
    print("=" * 58)
    print("  DTQEM Qubit Decoherence Simulator  —  V44.0")
    print("  ipywidgets  |  zero overlap  |  Colab ready")
    print("=" * 58)
    dash = QubitDashboard()
    dash.show()
