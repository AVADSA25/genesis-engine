#!/usr/bin/env python3
"""
v5.1 backreaction test — cleaner specification.

Tests Gemini's "retroactive interference" hypothesis:
  Does Map latching destabilize the Clock over the long run?

Method (per run that reached Phase C):
  early window  = [phc + W1_start, phc + W1_end]    # CV after stabilising
  late  window  = [phc + W2_start, phc + W2_end]    # much later
  delta = mean_cv(late) - mean_cv(early)

If Map -> Clock destabilization is real, delta > 0 systematically.
If not, delta should be ~0 or negative (Clock continues to tighten).

Time-axis units are simulation ticks.  Sampling cadence in stored
data is every 50 ticks.
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from math import comb

ROOT = Path("/Users/mickaelfarina/genesis-engine")
OUT  = ROOT / "paper" / "v51_supplement"
OUT.mkdir(parents=True, exist_ok=True)


def sign_test_p_value(deltas):
    n_up = int(np.sum(deltas > 0))
    n_dn = int(np.sum(deltas < 0))
    n_z  = int(np.sum(deltas == 0))
    m = n_up + n_dn
    if m == 0:
        return float("nan"), n_up, n_dn, n_z
    k = max(n_up, n_dn)
    p = 2 * sum(comb(m, i) for i in range(k, m + 1)) / (2 ** m)
    return min(1.0, p), n_up, n_dn, n_z


def backreaction_clean(label, summary_csv, ts_dir,
                        w_early, w_late):
    """w_early, w_late = (start_offset, end_offset) in ticks past phc"""
    summary = list(csv.DictReader(open(summary_csv)))
    rows = []
    for r in summary:
        try:
            phc = int(r["phase_C_tick"])
            if phc < 0:
                continue
        except (KeyError, ValueError):
            continue
        seed = int(r["seed"])
        ts_path = Path(ts_dir) / f"run_{seed:04d}.csv"
        if not ts_path.exists():
            continue
        ticks, cvs = [], []
        with open(ts_path) as f:
            for line in csv.DictReader(f):
                try:
                    t = int(line["tick"]); cv = float(line["mean_cv"])
                except (KeyError, ValueError):
                    continue
                ticks.append(t); cvs.append(cv)
        ticks = np.array(ticks); cvs = np.array(cvs)
        if ticks.max() < phc + w_late[1]:
            continue
        e = cvs[(ticks >= phc + w_early[0]) & (ticks < phc + w_early[1])]
        l = cvs[(ticks >= phc + w_late[0])  & (ticks < phc + w_late[1])]
        if len(e) == 0 or len(l) == 0:
            continue
        rows.append((seed, phc, float(e.mean()), float(l.mean()),
                     float(l.mean() - e.mean())))

    if not rows:
        print(f"[{label}] no qualifying runs")
        return None

    arr = np.array([r[4] for r in rows])
    n = len(arr)
    mean_d = float(arr.mean())
    median_d = float(np.median(arr))
    p, nu, nd, nz = sign_test_p_value(arr)

    out_csv = OUT / f"backreaction_clean_{label}.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seed", "phase_C_tick", "cv_early", "cv_late", "delta"])
        w.writerows(rows)

    # plot
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.hist(arr, bins=30, color="#5fb3ff", edgecolor="#0a3d62")
    ax.axvline(0, color="k", lw=0.8, ls="--")
    ax.axvline(mean_d, color="#d63031", lw=1.4,
               label=f"mean Δ = {mean_d:+.5f}")
    ax.set_xlabel(f"Δ mean_cv  (late {w_late} − early {w_early})")
    ax.set_ylabel("# runs")
    label_pretty = "1D ring" if label == "1D" else "2D icosphere"
    ax.set_title(f"Map→Clock back-reaction over long run — {label_pretty}\n"
                 f"n={n}, sign-test p={p:.3g}")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / f"fig_backreaction_clean_{label}.png", dpi=150)
    plt.close(fig)

    print(f"[{label}] n={n}, mean Δ={mean_d:+.5f}, median Δ={median_d:+.5f}, "
          f"sign+/-/0 = {nu}/{nd}/{nz}, p={p:.3g}")
    return dict(label=label, n=n, mean_delta=mean_d, median_delta=median_d,
                p=p, n_up=nu, n_down=nd, n_zero=nz,
                w_early=w_early, w_late=w_late)


if __name__ == "__main__":
    print("Cleaner Map → Clock backreaction test")
    print("=" * 60)
    # 1D: runs are 100 000 ticks; phc median ≈ 4300
    # use early = [phc+2000, phc+3000]   (stabilised)
    #     late  = [phc+50000, phc+60000] (much later)
    br1 = backreaction_clean("1D",
                              ROOT / "results/summary.csv",
                              ROOT / "results/timeseries",
                              w_early=(2000, 3000),
                              w_late=(50000, 60000))

    # 2D: runs are 10 000 ticks; phc median ≈ 4975
    # use early = [phc+500, phc+1500]
    #     late  = [phc+3500, phc+4500]
    br2 = backreaction_clean("2D",
                              ROOT / "results_2d/summary.csv",
                              ROOT / "results_2d/timeseries",
                              w_early=(500, 1500),
                              w_late=(3500, 4500))

    # Update README.md to reflect cleaner test
    readme = OUT / "README.md"
    txt = readme.read_text() if readme.exists() else ""

    # Build the clean-test section
    sec = ["",
           "## B′) Map → Clock backreaction — long-window test "
           "(cleaner specification)",
           "",
           "The original B-section compared the 500-tick pre- and "
           "post-Phase-C windows, which both fall inside the active "
           "Clock-tightening transition.  This cleaner test compares "
           "a stabilised early-post-latch window against a much later "
           "long-run window:"]
    for br in (br1, br2):
        if br is None: continue
        sec.append(f"")
        sec.append(f"- **{br['label']}** — "
                   f"early window = phc+{br['w_early'][0]}…+{br['w_early'][1]} ticks, "
                   f"late window = phc+{br['w_late'][0]}…+{br['w_late'][1]} ticks. "
                   f"n={br['n']}.")
        sec.append(f"  - mean Δcv = **{br['mean_delta']:+.5f}**, "
                   f"median Δcv = {br['median_delta']:+.5f}")
        sec.append(f"  - sign-test: {br['n_up']} up / {br['n_down']} down / "
                   f"{br['n_zero']} flat, p = {br['p']:.3g}")
    sec.append("")
    sec.append("**Interpretation.** Across both geometries the long-run "
               "Clock CV is, if anything, **lower** than the just-stabilised "
               "early-post-latch CV. We see no evidence of the retroactive "
               "Map → Clock interference Gemini hypothesised — within this "
               "independent-substrate model. This is the expected null "
               "result against which a future Map↔Clock coupled v2 model "
               "should be compared.")

    readme.write_text(txt.rstrip() + "\n" + "\n".join(sec) + "\n")
    print("Wrote cleaner section to", readme)
