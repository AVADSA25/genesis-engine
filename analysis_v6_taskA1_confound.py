#!/usr/bin/env python3
"""
v6 TASK A1 ANALYSIS — does the Task 3 refutation survive its confounds?

Task 3 reported rho(CV, S) = +0.2196 (p = 2.56e-06) over the physically
valid conditions: steady-state pattern stability RISES with imposed
division irregularity, contrary to the paper's physical hypothesis.

Three confounds could produce that without irregularity mattering:

  A1  Gamma right tail. Intervals ~ Gamma(1/CV^2, T*CV^2): mean T at
      every CV, but skew grows with CV, so high-CV populations contain
      cells with much longer realized intervals. If S tracks a cell's
      OWN realized interval, rho(CV,S) is a period effect in disguise.
  A2  Was rho computed on physically valid conditions only? (answered
      separately: yes, T in {3200,6400}, n=450)
  A3  Survivorship from extinctions. (answered separately: zero
      extinctions in the physical window)

Plus the addendum: cells whose realized interval exceeds the run length
barely divide at all, so their RD field is never perturbed and S is
trivially high. If that fraction climbs with CV, rho measures "some
cells stopped dividing", not "irregularity helps".

MEASURE VALIDITY. This analysis uses per-cell observations sampled
across the last 20% of each run, all cells included -- identical
population and temporal window to the grid's steady_S. The
reconstruction is verified numerically against the grid before any
conclusion is drawn.

Writes: paper/v6_supplement/taskA1_confound.md
"""
import csv
import collections
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).parent
OUT = ROOT / "paper" / "v6_supplement"
OUT.mkdir(parents=True, exist_ok=True)

OBS = ROOT / "results_v6" / "taskA1_obs.csv"
RUNS = ROOT / "results_v6" / "taskA1_runs.csv"
GRID = ROOT / "results_v6" / "task3_imposed_grid.csv"
PHYS = {3200, 6400}


def fnum(x, d=None):
    try:
        v = float(x)
        return v if v == v else d
    except (TypeError, ValueError):
        return d


def main():
    obs = list(csv.DictReader(open(OBS)))
    runs = list(csv.DictReader(open(RUNS)))
    grid = [r for r in csv.DictReader(open(GRID))
            if int(float(r["imposed_T"])) in PHYS]

    L = ["# v6 Task A1 — does the refutation survive its confounds?", "",
         "Task 3 reported ρ(CV, S) = +0.2196 (p = 2.56e-06) on the "
         "physically valid conditions: steady-state pattern stability "
         "**rises** with imposed division irregularity, contrary to the "
         "paper's physical hypothesis. This tests whether that is real.",
         "", "---", ""]

    # ── 0. Measure validity ───────────────────────────────────────────
    L += ["## 0. Measure validity (checked before anything else)", "",
          "This analysis must adjudicate the grid's `steady_S`, so it "
          "must measure the same thing. Two earlier versions did not:",
          "",
          "- v1 logged only cells with ≥2 divisions, excluding ~42% of "
          "the population — precisely the barely-dividing cells the "
          "confound concerns.",
          "- v2 logged all cells but only at the **final tick**. That is "
          "CV-dependent by construction: at CV=0 every cell divides in "
          "lockstep, so at any single tick all cells sit at the same "
          "phase of their division cycle; if that phase is a "
          "post-division low-S moment the entire CV=0 group is "
          "depressed. That artifact alone manufactures ρ(CV,S) > 0 — the "
          "same direction as the effect under test.",
          "",
          "This version samples all cells across the last 20% of each "
          "run, matching the grid's population and temporal window.",
          ""]

    gmap = {(fnum(r["imposed_cv"]), int(float(r["imposed_T"])),
             int(r["seed"])): fnum(r["steady_S"]) for r in grid}
    diffs = []
    for r in runs:
        k = (fnum(r["imposed_cv"]), int(float(r["imposed_T"])),
             int(r["seed"]))
        g, a = gmap.get(k), fnum(r["steady_S"])
        if g is not None and a is not None:
            diffs.append(abs(g - a))
    if diffs:
        L += [f"Reconstructed `steady_S` vs the grid's, over "
              f"{len(diffs)} matched runs: mean |Δ| = "
              f"**{np.mean(diffs):.6f}**, max |Δ| = "
              f"**{np.max(diffs):.6f}**.",
              "",
              ("✅ The reconstruction reproduces the grid's measure; this "
               "analysis is entitled to adjudicate it."
               if np.max(diffs) < 1e-3 else
               "⚠️ The reconstruction does NOT match the grid's measure. "
               "Conclusions below are not licensed."), ""]

    # ── 1. Barely-dividing cells ──────────────────────────────────────
    L += ["## 1. Are high-CV populations carried by cells that stopped "
          "dividing?", "",
          "| imposed CV | % cell-obs with <2 divisions | % with <4 | "
          "mean realized interval |", "|---|---|---|---|"]
    by_cv = collections.defaultdict(list)
    for o in obs:
        by_cv[fnum(o["imposed_cv"])].append(o)
    cvs = sorted(by_cv)
    lt2, lt4 = {}, {}
    for cv in cvs:
        g = by_cv[cv]
        ni = np.array([int(o["n_intervals"]) for o in g])
        lt2[cv] = 100.0 * float((ni == 0).mean())
        lt4[cv] = 100.0 * float((ni < 3).mean())
        iv = np.array([fnum(o["realized_interval"], -1) for o in g])
        mi = iv[iv > 0]
        L.append(f"| {cv} | {lt2[cv]:.1f}% | {lt4[cv]:.1f}% | "
                 f"{mi.mean():.0f} |" if len(mi) else
                 f"| {cv} | {lt2[cv]:.1f}% | {lt4[cv]:.1f}% | — |")
    rng2 = max(lt2.values()) - min(lt2.values())
    rng4 = max(lt4.values()) - min(lt4.values())
    L += ["",
          f"- Range of <2-division fraction across CV: **{rng2:.1f} pp** "
          f"({lt2[cvs[0]]:.1f}% at CV={cvs[0]} → {lt2[cvs[-1]]:.1f}% at "
          f"CV={cvs[-1]})",
          f"- Range of <4-division fraction across CV: **{rng4:.1f} pp**",
          ""]

    # ── 2. Does a cell's own interval predict its own S? ──────────────
    L += ["## 2. Within-condition: does a cell's own realized interval "
          "predict its own S?", "",
          "| imposed CV | imposed T | n obs | ρ(own interval, own S) | p |",
          "|---|---|---|---|---|"]
    cell_rhos = []
    by_cond = collections.defaultdict(list)
    for o in obs:
        if int(o["n_intervals"]) > 0:
            by_cond[(fnum(o["imposed_cv"]),
                     int(float(o["imposed_T"])))].append(o)
    for k in sorted(by_cond):
        g = by_cond[k]
        if len(g) < 30:
            continue
        iv = [fnum(o["realized_interval"]) for o in g]
        s = [fnum(o["cell_S"]) for o in g]
        rho, p = spearmanr(iv, s)
        cell_rhos.append(rho)
        L.append(f"| {k[0]} | {k[1]} | {len(g)} | {rho:+.4f} | {p:.3g} |")
    if cell_rhos:
        L += ["",
              f"Median within-condition ρ(own interval, own S) = "
              f"**{np.median(cell_rhos):+.4f}** "
              f"(range {min(cell_rhos):+.3f} to {max(cell_rhos):+.3f}).",
              ""]

    # ── 3. Does CV survive controlling for realized interval? ─────────
    L += ["## 3. Does CV retain explanatory power once realized interval "
          "is controlled?", "",
          "Matched-bin comparison: within bins of realized interval, "
          "does mean cell-S still rise with imposed CV?", ""]
    div = [o for o in obs if int(o["n_intervals"]) > 0]
    ivs = np.array([fnum(o["realized_interval"]) for o in div])
    edges = np.percentile(ivs, [0, 20, 40, 60, 80, 100])
    L += ["| interval bin | " + " | ".join(f"CV={c}" for c in cvs) +
          " | ρ(CV,S) within bin | p |",
          "|---|" + "---|" * (len(cvs) + 2)]
    within_rhos = []
    for bi in range(5):
        lo, hi = edges[bi], edges[bi + 1]
        sel = [o for o in div
               if lo <= fnum(o["realized_interval"]) <= hi]
        if len(sel) < 50:
            continue
        cells = []
        for c in cvs:
            v = [fnum(o["cell_S"]) for o in sel
                 if fnum(o["imposed_cv"]) == c]
            cells.append(f"{np.mean(v):.3f}" if len(v) >= 5 else "—")
        cvv = [fnum(o["imposed_cv"]) for o in sel]
        sv = [fnum(o["cell_S"]) for o in sel]
        rho, p = spearmanr(cvv, sv)
        within_rhos.append(rho)
        L.append(f"| {lo:.0f}–{hi:.0f} | " + " | ".join(cells) +
                 f" | **{rho:+.4f}** | {p:.3g} |")
    L.append("")

    # unconditional, same observation set
    cvv = [fnum(o["imposed_cv"]) for o in div]
    sv = [fnum(o["cell_S"]) for o in div]
    rho_uncond, p_uncond = spearmanr(cvv, sv)
    med_within = float(np.median(within_rhos)) if within_rhos else float("nan")
    L += [f"- Unconditional ρ(CV, cell-S) on the same observations: "
          f"**{rho_uncond:+.4f}** (p = {p_uncond:.3g}, n = {len(div)})",
          f"- Median ρ(CV, cell-S) **within** interval bins: "
          f"**{med_within:+.4f}**",
          f"- Attenuation: "
          f"**{100*(1 - abs(med_within)/max(abs(rho_uncond),1e-9)):.0f}%**",
          ""]

    # ── verdict ───────────────────────────────────────────────────────
    L += ["---", "", "## Verdict", ""]
    survives = (med_within > 0.05 and rng2 < 10.0)
    if survives:
        L += ["**REFUTED — the refutation survives.**", "",
              f"The CV effect persists within interval-matched bins "
              f"(median ρ = {med_within:+.4f}), so it is not the Gamma "
              f"right tail. The fraction of barely-dividing cells varies "
              f"by only {rng2:.1f} pp across the CV sweep, so it is not "
              f"carried by cells that stopped dividing. Combined with A2 "
              f"(physical conditions only) and A3 (zero extinctions in "
              f"the physical window), the Task 3 result stands: imposed "
              f"regularity does not improve persistent spatial "
              f"organization, and the measured association runs opposite "
              f"to the paper's hypothesis."]
    else:
        L += ["**CANNOT CURRENTLY ANSWER.**", "", ]
        if med_within <= 0.05:
            L += [f"The CV effect does **not** survive controlling for "
                  f"realized interval: unconditional ρ = {rho_uncond:+.4f} "
                  f"falls to a median of {med_within:+.4f} within "
                  f"interval-matched bins. The apparent regularity effect "
                  f"is substantially a period effect produced by the "
                  f"Gamma right tail."]
        if rng2 >= 10.0:
            L += [f"The fraction of cells completing <2 divisions varies "
                  f"by {rng2:.1f} pp across the CV sweep, so the "
                  f"comparison is partly between populations that divide "
                  f"and populations that largely do not."]
        L += ["",
              "**This does not restore the original claim.** It is a "
              "weaker and different statement: with this model and this "
              "design, the physical hypothesis can be neither confirmed "
              "nor refuted. The correction must say that rather than "
              "claiming refutation."]

    L += ["", "## Stated limitation (for the correction)", "",
          "The physical window contains only **two** period values "
          "(T = 3200 and 6400), both at or above the model's natural "
          "period (~3,170 ticks). Below that, forcing division splits "
          "cells before they have grown — 79.4% premature at T=1600, "
          "rising to 100% at T=200. The **'too fast to organize' regime "
          "is therefore unphysical by construction in this model and "
          "cannot be tested with it.** That is a limitation of the "
          "design, not a finding.",
          "", "## Evaluation criteria used", "",
          "- Measure validity checked numerically against the grid "
          "before drawing conclusions (mean |Δ| reported above).",
          "- 'Survives' requires BOTH: median within-bin ρ > +0.05, AND "
          "<2-division fraction varying by < 10 pp across the CV sweep. "
          "Both thresholds fixed before running.",
          "- Interval bins are quintiles of the pooled realized-interval "
          "distribution, so bins are equally populated.",
          "- Physical conditions only (T ∈ {3200, 6400}); zero "
          "extinctions in this window, so no survivorship correction.",
          ""]

    p = OUT / "taskA1_confound.md"
    p.write_text("\n".join(L))
    print("\n".join(L))
    print(f"\nWrote {p}")


if __name__ == "__main__":
    main()
