#!/usr/bin/env python3
"""
v6 TASK P ANALYSIS — interval-floor hypothesis.

Evaluated strictly against
paper/v6_supplement/taskP_interval_floor_PREREGISTRATION.md,
committed at 3e7eb4a BEFORE the experiment ran.

Pre-registered predictions (thresholds fixed in advance, NOT movable):
  P1  rho(min_interval, cell_S) > +0.25 AND larger in magnitude than
      the +0.22 CV effect from Task 3
  P2  mean S in the lowest min-interval bin is >= 0.15 below the
      highest bin
  P3  (arm B only) controlling for min_interval attenuates the CV
      effect by > 50%
  P4  any threshold falls within 2x of the ~1350-tick consolidation
      time, i.e. 675-2700

Decision rule:
  P1 AND P2      -> interval-floor SUPPORTED (reformulation licensed)
  exactly one    -> PARTIAL (suggestive only, do not reframe)
  neither        -> NOT SUPPORTED (goes to the lab untested)

Known risk, pre-registered: min_interval and n_intervals are not
independent (few divisions -> minimum biased upward). Effects present
only in low-n cells are reported as artifacts, not findings.

Writes: paper/v6_supplement/taskP_interval_floor_RESULTS.md
"""
import csv
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).parent
OUT = ROOT / "paper" / "v6_supplement"
OUT.mkdir(parents=True, exist_ok=True)

CONSOLIDATION = 1350
CV_EFFECT_TASK3 = 0.22          # the number P1 must beat
P1_MIN_RHO = 0.25
P2_MIN_GAP = 0.15


def load(arm):
    p = ROOT / "results_v6" / f"taskP_{arm}_obs.csv"
    if not p.exists():
        return None
    rows = list(csv.DictReader(open(p)))
    # only cells that have at least one completed interval
    return [r for r in rows if int(r["n_intervals"]) > 0]


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def analyse_arm(arm, L):
    rows = load(arm)
    if not rows:
        L.append(f"\n## Arm {arm} — NO DATA\n")
        return None

    mn = np.array([fnum(r["min_interval"]) for r in rows])
    s = np.array([fnum(r["cell_S"]) for r in rows])
    ni = np.array([int(r["n_intervals"]) for r in rows])

    rho, p = spearmanr(mn, s)

    L.append(f"\n## Arm {arm} — n = {len(rows):,} cell-observations\n")
    L.append(f"- ρ(min_interval, cell_S) = **{rho:+.4f}** (p = {p:.3g})")
    L.append(f"- min_interval range: {mn.min():.0f} – {mn.max():.0f} ticks "
             f"(median {np.median(mn):.0f})")
    L.append(f"- cell_S range: {s.min():.3f} – {s.max():.3f} "
             f"(median {np.median(s):.3f})")
    L.append("")

    # binned profile
    edges = np.percentile(mn, [0, 20, 40, 60, 80, 100])
    L.append("### S by min-interval quintile\n")
    L.append("| bin | min_interval range | n | mean S | median S |")
    L.append("|---|---|---|---|---|")
    bin_means = []
    for i in range(5):
        lo, hi = edges[i], edges[i + 1]
        m = (mn >= lo) & (mn <= hi) if i == 4 else (mn >= lo) & (mn < hi)
        if m.sum() < 10:
            continue
        bin_means.append(float(s[m].mean()))
        L.append(f"| {i+1} | {lo:.0f}–{hi:.0f} | {int(m.sum()):,} | "
                 f"**{s[m].mean():.4f}** | {np.median(s[m]):.4f} |")
    gap = (bin_means[-1] - bin_means[0]) if len(bin_means) >= 2 else float("nan")
    L.append("")
    L.append(f"- Gap (highest bin − lowest bin): **{gap:+.4f}**")
    L.append("")

    # confound: stratify by n_intervals
    L.append("### Confound check — stratified by n_intervals\n")
    L.append("Pre-registered risk: a cell with few divisions has few "
             "intervals to minimise over, so its minimum is biased "
             "upward. An effect present only in low-n cells is an "
             "artifact.\n")
    L.append("| n_intervals | n obs | ρ(min_interval, S) | p | mean S |")
    L.append("|---|---|---|---|---|")
    strat = []
    for lo, hi, lab in [(1, 2, "1–2"), (3, 4, "3–4"),
                        (5, 8, "5–8"), (9, 99, "9+")]:
        m = (ni >= lo) & (ni <= hi)
        if m.sum() < 30:
            continue
        r2, p2 = spearmanr(mn[m], s[m])
        strat.append((lab, int(m.sum()), r2, p2))
        L.append(f"| {lab} | {int(m.sum()):,} | **{r2:+.4f}** | "
                 f"{p2:.3g} | {s[m].mean():.4f} |")
    L.append("")
    if strat:
        highn = [r for lab, n, r, p in strat if lab in ("5–8", "9+")]
        if highn:
            L.append(f"- ρ among well-divided cells (5+ intervals): "
                     f"**{np.mean(highn):+.4f}**")
            L.append(f"- If this is near zero while the pooled ρ is not, "
                     f"the effect is the n-bias artifact.")
    L.append("")
    return dict(arm=arm, n=len(rows), rho=float(rho), p=float(p),
                gap=float(gap), bin_means=bin_means, edges=edges.tolist(),
                strat=strat)


if __name__ == "__main__":
    L = ["# Task P — interval-floor hypothesis: RESULTS", "",
         "Evaluated against the pre-registration committed at `3e7eb4a` "
         "**before** this experiment ran. Thresholds were fixed in "
         "advance and have not been moved.", "",
         "**H1:** a cell's own *minimum* recent division interval "
         "predicts its own pattern stability; regularity matters only "
         "insofar as it produces short intervals.", "",
         "| prediction | threshold |", "|---|---|",
         f"| P1 | ρ(min_interval, S) > +{P1_MIN_RHO} and > {CV_EFFECT_TASK3} |",
         f"| P2 | highest − lowest bin gap ≥ {P2_MIN_GAP} |",
         "| P3 | CV effect attenuates > 50% controlling min_interval (arm B) |",
         f"| P4 | threshold within 2× of {CONSOLIDATION} ticks (675–2700) |",
         "", "---"]

    res = {}
    for arm, name in (("A", "natural division (PRIMARY)"),
                      ("B", "forced division (secondary)")):
        L.append(f"\n# {name}")
        res[arm] = analyse_arm(arm, L)

    # verdict on the primary arm
    L += ["", "---", "", "# Verdict", ""]
    a = res.get("A")
    if a is None:
        L.append("Primary arm has no data; no verdict.")
    else:
        p1_raw = (a["rho"] > P1_MIN_RHO) and (abs(a["rho"]) > CV_EFFECT_TASK3)
        p2 = (a["gap"] >= P2_MIN_GAP)
        # Pre-registered disqualifier: the pooled rho is contaminated if
        # the association does not survive stratification by n_intervals.
        # The pre-registration states that an effect not present within
        # strata is an artifact, not a finding.
        highn = [r for lab, n, r, pp in a["strat"] if lab in ("5-8", "5\u20138", "9+")]
        strat_ok = bool(highn) and (np.mean(highn) > P1_MIN_RHO)
        p1 = p1_raw and strat_ok
        L.append(f"- **P1 (pooled)** ρ = {a['rho']:+.4f} vs required > "
                 f"+{P1_MIN_RHO}: {'passes on the pooled statistic' if p1_raw else 'FAIL'}")
        L.append(f"- **P1 (stratified, pre-registered disqualifier)** "
                 f"ρ among cells with 5+ intervals = "
                 f"{np.mean(highn) if highn else float('nan'):+.4f}: "
                 f"**{'PASS' if strat_ok else 'FAIL'}**")
        L.append(f"- **P1 overall**: **{'PASS' if p1 else 'FAIL'}**")
        L.append(f"- **P2** gap = {a['gap']:+.4f} vs required ≥ "
                 f"{P2_MIN_GAP}: **{'PASS' if p2 else 'FAIL'}**")
        L.append("")
        if p1 and p2:
            L.append("## INTERVAL-FLOOR SUPPORTED")
            L.append("")
            L.append("The original theory had the right structure and the "
                     "wrong variable. What predicts spatial organization "
                     "is the minimum uninterrupted division interval, not "
                     "division regularity. Reformulation is licensed.")
        elif p1 or p2:
            L.append("## PARTIAL — suggestive only")
            L.append("")
            L.append("One pre-registered prediction passed and one failed. "
                     "Per the decision rule fixed in advance, this does "
                     "**not** license reframing the theory. Report as "
                     "suggestive and unresolved.")
        else:
            L.append("## NOT SUPPORTED")
            L.append("")
            L.append("Neither pre-registered prediction passed. The "
                     "interval-floor reformulation does not rescue the "
                     "theory within this model. The ordering question "
                     "goes to the laboratory untested — which is where "
                     "the v6 audit already placed it.")
    L += ["", "## Evaluation criteria used", "",
          "- Thresholds fixed in the pre-registration and not adjusted.",
          "- Arm A (natural geometric division) is the primary test; it "
          "contains none of the Task 3 forcing artifacts.",
          "- Only cells with ≥1 completed interval are included, since "
          "min_interval is undefined otherwise.",
          "- Stratification by n_intervals reports whether the effect is "
          "the pre-registered n-bias artifact.",
          "- Spearman rank correlation throughout.", ""]

    path = OUT / "taskP_interval_floor_RESULTS.md"
    path.write_text("\n".join(L))
    print("\n".join(L))
    print(f"\nWrote {path}")
