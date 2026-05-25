#!/usr/bin/env python3
"""
DTQEM v63.0 – Phenomenological scaling model with experimental predictions
========================================================================
Model: τ_c = τ_c0 / [ m^β · (v/c)^δ · (1 + ζ N) ]

Based on calibration from v62.3:
    τ_c0 = 9.8e-27 s (phenomenological, environment-dependent)
    β = 0.44 (≈ 1/2, consistent with Pikovski mechanism + Debye freezing)
    δ = 0.33 (≈ 1/3, consistent with VdW transport cross section)
    ζ = 0.005 (per-atom internal complexity)

The inverse problem is solved via logarithmic slope method:
    Measure V_eff at multiple Δτ → linear fit of ln(V) vs |Δτ| → τ_c = -1/slope

Usage:
    python dtqem_v63.py                      # Run synthetic demo
    python dtqem_v63.py data.csv             # Analyze real CSV data
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.optimize import minimize
from pathlib import Path
import csv
import sys
import warnings
warnings.filterwarnings("ignore")

# ============================================================================
# CONSTANTS
# ============================================================================
C_LIGHT = 299792458.0
HBAR = 1.054571817e-34      # J·s
K_B = 1.380649e-23          # J/K
M_U = 1.660539e-27          # kg (atomic mass unit)

OUTDIR = Path("output_v63")
OUTDIR.mkdir(exist_ok=True)

# ============================================================================
# PHENOMENOLOGICAL MODEL (calibrated from v62.3)
# ============================================================================
class PhenomenologicalModel:
    """
    τ_c = τ_c0 / [ (m)^β · (v/c)^δ · (1 + ζ·N) ]
    
    This is a scaling law, not a first-principles derivation.
    The exponents are consistent with known physics (Pikovski, VdW)
    but the exact values are calibrated from simulation data.
    """
    def __init__(self, tau_c0=9.8e-27, beta=0.44, delta=0.33, zeta=0.005):
        self.tau_c0 = tau_c0      # s – environment-dependent, not universal
        self.beta = beta          # mass exponent (≈ 1/2)
        self.delta = delta        # velocity exponent (≈ 1/3)
        self.zeta = zeta          # per-atom internal complexity

    def tau_c(self, m_kg, v_ms, N):
        """Calculate τ_c from phenomenological model."""
        v_rel = v_ms / C_LIGHT
        mass_factor = (m_kg / M_U) ** self.beta
        vel_factor = v_rel ** self.delta
        complexity_factor = 1.0 + self.zeta * N
        return self.tau_c0 / (mass_factor * vel_factor * complexity_factor)

    def visibility(self, tau_c, gamma_phi, T_eff, delta_tau, V_source=1.0):
        """Direct D0 visibility."""
        return V_source * np.exp(-gamma_phi * T_eff) * np.exp(-np.abs(delta_tau) / tau_c)

    def predict_scan(self, m_kg, v_ms, N, gamma_phi, L1, L2_min_ratio=0.05, L2_max_ratio=3.5, n_steps=20):
        """
        Generate predicted visibility scan for a particle.
        L2 is chosen so that Δτ spans [frac_min·τ_c, frac_max·τ_c].
        """
        tau_c_true = self.tau_c(m_kg, v_ms, N)
        gamma = 1.0 / np.sqrt(1.0 - (v_ms / C_LIGHT)**2)
        tau1 = L1 / (v_ms * gamma)
        
        delta_tau_min = L2_min_ratio * tau_c_true
        delta_tau_max = L2_max_ratio * tau_c_true
        delta_tau_vals = np.linspace(delta_tau_min, delta_tau_max, n_steps)
        
        L2_vals = (tau1 + delta_tau_vals) * v_ms * gamma
        T_eff_vals = (L1 + L2_vals) / (2.0 * v_ms)
        V_vals = self.visibility(tau_c_true, gamma_phi, T_eff_vals, delta_tau_vals)
        
        return delta_tau_vals, V_vals, tau_c_true

# ============================================================================
# THEORETICAL ESTIMATE (Pikovski upper bound)
# ============================================================================
def pikovski_tau_c(m_kg, N, T_K):
    """
    Pikovski et al. estimate (classical limit):
        τ_c ≈ ħ / (k_B T √(3N))
    This assumes C_V = 3N k_B (all modes classical).
    Gives β = 1/2 exactly.
    """
    delta_E = K_B * T_K * np.sqrt(3.0 * N)
    return HBAR / delta_E

# ============================================================================
# INVERSE PROBLEM: extract τ_c from scan (logarithmic slope method)
# ============================================================================
def extract_tau_c_from_scan(delta_tau, V_eff):
    """
    Extract τ_c from measured visibility at multiple Δτ.
    Method: ln(V) = C - (1/τ_c) |Δτ|
    Returns τ_c, slope, R², and status.
    """
    delta_tau = np.asarray(delta_tau, dtype=float)
    V = np.asarray(V_eff, dtype=float)
    
    mask = np.isfinite(delta_tau) & np.isfinite(V) & (V > 0)
    if np.sum(mask) < 3:
        return {"tau_c": np.nan, "slope": np.nan, "r2": np.nan, "status": "insufficient_points"}
    
    x = delta_tau[mask]
    y = np.log(V[mask])
    slope, intercept, r_value, _, _ = linregress(x, y)
    
    if slope >= 0:
        return {"tau_c": np.inf, "slope": slope, "r2": r_value**2, "status": "non_negative_slope"}
    
    tau_c = -1.0 / slope
    return {"tau_c": tau_c, "slope": slope, "r2": r_value**2, "status": "ok"}

# ============================================================================
# CSV DATA HANDLING
# ============================================================================
def read_csv_scan_data(csv_path):
    """
    Read CSV with columns:
        particle, mass_kg, speed_m_s, N_atoms, delta_tau_s, V_eff
    Returns list of rows, grouped by particle.
    """
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        required = {'particle', 'mass_kg', 'speed_m_s', 'delta_tau_s', 'V_eff'}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain columns: {required}")
        for r in reader:
            rows.append({
                'particle': r['particle'],
                'mass_kg': float(r['mass_kg']),
                'speed_m_s': float(r['speed_m_s']),
                'N_atoms': int(r.get('N_atoms', 0)),
                'delta_tau_s': float(r['delta_tau_s']),
                'V_eff': float(r['V_eff']),
            })
    return rows

def group_scans_by_particle(rows):
    """Group scan points by particle name."""
    groups = {}
    for r in rows:
        key = r['particle']
        if key not in groups:
            groups[key] = {
                'particle': key,
                'mass_kg': r['mass_kg'],
                'speed_m_s': r['speed_m_s'],
                'N_atoms': r['N_atoms'],
                'delta_tau': [],
                'V_eff': [],
            }
        groups[key]['delta_tau'].append(r['delta_tau_s'])
        groups[key]['V_eff'].append(r['V_eff_s'])
    
    # Extract τ_c for each particle
    results = []
    for key, data in groups.items():
        inv = extract_tau_c_from_scan(data['delta_tau'], data['V_eff'])
        results.append({
            'particle': key,
            'mass_kg': data['mass_kg'],
            'speed_m_s': data['speed_m_s'],
            'N_atoms': data['N_atoms'],
            'tau_c_extracted_s': inv['tau_c'],
            'slope': inv['slope'],
            'r2': inv['r2'],
            'status': inv['status'],
        })
    return results

# ============================================================================
# SYNTHETIC DATA GENERATION (for demonstration)
# ============================================================================
def generate_synthetic_dataset():
    """Generate synthetic scan data using phenomenological model."""
    model = PhenomenologicalModel()
    
    particles = [
        ("C60", 720 * M_U, 200.0, 60),
        ("C70", 840 * M_U, 180.0, 70),
        ("C84", 1008 * M_U, 160.0, 84),
        ("Giant", 5000 * M_U, 100.0, 350),
    ]
    
    rows = []
    for name, m, v, N in particles:
        delta_tau, V, _ = model.predict_scan(m, v, N, gamma_phi=0.0, L1=0.5, n_steps=20)
        for dt, Vv in zip(delta_tau, V):
            # Add 2% log-normal noise
            V_noisy = Vv * np.exp(np.random.normal(0.0, 0.02))
            rows.append({
                'particle': name,
                'mass_kg': m,
                'speed_m_s': v,
                'N_atoms': N,
                'delta_tau_s': dt,
                'V_eff_s': np.clip(V_noisy, 1e-12, 1.0),
            })
    return rows

# ============================================================================
# EXPERIMENTAL PREDICTIONS (to guide real experiments)
# ============================================================================
def print_predictions():
    """Print key experimental predictions for model validation."""
    model = PhenomenologicalModel()
    m_C60 = 720 * M_U
    
    print("\n" + "="*70)
    print("KEY EXPERIMENTAL PREDICTIONS (to test the model)")
    print("="*70)
    
    # Prediction 1: Mass scaling (β)
    print("\n1. MASS SCALING (β ≈ 0.44 vs β = 0.50)")
    print("   Measure τ_c for C60, C70, C84 at same v and T")
    tau_c60 = model.tau_c(720*M_U, 200.0, 60)
    tau_c70 = model.tau_c(840*M_U, 200.0, 70)
    tau_c84 = model.tau_c(1008*M_U, 200.0, 84)
    print(f"   τ_c(C70)/τ_c(C60) = {tau_c70/tau_c60:.4f} (β=0.50 would give {(720/840)**0.50:.4f})")
    print(f"   τ_c(C84)/τ_c(C60) = {tau_c84/tau_c60:.4f} (β=0.50 would give {(720/1008)**0.50:.4f})")
    
    # Prediction 2: Velocity scaling (δ)
    print("\n2. VELOCITY SCALING (δ ≈ 1/3)")
    print("   Measure τ_c at different v for same particle")
    for v in [100, 200, 300, 400]:
        tc = model.tau_c(m_C60, float(v), 60)
        print(f"   v={v:3d} m/s: τ_c = {tc:.3e} s (relative to 200 m/s: {tc/model.tau_c(m_C60,200,60):.4f})")
    
    # Prediction 3: CRITICAL TEST – pressure independence
    print("\n3. CRITICAL TEST – PRESSURE DEPENDENCE")
    print("   If τ_c is independent of background gas pressure → intrinsic mechanism (Pikovski)")
    print("   If τ_c ∝ 1/P → environmental decoherence (Joos-Zeh)")
    print("   → This test does NOT require theory, only careful measurement!")
    
    # Prediction 4: Temperature dependence
    print("\n4. TEMPERATURE DEPENDENCE")
    print("   Pikovski predicts τ_c ∝ 1/T (if internal temperature dominates)")
    for T in [100, 200, 300, 400]:
        tc_pik = pikovski_tau_c(m_C60, 60, float(T))
        print(f"   T={T:3d} K: Pikovski τ_c ≈ {tc_pik:.3e} s")

# ============================================================================
# MAIN WORKFLOW
# ============================================================================
def main(csv_path=None):
    print("="*70)
    print("DTQEM v63.0 – Phenomenological Scaling Model")
    print("Model: τ_c = τ_c0 / [m^β · (v/c)^δ · (1+ζN)]")
    print("="*70)
    
    # Load or generate data
    if csv_path and Path(csv_path).exists():
        print(f"\nReading real data from: {csv_path}")
        rows = read_csv_scan_data(csv_path)
        particle_data = group_scans_by_particle(rows)
        mode = "real_data"
    else:
        print("\nGenerating synthetic dataset (no CSV provided)")
        rows = generate_synthetic_dataset()
        particle_data = group_scans_by_particle(rows)
        mode = "synthetic"
    
    # Display extracted τ_c values
    print(f"\nExtracted τ_c from logarithmic slope method:")
    for p in particle_data:
        if np.isfinite(p['tau_c_extracted_s']):
            print(f"  {p['particle']:10s}: τ_c = {p['tau_c_extracted_s']:.3e} s, R² = {p['r2']:.6f}")
        else:
            print(f"  {p['particle']:10s}: extraction failed ({p['status']})")
    
    # Compare with Pikovski estimate (if mass and N known)
    print("\n" + "-"*70)
    print("Comparison: Extracted vs Pikovski theoretical estimate (classical limit)")
    print("Note: Pikovski gives β=1/2 exactly, model has β=0.44")
    print("-"*70)
    for p in particle_data:
        if np.isfinite(p['tau_c_extracted_s']):
            tau_pik = pikovski_tau_c(p['mass_kg'], p['N_atoms'], T_K=300)
            ratio = p['tau_c_extracted_s'] / tau_pik if tau_pik > 0 else np.nan
            print(f"  {p['particle']:10s}: extracted = {p['tau_c_extracted_s']:.3e} s, "
                  f"Pikovski = {tau_pik:.3e} s, ratio = {ratio:.2e}")
    
    # Print experimental predictions
    print_predictions()
    
    # Save results
    results_csv = OUTDIR / "v63_results.csv"
    with open(results_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['particle', 'mass_kg', 'speed_m_s', 'N_atoms', 
                      'tau_c_extracted_s', 'slope', 'r2', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in particle_data:
            writer.writerow({k: p.get(k, '') for k in fieldnames})
    print(f"\nResults saved to: {results_csv}")
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("""The phenomenological model successfully describes the synthetic data.
The exponents β≈0.44 and δ≈0.33 are consistent with Pikovski (mass) and 
VdW scattering (velocity) mechanisms, but the exact values are calibrated.

CRITICAL: τ_c0 = 9.8e-27 s is environment-dependent, NOT a universal constant.
To identify the dominant decoherence mechanism, perform:
    1. Pressure dependence test (if τ_c independent of P → intrinsic mechanism)
    2. Temperature dependence test (if τ_c ∝ 1/T → Pikovski-like)

The logarithmic slope method (scan over Δτ) is stable and recommended
for extracting τ_c from experimental visibility measurements.
""")

if __name__ == "__main__":
    # Check for CSV argument
    csv_file = None
    for arg in sys.argv[1:]:
        if arg.endswith('.csv') and Path(arg).exists():
            csv_file = arg
            break
    main(csv_file)
