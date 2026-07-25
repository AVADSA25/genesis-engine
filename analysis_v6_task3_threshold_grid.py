#!/usr/bin/env python3
"""
v6 TASK 3 — Threshold grid ablation (post-hoc, zero new simulation).

Precondition checked: the archived runs DO log mean_cv and mean_s
timeseries (results/timeseries/, results_2d/timeseries/, 50-tick
resolution), so the whole grid is pure re-thresholding of existing data.

The published paper ablates four physics parameters but never ablates
the two numbers the ordering result actually depends on:
    PHASE_B_CV = 0.25   (Clock predicate)
    PHASE_C_S  = 0.25   (Map predicate)
Two different metrics on different natural scales that happen to share
a threshold value -- which reads as aesthetic rather than principled.

Grid: CV_th in {0.15, 0.25, 0.35} x S_th in {0.15, 0.25, 0.35}.

CRITICAL METHOD NOTE. Ordering is computed from UNGATED first
crossings:
    t_clock = first tick with 0 < mean_cv < CV_th
    t_map   = first tick with     mean_s  > S_th
The published gated detector cannot be used here: it latches Map only
after Clock has latched at a strictly earlier tick, so it returns
Clock-before-Map = 100% for every cell of the grid by construction and
carries no information.

Writes: paper/v6_supplement/task3_threshold_grid.md
"""
import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
OUT = ROOT / "paper" / "v6_supplement"
OUT.mkdir(parents=True, exist_ok=True)

CV_THRESHOLDS = [0.15, 0.25, 0.35]
S_THRESHOLDS = [0.15, 0.25, 0.35]

GEOMS = [
    ("1D", ROOT / "results/summary.csv", ROOT / "results/timeseries"),
    ("2D", ROOT / "results_2d/summary.csv", ROOT / "results_2d/timeseries"),
]


def load_series(summary_csv, ts_dir, limit=None):
    """Return list of (seed, ticks[], cv[], s[]) from archived timeseries."""
    rows = list(csv.DictReader(open(summary_csv)))
    if limit:
        rows = rows[:limit]
    out = []
    for r in rows:
        seed = int(r["seed"])
        p = ts_dir / f"run_{seed:04d}.csv"
        if not p.exists():
            continue
        t, cv, s = [], [], []
        for ln in csv.DictReader(open(p)):
            try:
                t.append(int(ln["tick"]))
                cv.append(float(ln["mean_cv"]))
                s.append(float(ln["mean_s"]))
            except (KeyError, ValueError):
                continue
        if t:
            out.append((seed, np.array(t), np.array(cv), np.array(s)))
    return out


def first_cross(ticks, vals, thresh, direction):
    """First tick where predicate holds. direction 'below' or 'above'."""
    if direction == "below":
        idx = np.flatnonzero((vals > 0) & (vals < thresh))
    else:
        idx = np.flatnonzero(vals > thresh)
    return int(ticks[idx[0]]) if len(idx) else None


def cell(series, cv_th, s_th):
    clock_first = map_first = tie = incomplete = 0
    delays = []
    for _seed, t, cv, s in series:
        tc = first_cross(t, cv, cv_th, "below")
        tm = first_cross(t, s, s_th, "above")
        if tc is None or tm is None:
            incomplete += 1
            continue
        delays.append(tm - tc)
        if tc < tm:
            clock_first += 1
        elif tm < tc:
            map_first += 1
        else:
            tie += 1
    n = clock_first + map_first + tie
    return dict(n=n, clock_first=clock_first, map_first=map_first,
                tie=tie, incomplete=incomplete,
                pct_clock=100.0 * clock_first / n if n else float("nan"),
                median_delay=float(np.median(delays)) if delays else float("nan"))


if __name__ == "__main__":
    L = ["# v6 Task 3 — Threshold grid ablation",
         "",
         "**Zero new simulation.** Precondition verified: the archived runs "
         "log `mean_cv` and `mean_s` timeseries at 50-tick resolution, so the "
         "entire grid is post-hoc re-thresholding of existing data.",
         "",
         "## Why this grid was needed",
         "",
         "The published paper ablates four physics parameters "
         "(`LIPID_SUPPLY`, `RD_NOISE`, `GROWTH_PERTURB`, `STAB_WINDOW`) but "
         "never ablates the two numbers the ordering result actually depends "
         "on: `PHASE_B_CV = 0.25` and `PHASE_C_S = 0.25`. These are two "
         "different metrics on different natural scales that happen to share "
         "a threshold value.",
         "",
         "## Method note (important)",
         "",
         "Ordering is computed from **ungated** first crossings:",
         "", "```",
         "t_clock = first tick with 0 < mean_cv < CV_th",
         "t_map   = first tick with     mean_s  > S_th",
         "```", "",
         "The published gated detector **cannot** be used for this grid: it "
         "latches Map only after Clock has latched at a strictly earlier "
         "tick, so it returns Clock-before-Map = 100% in every cell by "
         "construction and carries no information. Verified in Task 1.",
         "", "---", ""]

    for label, sc, td in GEOMS:
        series = load_series(sc, td, limit=150)
        L += [f"## {label} — Clock-before-Map %, ungated (n≈{len(series)} runs)",
              "",
              "Rows = CV threshold (Clock), columns = S threshold (Map). "
              "Published cell is CV 0.25 / S 0.25.",
              "",
              "| CV\\\\S | " + " | ".join(f"S={s}" for s in S_THRESHOLDS) + " |",
              "|---|" + "---|" * len(S_THRESHOLDS)]
        grid = {}
        for cv_th in CV_THRESHOLDS:
            cells = []
            for s_th in S_THRESHOLDS:
                c = cell(series, cv_th, s_th)
                grid[(cv_th, s_th)] = c
                mark = " *" if (cv_th == 0.25 and s_th == 0.25) else ""
                cells.append(f"**{c['pct_clock']:.1f}%**{mark}")
            L.append(f"| **CV={cv_th}** | " + " | ".join(cells) + " |")
        L += ["", "\\* = published threshold pair", ""]

        L += ["Median delay (t_map − t_clock), ticks; negative = Map first:",
              "",
              "| CV\\\\S | " + " | ".join(f"S={s}" for s in S_THRESHOLDS) + " |",
              "|---|" + "---|" * len(S_THRESHOLDS)]
        for cv_th in CV_THRESHOLDS:
            cells = [f"{grid[(cv_th,s_th)]['median_delay']:+.0f}"
                     for s_th in S_THRESHOLDS]
            L.append(f"| **CV={cv_th}** | " + " | ".join(cells) + " |")
        L.append("")

        pcts = [grid[k]["pct_clock"] for k in grid]
        L += [f"- Range of Clock-before-Map across the 9 cells: "
              f"**{min(pcts):.1f}% – {max(pcts):.1f}%**",
              f"- Published detector reports **100%** in every cell "
              f"(by construction).", ""]

    L += ["---", "", "## Evaluation criteria used", "",
          "- Ordering judged on ungated first crossings only; the gated "
          "detector is uninformative here (returns 100% everywhere).",
          "- A run contributes only if BOTH predicates cross within the "
          "archived record; otherwise counted as incomplete.",
          "- Archived 50-tick timeseries; no re-simulation, no tuning.",
          "- Note the CV metric is undefined (pinned at 1.0) until a cell "
          "completes four divisions (Task 1 companion), which floors "
          "`t_clock` in every cell of this grid. The grid therefore tests "
          "threshold-sensitivity, not the underlying ordering.",
          ""]

    path = OUT / "task3_threshold_grid.md"
    path.write_text("\n".join(L))
    print("\n".join(L))
    print(f"\nWrote {path}")
