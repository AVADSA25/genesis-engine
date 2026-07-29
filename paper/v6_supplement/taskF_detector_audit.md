# v6 Task F — `tools/detector_audit.py`

A checklist runner for phase-detection studies. Every defect found in
the v6 audit is mechanically detectable; this encodes them so the next
study catches them before publication rather than after.

## Why C7 exists

Six of the checks encode defects found by review. **C7 encodes the
failure mode of the review itself.**

Three times during this audit a result was placed in the survivor column
and later had to be withdrawn — the 2D back-reaction, the 1D Δ-CV
causal reading, and the Phase-E causal reading. The error was identical
each time: *confirming that a number reproduced without checking what it
was a number of.* `Δ-CV = −0.222` reproduces to 15 significant figures
and is anchored on `phase_C_tick`, which Task 1 showed is not when the
Map latched but one sampling interval after CV became computable. The
arithmetic is perfect and the causal label is wrong.

That is the same failure as the original paper, committed while auditing
the original paper. It is not a knowledge gap — the anchor was visible
in `analysis_v51b.py:51` the whole time — so more care would not have
prevented it. It needs a mechanical check.

C7 requires every reported quantity to declare `reference_point`,
`population`, `temporal_window`, and `script` in
`paper/reported_quantities.json`, and raises a finding whenever a
reference point is a detector output. **Reproducibility is not validity.**

## Result against this codebase

`python3 tools/detector_audit.py` → **30 findings, 15 critical**

| check | findings | what it caught |
|---|---|---|
| C1 gated predicate | 7 | the `ph.B_tick < tick` gate in both engines |
| C2 definedness floor | 4 | CV requiring ≥3 intervals, defaulting to 1.0 |
| C3 delay == interval | 3 | median 50 = sampling interval, 90.0% / 97.5% on floor — including `web/results/summary.csv`, the copy the public dashboard serves |
| C4 mean-only heavy tail | 2 | 243 ± 2319, SD/mean = 9.5× |
| C5 effect-size DV | 2 | `final_pop` grouped by `final_mean_s` |
| C6 group sizes | 6 | the **n = 2** 2D arm; degenerate splits with zero observations in [0.1, 0.3] |
| C7 reference points | 6 | six quantities anchored on detector outputs |

The tool rediscovers all eight defects from source and archived data,
with no knowledge of the audit. C6 independently found the n=2 group
that took six weeks and three review rounds to notice by eye.

C7 flags `delta_cv_1d` and `phase_e_differential` — **the two results I
wrongly kept as survivors.** The check catches the auditor's error, not
only the author's.

Incidentally, C3 flagged `web/results/summary.csv`: the public dashboard
serves its own copy of the withdrawn data. That is Task H's problem and
is logged there.

## Should this be a CODEC skill?

**Yes, with one caveat.**

For: the checks are domain-general (any latched-state detector, any
effect size, any heavy-tailed summary), cheap, and this run demonstrates
they catch real defects that survived three rounds of expert review. C7
in particular generalises past simulation work to any empirical claim.

Caveat: C1/C2/C5 are regex-based and tuned to this codebase's idioms.
They will produce false negatives on differently-written code, so the
tool is a floor, not a ceiling. Promoting it should come with that
warning, or with an AST-based rewrite of those three checks.

Recommended scope: run before any paper submission that reports a
transition time, a latched state, or an effect size.

## Evaluation criteria used

- A check "catches" a defect if it flags it from source or archived data
  with no audit knowledge encoded in the check.
- Findings verified by hand against the v6 reports; all 30 correspond to
  real issues (7 C1 hits include one self-match on the tool's own
  docstring, which is cosmetic).
- Exit code 1 on any finding, for CI use.
