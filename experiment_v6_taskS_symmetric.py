#!/usr/bin/env python3
"""
v6 TASK S — symmetric-metrics experiment (ARCHIVED RE-RUN).

Pre-registered at 0ff4ed0. The original execution was done inline via
`python3 -c` and its outputs were never saved, so the numbers in
taskS_symmetric_RESULTS.md and in the paper had no backing data file.
An adversarial fact-check flagged them as unverifiable. This script is
the archival re-run: same design, larger N, outputs written to disk.

WHAT IS MEASURED

The ordering question failed repeatedly because Clock and Map are
measured by instruments with different definedness properties:
  Map  (S)  -- spatial autocorrelation of the RD field, defined after
               STAB_DEPTH * STAB_WINDOW ticks, no divisions needed
  Clock(CV) -- coefficient of variation of division intervals, needs
               four completed divisions before it exists at all

The redesign replaces CV with clock_r, the normalised autocorrelation
of a cell's own radius trajectory, which needs no divisions and is
defined as soon as its buffer fills.

TWO PARAMETERISATIONS, both run:
  short : RHIST_EVERY=10, RHIST_LEN=40   -> 400-tick buffer, lags 30-200
  long  : RHIST_EVERY=50, RHIST_LEN=120  -> 6000-tick buffer, lags 150-3000

The measured division period is ~2,500 ticks, so `short` cannot reach it
and is expected to fail a validity check; `long` can.

PER-RUN OUTPUTS
  def_S        first sampled tick with mean_s > 0        (engine field)
  def_CV       first sampled tick with mean_cv < 1.0, i.e. computable
  def_clock_r  first sampled tick with clock_r >= 0      (engine field)
  xB, xC       ungated first-crossings of the CV and S *thresholds*
                 (definedness and crossing are different events; the
                  paper compares definedness, so both are recorded)
  ss_clock_r   steady-state mean clock_r (last 20% of run)
  ss_cv        steady-state mean CV (last 20%)
    -> rho(ss_clock_r, ss_cv) across runs is the VALIDITY check: a
       genuine regularity metric must correlate NEGATIVELY with CV.

NOTE ON GRID: SAMPLE_INTERVAL = 50, so every per-run tick below is a
multiple of 50. Medians over an even number of runs can therefore land
halfway between grid points (e.g. 4825 = (4800+4850)/2); such a value is
a median, not an observation.

Output: results_v6/taskS_symmetric.csv
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

N_SEEDS = int(os.environ.get("V6_N_SEEDS", "40"))
SEED0 = int(os.environ.get("V6_SEED0", "0"))
MAX_TICKS = int(os.environ.get("V6_MAX_TICKS", "20000"))

PARAMS = {
    "short": {"RHIST_EVERY": 10, "RHIST_LEN": 40,
              "RHIST_LAG_LO": 3, "RHIST_LAG_HI": 20},
    "long":  {"RHIST_EVERY": 50, "RHIST_LEN": 120,
              "RHIST_LAG_LO": 3, "RHIST_LAG_HI": 60},
}

# --- Buffer sweep (V6_SWEEP=1) -------------------------------------
# Neither parameterisation above passes the validity check, so the
# question "is a valid Clock metric reachable at ANY buffer length?"
# is still open. This sweep answers it as a curve rather than by
# picking a length that works, which would be tuning.
#
# One variable only: RHIST_LEN is held at 120 so every arm uses the
# same number of samples (identical estimator quality) and only the
# span in ticks changes. Max searched lag is half the buffer in all
# arms, which is the standard choice, not a per-arm tuning knob.
#
# V6_SWEEP_EVERY selects which arms to run (comma-separated RHIST_EVERY
# values); V6_OUT names the output file. Together these allow an
# out-of-sample confirmation of a single arm on fresh seeds via
# V6_SEED0, which is how the 24000-tick arm was re-tested after the
# initial sweep gave it p = 0.016 against a Bonferroni threshold of
# 0.0125 over four arms.
SWEEP_EVERY = tuple(
    int(x) for x in os.environ.get("V6_SWEEP_EVERY", "10,50,100,200").split(",")
)
SWEEP = {
    f"buf{e*120}": {"RHIST_EVERY": e, "RHIST_LEN": 120,
                    "RHIST_LAG_LO": 3, "RHIST_LAG_HI": 60}
    for e in SWEEP_EVERY
}
if os.environ.get("V6_SWEEP") == "1":
    PARAMS = SWEEP


def first_tick(ticks, vals, pred):
    for t, v in zip(ticks, vals):
        if pred(v):
            return int(t)
    return -1


def one(job):
    variant, seed = job
    from genesis_engine import run_simulation
    r = run_simulation(seed=seed, max_ticks=MAX_TICKS,
                       overrides=dict(PARAMS[variant]))
    t = np.array(r.ts_ticks)
    s = np.array(r.ts_mean_s)
    cv = np.array(r.ts_mean_cv)
    cr = np.array(r.ts_clock_r)

    lo = MAX_TICKS * 0.8
    m = t >= lo
    mm = m & (cr >= 0) & (cv < 1.0)

    return dict(
        variant=variant, seed=seed, max_ticks=MAX_TICKS,
        rhist_every=PARAMS[variant]["RHIST_EVERY"],
        rhist_len=PARAMS[variant]["RHIST_LEN"],
        buffer_ticks=PARAMS[variant]["RHIST_EVERY"] * PARAMS[variant]["RHIST_LEN"],
        sample_interval=50,
        def_S=r.sym_mapdef_tick,
        def_CV=first_tick(t, cv, lambda v: v < 1.0),
        def_clock_r=r.sym_clockdef_tick,
        xB=r.ungated_B_tick,
        xC=r.ungated_C_tick,
        ss_clock_r=round(float(cr[mm].mean()), 6) if mm.any() else "",
        ss_cv=round(float(cv[mm].mean()), 6) if mm.any() else "",
        final_pop=r.final_pop,
        total_divisions=r.total_divisions,
        T_div=(round(r.final_pop * MAX_TICKS / r.total_divisions, 1)
               if r.total_divisions > 0 else ""),
    )


if __name__ == "__main__":
    jobs = [(v, s) for v in PARAMS for s in range(SEED0, SEED0 + N_SEEDS)]
    print(f"Task S archival re-run: {len(PARAMS)} parameterisations x "
          f"{N_SEEDS} seeds = {len(jobs)} runs @ {MAX_TICKS} ticks",
          flush=True)
    t0 = time.time()
    rows = []
    with Pool(processes=int(os.environ.get("V6_WORKERS", "16"))) as pool:
        for i, row in enumerate(pool.imap_unordered(one, jobs), 1):
            rows.append(row)
            if i % 20 == 0 or i == len(jobs):
                print(f"  [{i}/{len(jobs)}] {time.time()-t0:.0f}s", flush=True)
    rows.sort(key=lambda r: (r["variant"], r["seed"]))
    path = OUT / os.environ.get(
        "V6_OUT",
        "taskS_buffer_sweep.csv" if os.environ.get("V6_SWEEP") == "1"
        else "taskS_symmetric.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows) in {time.time()-t0:.0f}s")
