#!/usr/bin/env python3
"""
v6 TASK 2b/2c — is the Delta-CV back-reaction an estimator artifact?

The published Delta-CV results (v5.1c, v5.3) compare population-mean
division CV between an early-post-latch window and a late window.

Concern. The production estimator `mean_cv` uses every interval a cell
has accumulated (>= 3, capped at 12), so the SAMPLE SIZE behind each CV
grows over a run. `numpy.std()` defaults to ddof=0, which is biased LOW
at small n. A growing n therefore INFLATES the CV estimate over time for
purely statistical reasons, independent of any dynamics.

Direction of the bias (important, and opposite to one common intuition):
    small n  -> std underestimated -> CV underestimated
    large n  -> bias shrinks       -> CV estimate rises
    => estimator alone pushes Delta-CV (late - early) POSITIVE.

So:
  1D published Delta-CV = -0.215 runs AGAINST the estimator direction
     -> cannot be explained by this artifact; more likely dynamical.
  2D published Delta-CV = +0.057 runs WITH the estimator direction
     -> is exactly what the artifact would produce; must be tested.

Test. Recompute Delta-CV using a fixed-n estimator (`mean_cv_fix`,
exactly the last N_CV_FIXED intervals from cells having at least that
many) so sample size cannot drift, and compare against the production
estimator on the SAME runs.

Requires re-simulation: the archived timeseries store only the
population-mean CV, not per-cell interval histories, so the fixed-n
estimator cannot be reconstructed post-hoc. This is a deviation from
"zero new simulation" and is stated as such. Sampling stays at the
production 50-tick interval, so runs are cheap.

Output: results_v6/estimator_{geom}.csv
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
N_FIX = int(os.environ.get("V6_N_FIX", "5"))

if GEOM == "2d":
    MAX_TICKS = int(os.environ.get("V6_MAX_TICKS", "10000"))
    WIN_E = (500, 1500)
    WIN_L = (3500, 4500)
else:
    MAX_TICKS = int(os.environ.get("V6_MAX_TICKS", "80000"))
    WIN_E = (2000, 3000)
    WIN_L = (50000, 60000)


def window_mean(ticks, vals, lo, hi, undefined=1.0):
    """Mean of vals over [lo,hi), ignoring undefined sentinel values.
    Returns (mean or None, n_defined, n_total)."""
    sel = [(t, v) for t, v in zip(ticks, vals) if lo <= t < hi]
    if not sel:
        return None, 0, 0
    good = [v for _t, v in sel if v < undefined]
    if not good:
        return None, 0, len(sel)
    return sum(good) / len(good), len(good), len(sel)


def one_run(seed):
    if GEOM == "2d":
        from genesis_engine_2d import run_simulation
    else:
        from genesis_engine import run_simulation
    r = run_simulation(seed=seed, max_ticks=MAX_TICKS,
                       overrides={"N_CV_FIXED": N_FIX})
    phc = r.phase_C_tick
    phd = r.phase_D_tick
    if phc <= 0:
        return None
    t = r.ts_ticks
    out = dict(seed=seed, phase_C=phc, phase_D=phd,
               reached_D=phd > 0, max_ticks=MAX_TICKS)
    for tag, series in (("prod", r.ts_mean_cv), ("fix", r.ts_mean_cv_fix)):
        e, ne, te = window_mean(t, series, phc + WIN_E[0], phc + WIN_E[1])
        l, nl, tl = window_mean(t, series, phc + WIN_L[0], phc + WIN_L[1])
        out[f"{tag}_early"] = round(e, 6) if e is not None else ""
        out[f"{tag}_late"] = round(l, 6) if l is not None else ""
        out[f"{tag}_delta"] = round(l - e, 6) if (e is not None and l is not None) else ""
        out[f"{tag}_ndef_early"] = ne
        out[f"{tag}_ntot_early"] = te
        out[f"{tag}_ndef_late"] = nl
        out[f"{tag}_ntot_late"] = tl
    return out


if __name__ == "__main__":
    print(f"v6 Task 2b/2c estimator test [{GEOM.upper()}] "
          f"{N_SEEDS} seeds x {MAX_TICKS} ticks; "
          f"early=phc+{WIN_E}, late=phc+{WIN_L}", flush=True)
    t0 = time.time()
    rows = []
    with Pool(processes=min(18, os.cpu_count() or 4)) as pool:
        for i, row in enumerate(pool.imap_unordered(one_run, range(N_SEEDS)), 1):
            if row:
                rows.append(row)
            if i % 10 == 0:
                print(f"  [{i}/{N_SEEDS}] {time.time()-t0:.0f}s", flush=True)
    rows.sort(key=lambda r: r["seed"])
    path = OUT / f"estimator_{GEOM}_n{N_FIX}.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows) in {time.time()-t0:.0f}s")
