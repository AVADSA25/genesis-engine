#!/usr/bin/env python3
"""
Negative controls for detector_audit.py.

A check that always fires is worth nothing, and we shipped one: C3
computed `si = sample_interval or int(med)` with sample_interval always
None, so its condition `med == si` reduced to "the median is an
integer", and its second clause `(a <= med).mean() > 0.5` is true of
almost any sample by the definition of a median. It could not emit a
pass. That is the same defect as the gated predicate the paper is about,
committed inside the tool built to detect it.

The lesson generalises past that one bug: every check needs an input on
which it is REQUIRED to stay silent. These tests supply those inputs.

Run: python3 tools/test_detector_audit.py
"""
import csv
import importlib.util
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("da", HERE / "detector_audit.py")
da = importlib.util.module_from_spec(spec)
spec.loader.exec_module(da)

PASS, FAIL = [], []


def check(name, cond):
    (PASS if cond else FAIL).append(name)
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}")


def write_summary(root, delays, extra=None):
    d = root / "sub"
    d.mkdir(parents=True, exist_ok=True)
    cols = ["seed", "phase_B_tick", "phase_C_tick"] + list((extra or {}).keys())
    with open(d / "summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for i, dl in enumerate(delays):
            row = [i, 1000, 1000 + dl]
            for k in (extra or {}):
                row.append(extra[k][i])
            w.writerow(row)
    return root


def c3_hits(root):
    return [f for f in da.check_delay_equals_interval(root)
            if f.check == "C3 delay==interval"]


def test_c3_fires_on_grid_locked_delays():
    with tempfile.TemporaryDirectory() as t:
        root = write_summary(Path(t), [50] * 18 + [100, 150])
        check("C3 fires when delays are pinned to the sampling grid",
              len(c3_hits(root)) == 1)


def test_c3_silent_on_real_spread():
    """The control that the shipped version could not pass."""
    with tempfile.TemporaryDirectory() as t:
        root = write_summary(Path(t), [50, 100, 200, 300, 400, 400, 500, 600,
                                       700, 800, 900, 1000, 250, 350, 450,
                                       550, 650, 750, 850, 950])
        check("C3 silent on a genuine spread sharing the same grid",
              c3_hits(root) == [])


def test_c3_silent_on_non_grid_delays():
    with tempfile.TemporaryDirectory() as t:
        root = write_summary(Path(t), [37, 113, 229, 341, 467, 509, 613, 733,
                                       829, 941, 1063, 1171, 1289, 1361, 1487,
                                       1523, 1637, 1741, 1853, 1907])
        check("C3 silent on unquantised delays", c3_hits(root) == [])


def test_comment_header_does_not_blind_the_tool():
    """The other failure: a disclosure note made a file invisible."""
    with tempfile.TemporaryDirectory() as t:
        root = write_summary(Path(t), [50] * 18 + [100, 150])
        p = root / "sub" / "summary.csv"
        p.write_text("# WITHDRAWN - stale copy\n# see results/\n" + p.read_text())
        hits = c3_hits(root)
        check("a '#' disclosure header does not hide a file from C3",
              len(hits) == 1)


def test_missing_columns_report_rather_than_skip():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t) / "sub"
        d.mkdir(parents=True)
        (d / "summary.csv").write_text("seed,unrelated\n1,2\n3,4\n")
        out = da.check_delay_equals_interval(Path(t))
        check("a summary.csv lacking the expected columns yields a finding",
              any("unparsed" in f.check for f in out))


if __name__ == "__main__":
    print("detector_audit negative controls\n")
    for fn in [test_c3_fires_on_grid_locked_delays,
               test_c3_silent_on_real_spread,
               test_c3_silent_on_non_grid_delays,
               test_comment_header_does_not_blind_the_tool,
               test_missing_columns_report_rather_than_skip]:
        fn()
    print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
    sys.exit(1 if FAIL else 0)
