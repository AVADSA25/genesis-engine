#!/usr/bin/env python3
"""
v6 TASK 1 ANALYSIS — sampling resolution + ungated ordering.

Consumes results_v6/resolution_{geom}_{sample}tick.csv produced by
experiment_v6_resolution.py and answers, for each geometry:

  Q1. What is the delay distribution at fine resolution?
      (median, IQR, min, max, % at the resolution floor)
  Q2. In how many runs did the raw S predicate fire BEFORE the raw
      CV predicate? (ungated -- this is the honest ordering test)
  Q3. How does this compare side-by-side with the published
      50-tick numbers?
  Q4. Does a real positive gap survive, or does it collapse?

Writes: paper/v6_supplement/task1_resolution.md
"""
import csv
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
RES = ROOT / "results_v6"
OUT = ROOT / "paper" / "v6_supplement"
OUT.mkdir(parents=True, exist_ok=True)

# Published 50-tick baselines, recomputed directly from the archived
# summary files (verified: 1D median 50, 90.0% floor; 2D median 50,
# 97.5% floor).
PUBLISHED = {
    "1d": dict(path=ROOT / "results/summary.csv", n=482, median=50,
               floor_pct=90.0, mean=242.9, sd=2318.8, max=38400),
    "2d": dict(path=ROOT / "results_2d/summary.csv", n=198, median=50,
               floor_pct=97.5, mean=55.8, sd=40.7, max=450),
}


def describe(arr, floor):
    arr = np.asarray(arr, dtype=float)
    n = len(arr)
    if n == 0:
        return None
    at_floor = int((arr <= floor).sum())
    return dict(
        n=n,
        mean=float(arr.mean()),
        sd=float(arr.std(ddof=1)) if n > 1 else 0.0,
        median=float(np.median(arr)),
        q1=float(np.percentile(arr, 25)),
        q3=float(np.percentile(arr, 75)),
        min=float(arr.min()),
        max=float(arr.max()),
        at_floor=at_floor,
        floor_pct=100.0 * at_floor / n,
    )


def load(geom, sample):
    p = RES / f"resolution_{geom}_{sample}tick.csv"
    if not p.exists():
        return None
    return list(csv.DictReader(open(p)))


def analyse(geom, sample, lines):
    rows = load(geom, sample)
    if not rows:
        lines.append(f"\n## {geom.upper()} — NO DATA (expected "
                     f"results_v6/resolution_{geom}_{sample}tick.csv)\n")
        return None

    n_total = len(rows)

    def ival(r, k):
        v = r.get(k, "")
        if v in ("", None):
            return None
        try:
            return int(float(v))
        except ValueError:
            return None

    ung_delays, gat_delays = [], []
    s_first = cv_first = tie = incomplete = 0
    s_first_seeds = []

    for r in rows:
        ub, uc = ival(r, "ungated_B"), ival(r, "ungated_C")
        gb, gc = ival(r, "gated_B"), ival(r, "gated_C")
        if gb and gc and gb > 0 and gc > 0:
            gat_delays.append(gc - gb)
        if ub and uc and ub > 0 and uc > 0:
            ung_delays.append(uc - ub)
            if uc < ub:
                s_first += 1
                s_first_seeds.append((r["seed"], ub, uc, uc - ub))
            elif uc > ub:
                cv_first += 1
            else:
                tie += 1
        else:
            incomplete += 1

    ung = describe(ung_delays, sample)
    gat = describe(gat_delays, sample)
    pub = PUBLISHED[geom]

    lines.append(f"\n## {geom.upper()} geometry — {n_total} seeds "
                 f"@ {sample}-tick sampling\n")

    lines.append("### Q1. Delay distribution at fine resolution\n")
    lines.append("| measure | UNGATED (honest) | GATED (published-style detector) |")
    lines.append("|---|---|---|")
    if ung and gat:
        lines.append(f"| n (both predicates fired) | {ung['n']} | {gat['n']} |")
        lines.append(f"| median | **{ung['median']:.0f}** | {gat['median']:.0f} |")
        lines.append(f"| IQR | [{ung['q1']:.0f}, {ung['q3']:.0f}] | "
                     f"[{gat['q1']:.0f}, {gat['q3']:.0f}] |")
        lines.append(f"| mean ± SD | {ung['mean']:.1f} ± {ung['sd']:.1f} | "
                     f"{gat['mean']:.1f} ± {gat['sd']:.1f} |")
        lines.append(f"| min | {ung['min']:.0f} | {gat['min']:.0f} |")
        lines.append(f"| max | {ung['max']:.0f} | {gat['max']:.0f} |")
        lines.append(f"| at resolution floor (≤{sample}) | "
                     f"**{ung['at_floor']}/{ung['n']} = {ung['floor_pct']:.1f}%** | "
                     f"{gat['at_floor']}/{gat['n']} = {gat['floor_pct']:.1f}% |")
    lines.append("")

    lines.append("### Q2. Ungated ordering — did S ever fire first?\n")
    lines.append(f"- CV predicate fired strictly first (Clock→Map): "
                 f"**{cv_first}/{len(ung_delays)}**")
    lines.append(f"- S predicate fired strictly first (Map→Clock): "
                 f"**{s_first}/{len(ung_delays)}**")
    lines.append(f"- Exact simultaneous tie (same tick): **{tie}/{len(ung_delays)}**")
    lines.append(f"- Runs where one predicate never fired: {incomplete}/{n_total}")
    if len(ung_delays):
        pct = 100.0 * cv_first / len(ung_delays)
        lines.append(f"- Clock-before-Map rate (ungated): **{pct:.1f}%**")
    if s_first_seeds:
        lines.append(f"\n**Map-before-Clock violations** "
                     f"(seed, cv_tick, S_tick, delay):")
        for sd, ub, uc, d in s_first_seeds[:25]:
            lines.append(f"  - seed {sd}: CV@{ub}, S@{uc}, delay {d}")
        if len(s_first_seeds) > 25:
            lines.append(f"  - ... and {len(s_first_seeds)-25} more")
    lines.append("")

    lines.append("### Q3. Side-by-side vs published 50-tick data\n")
    lines.append("| | published @50-tick | this run @"
                 f"{sample}-tick (gated) | this run @{sample}-tick (ungated) |")
    lines.append("|---|---|---|---|")
    lines.append(f"| n | {pub['n']} | {gat['n'] if gat else '—'} | "
                 f"{ung['n'] if ung else '—'} |")
    lines.append(f"| median delay | {pub['median']} | "
                 f"{gat['median']:.0f} | **{ung['median']:.0f}** |")
    lines.append(f"| mean delay | {pub['mean']:.1f} | {gat['mean']:.1f} | "
                 f"{ung['mean']:.1f} |")
    lines.append(f"| % at floor | {pub['floor_pct']:.1f}% | "
                 f"{gat['floor_pct']:.1f}% | **{ung['floor_pct']:.1f}%** |")
    lines.append(f"| max delay | {pub['max']} | {gat['max']:.0f} | "
                 f"{ung['max']:.0f} |")
    lines.append("")

    lines.append("### Q4. Does a real positive gap survive?\n")
    if ung:
        if ung["median"] <= sample and ung["floor_pct"] >= 50:
            verdict = (
                f"**NO — the gap collapses.** At {sample}-tick resolution the "
                f"ungated median delay is {ung['median']:.0f} tick(s) and "
                f"{ung['floor_pct']:.1f}% of runs sit at the resolution floor. "
                f"The apparent 50-tick gap in the published data was an "
                f"artifact of the 50-tick measurement interval: the two "
                f"predicates cross within one measurement of each other. "
                f"At this resolution 'sequential' is NOT distinguishable "
                f"from 'simultaneous'.")
        elif ung["median"] > 5 * sample:
            verdict = (
                f"**YES — a real positive gap survives.** The ungated median "
                f"delay is {ung['median']:.0f} ticks, "
                f"{ung['median']/sample:.0f}x the {sample}-tick measurement "
                f"floor, with IQR [{ung['q1']:.0f}, {ung['q3']:.0f}] and only "
                f"{ung['floor_pct']:.1f}% of runs at the floor. The ordering "
                f"is resolvable and is not a sampling artifact.")
        else:
            verdict = (
                f"**PARTIAL.** Ungated median delay {ung['median']:.0f} ticks "
                f"(floor {sample}), IQR [{ung['q1']:.0f}, {ung['q3']:.0f}], "
                f"{ung['floor_pct']:.1f}% at floor. The gap is positive but "
                f"small relative to the dynamics; report with the "
                f"distribution, not the mean.")
        lines.append(verdict)
    lines.append("")
    return dict(geom=geom, ungated=ung, gated=gat,
                cv_first=cv_first, s_first=s_first, tie=tie)


if __name__ == "__main__":
    sample = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    lines = [
        "# v6 Task 1 — Unconditional predicate logging + "
        "high-resolution resample",
        "",
        "## What this tests",
        "",
        "The published detector `detect_phase()` latches Map (C) only if "
        "Clock (B) latched at a **strictly earlier tick**:",
        "",
        "```python",
        "if ph.B and ph.B_tick < tick and not ph.C and mean_s > PHASE_C_S:",
        "```",
        "",
        "Two consequences follow mechanically:",
        "",
        "1. Clock-before-Map is **true by construction**. The published "
        "1,845/1,845 result cannot come out any other way, so it is not "
        "evidence for the ordering hypothesis.",
        "2. The minimum observable delay is pinned to **one sample "
        "interval**, which is why 90.0% of published 1D runs and 97.5% of "
        "2D runs report a delay of exactly 50 ticks.",
        "",
        "This task adds ungated first-crossing logging (each predicate "
        "evaluated every measurement tick, independently, with no "
        "sequential gate) and re-runs at fine sampling. The gated detector "
        "is kept running alongside, unchanged, for comparison.",
        "",
        "Instrumentation: `genesis_engine.py` / `genesis_engine_2d.py`, "
        "fields `ungated_B_tick`, `ungated_C_tick`, `cosat_tick`, "
        "`ungated_clock_before_map`. Default behaviour is unchanged; "
        "the new fields are purely additive.",
        "",
        "---",
    ]
    out = [analyse(g, sample, lines) for g in ("1d", "2d")]

    lines += ["", "---", "", "## Evaluation criteria used", "",
              "- **Resolution floor** = the sampling interval. A delay at "
              "or below it is unresolvable.",
              "- **Gap survives** iff ungated median delay > 5x the "
              "sampling interval AND fewer than 50% of runs sit at the floor.",
              "- **Gap collapses** iff ungated median <= sampling interval "
              "AND >= 50% of runs sit at the floor.",
              "- Ordering is judged on the **ungated** predicates only. The "
              "gated detector cannot falsify the hypothesis and is reported "
              "for comparison, not as evidence.",
              ""]

    path = OUT / "task1_resolution.md"
    path.write_text("\n".join(lines))
    print("\n".join(lines))
    print(f"\n\nWrote {path}")
