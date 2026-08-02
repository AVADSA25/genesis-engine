# Task S — RESULTS: the asymmetry is physical, not a defect

Pre-registered at `0ff4ed0`. **S1 fails.** Per the decision rule fixed
in advance, S2 and S3 were not computed.

---

## What was attempted

Replace the Clock metric (CV of division intervals, undefined until four
divisions) with one having no definedness floor, so Clock and Map switch
on at comparable times and their first-crossing times can be compared.

## What happened — twice

**First attempt (short buffer, 400 ticks, lags 30–200).**
Invalidated before S1 was run at scale:

```
rho(clock_r, CV) = +0.0420, p = 0.897   (n = 12, steady state)
```

No correlation with regularity at all. Cause: the measured division
period is **~2,495 ticks**; the lag window reached only 200. The metric
was measuring short-timescale growth smoothness.

**Second attempt (valid buffer, 6,000 ticks, lags 150–3,000).**
Buffer widened to span the division period. Definedness, 10 seeds,
medians:

| metric | defined at tick | asymmetry vs S |
|---|---|---|
| **S** (Map) | **150** | — |
| **CV** (old Clock) | **4,825** | 32× |
| **clock_r** (new Clock) | **6,000** | **40×** |

`rho(clock_r, CV) = −0.2364, p = 0.511` — correct sign, still not
significant.

**S1 criterion:** the two metrics must become defined within 20% of each
other. Observed ratio: **40×**. The redesign made the asymmetry *worse
than the problem it was built to solve.*

---

## Why this is a finding rather than a failure

The redesign could not have worked, for a reason that has nothing to do
with implementation.

**To measure how regular a periodic process is, you must observe several
of its periods.** This is a time-frequency constraint, not a coding
choice. Every candidate Clock metric inherits it:

| metric | minimum observation |
|---|---|
| CV of division intervals | 4 divisions ≈ 4 × 2,495 ticks |
| autocorrelation of radius | ≥ 2 periods ≈ 5,000 ticks |
| *any* per-cell regularity measure | several division periods |

Meanwhile **S** measures spatial correlation of a reaction-diffusion
field, whose intrinsic correlation time is ~40 ticks. It is defined
after ~150.

The ~4,000-tick gap is therefore set by the **ratio of the two
phenomena's intrinsic timescales** — a slow periodic process
(~2,500 ticks) against a fast field process (~40 ticks) — and not by any
choice we made.

### Consequence: Defect 3 is partly not a defect

The v6 audit catalogued the CV definedness floor as **Defect 3**, an
implementation error. That was only half right.

- The *specific* floor (four divisions, from `len(division_times) >= 3`)
  is an implementation choice and could be loosened somewhat.
- The *existence* of a floor of order several division periods is
  **physical and unavoidable**.

**No simulation redesign removes it.** Not this one, not a better one.

### Consequence: the ordering question is malformed as posed

"Does Clock precede Map?" asked as *which metric crosses its threshold
first* compares two quantities that become knowable at different times
**by their nature**. The comparison measures the timescale ratio, not
the dynamics.

This explains, in one stroke, why every approach in this audit failed
the same way — the gate, the definedness floor, the imposed-CV grid, the
interval floor. All were attempts to time-order two phenomena that
cannot be timed against each other.

---

## The constructive part

Ordering claims of this kind should be tested by **intervention**, not
by first-crossing timing:

> *Does perturbing division regularity change spatial organization?*

That is causal, has no definedness problem, and is exactly what Task 3
did by imposing CV as a control variable. Its answer was **no support**
for the theory (ρ(CV, S) = +0.22, opposite in sign, and it did not
survive its confound checks).

So the theory has been tested by the method that *can* test it, and it
did not find support. It has not been tested by the method that
*cannot* — and never could have been.

### And a laboratory escapes this entirely

A microscope tracking individual lineages measures both quantities
continuously from t = 0. It does not wait for a statistic to become
computable, because it records events rather than estimating summaries.
Experiment E in `LAB_PROTOCOL.md` is not a fallback — it is the only
instrument that can pose the question as originally intended.

---

## Evaluation criteria used

- S1 threshold (20% agreement in definedness) fixed in the
  pre-registration; not moved.
- The first `clock_r` parameterisation was disqualified on a validity
  check (correlation with CV) **before** S1 was evaluated, not after.
- Definedness measured as the first sampled tick at which each metric
  returns a value, medians over 10 seeds.
- S2 and S3 not computed, per the pre-registered decision rule.
