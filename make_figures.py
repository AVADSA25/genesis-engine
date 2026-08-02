#!/usr/bin/env python3
"""
Generate the two figures for detector_paper_farina_2026.tex.

fig1_positive_control.pdf
    The positive control. Plants a known Clock-before-Map ordering by
    delaying the Map physically, and shows the measured ordering
    following it. Left: median first-crossing tick of each predicate
    against plant strength. Right: fraction of runs measured Clock-first.
    The left panel also shows the non-orthogonality caveat -- the Clock
    crossing itself shifts when the plant is applied -- which is why
    ordering is judged within-run rather than against a fixed Clock time.

fig2_definedness.pdf
    The constraint. Left: validity of clock_r against buffer span,
    showing that it measures nothing until its history spans ~9 division
    periods. Right: definedness time of each metric on a log axis, with
    the identity definedness = buffer marked, so the reader can see that
    buying validity costs definedness one-for-one.

Both are greyscale-legible and vector. Run: python3 make_figures.py
"""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

ROOT = Path(__file__).parent
RES = ROOT / "results_v6"
FIG = ROOT / "paper" / "submission" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "grid.linewidth": 0.4,
    "lines.linewidth": 1.4,
})

INK = "#1a1a1a"
ACC = "#8c2d04"


def fig_positive_control():
    rows = list(csv.DictReader(open(RES / "taskQ_positive_control.csv")))
    by = defaultdict(list)
    for r in rows:
        by[int(r["plant"])].append(r)

    plants, medB, medC, pct, nboth = [], [], [], [], []
    for p in sorted(by):
        rs = by[p]
        both = [r for r in rs if r["both_fired"] == "1"]
        if not both:
            continue
        plants.append(p)
        medB.append(np.median([int(r["ungated_B"]) for r in both]))
        medC.append(np.median([int(r["ungated_C"]) for r in both]))
        pct.append(100 * sum(r["clock_first"] == "1" for r in both) / len(both))
        nboth.append(len(both))

    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.9))

    a.plot(plants, medC, "o-", color=ACC, label="Map ($S$) crossing", ms=4)
    a.plot(plants, medB, "s--", color=INK, label="Clock (CV) crossing", ms=4)
    a.plot([0, 14000], [0, 14000], ":", color="#999999", lw=0.9,
           label="plant tick (identity)")
    a.set_xlabel("Planted Map delay (ticks)")
    a.set_ylabel("Median first crossing (ticks)")
    a.set_title("The plant moves the Map, not the Clock", pad=6)
    a.legend(frameon=False, loc="upper left", handlelength=2.0)
    a.grid(alpha=0.25)
    a.set_xticks([0, 3000, 6000, 9000, 12000, 15000])
    a.set_xlim(-600, 15200)

    # mark the crossover region
    a.axvspan(1000, 3000, color="#cccccc", alpha=0.35, lw=0)
    a.annotate("ordering flips\nin this band", xy=(2600, 900),
               xytext=(5600, 700), fontsize=7, color="#555555",
               ha="left", va="center",
               arrowprops=dict(arrowstyle="->", lw=0.7, color="#777777"))

    b.plot(plants, pct, "o-", color=ACC, ms=4)
    b.set_xlabel("Planted Map delay (ticks)")
    b.set_ylabel("Runs measured Clock-first (%)")
    b.set_title("Measured ordering follows the plant", pad=6)
    b.set_ylim(-12, 108)
    b.grid(alpha=0.25)
    b.set_xticks([0, 3000, 6000, 9000, 12000, 15000])
    b.set_xlim(-600, 15200)
    for i, (x, y, n) in enumerate(zip(plants, pct, nboth)):
        dy = 7 if y < 50 else 7
        dx = -9 if (i == 0) else (9 if i == 1 else 0)
        b.annotate(f"n={n}", xy=(x, y), xytext=(dx, dy),
                   textcoords="offset points", ha="center",
                   fontsize=6.5, color="#666666")
    b.axhline(2.6, color="#999999", ls=":", lw=0.9)
    b.annotate("2.6% unplanted", xy=(8200, -9), fontsize=7.5,
               color="#555555")

    fig.tight_layout()
    out = FIG / "fig1_positive_control.pdf"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")
    return dict(plants=plants, pct=pct)


def fig_definedness():
    rows = list(csv.DictReader(open(RES / "taskS_buffer_sweep.csv")))
    arms = sorted({r["variant"] for r in rows}, key=lambda v: int(v[3:]))

    bufs, rhos, ps, defs, periods = [], [], [], [], []
    for v in arms:
        rs = [r for r in rows if r["variant"] == v]
        cr = np.array([float(r["ss_clock_r"]) for r in rs if r["ss_clock_r"] != ""])
        cv = np.array([float(r["ss_cv"]) for r in rs if r["ss_clock_r"] != ""])
        rho, p = stats.spearmanr(cr, cv)
        T = np.median([float(r["T_div"]) for r in rs if r["T_div"]])
        buf = int(rs[0]["buffer_ticks"])
        bufs.append(buf)
        rhos.append(rho)
        ps.append(p)
        periods.append(buf / T)
        defs.append(np.median([int(r["def_clock_r"]) for r in rs
                               if int(r["def_clock_r"]) >= 0]))

    conf = list(csv.DictReader(open(RES / "taskS_buffer_confirm.csv")))
    ccr = np.array([float(r["ss_clock_r"]) for r in conf if r["ss_clock_r"] != ""])
    ccv = np.array([float(r["ss_cv"]) for r in conf if r["ss_clock_r"] != ""])
    crho, cp = stats.spearmanr(ccr, ccv)

    defS = np.median([int(r["def_S"]) for r in rows if int(r["def_S"]) >= 0])
    defCV = np.median([int(r["def_CV"]) for r in rows if int(r["def_CV"]) >= 0])

    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.9))

    cols = [ACC if (r < 0 and p < 0.0125) else INK for r, p in zip(rhos, ps)]
    a.axhline(0, color="#999999", lw=0.8)
    a.plot(periods, rhos, "-", color="#bbbbbb", lw=1.0, zorder=1)
    a.scatter(periods, rhos, c=cols, s=34, zorder=3)
    a.scatter([periods[-1]], [crho], marker="D", s=34,
              facecolor="white", edgecolor=ACC, zorder=4)
    for i, (x, y, p) in enumerate(zip(periods, rhos, ps)):
        off = (0, 9) if i == len(periods) - 1 else (0, -14)
        a.annotate(f"p={p:.3f}", xy=(x, y), xytext=off,
                   textcoords="offset points", ha="center", fontsize=6.5,
                   color="#555555")
    a.annotate(f"p={cp:.4f}", xy=(periods[-1], crho), xytext=(16, 3),
               textcoords="offset points", ha="left", fontsize=6.5,
               color=ACC)
    a.set_xlabel("Buffer span (division periods)")
    a.set_ylabel(r"$\rho(\mathrm{clock}_r,\ \mathrm{CV})$")
    a.set_title("The metric measures nothing until\nit spans several periods",
                pad=10)
    a.set_ylim(-0.55, 0.38)
    a.set_xlim(-0.3, 10.6)
    a.annotate("out-of-sample\nconfirmation, fresh seeds",
               xy=(periods[-1] - 0.25, crho), xytext=(4.9, -0.50),
               fontsize=6.8, color=ACC, ha="center", va="center",
               arrowprops=dict(arrowstyle="->", lw=0.7, color=ACC))
    a.grid(alpha=0.25)

    labels = ["$S$ (Map)", "CV (Clock)", r"$\mathrm{clock}_r$" + "\nvalid"]
    vals = [defS, defCV, 24000]
    colors = ["#4a4a4a", "#4a4a4a", ACC]
    ypos = np.arange(len(vals))
    b.barh(ypos, vals, color=colors, height=0.55)
    b.set_yticks(ypos)
    b.set_yticklabels(labels)
    b.set_xscale("log")
    b.set_xlim(80, 60000)
    b.set_xlabel("First tick at which the metric is defined (log)")
    b.set_title("Buying validity costs definedness", pad=10)
    for y, v in zip(ypos, vals):
        b.annotate(f"{v:,.0f}", xy=(v, y), xytext=(5, 0),
                   textcoords="offset points", va="center", fontsize=7.5)
    b.annotate(r"$160\times$ later than $S$", xy=(24000, 2),
               xytext=(38, 14), textcoords="offset points",
               ha="center", fontsize=7.5, color=ACC)
    b.grid(alpha=0.25, axis="x")
    b.invert_yaxis()

    fig.tight_layout()
    out = FIG / "fig2_definedness.pdf"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    fig_positive_control()
    fig_definedness()
