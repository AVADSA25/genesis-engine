#!/usr/bin/env python3
"""
v6 TASK R — is the barely-dividing limit structural or a parameter choice?
Pre-registered at aad89e8 before running.
"""
import csv, os, sys, time
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
ROOT = Path(__file__).parent
OUT = ROOT / "results_v6"; OUT.mkdir(exist_ok=True)

CAPS = [20, 50, 100]
N_SEEDS = int(os.environ.get("V6_N_SEEDS", "40"))
MAX_TICKS = int(os.environ.get("V6_MAX_TICKS", "40000"))


def one(job):
    cap, seed = job
    from genesis_engine import run_simulation
    r = run_simulation(seed=seed, max_ticks=MAX_TICKS,
                       overrides={"MAX_CELLS": int(cap)})
    rows = []
    for (tick, last_iv, s, n_int, mn, mx, av, rv) in r.ss_obs:
        rows.append(dict(max_cells=cap, seed=seed, tick=tick,
                         n_intervals=n_int, n_divisions=(n_int + 1 if n_int > 0 else 0),
                         cell_S=round(s, 5)))
    return rows


if __name__ == "__main__":
    jobs = [(c, s) for c in CAPS for s in range(N_SEEDS)]
    print(f"Task R: {len(CAPS)} caps x {N_SEEDS} seeds = {len(jobs)} runs @ {MAX_TICKS} ticks", flush=True)
    t0 = time.time(); allrows = []
    with Pool(processes=int(os.environ.get("V6_WORKERS", "16"))) as pool:
        for i, part in enumerate(pool.imap_unordered(one, jobs), 1):
            allrows.extend(part)
            if i % 20 == 0 or i == len(jobs):
                print(f"  [{i}/{len(jobs)}] {len(allrows):,} obs {time.time()-t0:.0f}s", flush=True)
    path = OUT / "taskR_maxcells.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(allrows[0].keys())); w.writeheader(); w.writerows(allrows)
    print(f"Wrote {path} ({len(allrows):,} rows) in {time.time()-t0:.0f}s")
