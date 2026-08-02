# Task R — RESULTS: a correction to my own published claim

Pre-registered at `aad89e8` before running. **My stated prediction was
wrong, and the pre-registered decision rule did not anticipate the
outcome that actually occurred.** Both are reported here.

---

## What I predicted

> "At `MAX_CELLS = 100` the population saturates the cap and competes
> for fixed resource... A lower cap gives each cell more resource →
> more divisions each → **fewer barely-dividing cells**. I therefore
> expect the fraction to drop."

## What happened

| MAX_CELLS | n obs | <2 divisions | <4 divisions | mean divisions |
|---|---|---|---|---|
| 20 | 32,799 | **80.5%** | 96.5% | 1.36 |
| 50 | 60,959 | **11.4%** | 11.8% | 11.43 |
| 100 | 60,973 | **11.3%** | 11.7% | 11.43 |

The fraction went **up**, not down, at the tight cap — and the effect is
non-monotonic, so R3 fails.

**Mechanism (not the one I hypothesised).** Division is *blocked* at the
cap:

```python
if rv < crit and len(cells) + len(to_add) < MAX_CELLS:
```

A tight cap therefore **suppresses** division. At `MAX_CELLS = 20` the
population saturates almost immediately and divisions are gated off, so
cells accumulate almost no intervals (mean 1.36 divisions). Resource per
cell was never the binding constraint; the cap itself was.

## Pre-registered criteria

| | criterion | result |
|---|---|---|
| R1 structural | ≥40% at cap 20 | 80.5% — **passes**, but via cap-blocking, not the hypothesised mechanism |
| R2 parameter | <25% at cap 20 | **fails** |
| R3 dose | monotonic decrease | **fails** — non-monotonic |

Applying the decision rule literally gives "structural, claim stands."
**That reading would be wrong**, for a reason the pre-registration did
not foresee.

---

## The actual finding — I mischaracterised the limit

Comparing like with like, natural division, same cap:

| run length | <2 divisions | mean divisions |
|---|---|---|
| 20,000 ticks | **13.3%** | 6.48 |
| 40,000 ticks | **11.3%** | 11.43 |

**Under natural division only 11–13% of cells barely divide, not ~50%.**

The ~50% figure came from **Task A1's forced-division design**, which
imposed division periods of 3,200–6,400 ticks inside 20,000-tick runs.
Under that design most cells necessarily divide rarely — 44.0% to 56.2%
across the CV sweep. That is a property of *that experimental design*,
not of the model.

I generalised it to "a property of the simulation class, not of one
study." **That generalisation was wrong and is withdrawn.**

## What changes

- **The methods paper's "hard limit" claim is corrected.** The model
  does not have a ~50% barely-dividing population under its own natural
  dynamics. The correct statement: *the Task 3 forced-division design,
  which imposes long periods within a fixed run length, produces
  populations in which ~50% of cells barely divide, and A1's confound
  check is specific to that design.*
- **Task A1's verdict is unaffected.** Its 44–56% figure was measured
  on its own forced-division runs and is correct for those runs. The
  "cannot currently answer" conclusion stands.
- **Task P's stratification is unaffected** — it stratified by observed
  division count rather than assuming a population-level fraction.

## What does *not* change

The ordering question remains blocked, but by the **CV definedness
floor**, not by the barely-dividing fraction. CV requires four completed
divisions before it exists at all, so the *first-crossing time* is
floor-limited regardless of how many divisions cells eventually
accumulate. That is what the symmetric-metrics redesign (Task S)
addresses, and this result does not reopen the ordering question by
itself.

## Why this is reported prominently

The pre-registration committed: *"If R2 holds... the revision is
reported prominently rather than folded quietly into a later commit."*
R2 did not hold, but a correction is required anyway, for a reason the
pre-registration did not anticipate. The spirit of the commitment
applies, so it is reported the same way.

This is the fourth time in this audit that a number reproduced correctly
while being a number of the wrong thing. Here the number (44–56%) was
right and its **scope** was wrong.

## Evaluation criteria used

- Thresholds (40%, 25%) fixed in the pre-registration; not moved.
- Like-for-like comparison holds division mode (natural), cap (100) and
  measurement window constant, varying only run length.
- 154,731 cell-observations across 120 runs of 40,000 ticks, plus
  176,693 observations from the 20,000-tick natural-division runs.
