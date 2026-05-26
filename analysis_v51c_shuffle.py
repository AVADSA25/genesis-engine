#!/usr/bin/env python3
"""
v5.1c — Shuffle control for the 2D Map→Clock back-reaction.

Question: Is the observed 2D Δcv = +0.057 (sign-test p=0.025) really
anchored to the Phase-C latch event, or is it a generic
"later-in-run-has-higher-cv" population-age drift that would appear
even if we anchored at meaningless times?

Tests run (2D only; 1D was unambiguously negative):
  T1  Real:                 windows anchored at each run's actual phc
  T2  Shuffled phc:         windows anchored at OTHER runs' phc values
                            (permutation, N=2000 shuffles)
  T3  Pre-latch anchor:     windows anchored at phc - 3000  (pre-Phase-B)
  T4  Late-shifted anchor:  windows anchored at phc + 2000  (deeper
                            post-latch, should still show the drift
                            if it's continuous)
  T5  Fixed-tick anchor:    windows at FIXED absolute ticks for every
                            run, ignoring phc entirely

Interpretation rules:
- If T2 (shuffled) gives a null distribution centered near 0 and the
  real T1 = +0.057 is in the upper tail → effect is genuinely
  phase-C-anchored.  KEEP B in the paper.
- If T2 centers near +0.057 too → the effect is a generic temporal
  drift, NOT a Map→Clock back-reaction.  PULL B from the paper.
- T3, T4, T5 are diagnostic sanity checks.
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from math import comb

np.random.seed(20260526)

ROOT = Path("/Users/mickaelfarina/genesis-engine")
RES  = ROOT / "results_2d"
OUT  = ROOT / "paper" / "v51_supplement"
OUT.mkdir(parents=True, exist_ok=True)

WIN_E = (500, 1500)
WIN_L = (3500, 4500)


def load_2d_runs():
    summary = list(csv.DictReader(open(RES / "summary.csv")))
    runs = []
    for r in summary:
        try:
            phc = int(r["phase_C_tick"])
            mt  = int(r["max_ticks"])
            if phc < 0: continue
        except (KeyError, ValueError):
            continue
        seed = int(r["seed"])
        ts = RES / "timeseries" / f"run_{seed:04d}.csv"
        if not ts.exists(): continue
        ticks, cvs = [], []
        with open(ts) as f:
            for line in csv.DictReader(f):
                try:
                    ticks.append(int(line["tick"]))
                    cvs.append(float(line["mean_cv"]))
                except (KeyError, ValueError):
                    continue
        runs.append((seed, phc, mt, np.array(ticks), np.array(cvs)))
    return runs


def delta_for_anchor(runs, anchor_value=None, use_run_phc=True):
    """If use_run_phc, anchor = each run's own phc + anchor_value (offset).
       Else anchor_value is an absolute tick used for every run.
       Returns array of per-run Δcv values."""
    out = []
    for seed, phc, mt, ticks, cvs in runs:
        if use_run_phc:
            A = phc + (anchor_value or 0)
        else:
            A = anchor_value
        if A + WIN_L[1] > mt or A + WIN_E[0] < 0:
            continue
        e_mask = (ticks >= A + WIN_E[0]) & (ticks < A + WIN_E[1])
        l_mask = (ticks >= A + WIN_L[0]) & (ticks < A + WIN_L[1])
        if not e_mask.any() or not l_mask.any():
            continue
        out.append(float(cvs[l_mask].mean() - cvs[e_mask].mean()))
    return np.array(out)


def delta_with_shuffled_phc(runs, rng):
    """Each run gets ANOTHER (random) run's phc as its anchor."""
    phcs = [phc for _, phc, _, _, _ in runs]
    shuffled = rng.permutation(phcs)
    out = []
    for (seed, _, mt, ticks, cvs), fake_phc in zip(runs, shuffled):
        A = int(fake_phc)
        if A + WIN_L[1] > mt or A + WIN_E[0] < 0:
            continue
        e_mask = (ticks >= A + WIN_E[0]) & (ticks < A + WIN_E[1])
        l_mask = (ticks >= A + WIN_L[0]) & (ticks < A + WIN_L[1])
        if not e_mask.any() or not l_mask.any():
            continue
        out.append(float(cvs[l_mask].mean() - cvs[e_mask].mean()))
    return np.array(out)


def sign_test_p(d):
    nu = int(np.sum(d > 0)); nd = int(np.sum(d < 0))
    m = nu + nd
    if m == 0: return float("nan"), nu, nd
    k = max(nu, nd)
    p = 2 * sum(comb(m, i) for i in range(k, m + 1)) / (2 ** m)
    return min(1.0, p), nu, nd


def summarise(name, d):
    n = len(d)
    if n == 0:
        print(f"  [{name}] no qualifying runs")
        return None
    mean = float(d.mean()); med = float(np.median(d))
    p, nu, nd = sign_test_p(d)
    print(f"  [{name}]  n={n:>3}  mean Δcv={mean:+.5f}  median={med:+.5f}  "
          f"sign +/-={nu}/{nd}  p={p:.3g}")
    return dict(name=name, n=n, mean=mean, median=med, p=p, nu=nu, nd=nd)


if __name__ == "__main__":
    runs = load_2d_runs()
    print(f"Loaded {len(runs)} 2D runs that reached Phase C\n")

    print("REAL & DIAGNOSTIC anchors")
    print("-" * 60)
    d_real = delta_for_anchor(runs, anchor_value=0,   use_run_phc=True)
    s_real = summarise("T1 real          (anchor = phc)         ", d_real)

    d_pre  = delta_for_anchor(runs, anchor_value=-3000, use_run_phc=True)
    s_pre  = summarise("T3 pre-latch     (anchor = phc - 3000)  ", d_pre)

    d_post = delta_for_anchor(runs, anchor_value=+2000, use_run_phc=True)
    s_post = summarise("T4 deeper-post   (anchor = phc + 2000)  ", d_post)

    # T5: anchor at median phc, used in absolute terms for all runs
    median_phc = int(np.median([phc for _, phc, _, _, _ in runs]))
    d_fix  = delta_for_anchor(runs, anchor_value=median_phc, use_run_phc=False)
    s_fix  = summarise(f"T5 fixed-abs     (anchor = {median_phc} for all runs)", d_fix)

    print()
    print("PERMUTATION NULL")
    print("-" * 60)
    rng = np.random.default_rng(20260526)
    null_means = []
    null_signp = []
    N_PERM = 2000
    for _ in range(N_PERM):
        d_perm = delta_with_shuffled_phc(runs, rng)
        if len(d_perm) > 0:
            null_means.append(d_perm.mean())
            p, nu, nd = sign_test_p(d_perm)
            null_signp.append(p)
    null_means = np.array(null_means)

    real_mean = d_real.mean()
    p_perm_two_sided = float(np.mean(np.abs(null_means) >= abs(real_mean)))
    p_perm_one_sided = float(np.mean(null_means >= real_mean))
    null_mean_mean   = float(null_means.mean())
    null_mean_sd     = float(null_means.std())

    print(f"  Null distribution of mean Δcv (N={N_PERM} shuffles):")
    print(f"     mean  = {null_mean_mean:+.5f}")
    print(f"     sd    = {null_mean_sd:.5f}")
    print(f"     2.5%  = {np.percentile(null_means, 2.5):+.5f}")
    print(f"    97.5%  = {np.percentile(null_means, 97.5):+.5f}")
    print(f"  Real mean Δcv = {real_mean:+.5f}")
    print(f"  Permutation p (one-sided, real ≥ null) = {p_perm_one_sided:.4f}")
    print(f"  Permutation p (two-sided)              = {p_perm_two_sided:.4f}")

    # Plot null vs real
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.hist(null_means, bins=40, color="#cfd8e8", edgecolor="#6c7280",
            label=f"null (N={N_PERM} phc-shuffles)")
    ax.axvline(real_mean, color="#d63031", lw=2.0,
               label=f"observed mean Δcv = {real_mean:+.4f}\n"
                     f"perm p (1-sided) = {p_perm_one_sided:.3f}")
    ax.axvline(0, color="k", ls="--", lw=0.7)
    ax.set_xlabel("mean Δcv across runs")
    ax.set_ylabel("# permutations")
    ax.set_title("2D Map→Clock back-reaction — permutation null test\n"
                 "(does phc-shuffling destroy the effect?)")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "fig_backreaction_2D_permutation_null.png", dpi=150)
    plt.close(fig)

    # Decision
    print()
    print("=" * 60)
    if p_perm_one_sided < 0.05:
        verdict = ("REAL: the 2D back-reaction effect is statistically "
                   "anchored to Phase C — survives phc-shuffle control.")
    else:
        verdict = ("ARTIFACT: the 2D Δcv = +0.057 is NOT specifically "
                   "anchored to Phase C — it appears in shuffled-phc "
                   "data too. Should be pulled from the paper.")
    print(f"VERDICT: {verdict}")
    print("=" * 60)

    # Persist a tidy markdown report
    md = ["# 2D back-reaction: shuffle control (Phase-C anchor test)",
          "",
          "## Question",
          "Is the observed 2D Δcv = +0.057 specifically caused by Phase-C",
          "latching, or is it a generic 'later-in-run' population-age",
          "drift that would appear at any anchor time?",
          "",
          "## Real and diagnostic anchors",
          "",
          "| Test | n | mean Δcv | median | sign +/− | p (sign-test) |",
          "|---|---|---|---|---|---|"]
    for s in (s_real, s_pre, s_post, s_fix):
        if s is None: continue
        md.append(f"| {s['name'].strip()} | {s['n']} | "
                  f"{s['mean']:+.5f} | {s['median']:+.5f} | "
                  f"{s['nu']}/{s['nd']} | {s['p']:.3g} |")
    md += ["",
           "## Permutation null (gold-standard control)",
           "",
           f"For each of N = {N_PERM} permutations, each run's `phc` "
           "value was replaced by the `phc` of a different (randomly "
           "chosen) run, and Δcv was recomputed at that random anchor.",
           "",
           f"- Null distribution mean = {null_mean_mean:+.5f}",
           f"- Null distribution sd   = {null_mean_sd:.5f}",
           f"- 95% interval = [{np.percentile(null_means, 2.5):+.5f}, "
                          f"{np.percentile(null_means, 97.5):+.5f}]",
           f"- Observed mean Δcv = {real_mean:+.5f}",
           f"- **Permutation p (one-sided, real ≥ null) = "
           f"{p_perm_one_sided:.4f}**",
           "",
           "## Verdict",
           "",
           f"**{verdict}**"]
    (OUT / "backreaction_2D_shuffle_control.md").write_text("\n".join(md))
    print(f"\nWritten: {OUT/'backreaction_2D_shuffle_control.md'}")
    print(f"Plot:    {OUT/'fig_backreaction_2D_permutation_null.png'}")
