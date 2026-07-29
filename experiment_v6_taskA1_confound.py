#!/usr/bin/env python3
"""
v6 TASK A1 (rebuilt) — the Gamma right-tail confound.

Task 3 reported Spearman rho(CV, S) = +0.2196 (p = 2.56e-06) over the
physically valid conditions: steady-state pattern stability RISES with
imposed division irregularity, refuting the paper's physical hypothesis.
That conclusion is only safe if the effect is really about irregularity.

CONFOUND UNDER TEST. Intervals are drawn from Gamma(k = 1/CV^2,
scale = T*CV^2). The mean is T at every CV, but skew grows with CV: a
CV=0.8 population contains cells with realized intervals far longer than
T; a CV=0 population contains none. If a cell's own S responds to its
own realized interval, then rho(CV, S) is a PERIOD effect wearing a
regularity costume.

WHY THIS SCRIPT WAS REBUILT (twice). Two earlier versions could not
adjudicate the grid result:

  v1 logged only cells with >=2 divisions, excluding ~42% of the
     population -- precisely the barely-dividing cells the confound is
     about.
  v2 logged all cells but only at the FINAL TICK. That is
     CV-dependent BY CONSTRUCTION: at CV=0 every cell divides in
     lockstep, so at any single tick all cells sit at the same phase of
     their division cycle; if that phase is a post-division low-S
     moment, the whole CV=0 group is depressed. That artifact alone
     manufactures rho(CV,S) > 0 -- the same direction as the effect
     under test. The grid's time-average over the last 20% washes it
     out, which is why the grid figure is safe and a snapshot is not.

This version matches the grid's measure exactly: ALL cells, sampled
ACROSS the steady-state window (last 20% of the run), so population and
temporal window are identical to the quantity being adjudicated.
`ss_pop_S` is also captured so the reconstruction can be verified
against the grid's steady_S numerically rather than assumed.

Physical conditions only (T in {3200, 6400}), matching the headline.

Output:
  results_v6/taskA1_obs.csv       per-cell steady-state observations
  results_v6/taskA1_runs.csv      per-run summary incl. measure check
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

CVS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 0.80, 1.0]
TS = [3200, 6400]                      # physical only (<50% premature)
N_SEEDS = int(os.environ.get("V6_N_SEEDS", "25"))
MAX_TICKS = int(os.environ.get("V6_MAX_TICKS", "20000"))


def one(args):
    cv, T, seed = args
    from genesis_engine import run_simulation
    r = run_simulation(seed=seed, max_ticks=MAX_TICKS,
                       overrides={"FORCE_DIVISION": True,
                                  "FORCE_T_MEAN": float(T),
                                  "FORCE_CV": float(cv)})
    obs = [dict(imposed_cv=cv, imposed_T=T, seed=seed, tick=t,
                realized_interval=round(iv, 2), cell_S=round(s, 5),
                n_intervals=ni,
                n_divisions=(ni + 1 if ni > 0 else 0))
           for t, iv, s, ni in r.ss_obs]
    # steady_S reconstructed the same way the grid computes it:
    # time-average of per-sample population-mean S over the window
    steady_S = float(np.mean(r.ss_pop_S)) if r.ss_pop_S else float("nan")
    ni_all = [o["n_intervals"] for o in obs]
    run = dict(
        imposed_cv=cv, imposed_T=T, seed=seed,
        steady_S=round(steady_S, 5),
        n_obs=len(obs),
        n_pop_samples=len(r.ss_pop_S),
        final_pop=r.final_pop,
        # fraction of steady-state cell-observations that barely divided
        frac_lt2_div=round(float(np.mean([n == 0 for n in ni_all])), 4) if ni_all else "",
        frac_lt4_div=round(float(np.mean([n < 3 for n in ni_all])), 4) if ni_all else "",
        mean_realized_interval=round(float(np.mean(
            [o["realized_interval"] for o in obs if o["n_intervals"] > 0])), 2)
            if any(o["n_intervals"] > 0 for o in obs) else "",
    )
    return obs, run


if __name__ == "__main__":
    jobs = [(cv, T, sd) for cv in CVS for T in TS for sd in range(N_SEEDS)]
    print(f"Task A1 (rebuilt): {len(jobs)} runs, physical T only, "
          f"{MAX_TICKS} ticks, steady-state window = last 20%", flush=True)
    t0 = time.time()
    all_obs, all_runs = [], []
    with Pool(processes=int(os.environ.get("V6_WORKERS", "16"))) as pool:
        for i, (obs, run) in enumerate(pool.imap_unordered(one, jobs), 1):
            all_obs.extend(obs)
            all_runs.append(run)
            if i % 50 == 0 or i == len(jobs):
                print(f"  [{i}/{len(jobs)}] {len(all_obs)} obs "
                      f"{time.time()-t0:.0f}s", flush=True)
    for path, rows in ((OUT / "taskA1_obs.csv", all_obs),
                       (OUT / "taskA1_runs.csv", all_runs)):
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"Wrote {path} ({len(rows)} rows)")
    print(f"done in {time.time()-t0:.0f}s")
