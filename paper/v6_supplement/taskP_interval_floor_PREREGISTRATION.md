# Task P — Interval-floor hypothesis: PRE-REGISTRATION

**Written 31 July 2026, BEFORE any analysis is run.**
Committed before the experiment executes. Any deviation from this
document must be declared explicitly in the results report.

---

## Motivation

The original theory states: *temporal regularity (Clock) precedes and
enables spatial organization (Map).*

The v6 audit established that the published evidence for this was
produced by a broken detector, and that the imposed-regularity
experiment (Task 3) could not adjudicate it. In that experiment,
sweeping imposed CV from 0 to 1.0 produced ρ(CV, S) = +0.22 — a weak
drift in the *opposite* direction to the theory.

**But the theory may have named the wrong variable.**

Physical reasoning: patterns need a consolidation time (measured
independently at ~1,350 ticks — the median first crossing of S > 0.25).
If a cell's division interval exceeds that, its pattern consolidates;
if it falls short, the pattern is scrambled before it can persist.

Under this account, what matters is **the length of the shortest
uninterrupted interval**, not the *variance* of intervals. Variance
matters only insofar as it produces short intervals.

This also explains why Task 3 came out flat: raising CV under a Gamma
distribution adds short intervals *and* long ones. If long-interval
cells consolidate well enough to offset short-interval cells, the
population mean barely moves — which is what was observed.

**Reformulated hypothesis (H1):**
> A cell's own *minimum recent division interval* predicts its own
> pattern stability. There exists an interval threshold below which S
> is suppressed. Division *regularity* has no effect once minimum
> interval is controlled.

---

## Design

**Two experiments. The first is the primary test.**

### P-A — Natural division (PRIMARY)

Division is **geometric (the Adder mechanism), not forced**. This
avoids every artifact of the Task 3 design: no premature splitting, no
imposed distribution, no unphysical regime. The natural spread of
division intervals arises from growth noise and resource dynamics.

- 3 lipid-supply conditions (0.008 / 0.015 / 0.025) to widen the
  natural interval range
- 75 seeds per condition = 225 runs, 20,000 ticks
- Per-cell logging across the steady-state window (last 20%, all cells):
  `min_interval`, `mean_interval`, `max_interval`, `n_intervals`,
  `pattern_s`, `rv` (reduced volume)

### P-B — Forced division, physical window (SECONDARY)

Re-uses the Task 3 design (T ∈ {3200, 6400}, 9 CV levels) but logs
per-cell interval *statistics* rather than only the last interval, so
minimum-interval and CV can be separated within a condition.

---

## Pre-registered predictions

If **H1 is true**:

- **P1.** ρ(min_interval, cell_S) > +0.25, and **larger in magnitude**
  than ρ(imposed_CV, cell_S) = +0.22 from Task 3.
- **P2.** A threshold exists: mean S in the lowest min-interval bin is
  at least **0.15 lower** than in the highest bin.
- **P3.** Controlling for min_interval, the CV effect attenuates by
  **more than 50%** (P-B only).
- **P4.** The threshold, if present, falls within **2×** of the
  independently measured consolidation time (~1,350 ticks), i.e.
  between ~675 and ~2,700 ticks.

If **H1 is false**, expect ρ(min_interval, S) ≈ 0 and no threshold.

## Decision rule, fixed in advance

| outcome | conclusion |
|---|---|
| P1 **and** P2 hold | **Interval-floor supported.** The original theory had the right structure and the wrong variable. Report as a reformulation. |
| P1 **or** P2 holds, not both | **Partial.** Report as suggestive, not established. Do not reframe the theory on this alone. |
| Neither holds | **Interval-floor not supported.** The model cannot rescue the theory; it goes to the lab untested. |

P3 and P4 are informative but **not** decision criteria — they refine
the mechanism, they do not license the claim.

## Anti-p-hacking commitments

1. **One run.** The experiment executes once. No re-running with
   adjusted parameters if the result is unfavourable.
2. **No threshold tuning.** The 0.25 / 0.15 / 50% / 2× values above are
   fixed now and will not be moved after seeing data.
3. **Both experiments reported**, regardless of whether they agree.
4. **Confounds checked before conclusions**, using the same discipline
   as Task A1: population match, temporal-window match, and a stated
   check on whether the effect is carried by barely-dividing cells.
5. **The null is a publishable outcome.** If H1 fails, the correction
   note and rewrite proceed unchanged, and this document is published
   alongside the negative result.

## Known risk to this test

`min_interval` and `n_intervals` are not independent: a cell with few
divisions has few intervals to take a minimum over, so its minimum is
biased upward. Since barely-dividing cells were the confound that sank
Task A1, this must be checked explicitly — the analysis will report
ρ(min_interval, S) **stratified by n_intervals**, and any effect present
only in low-n cells will be reported as an artifact, not a finding.
