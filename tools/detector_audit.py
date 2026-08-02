#!/usr/bin/env python3
"""
detector_audit.py — a checklist runner for phase-detection studies.

Motivation. The Genesis Engine paper reported a 100% ordering result
(1,845/1,845, p ~ 1e-146) that was produced entirely by measurement
artifacts. Three rounds of competent external conceptual review missed
all of them, because conceptual review reads the ARGUMENT and nobody
ran the DETECTOR against itself.

Every defect found in the v6 audit is mechanically detectable. This
script encodes them so the next study catches them before publication
rather than after.

CHECKS
  C1  gated predicate      a predicate whose latching is conditioned on
                           another predicate's state -> ordering results
                           become unfalsifiable
  C2  definedness floor    a metric undefined below n observations ->
                           its first-crossing time measures the floor,
                           not a transition
  C3  delay == interval    a reported delay whose median equals the
                           sampling interval -> the "gap" is the
                           measurement grid
  C4  mean-only heavy tail a summary reported as mean +/- SD where
                           |SD| > |mean| -> the mean is not a summary
  C5  circular effect size an effect-size DV causally downstream of the
                           grouping variable -> measures the coupling
                           constants, not an effect
  C6  degenerate groups    an effect size where either group has n < 10,
                           or the grouping thresholds leave a gap that
                           contains zero observations
  C8  pooled-not-stratified  a correlation reported over pooled data
                           whose sign or magnitude does not survive
                           stratification by an entanglement variable.
                           THREE Simpson's paradoxes were found in this
                           project by hand and none of C1-C7 catches
                           any of them. In a model of a dividing
                           population almost every quantity is entangled
                           with division count, so pooling produces sign
                           reversals as a matter of course.
  C7  undeclared reference EVERY reported quantity must declare what its
                           reference point is. This is the check that
                           would have caught the most expensive errors
                           in this project, including ones made DURING
                           the audit: a number can reproduce exactly and
                           still be a number of the wrong thing. A delay
                           anchored on phase_C_tick reproduces perfectly
                           while measuring time-since-CV-became-
                           computable rather than time-since-Map-latched.
                           Reproducibility is not validity.

USAGE
    python3 tools/detector_audit.py            # audit this repo
    python3 tools/detector_audit.py --path X   # audit elsewhere

Exit code 0 if no findings, 1 otherwise.
"""
from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np

# Quantities whose reference point must be declared, and the file that
# declares them. See C7.
MANIFEST_NAME = "reported_quantities.json"


class Finding:
    def __init__(self, check, severity, location, detail, remedy):
        self.check = check
        self.severity = severity
        self.location = location
        self.detail = detail
        self.remedy = remedy

    def __str__(self):
        return (f"[{self.severity.upper():8s}] {self.check}  {self.location}\n"
                f"           {self.detail}\n"
                f"           remedy: {self.remedy}")


# ── C1: gated predicates ──────────────────────────────────────────────
def check_gated_predicates(root):
    """Find `if <state>.X and <state>.X_tick < tick and ... not <state>.Y`
    patterns: predicate Y cannot latch unless X latched strictly earlier."""
    out = []
    for py in sorted(root.rglob("*.py")):
        if ".git" in py.parts or "__pycache__" in py.parts:
            continue
        try:
            src = py.read_text()
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(src.splitlines(), 1):
            # a condition that references another predicate's latch tick
            if re.search(r"\bif\b.*\.\w*_tick\s*<\s*\w+.*\bnot\b", line):
                out.append(Finding(
                    "C1 gated-predicate", "critical", f"{py.name}:{i}",
                    f"predicate latching conditioned on another "
                    f"predicate's latch tick: {line.strip()[:88]}",
                    "an ordering claim from this detector is unfalsifiable; "
                    "log ungated first-crossings alongside and report those"))
    return out


# ── C2: definedness floors ────────────────────────────────────────────
def check_definedness_floor(root):
    """Find `if len(x) >= N:` guards feeding a statistic, plus a
    sentinel default -- the statistic is undefined until N observations
    accumulate, so its first crossing measures the floor."""
    out = []
    for py in sorted(root.rglob("*.py")):
        if ".git" in py.parts or "__pycache__" in py.parts:
            continue
        try:
            lines = py.read_text().splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(lines, 1):
            m = re.search(r"if\s+len\(([\w\.\[\]]+)\)\s*>=\s*(\d+)", line)
            if not m:
                continue
            window = "\n".join(lines[i - 1:i + 8])
            if re.search(r"=\s*np\.mean\(|\.std\(\)|/\s*\w*mean", window):
                sentinel = re.search(r"if\s+\w+\s+else\s+([\d\.]+)", window)
                out.append(Finding(
                    "C2 definedness-floor", "critical", f"{py.name}:{i}",
                    f"statistic requires >= {m.group(2)} observations of "
                    f"`{m.group(1)}`"
                    + (f", defaulting to {sentinel.group(1)} until then"
                       if sentinel else ""),
                    "the first tick this crosses a threshold measures when "
                    "it became COMPUTABLE, not when the system changed; "
                    "report time-to-definedness alongside any latch time"))
    return out


# ── CSV reading ───────────────────────────────────────────────────────
# Read a CSV, skipping leading `#` comment lines.
#
# This exists because of a self-inflicted C0-class failure. A staleness
# disclosure was prepended to web/results/summary.csv as `#` comments.
# csv.DictReader treated the first comment as the header, every expected
# column went missing, the `not rows or KEY not in rows[0]` guards below
# skipped the file, and two real findings silently disappeared from the
# report -- total 30 -> 29. Nothing errored. The tool went blind to a
# file it was asked to check, and the drop went unnoticed for a day
# because the audit was not re-run after the note was added.
#
# A checker that silently skips what it cannot parse reports a clean
# bill of health for files it never read. read_csv therefore strips
# comments, and callers use want_cols() so that an unreadable or
# unexpected file produces a FINDING rather than silence.
def read_csv(path):
    try:
        with open(path) as f:
            lines = [ln for ln in f if not ln.lstrip().startswith("#")]
    except OSError:
        return None
    if not lines:
        return []
    return list(csv.DictReader(lines))


def want_cols(out, path, rows, cols, check):
    """True if `rows` is usable and has `cols`; else record why and stop."""
    if rows is None:
        out.append(Finding(f"{check} unreadable", "major", str(path),
                           "file could not be read",
                           "a check that cannot read its input is not a "
                           "passing check; fix the path or the permissions"))
        return False
    if not rows:
        return False
    missing = [c for c in cols if c not in rows[0]]
    if missing:
        hdr = ",".join(list(rows[0].keys())[:3])
        out.append(Finding(f"{check} unparsed", "major", str(path),
                           f"expected column(s) {missing} absent; header "
                           f"parsed as `{hdr}...`",
                           "the file was skipped rather than checked -- "
                           "verify the header row is the first "
                           "non-comment line"))
        return False
    return True


# ── C3 / C4: data-level checks ────────────────────────────────────────
def check_delay_equals_interval(root, sample_interval=None):
    out = []
    for csvp in sorted(root.rglob("summary.csv")):
        rows = read_csv(csvp)
        if not want_cols(out, csvp, rows, ["phase_B_tick", "phase_C_tick"],
                         "C3 delay==interval"):
            continue
        d = []
        for r in rows:
            try:
                b, c = int(r["phase_B_tick"]), int(r["phase_C_tick"])
                if b > 0 and c > 0:
                    d.append(c - b)
            except (KeyError, ValueError):
                continue
        if len(d) < 10:
            continue
        a = np.array(d, float)
        med = float(np.median(a))

        # The grid is INFERRED from the data (gcd of the observed delays)
        # or supplied by the caller -- never defined to be the median.
        #
        # An earlier version computed `si = sample_interval or int(med)`
        # with sample_interval always None, so `med == si` held for any
        # integral median; and `(a <= med).mean() > 0.5` holds for almost
        # any sample, by the definition of a median. The check could not
        # fail. In a tool whose C1 detects predicates that cannot emit a
        # violation, C3 was a check that could not emit a pass.
        #
        # The test below can fail, and does: it requires the median to be
        # ONE grid step and a majority of delays to sit EXACTLY there.
        nz = [int(x) for x in d if x > 0]
        if not nz:
            continue
        grid = float(sample_interval) if sample_interval else float(
            np.gcd.reduce(np.array(nz, dtype=np.int64)))
        if grid <= 0:
            continue
        atfloor = float((a == grid).mean())
        if med == grid and atfloor > 0.5:
            out.append(Finding(
                "C3 delay==interval", "critical",
                str(csvp.relative_to(root)),
                f"median delay = {med:.0f} = the inferred sampling grid "
                f"({grid:.0f}); {100*atfloor:.1f}% of runs sit exactly on "
                f"it (IQR [{np.percentile(a,25):.0f}, "
                f"{np.percentile(a,75):.0f}])",
                "re-run at finer sampling before claiming a temporal gap; "
                "if the delay tracks the interval it IS the interval"))
    return out


def check_mean_only_heavy_tail(root):
    out = []
    for jp in sorted(root.rglob("*.json")):
        if ".git" in jp.parts:
            continue
        try:
            data = json.loads(jp.read_text())
        except (OSError, ValueError):
            continue

        def walk(node, path=""):
            if isinstance(node, dict):
                mean = node.get("mean")
                sd = node.get("std", node.get("sd"))
                if isinstance(mean, (int, float)) and isinstance(sd, (int, float)):
                    if abs(mean) > 1e-12 and abs(sd) > abs(mean):
                        has_med = "median" in node
                        out.append(Finding(
                            "C4 mean-only-heavy-tail",
                            "major" if has_med else "critical",
                            f"{jp.name}:{path}",
                            f"mean={mean:.4g}, SD={sd:.4g} "
                            f"(SD/|mean| = {abs(sd/mean):.1f}x)"
                            + ("; median IS present alongside"
                               if has_med else "; NO median present"),
                            "report median + IQR; a mean whose SD exceeds "
                            "it describes outliers, not the distribution"))
                for k, v in node.items():
                    walk(v, f"{path}/{k}")
            elif isinstance(node, list):
                for i, v in enumerate(node[:50]):
                    walk(v, f"{path}[{i}]")

        walk(data)
    return out


# ── C5 / C6: effect sizes ─────────────────────────────────────────────
def check_effect_sizes(root):
    out = []
    for py in sorted(root.rglob("*.py")):
        if ".git" in py.parts or "__pycache__" in py.parts or py.name == "detector_audit.py":
            continue
        try:
            lines = py.read_text().splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(lines, 1):
            if not re.search(r"hedges_g\(|cohens_d\(|effect_size\(", line):
                continue
            ctx = "\n".join(lines[max(0, i - 12):i + 2])
            groups = re.findall(
                r'\[\s*r\[[\'"](\w+)[\'"]\]\s+for\s+\w+\s+in\s+\w+\s+'
                r'if\s+r\[[\'"](\w+)[\'"]\]\s*([<>]=?)\s*([\d\.]+)', ctx)
            if len(groups) >= 2:
                dv = groups[0][0]
                gv = groups[0][1]
                thresholds = sorted(float(g[3]) for g in groups)
                out.append(Finding(
                    "C5 effect-size-DV", "major", f"{py.name}:{i}",
                    f"DV = `{dv}`, grouping variable = `{gv}`. "
                    f"Verify `{gv}` is not causally upstream of `{dv}`.",
                    f"if `{gv}` multiplies any term that determines "
                    f"`{dv}`, the effect size measures the coupling "
                    f"constants; name the DV explicitly in the paper"))
                if len(thresholds) >= 2 and thresholds[0] < thresholds[-1]:
                    out.append(Finding(
                        "C6 group-gap", "major", f"{py.name}:{i}",
                        f"grouping leaves the interval "
                        f"[{thresholds[0]}, {thresholds[-1]}] unassigned",
                        "count observations in the gap; if zero, the split "
                        "is degenerate and g is not interpretable. "
                        "Report both group sizes with the effect size"))
    return out


def check_group_sizes(root):
    """Recompute effect-size group sizes from archived summaries."""
    out = []
    for csvp in sorted(root.rglob("summary.csv")):
        rows = read_csv(csvp)
        if not want_cols(out, csvp, rows, ["final_mean_s"], "C6 group sizes"):
            continue
        hi = [r for r in rows if float(r["final_mean_s"]) > 0.3]
        lo = [r for r in rows if float(r["final_mean_s"]) < 0.1]
        gap = [r for r in rows if 0.1 <= float(r["final_mean_s"]) <= 0.3]
        for name, grp in (("organized", hi), ("disorganized", lo)):
            if 0 < len(grp) < 10:
                out.append(Finding(
                    "C6 tiny-group", "critical",
                    str(csvp.relative_to(root)),
                    f"'{name}' group has n = {len(grp)} "
                    f"(other group n = {len(hi) if name!='organized' else len(lo)})",
                    "an effect size against an n<10 arm is not "
                    "interpretable; report n for both groups"))
        if hi and lo and not gap:
            out.append(Finding(
                "C6 degenerate-split", "major",
                str(csvp.relative_to(root)),
                f"zero observations fall between the thresholds "
                f"(0.1, 0.3); split is degenerate, not merely unbalanced",
                "the two groups are separated by construction; the effect "
                "size describes the thresholds, not a gradient"))
    return out


# ── C7: undeclared reference points ───────────────────────────────────
def check_reference_points(root):
    """Every reported quantity must declare its reference point.

    This is the check that would have caught the most expensive errors
    in this project -- including errors made DURING the audit. A delay
    anchored on `phase_C_tick` reproduces exactly while measuring
    time-since-CV-became-computable rather than time-since-Map-latched.
    Reproducibility is not validity: you must state what the number is a
    number OF.
    """
    out = []
    manifest = root / "paper" / MANIFEST_NAME
    if not manifest.exists():
        out.append(Finding(
            "C7 no-manifest", "critical", f"paper/{MANIFEST_NAME}",
            "no manifest of reported quantities exists, so no quantity "
            "declares its reference point",
            f"create paper/{MANIFEST_NAME}: for every headline number, "
            "record {name, value, script, reference_point, "
            "population, temporal_window}. A quantity anchored on a "
            "detector output must say so."))
        return out
    try:
        entries = json.loads(manifest.read_text())
    except ValueError as e:
        out.append(Finding("C7 bad-manifest", "critical",
                           f"paper/{MANIFEST_NAME}", f"unparseable: {e}",
                           "fix the JSON"))
        return out
    required = ("reference_point", "population", "temporal_window", "script")
    for e in entries if isinstance(entries, list) else []:
        missing = [k for k in required if not e.get(k)]
        if missing:
            out.append(Finding(
                "C7 undeclared-reference", "critical",
                f"{MANIFEST_NAME}:{e.get('name','?')}",
                f"missing {', '.join(missing)}",
                "state explicitly what this number is measured FROM; "
                "if the anchor is a detector output, the causal reading "
                "is not licensed even when the arithmetic reproduces"))
        ref = str(e.get("reference_point", "")).lower()
        if any(t in ref for t in ("phase_b_tick", "phase_c_tick",
                                  "phase_d_tick", "latched")):
            out.append(Finding(
                "C7 detector-anchored", "major",
                f"{MANIFEST_NAME}:{e.get('name','?')}",
                f"reference point is a detector output "
                f"(`{e.get('reference_point')}`)",
                "the measurement may be valid arithmetic while its causal "
                "label is not; report it as measurement-only unless the "
                "detector itself has been validated"))
    return out



# ── C8: pooled statistics that do not survive stratification ──────────
def check_pooled_not_stratified(root):
    """Recompute reported correlations both pooled and stratified.

    Three Simpson's paradoxes were found by hand in this project:
      rho(T_div, S)        +0.43 pooled, -0.60..-0.75 within lipid level
      the 1,845 denominator  a shared OAT baseline summed across rows
      rho(min_interval, S) +0.38 pooled, -0.07 within division-count

    None of C1-C7 catches any of them. They share one cause: in a model
    of a dividing population, nearly every quantity is entangled with
    how many times a cell has divided. Pooling across that variable
    reverses signs routinely.

    This check flags any correlation whose sign flips, or whose
    magnitude drops by more than half, under stratification.
    """
    out = []
    try:
        from scipy.stats import spearmanr
    except ImportError:
        return out

    # (csv glob, x column, y column, stratify-by column, label)
    specs = [
        ("taskP_*_obs.csv", "min_interval", "cell_S", "n_intervals",
         "min-interval vs S"),
        ("taskA1_obs.csv", "realized_interval", "cell_S", "n_intervals",
         "realized-interval vs S"),
    ]
    for pattern, xc, yc, sc, label in specs:
        for csvp in sorted((root / "results_v6").glob(pattern)) \
                if (root / "results_v6").exists() else []:
            rows = read_csv(csvp)
            if not rows or xc not in rows[0] or sc not in rows[0]:
                continue
            def col(c):
                v = []
                for r in rows:
                    try:
                        v.append(float(r[c]))
                    except (TypeError, ValueError):
                        v.append(np.nan)
                return np.array(v)
            x, y, st = col(xc), col(yc), col(sc)
            m = ~(np.isnan(x) | np.isnan(y) | np.isnan(st)) & (x > 0)
            if m.sum() < 200:
                continue
            x, y, st = x[m], y[m], st[m]
            pooled, _ = spearmanr(x, y)
            strat = []
            for lo, hi in ((1, 2), (3, 4), (5, 8), (9, 999)):
                k = (st >= lo) & (st <= hi)
                if k.sum() < 50:
                    continue
                r_, _ = spearmanr(x[k], y[k])
                if r_ == r_:
                    strat.append(r_)
            if len(strat) < 2:
                continue
            mean_strat = float(np.mean(strat))
            flipped = (pooled * mean_strat) < 0
            shrunk = abs(mean_strat) < 0.5 * abs(pooled)
            if flipped or shrunk:
                out.append(Finding(
                    "C8 pooled-not-stratified",
                    "critical" if flipped else "major",
                    f"{csvp.name}: {label}",
                    f"pooled rho = {pooled:+.4f}, mean within-stratum rho = "
                    f"{mean_strat:+.4f} (strata: "
                    + ", ".join(f"{r_:+.3f}" for r_ in strat) + ")"
                    + ("  -- SIGN REVERSES" if flipped else
                       "  -- magnitude more than halves"),
                    f"a Simpson's paradox on `{sc}`. Report the "
                    f"stratified association, not the pooled one; the "
                    f"pooled sign is an artifact of the entanglement"))
    return out


CHECKS = [
    ("C1 gated predicates", check_gated_predicates),
    ("C2 definedness floors", check_definedness_floor),
    ("C3 delay == sampling interval", check_delay_equals_interval),
    ("C4 mean-only heavy tails", check_mean_only_heavy_tail),
    ("C5 effect-size DV", check_effect_sizes),
    ("C6 group sizes", check_group_sizes),
    ("C7 reference points", check_reference_points),
    ("C8 pooled vs stratified", check_pooled_not_stratified),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", default=".", help="repo root to audit")
    args = ap.parse_args()
    root = Path(args.path).resolve()

    print("=" * 74)
    print(f"detector_audit.py — {root}")
    print("=" * 74)

    all_f = []
    for name, fn in CHECKS:
        try:
            found = fn(root)
        except Exception as exc:                      # noqa: BLE001
            print(f"\n## {name}: ERROR {exc}")
            continue
        all_f.extend(found)
        print(f"\n## {name}: {len(found)} finding(s)")
        for f in found[:12]:
            print(f)
        if len(found) > 12:
            print(f"           ... and {len(found)-12} more")

    crit = sum(1 for f in all_f if f.severity == "critical")
    print("\n" + "=" * 74)
    print(f"TOTAL: {len(all_f)} findings ({crit} critical)")
    print("=" * 74)
    return 1 if all_f else 0


if __name__ == "__main__":
    sys.exit(main())
