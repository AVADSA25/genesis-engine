#!/usr/bin/env python3
"""
v6 TASK P — interval-floor hypothesis.

See paper/v6_supplement/taskP_interval_floor_PREREGISTRATION.md, which
was committed BEFORE this ran (commit 3e7eb4a).

H1: a cell's own MINIMUM recent division interval predicts its own
    pattern stability; division REGULARITY has no effect once minimum
    interval is controlled.

P-A (primary): natural geometric division, three lipid-supply levels.
    No forcing, so none of the Task 3 artifacts apply -- no premature
    splitting, no imposed distribution, no unphysical regime. The
    interval spread arises naturally from growth noise.

P-B (secondary): forced division, physical window only, logging per-cell
    interval STATISTICS so min-interval and CV can be separated within
    a condition.

Output: results_v6/taskP_{A,B}_obs.csv
"""
import csv
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).parent
OUT = ROOT / "results_v6"
OUT.mkdir(exist_ok=True)

ARM = os.environ.get("V6_ARM", "A").upper()
MAX_TICKS = int(os.environ.get("V6_MAX_TICKS", "20000"))

if ARM == "A":
    LIPIDS = [0.008, 0.015, 0.025]
    N_SEEDS = int(os.environ.get("V6_N_SEEDS", "75"))
    JOBS = [(l, s) for l in LIPIDS for s in range(N_SEEDS)]
else:
    CVS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 0.80, 1.0]
    TS = [3200, 6400]
    N_SEEDS = int(os.environ.get("V6_N_SEEDS", "25"))
    JOBS = [(cv, T, s) for cv in CVS for T in TS for s in range(N_SEEDS)]


def one(job):
    from genesis_engine import run_simulation
    if ARM == "A":
        lipid, seed = job
        ov = {"LIPID_SUPPLY": float(lipid)}
        tag = dict(lipid_supply=lipid, imposed_cv="", imposed_T="")
    else:
        cv, T, seed = job
        ov = {"FORCE_DIVISION": True, "FORCE_T_MEAN": float(T),
              "FORCE_CV": float(cv)}
        tag = dict(lipid_supply="", imposed_cv=cv, imposed_T=T)
    r = run_simulation(seed=seed, max_ticks=MAX_TICKS, overrides=ov)
    rows = []
    for (tick, last_iv, s, n_int, mn, mx, av, rv) in r.ss_obs:
        rows.append(dict(**tag, seed=seed, tick=tick,
                         n_intervals=n_int,
                         min_interval=round(mn, 2),
                         max_interval=round(mx, 2),
                         mean_interval=round(av, 2),
                         last_interval=round(last_iv, 2),
                         cell_S=round(s, 5),
                         rv=round(rv, 4)))
    return rows


if __name__ == "__main__":
    print(f"Task P arm {ARM}: {len(JOBS)} runs @ {MAX_TICKS} ticks", flush=True)
    t0 = time.time()
    allrows = []
    with Pool(processes=int(os.environ.get("V6_WORKERS", "16"))) as pool:
        for i, part in enumerate(pool.imap_unordered(one, JOBS), 1):
            allrows.extend(part)
            if i % 25 == 0 or i == len(JOBS):
                print(f"  [{i}/{len(JOBS)}] {len(allrows):,} obs "
                      f"{time.time()-t0:.0f}s", flush=True)
    path = OUT / f"taskP_{ARM}_obs.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(allrows[0].keys()))
        w.writeheader(); w.writerows(allrows)
    print(f"Wrote {path} ({len(allrows):,} rows) in {time.time()-t0:.0f}s")
