#!/usr/bin/env python3
"""
v6 TASK 1 — Unconditional predicate logging + high-resolution resample.

Two defects motivate this run:

(1) SAMPLING FLOOR. In the published 50-tick-sampled data the
    Clock-to-Map delay has median 50 and IQR [50, 50]; 90.0% of 1D
    runs (434/482) and 97.5% of 2D runs (193/198) sit at exactly the
    sampling interval. The reported mean (243 +/- 2319) is carried by
    3 runs out of 482 (69.0% of total delay mass). At 50-tick
    resolution "sequential" and "simultaneous" are indistinguishable.

(2) CONSTRUCTED ORDERING. detect_phase() latches C only if B latched
    at a STRICTLY EARLIER tick:
        if ph.B and ph.B_tick < tick and not ph.C and mean_s > PHASE_C_S
    So Clock-before-Map is true by construction and the minimum
    observable delay is pinned to one sample interval. The published
    1845/1845 result cannot come out any other way.

This experiment re-runs the same seed range at fine sampling and
records BOTH the gated ticks (comparable to published) and the
ungated first-crossing ticks (no sequential gate -- the honest test).

Usage:
    V6_GEOM=1d V6_N_SEEDS=100 V6_MAX_TICKS=80000 V6_SAMPLE=1 python3 experiment_v6_resolution.py
    V6_GEOM=2d V6_N_SEEDS=100 V6_MAX_TICKS=10000 V6_SAMPLE=1 python3 experiment_v6_resolution.py

Output: results_v6/resolution_{geom}_{sample}tick.csv
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

GEOM = os.environ.get("V6_GEOM", "1d").lower()
N_SEEDS = int(os.environ.get("V6_N_SEEDS", "100"))
MAX_TICKS = int(os.environ.get("V6_MAX_TICKS", "80000" if GEOM == "1d" else "10000"))
SAMPLE = int(os.environ.get("V6_SAMPLE", "1"))


def one_run(seed):
    if GEOM == "2d":
        from genesis_engine_2d import run_simulation
    else:
        from genesis_engine import run_simulation
    t0 = time.time()
    r = run_simulation(seed=seed, max_ticks=MAX_TICKS,
                       overrides={"SAMPLE_INTERVAL": SAMPLE})
    gated_delay = (r.phase_C_tick - r.phase_B_tick
                   if r.phase_B_tick > 0 and r.phase_C_tick > 0 else None)
    ungated_delay = (r.ungated_C_tick - r.ungated_B_tick
                     if r.ungated_B_tick > 0 and r.ungated_C_tick > 0 else None)
    return dict(
        geom=GEOM,
        seed=seed,
        sample_interval=SAMPLE,
        max_ticks=MAX_TICKS,
        # gated (published-style) detector
        gated_B=r.phase_B_tick,
        gated_C=r.phase_C_tick,
        gated_D=r.phase_D_tick,
        gated_delay=gated_delay if gated_delay is not None else "",
        gated_clock_first=r.clock_before_map,
        # ungated (honest) predicates
        ungated_B=r.ungated_B_tick,
        ungated_C=r.ungated_C_tick,
        cosat=r.cosat_tick,
        ungated_delay=ungated_delay if ungated_delay is not None else "",
        ungated_clock_first=r.ungated_clock_before_map,
        final_phase=r.final_phase,
        final_pop=r.final_pop,
        final_mean_s=round(r.final_mean_s, 4),
        final_mean_cv=round(r.final_mean_cv, 4),
        total_divisions=r.total_divisions,
        elapsed_s=round(time.time() - t0, 1),
    )


if __name__ == "__main__":
    seeds = list(range(N_SEEDS))
    print(f"v6 TASK 1 resolution experiment [{GEOM.upper()}]: "
          f"{N_SEEDS} seeds x {MAX_TICKS} ticks @ sample_interval={SAMPLE}",
          flush=True)
    t0 = time.time()
    rows = []
    with Pool(processes=min(18, os.cpu_count() or 4)) as pool:
        for i, row in enumerate(pool.imap_unordered(one_run, seeds), 1):
            rows.append(row)
            print(f"  [{i}/{N_SEEDS}] seed={row['seed']:>3} "
                  f"gated {row['gated_B']}->{row['gated_C']} "
                  f"(d={row['gated_delay']})  "
                  f"ungated {row['ungated_B']}->{row['ungated_C']} "
                  f"(d={row['ungated_delay']})  "
                  f"clock_first={row['ungated_clock_first']}  "
                  f"{row['elapsed_s']}s", flush=True)

    rows.sort(key=lambda r: r["seed"])
    path = OUT / f"resolution_{GEOM}_{SAMPLE}tick.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {path}  ({len(rows)} rows) in {time.time()-t0:.0f}s")
