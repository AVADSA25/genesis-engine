#!/usr/bin/env python3
"""
v6 TASK 4 — Statistics correction.

Four defects in the published statistical presentation:

  4a. "243 +/- 2319 ticks" summarises a distribution whose median is 50
      and whose IQR is [50, 50]. Recompute as median + IQR + %-on-floor.
  4b. Identify the exact seeds carrying the mean and their share of
      total delay mass (Figure-2 estimate was ~3 runs / ~69%).
  4c. Hedges' g = 9.41 never names its dependent variable. Name it, and
      determine whether it is circular via the S-linked bonus terms.
  4d. Wilcoxon signed-rank input is ~90% tied at exactly 50. Quantify
      the tie structure and state whether the p-value is informative.

Writes: paper/v6_supplement/task4_statistics.md
"""
import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
OUT = ROOT / "paper" / "v6_supplement"
OUT.mkdir(parents=True, exist_ok=True)

SAMPLE_INTERVAL = 50


def delays(summary_csv):
    out = []
    for r in csv.DictReader(open(summary_csv)):
        try:
            b, c = int(r["phase_B_tick"]), int(r["phase_C_tick"])
            if b < 0 or c < 0:
                continue
            out.append((int(r["seed"]), c - b))
        except (KeyError, ValueError):
            continue
    return out


if __name__ == "__main__":
    L = ["# v6 Task 4 — Statistics correction", ""]

    # ── 4a / 4b ────────────────────────────────────────────────────────
    d1 = delays(ROOT / "results/summary.csv")
    d2 = delays(ROOT / "results_2d/summary.csv")

    L += ["## 4a. The delay summary is a mean of a floor-censored, "
          "heavy-tailed distribution", ""]
    L += ["| geometry | n | published summary | median | IQR | min | max | "
          "% at 50-tick floor |", "|---|---|---|---|---|---|---|---|"]
    store = {}
    for label, dd, pub in [("1D", d1, "243 ± 2319"), ("2D", dd2 := d2, "56 ± 41")]:
        a = np.array([x for _s, x in dd], dtype=float)
        floor = int((a <= SAMPLE_INTERVAL).sum())
        store[label] = a
        L.append(f"| {label} | {len(a)} | {pub} | **{np.median(a):.0f}** | "
                 f"[{np.percentile(a,25):.0f}, {np.percentile(a,75):.0f}] | "
                 f"{a.min():.0f} | {a.max():.0f} | "
                 f"**{floor}/{len(a)} = {100*floor/len(a):.1f}%** |")
    L += ["",
          "The median equals the sampling interval and the IQR has **zero "
          "width** in both geometries. `paper/paper_data.json` already "
          "contained `delay_C_minus_B/median = 50.0` alongside the mean; the "
          "manuscript sentence reported only the mean.",
          "",
          "The same file records the 2D pilot as "
          "`mean=50, median=50, min=50, max=50` — every run at exactly the "
          "sampling interval, zero variance.",
          ""]

    # 4b outliers
    L += ["## 4b. Which runs carry the 1D mean", ""]
    arr = sorted(d1, key=lambda t: -t[1])
    total = sum(x for _s, x in d1)
    L += [f"Total 1D delay mass: **{total:,} ticks** across {len(d1)} runs.",
          "",
          "| rank | seed | delay | share of total mass | cumulative |",
          "|---|---|---|---|---|"]
    cum = 0
    for i, (s, v) in enumerate(arr[:6], 1):
        cum += v
        L.append(f"| {i} | {s} | {v:,} | {100*v/total:.1f}% | "
                 f"**{100*cum/total:.1f}%** |")
    top3 = sum(v for _s, v in arr[:3])
    L += ["",
          f"**Three runs out of {len(d1)} carry {100*top3/total:.1f}% of the "
          f"entire delay mass.** Removing them changes the mean from "
          f"{np.mean([v for _s,v in d1]):.1f} to "
          f"{np.mean([v for _s,v in arr[3:]]):.1f} ticks — i.e. to within "
          f"{np.mean([v for _s,v in arr[3:]]) - SAMPLE_INTERVAL:.1f} ticks of "
          f"the sampling floor.",
          "",
          "The reported SD (2319) is roughly **10x its own mean** (243). "
          "That is not a summary statistic; it is a description of three "
          "lineages.", ""]

    # ── 4c Hedges' g ───────────────────────────────────────────────────
    L += ["## 4c. Hedges' g — dependent variable and circularity", "",
          "Located at `analyze_results.py:147-151`:", "", "```python",
          'organized    = [r["final_pop"] for r in data if r["final_mean_s"] > 0.3]',
          'disorganized = [r["final_pop"] for r in data if r["final_mean_s"] < 0.1]',
          "g = hedges_g(np.array(organized), np.array(disorganized))",
          "```", "",
          "**The dependent variable is `final_pop`** — final population count "
          "— with groups split on `final_mean_s`. This is named nowhere in the "
          "manuscript, Table 1, Table 2, or `paper_data.json`.",
          "",
          "**The effect is substantially circular.** In `genesis_engine.py` "
          "the same S that defines the grouping multiplies three fitness "
          "terms directly (lines 356-359):", "", "```python",
          "uptake = E_UPTAKE * (1 + UPT_BONUS  * S) * resource_frac   # UPT_BONUS  = 0.12",
          "eff    = E_EFFICIENCY * (1 + EFF_BONUS * S)                # EFF_BONUS  = 0.70",
          "maint  = E_MAINTENANCE * (1 - MAINT_BONUS * S)             # MAINT_BONUS= 0.35",
          "```", "",
          "High S raises uptake and efficiency and lowers maintenance, which "
          "raises energy, which lowers death rate, which raises `final_pop`. "
          "Grouping on S and measuring `final_pop` therefore largely measures "
          "the magnitude of `EFF_BONUS`, `MAINT_BONUS` and `UPT_BONUS` — "
          "constants chosen by the modeller — rather than a discovered "
          "thermodynamic effect.",
          "",
          "Group sizes are also severely imbalanced: "
          "**n_organized = 482 vs n_disorganized = 18** "
          "(from `paper_data.json`), so the pooled SD is dominated by one arm.",
          ""]

    # ── 4d Wilcoxon ────────────────────────────────────────────────────
    a1 = store["1D"]
    ties = int((a1 == SAMPLE_INTERVAL).sum())
    L += ["## 4d. Wilcoxon signed-rank — tie structure and what it tests", "",
          f"- Input: 1D delays, n = {len(a1)}",
          f"- Tied at exactly {SAMPLE_INTERVAL}: "
          f"**{ties}/{len(a1)} = {100*ties/len(a1):.1f}%**",
          f"- Distinct values in the whole sample: "
          f"**{len(np.unique(a1))}**",
          f"- Minimum value: {a1.min():.0f} (= the sampling interval)",
          "",
          "Published: `W = 116403, p = 1.66e-98`, `alternative='greater'`, "
          "i.e. H0: median delay <= 0.",
          "",
          "**The test is uninformative, for a reason more basic than the "
          "ties.** The gate in `detect_phase()` cannot emit C at or before B, "
          "so every delay is >= one sampling interval by construction. The "
          "null (delay <= 0) is not merely false, it is *unreachable* — no "
          "possible run could have produced a value inconsistent with it. "
          "A p-value against an unreachable null carries no evidence.",
          "",
          f"Separately, {100*ties/len(a1):.1f}% of the input is a single "
          f"repeated value, so the signed-rank statistic is computed over "
          f"{len(np.unique(a1))} distinct levels; the normal approximation "
          f"behind the reported p-value is not appropriate at this tie "
          f"fraction.", ""]

    L += ["---", "", "## Proposed replacement for the manuscript sentence", "",
          "Current (`paper_data.json:/mc_1d/manuscript_sentence`):", "",
          "> In N = 500 independent simulations ... the Clock preceded the "
          "Map in 482 of 482 runs (100 %; binomial test p = 8.01e-146). The "
          "mean Clock → Map delay was 243 ± 2319 ticks (Wilcoxon signed-rank "
          "W = 116 403, p = 1.66e-98). Populations that achieved stable "
          "patterns (S > 0.3, N = 482) outperformed disorganized populations "
          "(S < 0.1, N = 18) with Hedges' g = 9.41.",
          "",
          "Corrected:", "",
          "> Across 482 runs in which both predicates latched, the gated "
          "detector reported Clock before Map in 482/482 cases. This "
          "proportion is not evidence: the detector latches Map only if Clock "
          "latched at a strictly earlier tick, so no other outcome was "
          "reachable, and the associated binomial and Wilcoxon tests are "
          "computed against unreachable nulls. The measured delay has median "
          "50 ticks (IQR [50, 50]; 90.0% of runs at exactly the 50-tick "
          "sampling interval); the mean of 243 ticks is carried by three runs "
          "holding 69.0% of total delay mass. Under ungated first-crossing "
          "measurement the ordering reverses (Clock first in 0.7% of 1D and "
          "0.0% of 2D runs). The reported Hedges' g = 9.41 is computed on "
          "final population count grouped by pattern stability S, a quantity "
          "S multiplies directly through the efficiency, uptake and "
          "maintenance terms; it therefore reflects the chosen coupling "
          "constants rather than a discovered effect.",
          "",
          "## Evaluation criteria used", "",
          "- All figures recomputed from `results/summary.csv` and "
          "`results_2d/summary.csv`; no re-simulation.",
          "- 'On the floor' = delay <= the 50-tick sampling interval.",
          "- Circularity judged by tracing whether the grouping variable "
          "appears in the causal chain producing the dependent variable.",
          ""]

    path = OUT / "task4_statistics.md"
    path.write_text("\n".join(L))
    print("\n".join(L[:60]))
    print(f"\n... [truncated] ...\n\nWrote {path}")
