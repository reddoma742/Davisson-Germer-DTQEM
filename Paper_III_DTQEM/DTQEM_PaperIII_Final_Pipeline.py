
# -*- coding: utf-8 -*-
"""
DTQEM Paper III — Final Publication-Ready Pipeline (with Auto-Download)
======================================================================
- Spectral statistics (lag-1, Brody MLE, Gap Ratio, Bootstrap CIs)
- Raman pair analysis (full spectrum, dual null models, FDR correction)
- Linewidth scan, target scan
- Publication-quality figures
- Automatic download of results (ZIP + individual files)

Usage:
    python dtqem_paper3_final.py

Output:
    ../outputs/  (CSV files, PNG figures, DTQEM_PaperIII_Results.zip)
    The script automatically downloads the ZIP file (and individual files
    if run in Google Colab) to your local machine.
"""

import os
import warnings
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import pearsonr
from scipy.interpolate import UnivariateSpline
from scipy.optimize import minimize_scalar
from scipy.special import gamma

warnings.filterwarnings("ignore")
plt.rcParams.update({"font.size": 11, "figure.dpi": 300})

# ============================================================
# CONFIGURATION
# ============================================================
RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)

DATA_DIR = "../data"
OUTPUT_DIR = "../outputs"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

N_BOOTSTRAP = 300
BOOT_MIN_VALID = 80
SUBSAMPLE_N = 20
SUBSAMPLE_TRIALS = 300
N_MONTE_CARLO = 5000
CONT_BASELINE_POINTS = 4000
CONT_BASELINE_TRIALS = 12
EPS = 1e-15

GHZ_TO_CM = 0.03335641
NV_SPIN_GHZ = 2.87
TARGET_SPIN_CM = NV_SPIN_GHZ * GHZ_TO_CM
SELECTED_TOLERANCE = 0.1
GAMMA_VALUES = np.logspace(-4, 0, 24)
TARGET_SCAN_VALUES = np.linspace(0.0, 5.0, 200)
TARGET_SCAN_GAMMA = SELECTED_TOLERANCE

SYSTEM_METADATA = {
    "Fe I (NIST)": {"type": "atomic", "source": "NIST ASD", "merge_threshold": 1.0, "min_gap": 0.5, "s_factor": 0.20},
    "Fe II (NIST)": {"type": "atomic", "source": "NIST ASD", "merge_threshold": 1.0, "min_gap": 0.5, "s_factor": 0.20},
    "N I (NIST)": {"type": "atomic", "source": "NIST ASD", "merge_threshold": 1.0, "min_gap": 0.5, "s_factor": 0.20},
    "NV (Doherty+)": {"type": "defect", "source": "Doherty et al.", "merge_threshold": 0.5, "min_gap": 0.1, "s_factor": 0.15},
    "SiV (Doherty+)": {"type": "defect", "source": "Doherty et al.", "merge_threshold": 0.5, "min_gap": 0.1, "s_factor": 0.15},
    "GeV (Doherty+)": {"type": "defect", "source": "Doherty et al.", "merge_threshold": 0.5, "min_gap": 0.1, "s_factor": 0.20},
}

SYSTEMS_LINKS = {
    "Fe I (NIST)": "https://drive.google.com/file/d/1TuUFUyVce8UsabR-ic2VukwIFl3pYP8L/view",
    "Fe II (NIST)": "https://drive.google.com/file/d/1XMDC9PYXNwnEeqEUhZY7Rzi5VHOwRAsC/view",
    "N I (NIST)": "https://drive.google.com/file/d/1TnPqWJjB-GPzw_rw-mZ1xNEBm2WY9nez/view",
    "NV (Doherty+)": "https://drive.google.com/file/d/1Xnr-ZssaUk383ipAVTsKXbpboOohAdgU/view",
    "SiV (Doherty+)": "https://drive.google.com/file/d/1GWd8FM2OvZmyg3uR4Zsx-Q-u20SMTN6J/view",
    "GeV (Doherty+)": "https://drive.google.com/file/d/1hM2sRgccgT5t4BIWNnjAtt8n75EUAwdb/view",
}

# ============================================================
# DATA LOADING
# ============================================================
def extract_gdrive_id(url):
    if "/d/" in url:
        return url.split("/d/")[1].split("/")[0]
    if "id=" in url:
        return url.split("id=")[1].split("&")[0]
    raise ValueError(f"Could not parse Google Drive ID: {url}")


def load_from_drive(share_link, local_filename):
    local_path = os.path.join(DATA_DIR, local_filename)
    if not os.path.exists(local_path):
        file_id = extract_gdrive_id(share_link)
        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(direct_url, timeout=60)
        response.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(response.content)

    df = pd.read_csv(local_path)
    chosen_col = None
    for col in df.columns:
        c = col.lower()
        if ("energy" in c) or ("level" in c):
            chosen_col = col
            break
    if chosen_col is None:
        chosen_col = df.columns[0]

    levels = pd.to_numeric(df[chosen_col], errors="coerce").dropna().values
    levels = np.sort(np.unique(levels[levels > 0]))
    return levels

# ============================================================
# SPECTRAL STATISTICS
# ============================================================
def merge_levels(levels, threshold):
    levels = np.sort(np.unique(np.asarray(levels, dtype=float)))
    if len(levels) == 0:
        return levels
    merged = [levels[0]]
    for x in levels[1:]:
        if x - merged[-1] > threshold:
            merged.append(x)
    return np.array(merged)


def compute_gaps(levels, min_gap):
    gaps = np.diff(np.sort(np.unique(np.asarray(levels, dtype=float))))
    return gaps[gaps > min_gap]


def lag1_autocorr(arr):
    arr = np.asarray(arr, dtype=float)
    arr = arr[np.isfinite(arr)]
    if len(arr) < 3:
        return np.nan
    try:
        return pearsonr(arr[:-1], arr[1:])[0]
    except Exception:
        return np.nan


def unfold_levels(levels, s_factor):
    E = np.sort(np.unique(np.asarray(levels, dtype=float)))
    n = len(E)
    if n < 10:
        return E.copy()
    N = np.arange(1, n + 1)
    spline = UnivariateSpline(E, N, s=s_factor * n, k=3)
    return np.maximum.accumulate(spline(E))


def normalized_spacings(unfolded):
    s = np.diff(np.asarray(unfolded, dtype=float))
    s = s[np.isfinite(s) & (s > 1e-8)]
    return s / np.mean(s) if len(s) > 0 else s


def brody_negloglik(q, s):
    if q <= 0 or q >= 1:
        return np.inf
    b = gamma((q + 2) / (q + 1)) ** (q + 1)
    pdf = (q + 1) * b * (s ** q) * np.exp(-b * s ** (q + 1))
    return -np.sum(np.log(np.clip(pdf, 1e-300, None)))


def brody_parameter(spacings):
    s = np.asarray(spacings, dtype=float)
    s = s[np.isfinite(s) & (s > 0)]
    if len(s) < 20:
        return np.nan
    res = minimize_scalar(lambda q: brody_negloglik(q, s), bounds=(1e-4, 0.999), method="bounded")
    return res.x if res.success else np.nan


def adjacent_gap_ratio_from_raw_gaps(gaps):
    g = np.asarray(gaps, dtype=float)
    g = g[np.isfinite(g) & (g > 0)]
    if len(g) < 3:
        return np.nan
    r = np.minimum(g[:-1], g[1:]) / np.maximum(g[:-1], g[1:])
    return float(np.mean(r))


def gap_ratio_interp(r):
    if not np.isfinite(r):
        return "N/A"
    if r < 0.42:
        return "Poisson-like / weakly correlated"
    if r < 0.58:
        return "Intermediate / GOE-like"
    return "Rigid / picket-fence-like"


def sample_warning(n_levels_merged):
    if n_levels_merged < 50:
        return "Small-sample caution"
    if n_levels_merged < 100:
        return "Moderate-sample caution"
    return ""


def choose_block_length(n):
    b = int(round(2 * n ** (1 / 3)))
    return int(max(5, min(b, max(5, n // 4))))


def moving_block_bootstrap_gaps(gaps, block_size, rng_local):
    n = len(gaps)
    if n <= block_size:
        return gaps.copy()
    starts = np.arange(0, n - block_size + 1)
    sampled = []
    while len(sampled) < n:
        s = rng_local.choice(starts)
        sampled.extend(gaps[s:s + block_size])
    return np.array(sampled[:n])


def ci_from_values(vals):
    vals = np.asarray(vals, dtype=float)
    vals = vals[np.isfinite(vals)]
    if len(vals) < BOOT_MIN_VALID:
        return np.nan, np.nan, np.nan
    return float(np.mean(vals)), float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def nan_bootstrap_schema():
    return {
        "lag1_raw_boot_mean": np.nan, "lag1_raw_ci_low": np.nan, "lag1_raw_ci_high": np.nan,
        "Brody_q_boot_mean": np.nan, "Brody_q_ci_low": np.nan, "Brody_q_ci_high": np.nan,
        "Gap_Ratio_boot_mean": np.nan, "Gap_Ratio_ci_low": np.nan, "Gap_Ratio_ci_high": np.nan,
    }


def bootstrap_metric_intervals(levels, meta):
    merged = merge_levels(levels, meta["merge_threshold"])
    gaps = compute_gaps(merged, meta["min_gap"])
    if len(gaps) < 30:
        return nan_bootstrap_schema()

    block_size = choose_block_length(len(gaps))
    rng_local = np.random.default_rng(RANDOM_SEED)
    lag1_vals, brody_vals, gapr_vals = [], [], []

    for _ in range(N_BOOTSTRAP):
        try:
            boot_gaps = moving_block_bootstrap_gaps(gaps, block_size, rng_local)
            boot_levels = np.cumsum(np.concatenate([[merged[0]], boot_gaps]))
            unfolded = unfold_levels(boot_levels, meta["s_factor"])
            spacings = normalized_spacings(unfolded)
            lag1_vals.append(lag1_autocorr(boot_gaps))
            brody_vals.append(brody_parameter(spacings))
            gapr_vals.append(adjacent_gap_ratio_from_raw_gaps(boot_gaps))
        except Exception:
            continue

    m1, l1, h1 = ci_from_values(lag1_vals)
    m2, l2, h2 = ci_from_values(brody_vals)
    m3, l3, h3 = ci_from_values(gapr_vals)
    return {
        "lag1_raw_boot_mean": m1, "lag1_raw_ci_low": l1, "lag1_raw_ci_high": h1,
        "Brody_q_boot_mean": m2, "Brody_q_ci_low": l2, "Brody_q_ci_high": h2,
        "Gap_Ratio_boot_mean": m3, "Gap_Ratio_ci_low": l3, "Gap_Ratio_ci_high": h3,
    }


def analyze_spectral_system(levels, name, meta):
    merged = merge_levels(levels, meta["merge_threshold"])
    gaps = compute_gaps(merged, meta["min_gap"])
    if len(gaps) < 10:
        return None

    unfolded = unfold_levels(merged, meta["s_factor"])
    spacings = normalized_spacings(unfolded)
    gapr = adjacent_gap_ratio_from_raw_gaps(gaps)

    row = {
        "System": name,
        "Type": meta["type"],
        "Source": meta["source"],
        "N_levels_raw": len(levels),
        "N_levels_merged": len(merged),
        "lag1_raw": lag1_autocorr(gaps),
        "lag1_unfolded": lag1_autocorr(spacings),
        "Brody_q": brody_parameter(spacings),
        "Gap_Ratio_Raw": gapr,
        "Gap_Ratio_Interp": gap_ratio_interp(gapr),
        "Sample_Warning": sample_warning(len(merged)),
    }
    row.update(bootstrap_metric_intervals(levels, meta))
    return row

# ============================================================
# RAMAN ANALYSIS
# ============================================================
def pair_diffs(levels):
    levels = np.sort(np.unique(np.asarray(levels, dtype=float)))
    n = len(levels)
    if n < 2:
        return np.array([], dtype=float)
    iu = np.triu_indices(n, k=1)
    return np.abs(levels[iu[0]] - levels[iu[1]])


def pair_count_full(levels, target, tolerance):
    d = pair_diffs(levels)
    if len(d) == 0:
        return 0, 0
    count = int(np.sum(np.abs(d - target) <= tolerance))
    return count, len(d)


def pair_density_full(levels, target, gamma):
    d = pair_diffs(levels)
    if len(d) == 0:
        return np.nan
    weights = np.exp(-0.5 * ((d - target) / gamma) ** 2)
    return float(np.mean(weights))


def min_distance_to_target(levels, target):
    d = pair_diffs(levels)
    if len(d) == 0:
        return np.nan
    return float(np.min(np.abs(d - target)))


def random_subsample_metrics(levels, target, tolerance, n_centers=SUBSAMPLE_N, n_trials=SUBSAMPLE_TRIALS, seed=RANDOM_SEED):
    rng_local = np.random.default_rng(seed)
    levels = np.sort(np.unique(np.asarray(levels, dtype=float)))
    n = len(levels)
    if n < n_centers:
        return np.nan, np.nan
    counts = []
    for _ in range(n_trials):
        subset = np.sort(rng_local.choice(levels, size=n_centers, replace=False))
        c, _ = pair_count_full(subset, target, tolerance)
        counts.append(c)
    counts = np.array(counts)
    return float(np.mean(counts > 0)), float(np.mean(counts))


def continuous_baseline_density_uniform(levels, target, gamma, n_points=CONT_BASELINE_POINTS, n_trials=CONT_BASELINE_TRIALS):
    levels = np.sort(np.unique(np.asarray(levels, dtype=float)))
    if len(levels) < 2:
        return np.nan
    lo, hi = float(np.min(levels)), float(np.max(levels))
    vals = []
    for _ in range(n_trials):
        cont = np.sort(rng.uniform(lo, hi, n_points))
        vals.append(pair_density_full(cont, target, gamma))
    return float(np.mean(vals))


def surrogate_levels_by_gap_shuffle(levels, rng_local):
    levels = np.sort(np.unique(np.asarray(levels, dtype=float)))
    if len(levels) < 2:
        return levels.copy()
    gaps = np.diff(levels)
    shuffled = rng_local.permutation(gaps)
    return np.concatenate([[levels[0]], levels[0] + np.cumsum(shuffled)])


def monte_carlo_null_counts_uniform(levels, target, tolerance, n_trials=N_MONTE_CARLO):
    levels = np.sort(np.unique(np.asarray(levels, dtype=float)))
    n = len(levels)
    if n < 2:
        return np.array([], dtype=int)
    lo, hi = float(np.min(levels)), float(np.max(levels))
    vals = []
    for _ in range(n_trials):
        sample = np.sort(rng.uniform(lo, hi, n))
        c, _ = pair_count_full(sample, target, tolerance)
        vals.append(c)
    return np.array(vals, dtype=int)


def monte_carlo_null_counts_gapshuffle(levels, target, tolerance, n_trials=N_MONTE_CARLO):
    levels = np.sort(np.unique(np.asarray(levels, dtype=float)))
    if len(levels) < 2:
        return np.array([], dtype=int)
    vals = []
    for _ in range(n_trials):
        sample = surrogate_levels_by_gap_shuffle(levels, rng)
        c, _ = pair_count_full(sample, target, tolerance)
        vals.append(c)
    return np.array(vals, dtype=int)


def monte_carlo_pvalue(observed, null_counts):
    if len(null_counts) == 0:
        return np.nan
    return (np.sum(null_counts >= observed) + 1) / (len(null_counts) + 1)


def benjamini_hochberg(pvals):
    pvals = np.asarray(pvals, dtype=float)
    out = np.full_like(pvals, np.nan, dtype=float)
    valid = np.isfinite(pvals)
    if valid.sum() == 0:
        return out
    pv = pvals[valid]
    n = len(pv)
    order = np.argsort(pv)
    ranked = pv[order]
    q = np.empty(n, dtype=float)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        val = ranked[i] * n / (i + 1)
        prev = min(prev, val)
        q[order[i]] = prev
    out[valid] = np.minimum(q, 1.0)
    return out


def format_floor_flag(p, n_trials=N_MONTE_CARLO):
    floor = 1.0 / (n_trials + 1)
    if np.isfinite(p) and abs(p - floor) < 1e-12:
        return f"p <= {floor:.6g}"
    return f"p = {p:.6g}" if np.isfinite(p) else "p = NaN"


def interpret_raman(row):
    if row["Full_Pair_Count"] == 0:
        return "No Raman-compatible pairs"
    if np.isfinite(row["GapShuffle_MonteCarlo_q"]) and row["GapShuffle_MonteCarlo_q"] < 0.05:
        return "Excess pair availability beyond gap-shuffle null"
    if np.isfinite(row["Uniform_MonteCarlo_q"]) and row["Uniform_MonteCarlo_q"] < 0.05:
        return "Pair availability explained by empirical gap structure"
    if np.isfinite(row["GapShuffle_MonteCarlo_p"]) and row["GapShuffle_MonteCarlo_p"] < 0.05:
        return "Excess pair availability beyond gap-shuffle null (uncorrected)"
    if np.isfinite(row["Uniform_MonteCarlo_p"]) and row["Uniform_MonteCarlo_p"] < 0.05:
        return "Structured but not FDR-significant"
    return "Not significant"


def build_raman_summary(levels_dict, meta_dict, target, tolerance):
    rows = []
    for name, levels in levels_dict.items():
        full_count, n_pairs = pair_count_full(levels, target, tolerance)
        full_density = pair_density_full(levels, target, tolerance)
        min_dist = min_distance_to_target(levels, target)
        subs_success, subs_mean = random_subsample_metrics(levels, target, tolerance)

        null_uniform = monte_carlo_null_counts_uniform(levels, target, tolerance)
        null_gapshuffle = monte_carlo_null_counts_gapshuffle(levels, target, tolerance)

        cont_uniform = continuous_baseline_density_uniform(levels, target, tolerance)
        gapshuffle_density = np.mean([
            pair_density_full(surrogate_levels_by_gap_shuffle(levels, rng), target, tolerance)
            for _ in range(CONT_BASELINE_TRIALS)
        ]) if len(levels) >= 2 else np.nan

        rows.append({
            "System": name,
            "Type": meta_dict[name]["type"],
            "Source": meta_dict[name]["source"],
            "N_levels": len(levels),
            "Full_Pair_Count": full_count,
            "Full_N_Pairs": n_pairs,
            "Full_Pair_Density": full_density,
            "Min_Distance_To_Target": min_dist,
            "Subsample_Success": subs_success,
            "Subsample_Mean": subs_mean,
            "Uniform_Null_Mean": float(np.mean(null_uniform)) if len(null_uniform) else np.nan,
            "Uniform_Null_SD": float(np.std(null_uniform)) if len(null_uniform) else np.nan,
            "Uniform_MonteCarlo_p": monte_carlo_pvalue(full_count, null_uniform),
            "GapShuffle_Null_Mean": float(np.mean(null_gapshuffle)) if len(null_gapshuffle) else np.nan,
            "GapShuffle_Null_SD": float(np.std(null_gapshuffle)) if len(null_gapshuffle) else np.nan,
            "GapShuffle_MonteCarlo_p": monte_carlo_pvalue(full_count, null_gapshuffle),
            "Cont_Baseline_Uniform_Dens": cont_uniform,
            "Cont_Baseline_GapShuffle_Dens": float(gapshuffle_density),
            "Physical_Note": "Atomic spectra are dense spectral references" if meta_dict[name]["type"] == "atomic" else "Effective discrete defect spectrum",
        })

    df = pd.DataFrame(rows)
    df["Uniform_MonteCarlo_q"] = benjamini_hochberg(df["Uniform_MonteCarlo_p"].values)
    df["GapShuffle_MonteCarlo_q"] = benjamini_hochberg(df["GapShuffle_MonteCarlo_p"].values)
    df["Uniform_p_Display"] = [format_floor_flag(p) for p in df["Uniform_MonteCarlo_p"]]
    df["GapShuffle_p_Display"] = [format_floor_flag(p) for p in df["GapShuffle_MonteCarlo_p"]]
    df["Interpretation"] = df.apply(interpret_raman, axis=1)
    return df


def build_raman_scan(levels_dict, meta_dict, target, gamma_values):
    rows = []
    for name, levels in levels_dict.items():
        kind = meta_dict[name]["type"]
        for g in gamma_values:
            dens = pair_density_full(levels, target, g)
            subs_success, subs_mean = random_subsample_metrics(levels, target, g)
            cont = continuous_baseline_density_uniform(levels, target, g)
            gapshuffle_cont = np.mean([
                pair_density_full(surrogate_levels_by_gap_shuffle(levels, rng), target, g)
                for _ in range(max(6, CONT_BASELINE_TRIALS // 2))
            ]) if len(levels) >= 2 else np.nan
            rows.append({
                "System": name,
                "Type": kind,
                "Gamma_cm^-1": g,
                "Pair_Density_Full": dens,
                "Subsample_Success": subs_success,
                "Subsample_Mean": subs_mean,
                "Continuous_Baseline_Uniform_Density": cont,
                "Continuous_Baseline_GapShuffle_Density": float(gapshuffle_cont),
            })
    return pd.DataFrame(rows)


def build_target_scan(levels_dict, meta_dict, target_values, gamma_value=TARGET_SCAN_GAMMA):
    rows = []
    for name, levels in levels_dict.items():
        for target in target_values:
            rows.append({
                "System": name,
                "Type": meta_dict[name]["type"],
                "Target_cm^-1": target,
                "Pair_Density": pair_density_full(levels, target, gamma_value),
                "Min_Distance": min_distance_to_target(levels, target),
            })
    return pd.DataFrame(rows)


def linewidth_separation_summary(df_scan):
    rows = []
    for g, grp in df_scan.groupby("Gamma_cm^-1"):
        a = grp[grp["Type"] == "atomic"]
        d = grp[grp["Type"] == "defect"]
        a_dens = a["Pair_Density_Full"].mean()
        d_dens = d["Pair_Density_Full"].mean()
        a_succ = a["Subsample_Success"].mean()
        d_succ = d["Subsample_Success"].mean()
        rows.append({
            "Gamma_cm^-1": g,
            "Atomic_Mean_Density": a_dens,
            "Defect_Mean_Density": d_dens,
            "Density_Difference": a_dens - d_dens,
            "Log10_Density_Ratio_eps": np.log10((a_dens + EPS) / (d_dens + EPS)) if pd.notna(a_dens) and pd.notna(d_dens) else np.nan,
            "Atomic_Mean_Subsample_Success": a_succ,
            "Defect_Mean_Subsample_Success": d_succ,
            "Success_Difference": a_succ - d_succ,
            "Defect_Density_Note": "Below numerical detection threshold" if pd.notna(d_dens) and d_dens == 0 else "",
        })
    return pd.DataFrame(rows).sort_values("Gamma_cm^-1")

# ============================================================
# PLOTTING
# ============================================================
def plot_pair_density(df_scan):
    plt.figure(figsize=(10, 6))
    for system, grp in df_scan.groupby("System"):
        plt.semilogx(grp["Gamma_cm^-1"], grp["Pair_Density_Full"], lw=2, label=system)
    plt.xlabel(r'Linewidth $\gamma$ (cm$^{-1}$)')
    plt.ylabel('Normalized pair density')
    plt.title(r'Pair density vs linewidth at $\Delta_s = 2.87$ GHz')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'Figure_FinalImproved_PairDensity.png'), dpi=300, bbox_inches='tight')
    plt.close()


def plot_subsample_success(df_scan):
    plt.figure(figsize=(10, 6))
    for system, grp in df_scan.groupby("System"):
        plt.semilogx(grp["Gamma_cm^-1"], grp["Subsample_Success"], lw=2, label=system)
    plt.xlabel(r'Linewidth $\gamma$ (cm$^{-1}$)')
    plt.ylabel(f'Subsample success (N={SUBSAMPLE_N})')
    plt.title(r'Subsample Raman success vs linewidth at $\Delta_s = 2.87$ GHz')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'Figure_FinalImproved_SubsampleSuccess.png'), dpi=300, bbox_inches='tight')
    plt.close()


def plot_target_scan(df_target_scan):
    plt.figure(figsize=(10, 6))
    for system, grp in df_target_scan.groupby("System"):
        plt.plot(grp["Target_cm^-1"], grp["Pair_Density"], lw=2, label=system)
    plt.axvline(TARGET_SPIN_CM, color='k', ls='--', lw=1.5, alpha=0.7)
    plt.xlabel(r'Target splitting $\Delta$ (cm$^{-1}$)')
    plt.ylabel(f'Pair density (gamma={TARGET_SCAN_GAMMA} cm$^{{-1}}$)')
    plt.title('Target scan around low-frequency pair availability')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'Figure_FinalImproved_TargetScan.png'), dpi=300, bbox_inches='tight')
    plt.close()

# ============================================================
# AUTO-DOWNLOAD RESULTS
# ============================================================
def download_results():
    """
    تحميل جميع ملفات النتائج (CSV و PNG) تلقائياً على الجهاز.
    في Colab: يستخدم google.colab.files.download.
    في بيئة محلية: ينشئ ملف ZIP للنتائج.
    """
    print("\n📥 Preparing results for download...")

    # إنشاء ملف ZIP يحتوي على كل النتائج
    import zipfile
    zip_path = os.path.join(OUTPUT_DIR, "DTQEM_PaperIII_Results.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for f in os.listdir(OUTPUT_DIR):
            if f.endswith('.csv') or f.endswith('.png'):
                filepath = os.path.join(OUTPUT_DIR, f)
                zipf.write(filepath, f)
    print(f"   📦 ZIP archive created: {zip_path}")

    try:
        # محاولة استخدام Google Colab للتحميل المباشر
        from google.colab import files
        print("   📥 Downloading individual files (Google Colab)...")
        for f in os.listdir(OUTPUT_DIR):
            if f.endswith('.csv') or f.endswith('.png'):
                files.download(os.path.join(OUTPUT_DIR, f))
        files.download(zip_path)
        print("   ✅ All files downloaded to your device.")
    except ImportError:
        # بيئة محلية
        print(f"   📁 You are running locally.")
        print(f"   📂 All results are in: {os.path.abspath(OUTPUT_DIR)}")
        print(f"   📦 A ZIP file has been created at: {os.path.abspath(zip_path)}")
        print(f"   ➡️ You can copy or download this ZIP file manually.")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 72)
    print("DTQEM Paper III — FINAL PUBLICATION-READY PIPELINE")
    print("=" * 72)
    print(f"Target: {TARGET_SPIN_CM:.6f} cm^-1 | Tolerance: {SELECTED_TOLERANCE} cm^-1")
    print(f"Monte Carlo trials per null model: {N_MONTE_CARLO}")

    all_levels = {}
    for name, link in SYSTEMS_LINKS.items():
        local_name = name.replace(' ', '_').replace('(', '').replace(')', '').replace('+', 'plus') + '.csv'
        levels = load_from_drive(link, local_name)
        all_levels[name] = levels
        print(f"✅ {name}: {len(levels)} levels")

    spectral_rows = []
    for name, levels in all_levels.items():
        row = analyze_spectral_system(levels, name, SYSTEM_METADATA[name])
        if row is not None:
            spectral_rows.append(row)
    df_spectral = pd.DataFrame(spectral_rows)
    df_spectral.to_csv(os.path.join(OUTPUT_DIR, 'final_improved_spectral_statistics.csv'), index=False)

    print("\n📊 Raman summary with FDR and interpretation...")
    df_raman = build_raman_summary(all_levels, SYSTEM_METADATA, TARGET_SPIN_CM, SELECTED_TOLERANCE)
    df_raman.to_csv(os.path.join(OUTPUT_DIR, 'final_improved_raman_summary.csv'), index=False)
    for _, r in df_raman.iterrows():
        print(
            f"   {r['System']}: pairs={int(r['Full_Pair_Count'])}, "
            f"{r['Uniform_p_Display']}, {r['GapShuffle_p_Display']}, "
            f"q_gapshuffle={r['GapShuffle_MonteCarlo_q']:.5f}, dens={r['Full_Pair_Density']:.8f}"
        )

    print("\n📈 Linewidth scan...")
    df_scan = build_raman_scan(all_levels, SYSTEM_METADATA, TARGET_SPIN_CM, GAMMA_VALUES)
    df_scan.to_csv(os.path.join(OUTPUT_DIR, 'final_improved_raman_scan.csv'), index=False)

    df_sep = linewidth_separation_summary(df_scan)
    df_sep.to_csv(os.path.join(OUTPUT_DIR, 'final_improved_linewidth_separation.csv'), index=False)

    print("\n🎯 Target scan...")
    df_target = build_target_scan(all_levels, SYSTEM_METADATA, TARGET_SCAN_VALUES, TARGET_SCAN_GAMMA)
    df_target.to_csv(os.path.join(OUTPUT_DIR, 'final_improved_target_scan.csv'), index=False)

    plot_pair_density(df_scan)
    plot_subsample_success(df_scan)
    plot_target_scan(df_target)

    print("\n" + "=" * 72)
    print("RAMAN SUMMARY")
    print("=" * 72)
    show_cols = [
        "System", "Type", "Full_Pair_Count", "Full_Pair_Density", "Min_Distance_To_Target",
        "Uniform_p_Display", "GapShuffle_p_Display", "Uniform_MonteCarlo_q", "GapShuffle_MonteCarlo_q",
        "Interpretation"
    ]
    print(df_raman[show_cols].round(6).to_string(index=False))

    print("\nTop linewidths by density difference:")
    top = df_sep.sort_values('Density_Difference', ascending=False).head(10)
    print(top.round(6).to_string(index=False))

    # تحميل النتائج تلقائياً
    download_results()

    print("\n✅ Final improved pipeline complete.")
