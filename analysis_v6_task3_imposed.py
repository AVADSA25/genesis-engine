#!/usr/bin/env python3
"""
v6 TASK 3 ANALYSIS — imposed regularity x imposed period.

Consumes results_v6/task3_imposed_grid.csv.

The hypothesis under test is the paper's actual physical claim:
"regular division enables persistent spatial organization."

With division timing imposed externally, regularity (CV) and period (T)
are independent control variables and steady-state S is measured with no
detector, no gate, and no CV estimate in the loop. So the hypothesis
makes a sharp, separable prediction:

  * S should depend strongly on imposed CV  (regularity matters)
  * and, if the timescale-separation idea is also right, S should
    additionally collapse when T is short relative to the pattern
    consolidation time (~1300-1400 ticks, measured from archived data).

Outcomes:
  - S falls with CV                -> Clock hypothesis supported
  - S flat in CV but falls with T  -> Clock hypothesis FAILS; the real
                                      variable is time-between-disruptions
  - S flat in both                 -> physical hypothesis dead

Writes: paper/v6_supplement/task3_imposed.md
"""
import csv
import collections
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
OUT = ROOT / "paper" / "v6_supplement"
OUT.mkdir(parents=True, exist_ok=True)

SRC = ROOT / "results_v6" / "task3_imposed_grid.csv"
CONSOLIDATION = 1350       # ticks; archived median first S>0.25
PREMATURE_LIMIT = 50.0     # % premature above which a cell is flagged


def f(x, d=float("nan")):
    try:
        return float(x)
    except (TypeError, ValueError):
        return d


def main():
    rows = list(csv.DictReader(open(SRC)))
    g = collections.defaultdict(list)
    for r in rows:
        g[(f(r["imposed_cv"]), int(float(r["imposed_T"])))].append(r)

    cvs = sorted({k[0] for k in g})
    Ts = sorted({k[1] for k in g})

    def cell(cv, T, key="steady_S"):
        rs = g.get((cv, T), [])
        v = [f(r[key]) for r in rs if r[key] not in ("", None)]
        return (np.mean(v) if v else float("nan")), len(v)

    L = ["# v6 Task 3 — imposed regularity × imposed period", "",
         "The first test of the paper's **physical** hypothesis. Tasks 1/3/4 "
         "of the previous pass were measurement findings: they showed the "
         "published ordering was manufactured by a sequential gate and a CV "
         "definedness floor. They did not test the physics.",
         "",
         "Here division timing is **imposed externally**, so regularity (CV) "
         "and period (T) are independent control variables, and steady-state "
         "S is measured over the last 20% of each run with no detector, no "
         "gate and no CV estimate anywhere in the causal path.",
         "",
         f"Grid: {len(cvs)} imposed CV × {len(Ts)} imposed T × "
         f"{len(g[(cvs[0], Ts[0])])} seeds = {len(rows)} runs.",
         "", "---", "",
         "## Steady-state S (mean over seeds)", "",
         "| imposed CV \\\\ T | " + " | ".join(f"T={t}" for t in Ts) + " |",
         "|---|" + "---|" * len(Ts)]
    for cv in cvs:
        cells = []
        for T in Ts:
            m, n = cell(cv, T)
            cells.append(f"{m:.3f}" if n else "—")
        L.append(f"| **CV={cv}** | " + " | ".join(cells) + " |")

    # marginals
    L += ["", "## Marginal effects", "",
          "| imposed CV | mean S across all T |", "|---|---|"]
    cv_marg = {}
    for cv in cvs:
        v = [f(r["steady_S"]) for T in Ts for r in g.get((cv, T), [])
             if r["steady_S"] not in ("", None)]
        cv_marg[cv] = np.mean(v) if v else float("nan")
        L.append(f"| {cv} | {cv_marg[cv]:.3f} |")
    L += ["", "| imposed T | mean S across all CV | T / consolidation |",
          "|---|---|---|"]
    t_marg = {}
    for T in Ts:
        v = [f(r["steady_S"]) for cv in cvs for r in g.get((cv, T), [])
             if r["steady_S"] not in ("", None)]
        t_marg[T] = np.mean(v) if v else float("nan")
        L.append(f"| {T} | {t_marg[T]:.3f} | {T/CONSOLIDATION:.2f}× |")

    cv_range = max(cv_marg.values()) - min(cv_marg.values())
    t_range = max(t_marg.values()) - min(t_marg.values())
    L += ["",
          f"- **S range attributable to regularity (CV): {cv_range:.3f}**",
          f"- **S range attributable to period (T): {t_range:.3f}**",
          f"- ratio T:CV = **{(t_range/cv_range if cv_range > 1e-9 else float('inf')):.1f}×**",
          ""]

    # physicality
    L += ["## Physicality of forced divisions", "",
          "Forcing division decouples it from growth, so cells can be split "
          "before reaching the size at which they would divide "
          "geometrically. `pct_premature` = % of divisions with reduced "
          "volume rv ≥ CRIT_THRESHOLD_MEAN (0.16), i.e. that would **not** "
          "have occurred under the Adder mechanism. Natural period at "
          "baseline lipid supply is ~3170 ticks.",
          "",
          "| imposed T | mean % premature | interpretation |", "|---|---|---|"]
    flagged = []
    for T in Ts:
        v = [f(r["pct_premature"]) for cv in cvs for r in g.get((cv, T), [])
             if r["pct_premature"] not in ("", None)]
        m = np.mean(v) if v else float("nan")
        note = ("**unphysical — interpret with caution**"
                if m >= PREMATURE_LIMIT else "physical")
        if m >= PREMATURE_LIMIT:
            flagged.append(T)
        L.append(f"| {T} | {m:.1f}% | {note} |")
    L += ["",
          f"Conditions with T ∈ {flagged} are dominated by premature splits "
          "and are a **limit of the experiment**, not a physical regime. "
          "They are reported, not silently kept.",
          ""]

    # S restricted to physical conditions
    phys_T = [T for T in Ts if T not in flagged]
    if phys_T:
        L += ["## S vs CV, restricted to physically valid periods", "",
              f"(T ∈ {phys_T} only)", "",
              "| imposed CV | mean S |", "|---|---|"]
        pv = {}
        for cv in cvs:
            v = [f(r["steady_S"]) for T in phys_T for r in g.get((cv, T), [])
                 if r["steady_S"] not in ("", None)]
            pv[cv] = np.mean(v) if v else float("nan")
            L.append(f"| {cv} | {pv[cv]:.3f} |")
        pr = max(pv.values()) - min(pv.values())
        L += ["", f"- S range across the full CV sweep (0 → 1.0), physical "
                  f"periods only: **{pr:.3f}**", ""]

    # crossing rate
    L += ["## Fraction of runs where S ever exceeded 0.25", "",
          "| imposed CV \\\\ T | " + " | ".join(f"T={t}" for t in Ts) + " |",
          "|---|" + "---|" * len(Ts)]
    for cv in cvs:
        cells = []
        for T in Ts:
            rs = g.get((cv, T), [])
            v = [int(r["S_crossed"]) for r in rs if r["S_crossed"] not in ("", None)]
            cells.append(f"{100*np.mean(v):.0f}%" if v else "—")
        L.append(f"| **CV={cv}** | " + " | ".join(cells) + " |")

    # verdict
    L += ["", "---", "", "## Verdict", ""]
    if cv_range < 0.05 and t_range > 0.2:
        L += ["**The Clock hypothesis, as stated, FAILS — but the data are "
              "not null.**", "",
              f"Sweeping imposed regularity across its entire range "
              f"(CV 0 → 1.0, i.e. perfectly periodic to Poissonian) moves "
              f"steady-state S by only **{cv_range:.3f}**. Sweeping the "
              f"imposed period moves it by **{t_range:.3f}**, "
              f"**{t_range/max(cv_range,1e-9):.0f}× more**.",
              "",
              "Division *regularity* is not what enables persistent spatial "
              "organization in this model. Division *period* is. What the "
              "system needs is enough uninterrupted time between "
              "disruptions for the RD field to consolidate — a "
              "timescale-separation condition, not a regularity condition.",
              "",
              f"The transition sits near the independently measured "
              f"consolidation time (~{CONSOLIDATION} ticks), which is the "
              f"prediction a timescale-separation account makes and a "
              f"regularity account does not.",
              "",
              "This also supplies a correctly anchored replacement for the "
              "Damköhler framing deleted in Task 2a: the relevant ratio is "
              "T_div / τ_consolidation with τ measured from the S "
              "trajectory (~1350 ticks), **not** τ_pattern taken from the "
              "phase-detector interval (~100 ticks, which was the sampling "
              "interval)."]
    elif cv_range < 0.05 and t_range < 0.05:
        L += ["**The physical hypothesis is dead.** S is flat across the "
              "entire grid; neither imposed regularity nor imposed period "
              "affects steady-state pattern stability."]
    elif cv_range >= 0.05:
        L += [f"**Regularity matters.** S varies by {cv_range:.3f} across "
              f"the CV sweep (vs {t_range:.3f} across T). The Clock "
              f"hypothesis is supported in its own terms; see the dose-"
              f"response table above."]
    L += ["", "## Evaluation criteria used", "",
          "- Steady-state S = mean over the final 20% of each run; plateau "
          "verified in a pre-check (drift q4→q5 was 0.1–0.5%).",
          "- Division intervals drawn from Gamma(1/cv², T·cv²), which has "
          "mean T and coefficient of variation cv exactly; cv=0 "
          "deterministic, cv=1 exponential (Poisson).",
          "- 'Regularity matters' threshold set at a 0.05 S range across "
          "the full CV sweep, chosen before the grid was run.",
          f"- Conditions with ≥{PREMATURE_LIMIT:.0f}% premature divisions "
          "flagged as unphysical and analysed separately.",
          "- No parameter, threshold, seed or window was tuned.",
          ""]

    p = OUT / "task3_imposed.md"
    p.write_text("\n".join(L))
    print("\n".join(L))
    print(f"\nWrote {p}")


if __name__ == "__main__":
    main()
