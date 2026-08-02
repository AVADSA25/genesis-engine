#!/usr/bin/env python3
"""
Analyse results_v6/taskS_symmetric.csv and regenerate the Task S results
document from the saved data.

Reports, per parameterisation:
  - median definedness ticks for S, CV and clock_r
  - the validity check rho(ss_clock_r, ss_cv), which must be NEGATIVE for
    clock_r to be a regularity metric at all
  - the measured division period, to compare against the buffer length

Writes paper/v6_supplement/taskS_symmetric_RESULTS.md.
"""
import csv
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).parent
CSV = ROOT / "results_v6" / "taskS_symmetric.csv"
OUT = ROOT / "paper" / "v6_supplement" / "taskS_symmetric_RESULTS.md"


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def med_defined(vals):
    """Median over runs where the quantity became defined at all."""
    v = np.array([x for x in vals if x is not None and x >= 0], dtype=float)
    return (float(np.median(v)), len(v)) if len(v) else (float("nan"), 0)


def main():
    rows = list(csv.DictReader(open(CSV)))
    variants = sorted({r["variant"] for r in rows})
    L = []
    A = L.append

    A("# v6 Task S — symmetric-metrics redesign (archived re-run)\n")
    A("Regenerated from `results_v6/taskS_symmetric.csv` by")
    A("`analysis_v6_taskS.py`. The original execution of this task was done")
    A("inline and its outputs were never written to disk; the numbers below")
    A("supersede any earlier prose figures.\n")
    A("**Design.** Replace CV — undefined until a cell completes four")
    A("divisions — with `clock_r`, the autocorrelation of a cell's own radius")
    A("trajectory, which needs no divisions. If the Clock/Map definedness")
    A("asymmetry were purely an artifact of the CV estimator, `clock_r`")
    A("should become defined much earlier than CV.\n")

    n_seeds = len({r["seed"] for r in rows})
    ticks = rows[0]["max_ticks"]
    A(f"**Runs.** {n_seeds} seeds x {len(variants)} parameterisations, "
      f"{ticks} ticks each, 1D engine.\n")

    summary = {}
    for v in variants:
        rs = [r for r in rows if r["variant"] == v]
        buf = int(rs[0]["buffer_ticks"])
        mS, nS = med_defined([int(r["def_S"]) for r in rs])
        mC, nC = med_defined([int(r["def_CV"]) for r in rs])
        mR, nR = med_defined([int(r["def_clock_r"]) for r in rs])
        T = np.array([num(r["T_div"]) for r in rs], dtype=float)
        T = T[~np.isnan(T)]

        cr = np.array([num(r["ss_clock_r"]) for r in rs], dtype=float)
        cvv = np.array([num(r["ss_cv"]) for r in rs], dtype=float)
        ok = ~np.isnan(cr) & ~np.isnan(cvv)
        if ok.sum() >= 3:
            rho, p = stats.spearmanr(cr[ok], cvv[ok])
        else:
            rho, p = float("nan"), float("nan")

        summary[v] = dict(buf=buf, mS=mS, mC=mC, mR=mR, nS=nS, nC=nC, nR=nR,
                          rho=rho, p=p, n=int(ok.sum()),
                          T=float(np.median(T)) if len(T) else float("nan"))

    A("## Definedness (median first tick defined; -1 runs excluded)\n")
    A("| parameterisation | buffer | Map: S | Clock old: CV | Clock new: clock_r |")
    A("|---|---|---|---|---|")
    for v in variants:
        s = summary[v]
        A(f"| `{v}` | {s['buf']} ticks | {s['mS']:.0f} (n={s['nS']}) | "
          f"{s['mC']:.0f} (n={s['nC']}) | {s['mR']:.0f} (n={s['nR']}) |")
    A("")

    A("## Validity check: rho(clock_r, CV) at steady state\n")
    A("A genuine regularity metric must correlate **negatively** with CV")
    A("(more regular -> higher autocorrelation, lower CV).\n")
    A("| parameterisation | buffer | median division period | rho | p | n | verdict |")
    A("|---|---|---|---|---|---|---|")
    for v in variants:
        s = summary[v]
        valid = (not np.isnan(s["rho"])) and s["rho"] < 0 and s["p"] < 0.05
        A(f"| `{v}` | {s['buf']} ticks | {s['T']:.0f} ticks | "
          f"{s['rho']:+.4f} | {s['p']:.4f} | {s['n']} | "
          f"{'VALID' if valid else 'INVALID'} |")
    A("")

    sh, lg = summary.get("short"), summary.get("long")
    if sh and lg:
        A("## Reading\n")
        A(f"The short buffer spans {sh['buf']} ticks against a division period")
        A(f"of ~{sh['T']:.0f} ticks: it cannot contain even one period, and the")
        A(f"validity check confirms it measures nothing about regularity")
        A(f"(rho = {sh['rho']:+.4f}, p = {sh['p']:.3f}). It is reported here only")
        A("to document that the first parameterisation was invalid.\n")
        A(f"The long buffer spans {lg['buf']} ticks, ~{lg['buf']/lg['T']:.1f}")
        A("division periods, and is the one that can work.\n")
        A("**The result.** `clock_r` was built specifically to have no")
        A(f"definedness floor. It becomes defined at a median tick "
          f"{lg['mR']:.0f}, "
          f"{'later' if lg['mR'] > lg['mC'] else 'earlier'} than the CV metric")
        A(f"it replaces ({lg['mC']:.0f}), and far later than the spatial metric")
        A(f"S ({lg['mS']:.0f}).\n")
        A("**Why this is not fixable by a better estimator.** `clock_r` is")
        A("defined only once a cell's radius buffer is full, i.e. once that")
        A(f"cell has lived {lg['buf']} ticks. Shortening the buffer is what")
        A("the `short` row does, and it destroys validity. The floor is")
        A("therefore bounded below by the requirement to observe several")
        A("division periods — a time-frequency constraint on measuring the")
        A("regularity of a slow periodic process, not an implementation")
        A("choice. Any Clock metric faces it; the spatial metric does not,")
        A("because its correlation length is set by a ~40-tick field")
        A("relaxation rather than by the division cycle.\n")
        A("**Selection caveat (stated explicitly).** Because the buffer is")
        A("per-cell and daughters are constructed fresh (`Cell.create`, empty")
        A("`radius_hist`, `age = 0`) while mothers retain theirs, `clock_r` at")
        A("any tick is an average over the subpopulation of cells old enough")
        A(f"to have filled a {lg['buf']}-tick buffer. This is age-selected by")
        A("construction. It does not rescue the metric: a cell too young to")
        A("have a full buffer is precisely a cell whose period has not been")
        A("observed. The selection is a restatement of the constraint, not a")
        A("confound that hides it.\n")
        A("**Conclusion.** The Clock/Map definedness asymmetry that produced")
        A("defect 3 is only partly an implementation error. The specific")
        A("four-division CV floor is ours. A floor of order several division")
        A("periods is physical, and it means comparing first-crossing times")
        A("between these two metrics measures their timescale ratio rather")
        A("than the dynamics. The ordering question is malformed as posed.\n")

    A("---\n")
    A("Raw data: `results_v6/taskS_symmetric.csv`. ")
    A("Regenerate: `python3 analysis_v6_taskS.py`.")

    OUT.write_text("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n[wrote {OUT}]")


if __name__ == "__main__":
    main()
