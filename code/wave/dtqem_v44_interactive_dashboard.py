
"""
dtqem_v44_colab.py — DTQEM Interactive Dashboard V44.0
=======================================================
Core equation: V_eff = V_source × exp(-γ_φ·τ) × exp(-|Δτ|/τ_c)

CONTRIBUTORS:
    • Berramdane Reddouane (Creator)
    • Gemini (Google)          — Theory & D3 proposal
    • DeepSeek (深度求索)       — Philosophy & critical analysis
    • Claude (Anthropic)       — Code implementation (V17, V44.0)
    • "Clore" (Anonymous)      — Mathematical extensions (D1-D6)

Version: 44.0 | Date: 2026-05-22 | License: MIT
"""
# ── إلغاء التفاعل مع matplotlib widgets واستخدام ipywidgets ──────────
import numpy as np
import matplotlib
matplotlib.use("Agg")  # رسم ثابت فقط، التفاعل عبر ipywidgets

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.lines as mlines
from matplotlib.patches import FancyArrowPatch
from typing import Tuple, Dict, List

import ipywidgets as widgets
from IPython.display import display, clear_output


# ===========================================================================
# Physical Constants
# ===========================================================================
C_LIGHT        = 299_792_458.0
LORENTZ_SAFETY = 0.9999


# ===========================================================================
# Visual Theme
# ===========================================================================
STYLE: Dict[str, str] = {
    "bg_main":        "#0d1117",
    "bg_panel":       "#161b22",
    "bg_slider":      "#21262d",
    "bg_slider_band": "#13181f",
    "accent_blue":    "#58a6ff",
    "accent_cyan":    "#39d0d8",
    "accent_green":   "#3fb950",
    "accent_orange":  "#d29922",
    "accent_red":     "#f85149",
    "accent_purple":  "#bc8cff",
    "text_primary":   "#e6edf3",
    "text_secondary": "#8b949e",
    "grid_color":     "#21262d",
}

def C(key: str) -> str:
    return STYLE[key]


# ===========================================================================
# Pure Physics Functions
# ===========================================================================

def _gamma(v: float) -> float:
    beta = np.clip(abs(v) / C_LIGHT, 0.0, LORENTZ_SAFETY)
    return 1.0 / np.sqrt(1.0 - beta * beta)

def _tau(a: float, v: float) -> float:
    return a / v if v > 0.0 else np.inf

def _delta_tau(tau: float, v: float) -> float:
    return tau * (1.0 - 1.0 / _gamma(v))

def _sinc(u: np.ndarray) -> np.ndarray:
    out = np.ones_like(u, dtype=float)
    nz  = u != 0.0
    out[nz] = np.sin(u[nz]) / u[nz]
    return out

def _V_source(d, lam, src, L_src):
    u = np.pi * src * d / (lam * L_src)
    return float(abs(_sinc(np.array([u]))[0]))

def _V_env(gph, tau):
    return float(np.exp(-gph * tau))

def _V_dtqem(dtau, tau_c):
    return float(np.exp(-abs(dtau) / tau_c))

def physics(d: float, p: dict) -> dict:
    tau   = _tau(p["a_m"], p["velocity"])
    dtau  = _delta_tau(tau, p["velocity"])
    grel  = _gamma(p["velocity"])
    beta  = p["velocity"] / C_LIGHT
    Vs    = _V_source(d, p["lambda_m"], p["source_size"], p["L_source"])
    Ve    = _V_env(p["gamma_phi"], tau)
    Vd    = _V_dtqem(dtau, p["tau_c"])
    Veff  = Vs * Ve * Vd
    return dict(
        tau=tau, delta_tau=dtau, gamma_rel=grel, beta=beta,
        V_source=Vs, V_env=Ve, V_dtqem=Vd, V_eff=Veff
    )

def intensity(x: np.ndarray, p: dict) -> Tuple[np.ndarray, dict]:
    lam, L, a = p["lambda_m"], p["L_m"], p["a_m"]
    sb = p["sigma_b"]
    G  = (np.exp(-x**2 / (2*sb**2))
          if sb > 0 and np.isfinite(sb) else np.ones_like(x))
    diff = _sinc(np.pi * a * x / (lam * L))**2
    info = physics(p["d"], p)
    phase = 2*np.pi * p["d"] * x / (lam * L) + p["phi"]
    I = p["I0"] * G * diff * (1.0 + info["V_eff"] * np.cos(phase)) \
        + p["B0"] + p["B1"] * x
    return I, info

def envelope(x: np.ndarray, p: dict, Veff: float):
    lam, L, a = p["lambda_m"], p["L_m"], p["a_m"]
    sb = p["sigma_b"]
    G  = (np.exp(-x**2 / (2*sb**2))
          if sb > 0 and np.isfinite(sb) else np.ones_like(x))
    base = p["I0"] * G * _sinc(np.pi * a * x / (lam * L))**2
    return base*(1+Veff) + p["B0"], base*(1-Veff) + p["B0"]

def quality_label(V: float) -> Tuple[str, str]:
    if V > 0.90: return "EXCELLENT", C("accent_green")
    if V > 0.70: return "GOOD",      C("accent_green")
    if V > 0.40: return "MODERATE",  C("accent_orange")
    if V > 0.10: return "POOR",      C("accent_red")
    return "LOST", C("accent_red")


# ===========================================================================
# Figure Drawing Function (pure, no widgets)
# ===========================================================================

def draw_figure(p: dict, figsize=(16, 10)) -> plt.Figure:
    """
    Draw the complete DTQEM figure with 3 zones:
        Zone A  (top 40%)   : Main interference pattern
        Zone B  (mid 35%)   : Vbar | Phasor | Vcurve
        Zone C  (bot 25%)   : Info panel
    NO sliders inside — they live outside in ipywidgets.
    """
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

    x    = np.linspace(-5e-3, 5e-3, 1500)
    I, info = intensity(x, p)

    fig = plt.figure(figsize=figsize, facecolor=C("bg_main"))
    fig.suptitle(
        "DTQEM  ·  Double-Slit Quantum Interference  ·  V44.0",
        fontsize=14, fontweight="bold",
        color=C("accent_blue"), y=0.98,
    )

    # ── GridSpec: 3 rows ──────────────────────────────────────────────
    gs = gridspec.GridSpec(
        3, 1,
        figure=fig,
        left=0.06, right=0.97,
        top=0.93, bottom=0.04,
        height_ratios=[4.0, 3.5, 2.5],
        hspace=0.45,
    )

    # ─────────────────────────────────────────────────────────────────
    # Zone A: Main Pattern
    # ─────────────────────────────────────────────────────────────────
    ax_pat = fig.add_subplot(gs[0])
    ax_pat.set_facecolor(C("bg_panel"))

    ax_pat.plot(x*1e3, I,
                color=C("accent_blue"), lw=1.6, zorder=3, label="I(x)")
    ax_pat.fill_between(x*1e3, I,
                        alpha=0.14, color=C("accent_blue"), zorder=2)

    eu, ed = envelope(x, p, info["V_eff"])
    ax_pat.plot(x*1e3, eu, color=C("accent_green"),
                lw=0.9, ls="--", alpha=0.7, label="Envelope")
    ax_pat.plot(x*1e3, ed, color=C("accent_green"),
                lw=0.9, ls="--", alpha=0.7)
    ax_pat.axvline(0, color=C("text_secondary"), lw=0.6, ls=":", alpha=0.5)

    ax_pat.set_xlabel("Position  x  [mm]", fontsize=10)
    ax_pat.set_ylabel("Intensity  [counts]", fontsize=10)
    ax_pat.set_xlim(x[0]*1e3, x[-1]*1e3)
    ax_pat.grid(True, alpha=0.35)
    ax_pat.spines["top"].set_visible(False)
    ax_pat.spines["right"].set_visible(False)
    ax_pat.legend(fontsize=8, loc="upper right",
                  facecolor=C("bg_slider"), edgecolor=C("text_secondary"))
    ax_pat.set_title(
        f"V_eff={info['V_eff']:.4f}  |  "
        f"V_src={info['V_source']:.4f}  |  "
        f"V_env={info['V_env']:.4f}  |  "
        f"V_dtqem={info['V_dtqem']:.4f}  |  "
        f"β={info['beta']:.5f}  |  γ={info['gamma_rel']:.4f}",
        fontsize=8.5, pad=5, color=C("text_primary"),
    )

    # ─────────────────────────────────────────────────────────────────
    # Zone B: Three Analytics Panels
    # ─────────────────────────────────────────────────────────────────
    gs_mid = gridspec.GridSpecFromSubplotSpec(
        1, 3, subplot_spec=gs[1], wspace=0.38,
    )

    # ── B1: Visibility Bar ───────────────────────────────────────────
    ax_vb = fig.add_subplot(gs_mid[0])
    ax_vb.set_facecolor(C("bg_panel"))
    lbls  = ["V_source", "V_env", "V_dtqem", "V_eff"]
    vals  = [info[k] for k in lbls]
    cols  = [C("accent_green"), C("accent_orange"),
              C("accent_purple"), C("accent_blue")]
    bars  = ax_vb.bar(lbls, vals, color=cols,
                      edgecolor=C("bg_main"), lw=1.0, width=0.55)
    for bar, v in zip(bars, vals):
        ax_vb.text(
            bar.get_x() + bar.get_width()/2,
            min(v+0.03, 0.96), f"{v:.4f}",
            ha="center", va="bottom",
            fontsize=8.5, fontweight="bold",
            color=C("text_primary"),
        )
    ax_vb.set_ylim(0, 1.15)
    ax_vb.axhline(1.0, color=C("text_secondary"),
                  lw=0.6, ls="--", alpha=0.5)
    ax_vb.set_ylabel("Visibility", fontsize=9)
    ax_vb.set_title("Visibility Decomposition", fontsize=10)
    ax_vb.grid(axis="y", alpha=0.3)
    ax_vb.spines["top"].set_visible(False)
    ax_vb.spines["right"].set_visible(False)
    ax_vb.tick_params(axis="x", labelsize=8)

    # ── B2: Phasor Diagram ───────────────────────────────────────────
    ax_ph = fig.add_subplot(gs_mid[1], polar=True)
    ax_ph.set_facecolor(C("bg_panel"))
    Veff  = info["V_eff"]
    phi   = p["phi"]
    theta = np.linspace(0, 2*np.pi, 300)

    ax_ph.plot([0, phi], [0, Veff],
               color=C("accent_blue"), lw=2.5, zorder=4)
    ax_ph.plot([phi], [Veff], "o",
               color=C("accent_blue"), ms=9, zorder=5)
    ax_ph.plot(theta, np.full_like(theta, Veff),
               color=C("accent_purple"), lw=1.0, ls="--", alpha=0.6)
    ax_ph.text(phi+0.2, min(Veff+0.12, 1.0),
               f"V={Veff:.3f}", fontsize=9, color=C("accent_blue"))
    ax_ph.set_ylim(0, 1.05)
    ax_ph.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax_ph.set_yticklabels(["0.25","0.5","0.75","1.0"],
                           fontsize=7.5, color=C("text_secondary"))
    ax_ph.set_title("Phasor Diagram", fontsize=10, pad=14)
    ax_ph.spines["polar"].set_color(C("text_secondary"))
    ax_ph.tick_params(colors=C("text_secondary"))

    # ── B3: V_eff vs d Curve ─────────────────────────────────────────
    ax_vc = fig.add_subplot(gs_mid[2])
    ax_vc.set_facecolor(C("bg_panel"))
    d_arr = np.linspace(10e-6, 700e-6, 400)
    V_arr = np.array([physics(dv, p)["V_eff"] for dv in d_arr])
    dc    = p["d"]
    Vc    = info["V_eff"]

    ax_vc.plot(d_arr*1e6, V_arr,
               color=C("accent_purple"), lw=1.8)
    ax_vc.axvline(dc*1e6, color=C("accent_orange"), lw=1.2, ls="--")
    ax_vc.plot([dc*1e6], [Vc], "o",
               color=C("accent_orange"), ms=8, zorder=5)
    ax_vc.text(0.97, 0.88, f"V = {Vc:.4f}",
               transform=ax_vc.transAxes, ha="right",
               fontsize=9, color=C("accent_orange"), fontweight="bold")
    ax_vc.set_xlim(10, 700)
    ax_vc.set_ylim(-0.02, 1.05)
    ax_vc.set_xlabel("d  [µm]", fontsize=9)
    ax_vc.set_ylabel("V_eff", fontsize=9)
    ax_vc.set_title("V_eff  vs  Slit Separation", fontsize=10)
    ax_vc.grid(True, alpha=0.3)
    ax_vc.spines["top"].set_visible(False)
    ax_vc.spines["right"].set_visible(False)
    ax_vc.tick_params(labelsize=8)

    # ─────────────────────────────────────────────────────────────────
    # Zone C: Info Panel
    # ─────────────────────────────────────────────────────────────────
    ax_info = fig.add_subplot(gs[2])
    ax_info.set_facecolor(C("bg_slider_band"))
    ax_info.set_xticks([])
    ax_info.set_yticks([])
    for sp in ax_info.spines.values():
        sp.set_edgecolor(C("text_secondary"))
        sp.set_linewidth(0.5)

    ql, qc = quality_label(info["V_eff"])

    # Two columns of info text
    col1 = [
        ("━━ PARTICLE ━━━━━━━━━━━━━━━━━━",       C("text_secondary")),
        (f" v       = {p['velocity']:.3e} m/s",   C("text_primary")),
        (f" β       = {info['beta']:.6f}",         C("accent_cyan")),
        (f" γ       = {info['gamma_rel']:.6f}",    C("accent_cyan")),
        ("━━ TIME SCALES ━━━━━━━━━━━━━━━",        C("text_secondary")),
        (f" τ       = {info['tau']:.3e} s",        C("text_primary")),
        (f" Δτ      = {info['delta_tau']:.3e} s",  C("accent_purple")),
        (f" τ_c     = {p['tau_c']:.3e} s",         C("accent_purple")),
        (f" |Δτ|/τc = {abs(info['delta_tau'])/p['tau_c']:.4f}",
                                                   C("accent_purple")),
    ]
    col2 = [
        ("━━ VISIBILITY ━━━━━━━━━━━━━━━━",        C("text_secondary")),
        (f" V_source = {info['V_source']:.6f}",    C("accent_green")),
        (f" V_env    = {info['V_env']:.6f}",       C("accent_orange")),
        (f" V_dtqem  = {info['V_dtqem']:.6f}",     C("accent_purple")),
        (f" V_eff    = {info['V_eff']:.6f}",       C("accent_blue")),
        ("", C("text_secondary")),
        (f" Coherence: [ {ql} ]",                  qc),
        ("", C("text_secondary")),
        (f" λ={p['lambda_m']*1e9:.0f}nm  "
         f"d={p['d']*1e6:.0f}µm  "
         f"L={p['L_m']:.1f}m",                    C("text_secondary")),
    ]

    dy = 1.0 / max(len(col1), len(col2))
    for i, (txt, clr) in enumerate(col1):
        ax_info.text(0.01, 0.97 - i*dy*0.95, txt,
                     transform=ax_info.transAxes,
                     fontsize=8, color=clr, fontfamily="monospace",
                     va="top")
    for i, (txt, clr) in enumerate(col2):
        ax_info.text(0.50, 0.97 - i*dy*0.95, txt,
                     transform=ax_info.transAxes,
                     fontsize=8, color=clr, fontfamily="monospace",
                     va="top")

    plt.close(fig)  # منع العرض التلقائي
    return fig


# ===========================================================================
# ipywidgets Dashboard
# ===========================================================================

class DTQEMDashboard:
    """
    DTQEM V44.0 — Colab/Jupyter edition.
    All sliders are ipywidgets (HTML) placed ABOVE the matplotlib figure.
    Zero overlap is structurally guaranteed.
    """

    DEFAULTS = {
        "lambda_m":    532e-9,
        "L_m":         1.0,
        "a_m":         50e-6,
        "d":           250e-6,
        "L_source":    0.5,
        "source_size": 10e-6,
        "velocity":    1e6,
        "gamma_phi":   1e10,
        "tau_c":       1e-15,
        "I0":          1500.0,
        "phi":         0.0,
        "sigma_b":     3e-3,
        "B0":          50.0,
        "B1":          0.0,
    }

    def __init__(self):
        self.p = dict(self.DEFAULTS)
        self._build_widgets()
        self._build_layout()

    # ─────────────────────────────────────────────────────────────────
    # Widget Construction
    # ─────────────────────────────────────────────────────────────────

    def _sl(self, desc, vmin, vmax, val, step, fmt=".4f", color="#58a6ff"):
        """Create a styled FloatSlider."""
        sl = widgets.FloatSlider(
            value=val, min=vmin, max=vmax, step=step,
            description="",
            continuous_update=False,
            readout=True,
            readout_format=fmt,
            layout=widgets.Layout(width="100%", height="28px"),
            style={"handle_color": color},
        )
        label = widgets.Label(
            value=desc,
            layout=widgets.Layout(width="100%"),
            style={"font_size": "11px",
                   "text_color": "#8b949e",
                   "font_family": "monospace"},
        )
        return sl, label

    def _build_widgets(self):
        """Build all 12 sliders + 2 buttons."""

        # ── Row 0: Optical / Geometric ────────────────────────────────
        self.sl_d,        self.lb_d        = self._sl(
            "d [µm]  slit sep",
            50, 600, self.DEFAULTS["d"]*1e6, 5, ".1f", "#58a6ff")

        self.sl_lambda,   self.lb_lambda   = self._sl(
            "λ [nm]  wavelength",
            400, 750, self.DEFAULTS["lambda_m"]*1e9, 1, ".0f", "#39d0d8")

        self.sl_L,        self.lb_L        = self._sl(
            "L [m]  screen dist",
            0.5, 3.0, self.DEFAULTS["L_m"], 0.05, ".2f", "#39d0d8")

        self.sl_phi,      self.lb_phi      = self._sl(
            "φ [rad]  phase",
            -3.14, 3.14, self.DEFAULTS["phi"], 0.01, ".3f", "#d29922")

        # ── Row 1: Beam / Background ──────────────────────────────────
        self.sl_sigma_b,  self.lb_sigma_b  = self._sl(
            "σ_b [mm]  envelope",
            0.5, 15.0, self.DEFAULTS["sigma_b"]*1e3, 0.1, ".1f", "#d29922")

        self.sl_I0,       self.lb_I0       = self._sl(
            "I₀ [cts]  peak intensity",
            100, 5000, self.DEFAULTS["I0"], 50, ".0f", "#3fb950")

        self.sl_B0,       self.lb_B0       = self._sl(
            "B₀ [cts]  background",
            0, 500, self.DEFAULTS["B0"], 5, ".0f", "#8b949e")

        self.sl_L_src,    self.lb_L_src    = self._sl(
            "L_src [m]  source dist",
            0.1, 2.0, self.DEFAULTS["L_source"], 0.05, ".2f", "#3fb950")

        # ── Row 2: Decoherence / Particle ─────────────────────────────
        self.sl_log_tauc, self.lb_log_tauc = self._sl(
            "log₁₀(τ_c) [s]  DTQEM param",
            -18, -10, np.log10(self.DEFAULTS["tau_c"]),
            0.1, ".2f", "#bc8cff")

        self.sl_log_v,    self.lb_log_v    = self._sl(
            "log₁₀(v) [m/s]  velocity",
            3, np.log10(0.9999*C_LIGHT),
            np.log10(self.DEFAULTS["velocity"]),
            0.05, ".3f", "#f85149")

        self.sl_log_gph,  self.lb_log_gph  = self._sl(
            "log₁₀(γ_φ) [Hz]  env deco",
            6, 15, np.log10(self.DEFAULTS["gamma_phi"]),
            0.1, ".1f", "#f85149")

        self.sl_src_size, self.lb_src_size = self._sl(
            "src_size [µm]  source size",
            1, 100, self.DEFAULTS["source_size"]*1e6,
            1, ".1f", "#3fb950")

        # ── Buttons ───────────────────────────────────────────────────
        self.btn_reset = widgets.Button(
            description="⟳  Reset",
            button_style="warning",
            layout=widgets.Layout(width="130px", height="32px"),
        )
        self.btn_export = widgets.Button(
            description="↓  Export PNG",
            button_style="success",
            layout=widgets.Layout(width="130px", height="32px"),
        )
        self.btn_reset.on_click(self._reset)
        self.btn_export.on_click(self._export)

        # ── Output widget for the figure ──────────────────────────────
        self.out = widgets.Output()

    # ─────────────────────────────────────────────────────────────────
    # Layout Assembly
    # ─────────────────────────────────────────────────────────────────

    def _row(self, pairs):
        """Build one slider row: [(label, slider), ...]"""
        cols = []
        for lb, sl in pairs:
            cell = widgets.VBox(
                [lb, sl],
                layout=widgets.Layout(
                    width="24%",
                    padding="2px 6px 2px 6px",
                    border="1px solid #21262d",
                ),
            )
            cols.append(cell)
        return widgets.HBox(
            cols,
            layout=widgets.Layout(
                width="100%",
                background="#13181f",
                padding="3px 0px",
            ),
        )

    def _build_layout(self):
        """
        Final layout (top → bottom):
            [header]
            [slider row 0]
            [slider row 1]
            [slider row 2]
            [buttons]
            [separator]
            [figure output]   ← matplotlib figure, NO sliders inside
        """
        header = widgets.HTML(
            value=(
                '<div style="background:#0d1117; padding:8px 12px; '
                'border-bottom:2px solid #21262d;">'
                '<span style="font-size:16px; font-weight:bold; '
                'color:#58a6ff; font-family:monospace;">'
                'DTQEM  ·  Double-Slit Quantum Interference  ·  V44.0'
                '</span><br>'
                '<span style="font-size:11px; color:#8b949e; '
                'font-family:monospace;">'
                'V_eff = V_source × exp(-γφ·τ) × exp(-|Δτ|/τ_c)  '
                '|  Δτ = τ·(1-1/γ)  |  τ = a/v'
                '</span></div>'
            ),
            layout=widgets.Layout(width="100%"),
        )

        sl_header = widgets.HTML(
            value=(
                '<div style="background:#13181f; padding:4px 10px;">'
                '<span style="font-size:11px; color:#8b949e; '
                'font-family:monospace;">'
                '━━  PARAMETER CONTROLS  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                '</span></div>'
            ),
            layout=widgets.Layout(width="100%"),
        )

        row0 = self._row([
            (self.lb_d,       self.sl_d),
            (self.lb_lambda,  self.sl_lambda),
            (self.lb_L,       self.sl_L),
            (self.lb_phi,     self.sl_phi),
        ])
        row1 = self._row([
            (self.lb_sigma_b, self.sl_sigma_b),
            (self.lb_I0,      self.sl_I0),
            (self.lb_B0,      self.sl_B0),
            (self.lb_L_src,   self.sl_L_src),
        ])
        row2 = self._row([
            (self.lb_log_tauc, self.sl_log_tauc),
            (self.lb_log_v,    self.sl_log_v),
            (self.lb_log_gph,  self.sl_log_gph),
            (self.lb_src_size, self.sl_src_size),
        ])

        btn_bar = widgets.HBox(
            [self.btn_reset, self.btn_export],
            layout=widgets.Layout(
                padding="5px 10px",
                background="#0d1117",
                gap="10px",
            ),
        )

        separator = widgets.HTML(
            value=(
                '<hr style="border:none; border-top:1px solid #21262d;'
                ' margin:4px 0px;"/>'
                '<div style="background:#0d1117; padding:2px 10px;">'
                '<span style="font-size:10px; color:#8b949e; '
                'font-family:monospace;">'
                '━━  VISUALIZATION  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                '</span></div>'
            ),
            layout=widgets.Layout(width="100%"),
        )

        self.dashboard = widgets.VBox(
            [
                header,
                sl_header,
                row0,
                row1,
                row2,
                btn_bar,
                separator,
                self.out,         # ← figure goes here, completely separate
            ],
            layout=widgets.Layout(
                width="100%",
                background="#0d1117",
                border="1px solid #21262d",
            ),
        )

        # Connect all slider observe callbacks
        for sl in [
            self.sl_d, self.sl_lambda, self.sl_L, self.sl_phi,
            self.sl_sigma_b, self.sl_I0, self.sl_B0, self.sl_L_src,
            self.sl_log_tauc, self.sl_log_v, self.sl_log_gph, self.sl_src_size,
        ]:
            sl.observe(self._update, names="value")

        # Draw initial figure
        self._update()

    # ─────────────────────────────────────────────────────────────────
    # Read widget values → params dict
    # ─────────────────────────────────────────────────────────────────

    def _read(self):
        self.p["d"]           = self.sl_d.value        * 1e-6
        self.p["lambda_m"]    = self.sl_lambda.value   * 1e-9
        self.p["L_m"]         = self.sl_L.value
        self.p["phi"]         = self.sl_phi.value
        self.p["sigma_b"]     = self.sl_sigma_b.value  * 1e-3
        self.p["I0"]          = self.sl_I0.value
        self.p["B0"]          = self.sl_B0.value
        self.p["L_source"]    = self.sl_L_src.value
        self.p["tau_c"]       = 10.0 ** self.sl_log_tauc.value
        self.p["velocity"]    = 10.0 ** self.sl_log_v.value
        self.p["gamma_phi"]   = 10.0 ** self.sl_log_gph.value
        self.p["source_size"] = self.sl_src_size.value * 1e-6

    # ─────────────────────────────────────────────────────────────────
    # Update callback
    # ─────────────────────────────────────────────────────────────────

    def _update(self, change=None):
        self._read()
        fig = draw_figure(self.p, figsize=(15, 9))
        with self.out:
            clear_output(wait=True)
            display(fig)
            plt.close(fig)

    # ─────────────────────────────────────────────────────────────────
    # Button Callbacks
    # ─────────────────────────────────────────────────────────────────

    def _reset(self, _):
        dv = self.DEFAULTS
        self.sl_d.value         = dv["d"]           * 1e6
        self.sl_lambda.value    = dv["lambda_m"]    * 1e9
        self.sl_L.value         = dv["L_m"]
        self.sl_phi.value       = dv["phi"]
        self.sl_sigma_b.value   = dv["sigma_b"]     * 1e3
        self.sl_I0.value        = dv["I0"]
        self.sl_B0.value        = dv["B0"]
        self.sl_L_src.value     = dv["L_source"]
        self.sl_log_tauc.value  = np.log10(dv["tau_c"])
        self.sl_log_v.value     = np.log10(dv["velocity"])
        self.sl_log_gph.value   = np.log10(dv["gamma_phi"])
        self.sl_src_size.value  = dv["source_size"] * 1e6

    def _export(self, _):
        self._read()
        fig = draw_figure(self.p, figsize=(16, 10))
        fname = "dtqem_v44_export.png"
        fig.savefig(fname, dpi=180,
                    bbox_inches="tight",
                    facecolor=C("bg_main"))
        plt.close(fig)
        print(f"[DTQEM V44.0]  Saved → {fname}")

    # ─────────────────────────────────────────────────────────────────
    # Display
    # ─────────────────────────────────────────────────────────────────

    def show(self):
        display(self.dashboard)


# ===========================================================================
# Entry Point
# ===========================================================================

if __name__ == "__main__":
    print("=" * 58)
    print("  DTQEM Interactive Dashboard  —  V44.0")
    print("  ipywidgets edition  |  Zero overlap guaranteed")
    print("=" * 58)
    dash = DTQEMDashboard()
    dash.show()
