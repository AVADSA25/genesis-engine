# Task Q — Positive control: can this model detect an ordering that exists?

**Pre-registered 31 July 2026, BEFORE the experiment runs.**

---

## Why this exists

The v6 audit has reported a series of null and negative results: the
published ordering was an artifact, the imposed-regularity test could
not adjudicate, the interval-floor reformulation failed.

**But no one has ever established that this model can detect an ordering
when one genuinely exists.** Without that, every null is uninterpretable
— it could mean "no ordering" or "blind instrument", and we cannot tell
which. Reporting nulls from an uncalibrated instrument is the same class
of error as the original paper, pointed the other way.

This is the calibration that should have existed on day one.

## Design

Plant a **known temporal ordering in the physics**, not in the detector,
then measure it with the ungated method and see whether the measurement
recovers what was planted.

**The plant.** `PLANT_MAP_DELAY = T`: pattern stability is held at zero
for every cell until tick `T`. Spatial organization is therefore
*physically impossible* before `T`, by construction of the dynamics.
Nothing about the phase detector, the gate, or CV is involved in
creating the plant.

**Why a time-based plant.** Gating the plant on division regularity
would inherit the same definedness floor we are trying to test around.
A wall-clock plant is independent of every metric under study, so the
ground truth is known exactly.

**The measurement.** Ungated first crossings, as used throughout the
audit: `ungated_B_tick` (first tick population CV < 0.25) and
`ungated_C_tick` (first tick population S > 0.25).

**Conditions.** `PLANT_MAP_DELAY` ∈ {0 (no plant), 1000, 3000, 5000,
7000, 10000, 14000}, 40 seeds each, 20,000 ticks, natural division.

The Clock predicate crosses naturally at ≈4,250 ticks (measured, Task 1).
So plants below ~4,250 should yield Map-first, and plants above should
yield Clock-first. **The ordering must flip as the plant crosses the
Clock time.**

## Pre-registered predictions

- **Q1 (recovery).** Measured `ungated_C_tick` tracks `PLANT_MAP_DELAY`:
  Spearman ρ > **+0.8** across conditions.
- **Q2 (flip).** Clock-before-Map rate is **< 20%** at
  `PLANT_MAP_DELAY = 1000` and **> 80%** at `PLANT_MAP_DELAY = 10000`.
- **Q3 (fidelity).** In the largest-plant condition (14,000), measured
  `ungated_C_tick` ≥ 14,000 in **> 90%** of runs — the plant is not
  leaking.

## Decision rule, fixed in advance

| outcome | meaning |
|---|---|
| Q1, Q2 and Q3 all pass | **Instrument is calibrated.** The ungated measurement detects a real ordering when one exists. Every null reported in the v6 audit is therefore informative, and the correction note stands as written. |
| Q1 or Q3 fails | **Instrument is blind.** The measurement cannot recover a known planted ordering, so no null it produced carries information. The correction note must be softened: several claims currently stated as findings become "not measurable with this method". |
| Q2 alone fails | **Partial.** The measurement tracks timing but not ordering. Report the limitation explicitly. |

## Commitments

1. One run. No parameter adjustment if the result is unfavourable.
2. Thresholds (+0.8, 20%, 80%, 90%) fixed now and not movable.
3. **A failure here is the most consequential outcome of the whole
   audit** and will be reported first and prominently, because it would
   retroactively weaken conclusions already published in the repository.
4. Reported whichever way it comes out, before the correction note is
   posted.
