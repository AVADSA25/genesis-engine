#!/usr/bin/env python3
"""
v6 TASK 3 — imposed regularity x imposed period.

THE point of the whole v6 pass. Tasks 1/3/4 of the previous brief were
all MEASUREMENT findings: they showed the published Clock->Map ordering
was manufactured by a sequential gate and a CV definedness floor. They
did NOT test the physical hypothesis, which has never been tested at
all.

This experiment tests it directly, with neither broken instrument in
the loop:

  * Division timing is IMPOSED externally (FORCE_DIVISION), so division
    regularity is a CONTROL variable, not an estimate. The CV
    definedness floor is gone because we never estimate CV to decide
    anything.
  * The dependent variable is steady-state pattern stability S measured
    over a late window. No sequential gate, no phase detector, no
    latching.

Hypothesis under test: regular division enables persistent spatial
organization. If true, S should be high at low imposed CV and collapse
above some CV threshold, and should also collapse when the imposed
period is short relative to pattern consolidation time (~1300-1400
ticks from archived data).

Grid: imposed CV x imposed mean period T_div.

PHYSICALITY CAVEAT (logged, not hidden). Forcing division decouples it
from growth, so cells can be split before they have grown to a size at
which they would divide geometrically. The natural period at baseline
LIPID_SUPPLY is ~3170 ticks, so every T below that produces premature
splits. We log the reduced volume rv = (MIN_RADIUS/radius)^2 at every
forced division and report the fraction with rv >= CRIT_THRESHOLD_MEAN
(0.16), i.e. the fraction that would NOT have divided geometrically.
Conditions with a high premature fraction are a limit of the
experiment and are reported as such.

Usage:
  V6_MODE=plateau python3 experiment_v6_task3_imposed.py   # pre-check
  V6_MODE=grid    python3 experiment_v6_task3_imposed.py   # full grid

Output: results_v6/task3_imposed_{mode}.csv
"""
import csv
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).parent
OUT = ROOT / "results_v6"
OUT.mkdir(exist_ok=True)

MODE = os.environ.get("V6_MODE", "grid").lower()
MAX_TICKS = int(os.environ.get("V6_MAX_TICKS", "30000"))
N_SEEDS = int(os.environ.get("V6_N_SEEDS", "25"))

CVS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 0.80, 1.0]
TS = [200, 400, 800, 1600, 3200, 6400]

if MODE == "plateau":
    # a few corners only, to verify S plateaus well before MAX_TICKS
    CVS = [0.05, 0.50]
    TS = [400, 3200]
    N_SEEDS = int(os.environ.get("V6_N_SEEDS", "4"))

S_THRESH = 0.25
CRIT = 0.16          # CRIT_THRESHOLD_MEAN; rv >= this == premature split


def one(args):
    cv, T, seed = args
    from genesis_engine import run_simulation
    r = run_simulation(seed=seed, max_ticks=MAX_TICKS,
                       overrides={"FORCE_DIVISION": True,
                                  "FORCE_T_MEAN": float(T),
                                  "FORCE_CV": float(cv)})
    t = np.array(r.ts_ticks)
    s = np.array(r.ts_mean_s)
    if len(t) == 0:
        return None
    # steady-state window: last 20% of the run
    lo = MAX_TICKS * 0.8
    m = t >= lo
    ss = float(s[m].mean()) if m.any() else float("nan")
    # plateau diagnostic: mean S in each quintile
    quint = []
    for q in range(5):
        a, b = MAX_TICKS * q / 5, MAX_TICKS * (q + 1) / 5
        sel = (t >= a) & (t < b)
        quint.append(round(float(s[sel].mean()), 4) if sel.any() else "")
    rv = np.array(r.rv_at_division) if r.rv_at_division else np.array([])
    return dict(
        imposed_cv=cv, imposed_T=T, seed=seed, max_ticks=MAX_TICKS,
        steady_S=round(ss, 4),
        final_S=round(r.final_mean_s, 4),
        S_crossed=int(r.ungated_C_tick > 0),
        S_cross_tick=r.ungated_C_tick,
        measured_cv=round(r.final_mean_cv, 4),
        final_pop=r.final_pop,
        total_div=r.total_divisions,
        n_rv=len(rv),
        rv_median=round(float(np.median(rv)), 4) if len(rv) else "",
        pct_premature=round(100.0 * float((rv >= CRIT).mean()), 1) if len(rv) else "",
        S_q1=quint[0], S_q2=quint[1], S_q3=quint[2],
        S_q4=quint[3], S_q5=quint[4],
    )


if __name__ == "__main__":
    jobs = [(cv, T, sd) for cv in CVS for T in TS for sd in range(N_SEEDS)]
    print(f"v6 Task 3 [{MODE}] {len(CVS)}x{len(TS)} conditions x {N_SEEDS} "
          f"seeds = {len(jobs)} runs @ {MAX_TICKS} ticks", flush=True)
    t0 = time.time()
    rows = []
    nw = int(os.environ.get("V6_WORKERS", "16"))
    with Pool(processes=nw) as pool:
        for i, row in enumerate(pool.imap_unordered(one, jobs), 1):
            if row:
                rows.append(row)
            if i % 25 == 0 or i == len(jobs):
                print(f"  [{i}/{len(jobs)}] {time.time()-t0:.0f}s", flush=True)
    rows.sort(key=lambda r: (r["imposed_cv"], r["imposed_T"], r["seed"]))
    path = OUT / f"task3_imposed_{MODE}.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows) in {time.time()-t0:.0f}s")
