#!/usr/bin/env python3
"""
v6 TASK Q — positive control.

Pre-registered at ba1c5fe BEFORE running.

Plants a known ordering in the PHYSICS (PLANT_MAP_DELAY holds pattern
stability at zero until tick T, making spatial organization physically
impossible before then) and asks whether the ungated measurement used
throughout the v6 audit recovers it.

If it does not, every null reported in the audit is uninterpretable and
the correction note must be softened.

KNOWN NON-ORTHOGONALITY, noted before running: suppressing S also
suppresses the S-linked metabolic bonuses, which changes population
dynamics and therefore shifts when CV becomes computable. The plant is
thus not a pure Map-only intervention. This is why BOTH crossings are
measured per run rather than assuming a fixed Clock time -- ordering is
judged within each run, on that run's own two measurements.

Output: results_v6/taskQ_positive_control.csv
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

PLANTS = [0, 1000, 3000, 5000, 7000, 10000, 14000]
N_SEEDS = int(os.environ.get("V6_N_SEEDS", "40"))
MAX_TICKS = int(os.environ.get("V6_MAX_TICKS", "20000"))


def one(job):
    plant, seed = job
    from genesis_engine import run_simulation
    ov = {} if plant == 0 else {"PLANT_MAP_DELAY": int(plant)}
    r = run_simulation(seed=seed, max_ticks=MAX_TICKS, overrides=ov)
    ub, uc = r.ungated_B_tick, r.ungated_C_tick
    if ub > 0 and uc > 0:
        clock_first = ub < uc
    else:
        clock_first = None
    return dict(
        plant=plant, seed=seed, max_ticks=MAX_TICKS,
        ungated_B=ub, ungated_C=uc,
        clock_first=("" if clock_first is None else int(clock_first)),
        both_fired=int(ub > 0 and uc > 0),
        c_after_plant=("" if uc <= 0 else int(uc >= plant)),
        gated_B=r.phase_B_tick, gated_C=r.phase_C_tick,
        final_pop=r.final_pop, final_S=round(r.final_mean_s, 4),
    )


if __name__ == "__main__":
    jobs = [(p, s) for p in PLANTS for s in range(N_SEEDS)]
    print(f"Task Q: {len(PLANTS)} plants x {N_SEEDS} seeds = {len(jobs)} runs "
          f"@ {MAX_TICKS} ticks", flush=True)
    t0 = time.time()
    rows = []
    with Pool(processes=int(os.environ.get("V6_WORKERS", "16"))) as pool:
        for i, row in enumerate(pool.imap_unordered(one, jobs), 1):
            rows.append(row)
            if i % 40 == 0 or i == len(jobs):
                print(f"  [{i}/{len(jobs)}] {time.time()-t0:.0f}s", flush=True)
    rows.sort(key=lambda r: (r["plant"], r["seed"]))
    path = OUT / "taskQ_positive_control.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows) in {time.time()-t0:.0f}s")
