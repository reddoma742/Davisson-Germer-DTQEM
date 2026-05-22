"""
dtqem_double_slit_forward_v44.py
=================================
DTQEM Double-Slit Forward Model — V44.0
Interactive dashboard (ipywidgets + matplotlib)

Core Equation:
    V_eff = V_source(d) × exp(-γ_φ·τ) × exp(-|Δτ|/τ_c)

where:
    Δτ = τ × (1 - 1/γ_rel)
    τ = a / v
    γ_rel = 1 / √(1 - v²/c²)

Physical Interpretation:
    V_eff -> effective fringe visibility
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
    • Claude (Anthropic)       — Code writing (V44.0 series)

Special Thanks:
    • "Clore" (Anonymous colleague) — Mathematical improvement proposals

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
from typing import Tuple, Dict, List, Optional

import ipywidgets as widgets
from IPython.display import display, clear_output


# ============================================================================
# Physical Constants
# ============================================================================
C_LIGHT = 299_792_458.0          # Speed of light [m/s]
LORENTZ_SAFETY = 0.9999          # Safety threshold for v/c


# ============================================================================
# Visual Theme — DTQEM Dark Theme (same as V44.0 series)
# ============================================================================
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


# ============================================================================
# Physical Model (D0 — baseline)
# ============================================================================

def lorentz_gamma(velocity: float) -> float:
    """Compute Lorentz factor with safety clipping."""
    beta = np.clip(np.abs(velocity) / C_LIGHT, 0.0, LORENTZ_SAFETY)
    return 1.0 / np.sqrt(1.0 - beta**2)


def compute_tau(a_m: float, velocity: float) -> float:
    """Transit time: tau = a / v"""
    if velocity <= 0:
        return np.inf
    return a_m / velocity


def compute_delta_tau(tau: float, velocity: float) -> float:
    """Relativistic proper-time difference: delta_tau = tau * (1 - 1/gamma)"""
    gamma = lorentz_gamma(velocity)
    return tau * (1.0 - 1.0 / gamma)


def sinc_physical(u: np.ndarray) -> np.ndarray:
    """Physical sinc: sin(u)/u with correct limit at u=0."""
    result = np.ones_like(u, dtype=float)
    mask = (u != 0.0)
    result[mask] = np.sin(u[mask]) / u[mask]
    return result


def compute_V_source(d: float, lambda_m: float, source_size: float, L_source: float) -> float:
    """Van Cittert-Zernike coherence: V_source = |sinc(π·src_size·d/(λ·L_src))|"""
    u = np.pi * source_size * d / (lambda_m * L_source)
    return float(np.abs(sinc_physical(np.array([u]))[0]))


def compute_V_env(gamma_phi: float, tau: float) -> float:
    """Environmental decoherence: exp(-gamma_phi * tau)"""
    return float(np.exp(-gamma_phi * tau))


def compute_V_dtqem(delta_tau: float, tau_c: float) -> float:
    """DTQEM proper-time decoherence (D0 — baseline): V_dtqem = exp(-|delta_tau| / tau_c)"""
    return float(np.exp(-np.abs(delta_tau) / tau_c))


def compute_V_eff(d: float, params: dict) -> Tuple[float, dict]:
    """Full effective visibility: V_eff = V_source × V_env × V_dtqem"""
    lam = params["lambda_m"]
    src_size = params["source_size"]
    L_src = params["L_source"]
    gamma_phi = params["gamma_phi"]
    velocity = params["velocity"]
    a_m = params["a_m"]
    tau_c = params["tau_c"]

    tau = compute_tau(a_m, velocity)
    delta_tau = compute_delta_tau(tau, velocity)
    gamma = lorentz_gamma(velocity)
    beta = velocity / C_LIGHT

    V_src = compute_V_source(d, lam, src_size, L_src)
    V_env = compute_V_env(gamma_phi, tau)
    V_dtq = compute_V_dtqem(delta_tau, tau_c)
    V_eff = V_src * V_env * V_dtq

    info = {
        "tau": tau,
        "delta_tau": delta_tau,
        "gamma_rel": gamma,
        "beta": beta,
        "V_source": V_src,
        "V_env": V_env,
        "V_dtqem": V_dtq,
        "V_eff": V_eff,
    }
    return V_eff, info


def model_forward(x: np.ndarray, I0: float, d: float, phi: float,
                  sigma_b: Optional[float], params: dict) -> np.ndarray:
    """
    Full forward model for the double-slit interference pattern.

    I(x) = I0 × G(x,σ_b) × sinc²(π·a·x/(λ·L)) × [1 + V_eff·cos(2π·d·x/(λ·L) + φ)] + B₀ + B₁·x
    """
    lam = params["lambda_m"]
    L = params["L_m"]
    a = params["a_m"]
    B0 = params["B0"]
    B1 = params["B1"]

    # Gaussian envelope
    if sigma_b is not None and np.isfinite(sigma_b) and sigma_b > 0:
        G = np.exp(-x**2 / (2.0 * sigma_b**2))
    else:
        G = np.ones_like(x)

    # Single-slit diffraction
    u_diff = np.pi * a * x / (lam * L)
    diffraction = sinc_physical(u_diff)**2

    # Effective visibility
    V_eff, _ = compute_V_eff(d, params)

    # Interference term
    phase = 2.0 * np.pi * d * x / (lam * L) + phi
    interference = 1.0 + V_eff * np.cos(phase)

    # Linear background
    background = B0 + B1 * x

    return I0 * G * diffraction * interference + background


def generate_pattern(params: dict, I0: float, d: float, phi: float,
                     sigma_b: Optional[float] = None,
                     x: Optional[np.ndarray] = None,
                     x_range: float = 5e-3, n_points: int = 1500) -> Tuple[np.ndarray, np.ndarray]:
    """Generate a complete double-slit interference pattern."""
    if x is None:
        x = np.linspace(-x_range, x_range, n_points)
    I = model_forward(x, I0, d, phi, sigma_b, params)
    return x, I


# ============================================================================
# Figure Drawing Function
# ============================================================================

def _apply_theme():
    plt.rcParams.update({
        "figure.facecolor": C("bg_main"),
        "axes.facecolor": C("bg_panel"),
        "axes.edgecolor": C("text_secondary"),
        "axes.labelcolor": C("text_primary"),
        "axes.titlecolor": C("text_primary"),
        "xtick.color": C("text_secondary"),
        "ytick.color": C("text_secondary"),
        "text.color": C("text_primary"),
        "grid.color": C("grid_color"),
        "grid.linewidth": 0.6,
        "font.family": "monospace",
    })


def _quality_label(V: float) -> Tuple[str, str]:
    if V > 0.90: return "EXCELLENT", C("accent_green")
    if V > 0.70: return "GOOD", C("accent_green")
    if V > 0.40: return "MODERATE", C("accent_orange")
    if V > 0.10: return "POOR", C("accent_red")
    return "LOST", C("accent_red")


def draw_figure(params: dict, I0: float, d: float, phi: float,
                sigma_b: Optional[float], x: np.ndarray, I: np.ndarray,
                figsize=(14, 10)) -> plt.Figure:
    """Draw the complete double-slit interference figure."""
    _apply_theme()
    fig = plt.figure(figsize=figsize, facecolor=C("bg_main"))
    fig.suptitle("DTQEM · Double-Slit Interference · V44.0",
                 fontsize=14, fontweight="bold", color=C("accent_blue"), y=0.98)

    x_mm = x * 1e3
    V_eff, info = compute_V_eff(d, params)

    # Grid layout: 2 rows (main pattern + diagnostics)
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.35,
                           height_ratios=[2.5, 1.5], left=0.08, right=0.97,
                           top=0.92, bottom=0.08)

    # ---- Main pattern ----
    ax_main = fig.add_subplot(gs[0, :])
    ax_main.set_facecolor(C("bg_panel"))
    ax_main.plot(x_mm, I, color=C("accent_blue"), lw=1.6, label="I(x)")
    ax_main.fill_between(x_mm, I, alpha=0.15, color=C("accent_blue"))

    # Envelopes
    lam, L, a = params["lambda_m"], params["L_m"], params["a_m"]
    sigma = sigma_b if sigma_b else 3e-3
    G = np.exp(-x**2 / (2 * sigma**2))
    u_diff = np.pi * a * x / (lam * L)
    diff = sinc_physical(u_diff)**2
    base = I0 * G * diff
    env_up = base * (1 + V_eff) + params["B0"]
    env_dn = base * (1 - V_eff) + params["B0"]
    ax_main.plot(x_mm, env_up, color=C("accent_green"), lw=0.8, ls="--", alpha=0.7)
    ax_main.plot(x_mm, env_dn, color=C("accent_green"), lw=0.8, ls="--", alpha=0.7)

    ax_main.set_xlabel("Position x [mm]", fontsize=11)
    ax_main.set_ylabel("Intensity [counts]", fontsize=11)
    ax_main.set_title(f"V_eff = {V_eff:.4f} | V_src = {info['V_source']:.4f} | "
                      f"V_env = {info['V_env']:.4f} | V_dtq = {info['V_dtqem']:.4f}",
                      fontsize=9)
    ax_main.grid(True, alpha=0.3)
    ax_main.spines["top"].set_visible(False)
    ax_main.spines["right"].set_visible(False)
    ax_main.legend(fontsize=9, facecolor=C("bg_slider"), edgecolor=C("text_secondary"))

    # ---- Visibility bar chart ----
    ax_bar = fig.add_subplot(gs[1, 0])
    ax_bar.set_facecolor(C("bg_panel"))
    labels = ["V_source", "V_env", "V_dtqem", "V_eff"]
    values = [info["V_source"], info["V_env"], info["V_dtqem"], info["V_eff"]]
    colors = [C("accent_green"), C("accent_orange"), C("accent_purple"), C("accent_blue")]
    bars = ax_bar.bar(labels, values, color=colors, edgecolor=C("bg_main"), lw=1.0, width=0.55)
    for bar, val in zip(bars, values):
        ax_bar.text(bar.get_x() + bar.get_width()/2, min(val + 0.03, 0.96),
                    f"{val:.4f}", ha="center", va="bottom", fontsize=9,
                    fontweight="bold", color=C("text_primary"))
    ax_bar.set_ylim(0, 1.15)
    ax_bar.set_ylabel("Visibility", fontsize=10)
    ax_bar.set_title("Visibility Decomposition", fontsize=11)
    ax_bar.grid(axis="y", alpha=0.3)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)

    # ---- Info panel ----
    ax_info = fig.add_subplot(gs[1, 1])
    ax_info.set_facecolor(C("bg_band"))
    ax_info.set_xticks([])
    ax_info.set_yticks([])
    for sp in ax_info.spines.values():
        sp.set_edgecolor(C("text_secondary"))
        sp.set_linewidth(0.5)

    qlabel, qcolor = _quality_label(V_eff)
    info_lines = [
        ("━━ PARTICLE ━━━━━━━━━━━━━", C("text_secondary")),
        (f" v = {params['velocity']:.3e} m/s", C("text_primary")),
        (f" β = {info['beta']:.6f}", C("accent_cyan")),
        (f" γ = {info['gamma_rel']:.6f}", C("accent_cyan")),
        ("━━ TIME SCALES ━━━━━━━━━━━", C("text_secondary")),
        (f" τ = {info['tau']:.3e} s", C("text_primary")),
        (f" Δτ = {info['delta_tau']:.3e} s", C("accent_purple")),
        (f" τ_c = {params['tau_c']:.3e} s", C("accent_purple")),
        ("━━ VISIBILITY ━━━━━━━━━━━", C("text_secondary")),
        (f" V_eff = {V_eff:.6f}", C("accent_blue")),
        (f" Status: [{qlabel}]", qcolor),
    ]

    for i, (txt, col) in enumerate(info_lines):
        ax_info.text(0.05, 0.95 - i * 0.072, txt, transform=ax_info.transAxes,
                     fontsize=8, color=col, fontfamily="monospace", va="top")

    plt.tight_layout()
    return fig


# ============================================================================
# ipywidgets Dashboard
# ============================================================================

class DoubleSlitDashboard:
    """DTQEM Double-Slit Forward Model Dashboard — V44.0"""

    DEFAULTS = {
        "lambda_m": 532e-9, "L_m": 1.0, "a_m": 50e-6, "d": 250e-6,
        "L_source": 0.5, "source_size": 10e-6, "velocity": 1e6,
        "gamma_phi": 1e10, "tau_c": 1e-15, "I0": 1500.0, "phi": 0.0,
        "sigma_b": 3e-3, "B0": 50.0, "B1": 0.0,
    }

    def __init__(self):
        self.params = dict(self.DEFAULTS)
        self.x = np.linspace(-5e-3, 5e-3, 1500)
        self._build_widgets()
        self._build_layout()

    def _fsl(self, desc, vmin, vmax, val, step, fmt=".3f", color="#58a6ff"):
        sl = widgets.FloatSlider(value=val, min=vmin, max=vmax, step=step,
                                 description="", continuous_update=False,
                                 readout=True, readout_format=fmt,
                                 layout=widgets.Layout(width="100%", height="26px"),
                                 style={"handle_color": color})
        lb = widgets.Label(value=desc, layout=widgets.Layout(width="100%"),
                           style={"font_size": "11px", "text_color": "#8b949e",
                                  "font_family": "monospace"})
        return sl, lb

    def _build_widgets(self):
        self.sl_d, self.lb_d = self._fsl("d [µm] slit sep", 50, 600,
                                          self.DEFAULTS["d"]*1e6, 5, ".1f", "#58a6ff")
        self.sl_lambda, self.lb_lambda = self._fsl("λ [nm] wavelength", 400, 750,
                                                   self.DEFAULTS["lambda_m"]*1e9, 1, ".0f", "#39d0d8")
        self.sl_L, self.lb_L = self._fsl("L [m] screen dist", 0.5, 3.0,
                                         self.DEFAULTS["L_m"], 0.05, ".2f", "#39d0d8")
        self.sl_phi, self.lb_phi = self._fsl("φ [rad] phase", -3.14, 3.14,
                                             self.DEFAULTS["phi"], 0.01, ".3f", "#d29922")
        self.sl_sigma_b, self.lb_sigma_b = self._fsl("σ_b [mm] envelope", 0.5, 15.0,
                                                     self.DEFAULTS["sigma_b"]*1e3, 0.1, ".1f", "#d29922")
        self.sl_I0, self.lb_I0 = self._fsl("I₀ [cts] peak", 100, 5000,
                                           self.DEFAULTS["I0"], 50, ".0f", "#3fb950")
        self.sl_log_tc, self.lb_log_tc = self._fsl("log₁₀(τ_c) [s] DTQEM", -18, -12,
                                                   np.log10(self.DEFAULTS["tau_c"]), 0.1, ".2f", "#bc8cff")
        self.sl_log_v, self.lb_log_v = self._fsl("log₁₀(v) [m/s] velocity", 3,
                                                 np.log10(0.9999*C_LIGHT),
                                                 np.log10(self.DEFAULTS["velocity"]), 0.05, ".3f", "#f85149")
        self.sl_log_gph, self.lb_log_gph = self._fsl("log₁₀(γ_φ) [Hz] env deco", 6, 15,
                                                     np.log10(self.DEFAULTS["gamma_phi"]), 0.1, ".1f", "#f85149")
        self.btn_reset = widgets.Button(description="⟳ Reset", button_style="warning",
                                        layout=widgets.Layout(width="130px", height="32px"))
        self.btn_export = widgets.Button(description="↓ Export PNG", button_style="success",
                                         layout=widgets.Layout(width="140px", height="32px"))
        self.btn_reset.on_click(self._reset)
        self.btn_export.on_click(self._export)
        self.out = widgets.Output()

    def _cell(self, lb, sl, w="24%"):
        return widgets.VBox([lb, sl], layout=widgets.Layout(width=w, padding="2px 6px",
                                                            border="1px solid #21262d"))

    def _build_layout(self):
        header = widgets.HTML(value='<div style="background:#0d1117;padding:8px 14px;border-bottom:2px solid #21262d;">'
                                    '<span style="font-size:16px;font-weight:bold;color:#58a6ff;font-family:monospace;">'
                                    'DTQEM · Double-Slit Interference · Forward Model · V44.0</span><br>'
                                    '<span style="font-size:11px;color:#8b949e;font-family:monospace;">'
                                    'V_eff = V_source × exp(-γφ·τ) × exp(-|Δτ|/τ_c) | Δτ = τ·(1-1/γ) | τ = a/v'
                                    '</span></div>', layout=widgets.Layout(width="100%"))
        ctrl_hdr = widgets.HTML(value='<div style="background:#13181f;padding:3px 10px;">'
                                      '<span style="font-size:11px;color:#8b949e;font-family:monospace;">'
                                      '━━ PARAMETER CONTROLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                                      '</span></div>', layout=widgets.Layout(width="100%"))
        row0 = widgets.HBox([self._cell(self.lb_d, self.sl_d), self._cell(self.lb_lambda, self.sl_lambda),
                             self._cell(self.lb_L, self.sl_L), self._cell(self.lb_phi, self.sl_phi)],
                            layout=widgets.Layout(width="100%", padding="3px 0px"))
        row1 = widgets.HBox([self._cell(self.lb_sigma_b, self.sl_sigma_b), self._cell(self.lb_I0, self.sl_I0),
                             self._cell(self.lb_log_tc, self.sl_log_tc), self._cell(self.lb_log_v, self.sl_log_v)],
                            layout=widgets.Layout(width="100%", padding="3px 0px"))
        row2 = widgets.HBox([self._cell(self.lb_log_gph, self.sl_log_gph),
                             widgets.VBox([widgets.HBox([self.btn_reset, self.btn_export])],
                                          layout=widgets.Layout(width="24%")),
                             widgets.VBox([], layout=widgets.Layout(width="24%")),
                             widgets.VBox([], layout=widgets.Layout(width="24%"))],
                            layout=widgets.Layout(width="100%", padding="3px 0px"))
        sep = widgets.HTML(value='<hr style="border:none;border-top:1px solid #21262d;margin:4px 0;"/>'
                                 '<div style="background:#0d1117;padding:2px 10px;">'
                                 '<span style="font-size:10px;color:#8b949e;font-family:monospace;">'
                                 '━━ VISUALIZATION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
                                 '</span></div>', layout=widgets.Layout(width="100%"))
        self.dashboard = widgets.VBox([header, ctrl_hdr, row0, row1, row2, sep, self.out],
                                      layout=widgets.Layout(width="100%", background="#0d1117",
                                                            border="1px solid #21262d"))
        for sl in [self.sl_d, self.sl_lambda, self.sl_L, self.sl_phi, self.sl_sigma_b,
                   self.sl_I0, self.sl_log_tc, self.sl_log_v, self.sl_log_gph]:
            sl.observe(self._update, names="value")
        self._update()

    def _read(self):
        self.params["d"] = self.sl_d.value * 1e-6
        self.params["lambda_m"] = self.sl_lambda.value * 1e-9
        self.params["L_m"] = self.sl_L.value
        self.params["phi"] = self.sl_phi.value
        self.params["sigma_b"] = self.sl_sigma_b.value * 1e-3
        self.params["I0"] = self.sl_I0.value
        self.params["tau_c"] = 10.0 ** self.sl_log_tc.value
        self.params["velocity"] = 10.0 ** self.sl_log_v.value
        self.params["gamma_phi"] = 10.0 ** self.sl_log_gph.value

    def _update(self, change=None):
        self._read()
        x, I = generate_pattern(self.params, self.params["I0"], self.params["d"],
                                 self.params["phi"], self.params["sigma_b"])
        fig = draw_figure(self.params, self.params["I0"], self.params["d"],
                          self.params["phi"], self.params["sigma_b"], x, I)
        with self.out:
            clear_output(wait=True)
            display(fig)
            plt.close(fig)

    def _reset(self, _):
        self.sl_d.value = self.DEFAULTS["d"] * 1e6
        self.sl_lambda.value = self.DEFAULTS["lambda_m"] * 1e9
        self.sl_L.value = self.DEFAULTS["L_m"]
        self.sl_phi.value = self.DEFAULTS["phi"]
        self.sl_sigma_b.value = self.DEFAULTS["sigma_b"] * 1e3
        self.sl_I0.value = self.DEFAULTS["I0"]
        self.sl_log_tc.value = np.log10(self.DEFAULTS["tau_c"])
        self.sl_log_v.value = np.log10(self.DEFAULTS["velocity"])
        self.sl_log_gph.value = np.log10(self.DEFAULTS["gamma_phi"])

    def _export(self, _):
        self._read()
        x, I = generate_pattern(self.params, self.params["I0"], self.params["d"],
                                 self.params["phi"], self.params["sigma_b"])
        fig = draw_figure(self.params, self.params["I0"], self.params["d"],
                          self.params["phi"], self.params["sigma_b"], x, I, figsize=(16, 11))
        fname = "dtqem_double_slit_forward_v44_export.png"
        fig.savefig(fname, dpi=180, bbox_inches="tight", facecolor=C("bg_main"))
        plt.close(fig)
        print(f"[DTQEM Double Slit V44.0] Saved → {fname}")

    def show(self):
        display(self.dashboard)


# ============================================================================
# Entry Point
# ============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  DTQEM Double-Slit Forward Model — V44.0")
    print("  ipywidgets | dark theme | zero overlap")
    print("=" * 60)
    print("\n  V_eff = V_source × exp(-γφ·τ) × exp(-|Δτ|/τ_c)")
    print("  Δτ = τ·(1-1/γ) | τ = a/v | γ = 1/√(1-β²)")
    print()
    dash = DoubleSlitDashboard()
    dash.show()
