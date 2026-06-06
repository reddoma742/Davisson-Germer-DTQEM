#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DTQEM Figures 1 & 2 - CORRECTED VERSION
Fixes:
- Added plt.show() for inline display in Jupyter/Colab
- Fixed figure closing before display
- Improved layout
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

# =========================================================
# إعداد matplotlib
# =========================================================
try:
    get_ipython()
    matplotlib.use('inline')
except:
    pass

plt.rcParams.update({
    'font.family'    : 'serif',
    'font.size'      : 11,
    'axes.linewidth' : 1.2,
    'figure.dpi'     : 120,
})

# =========================================================
# Figure 1: Lorentzian Curve
# =========================================================
def generate_figure1(
    output_path="figure1.png",
    show=True
):
    """
    Figure 1: Lorentzian spectral line shape
    of path-decoherence coefficient a(omega_c).
    """

    print("\n" + "=" * 60)
    print("Generating Figure 1: Lorentzian Peak...")
    print("=" * 60)

    # Parameters
    omega_path = 5.0
    gamma      = 1.0
    eta        = 1.6968

    # Frequency range
    omega_c = np.linspace(1.0, 9.0, 500)

    # Lorentzian
    a_omega = (
        (eta / gamma)
        /
        (
            1.0
            + ((omega_c - omega_path) / gamma) ** 2
        )
    )

    peak_value = eta / gamma

    print(f"   omega_path = {omega_path} GHz")
    print(f"   gamma      = {gamma} GHz")
    print(f"   eta        = {eta}")
    print(f"   Peak value = {peak_value:.4f}")

    # =====================================================
    # Figure
    # =====================================================
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.plot(
        omega_c,
        a_omega,
        color='darkblue',
        linewidth=2.0,
        label=r'Analytical $a(\omega_c, T)$'
    )

    ax.axvline(
        x=omega_path,
        color='red',
        linestyle='--',
        linewidth=1.5,
        label=r'$\omega_{\mathrm{path}} = 5.0$ GHz'
    )

    ax.scatter(
        [omega_path],
        [peak_value],
        color='red',
        s=80,
        zorder=5,
        label=f'Peak = {peak_value:.4f}'
    )

    # Fill under curve
    ax.fill_between(
        omega_c,
        a_omega,
        alpha=0.12,
        color='darkblue'
    )

    ax.set_title(
        r'Detector Path-Decoherence Spectral Line Shape $a(\omega_c)$',
        fontsize=12,
        pad=12,
        fontweight='bold'
    )

    ax.set_xlabel(
        r'Detector Coupling Frequency $\omega_c$ (GHz)',
        fontsize=11
    )

    ax.set_ylabel(
        r'Path Decoherence Coefficient $a(\omega_c)$',
        fontsize=11
    )

    ax.grid(
        True,
        linestyle=':',
        alpha=0.6
    )

    ax.legend(
        loc='upper right',
        frameon=True,
        fancybox=False,
        edgecolor='black',
        fontsize=10
    )

    ax.set_xlim(1.0, 9.0)
    ax.set_ylim(0, peak_value * 1.15)

    plt.tight_layout()

    # Save
    out = Path(output_path)
    fig.savefig(
        out,
        dpi=300,
        bbox_inches='tight',
        facecolor='white'
    )
    print(f"\n✅ Figure 1 saved: {out.resolve()}")

    # Show inline
    if show:
        plt.show()

    plt.close(fig)

    return str(out.resolve())

# =========================================================
# Figure 2: AICc Model Selection
# =========================================================
def generate_figure2(
    output_path="figure2.png",
    show=True
):
    """
    Figure 2: AICc model selection probability
    vs sample size N.
    Threshold at N=36.
    """

    print("\n" + "=" * 60)
    print("Generating Figure 2: AICc Threshold...")
    print("=" * 60)

    # Data
    N = np.array([
        8, 16, 24, 32, 36, 50, 80
    ])

    v17_prob = np.array([
        89.0, 57.0, 43.0,
        33.0, 21.0, 10.0, 5.0
    ])

    v18_prob = np.array([
        11.0, 43.0, 57.0,
        67.0, 79.0, 90.0, 95.0
    ])

    print(f"\n{'N':<6} {'v17(%)':>10} {'v18(%)':>10}")
    print("-" * 28)
    for n, p17, p18 in zip(N, v17_prob, v18_prob):
        print(f"{n:<6} {p17:>10.1f} {p18:>10.1f}")

    # =====================================================
    # Figure
    # =====================================================
    fig, ax = plt.subplots(figsize=(7, 5))

    # v17 model
    ax.plot(
        N, v17_prob,
        'o--',
        color='crimson',
        linewidth=1.8,
        markersize=8,
        label='Baseline Model v17.0-C ($c=0$)'
    )

    # v18 model
    ax.plot(
        N, v18_prob,
        's-',
        color='darkblue',
        linewidth=2.0,
        markersize=8,
        label='Joint Model v18.0-C ($c=0.5$)'
    )

    # Threshold line
    ax.axvline(
        x=36,
        color='forestgreen',
        linestyle=':',
        linewidth=2.0,
        label='Threshold $N=36$'
    )

    # Threshold annotation
    ax.annotate(
        r'Reliability Threshold $N \geq 36$',
        xy=(36, 79),
        xytext=(40, 65),
        fontsize=10,
        fontweight='bold',
        color='forestgreen',
        arrowprops=dict(
            arrowstyle='->',
            color='forestgreen',
            lw=1.5
        )
    )

    # Shaded region
    ax.axvspan(
        36, 85,
        alpha=0.07,
        color='forestgreen',
        label='Reliable region'
    )

    ax.set_title(
        'AICc Model Selection Probability vs. Sample Size $N$',
        fontsize=12,
        pad=12,
        fontweight='bold'
    )

    ax.set_xlabel(
        'Sample Size $N$ (Measurement Points)',
        fontsize=11
    )

    ax.set_ylabel(
        'Selection Probability (%)',
        fontsize=11
    )

    ax.set_xlim(5, 85)
    ax.set_ylim(-5, 105)

    ax.grid(
        True,
        linestyle=':',
        alpha=0.6
    )

    ax.legend(
        loc='center right',
        frameon=True,
        fancybox=False,
        edgecolor='black',
        fontsize=10
    )

    plt.tight_layout()

    # Save
    out = Path(output_path)
    fig.savefig(
        out,
        dpi=300,
        bbox_inches='tight',
        facecolor='white'
    )
    print(f"\n✅ Figure 2 saved: {out.resolve()}")

    # Show inline
    if show:
        plt.show()

    plt.close(fig)

    return str(out.resolve())

# =========================================================
# Main
# =========================================================
print("=" * 60)
print("DTQEM Figures 1 & 2 — CORRECTED VERSION")
print("=" * 60)

path1 = generate_figure1(
    output_path="figure1.png",
    show=True
)

path2 = generate_figure2(
    output_path="figure2.png",
    show=True
)

print("\n" + "=" * 60)
print("✅ All figures generated successfully!")
print(f"   figure1.png → {path1}")
print(f"   figure2.png → {path2}")
print("\n📝 Acknowledgment:")
print("   - DeepSeek")
print("   - Claude (Anthropic)")
print("   - Arena AI")
print("   Human supervision: Reddouane Berramdane")
print("=" * 60)
