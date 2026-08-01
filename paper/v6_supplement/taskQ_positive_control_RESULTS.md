# Task Q — Positive control: RESULTS

Evaluated against the pre-registration locked at `ba1c5fe` **before**
this experiment ran. Thresholds were not moved.

**Question.** Can this model's ungated measurement detect a Clock→Map
ordering when one genuinely exists? Without an answer, every null in
the v6 audit is uninterpretable — "no ordering" and "blind instrument"
look identical.

**Method.** A known ordering was planted in the **physics**, not the
detector: `PLANT_MAP_DELAY = T` holds pattern stability at zero for
every cell until tick `T`, so spatial organization is physically
impossible before then. No involvement of the phase detector, the
sequential gate, or CV. Ground truth is therefore known exactly.

---

## Results — 280 runs, 7 plant levels × 40 seeds

| plant | n | both predicates fired | median measured C | Clock-first | C ≥ plant |
|---|---|---|---|---|---|
| 0 (none) | 40 | 38/40 | 1,400 | 2.6% | — |
| 1,000 | 40 | 38/40 | 1,600 | **2.6%** | 100% |
| 3,000 | 40 | 32/40 | 4,325 | 75.0% | 100% |
| 5,000 | 40 | 27/40 | 6,150 | 100% | 100% |
| 7,000 | 40 | 27/40 | 8,100 | 100% | 100% |
| 10,000 | 40 | 21/40 | 10,750 | **100%** | 100% |
| 14,000 | 40 | 17/40 | 14,450 | 100% | **100%** |

## Pre-registered predictions

| | criterion | result | |
|---|---|---|---|
| **Q1** recovery | ρ(plant, measured C) > +0.8 | **+0.9560** (p = 2.3e-107, n = 200) | ✅ **PASS** |
| **Q2** flip | Clock-first <20% @1,000 and >80% @10,000 | **2.6%** → **100%** | ✅ **PASS** |
| **Q3** fidelity | C ≥ plant in >90% @14,000 | **100%** | ✅ **PASS** |

## Verdict — INSTRUMENT CALIBRATED

The ungated measurement recovers a planted ordering with high fidelity,
and the measured ordering **flips** as the plant crosses the natural
Clock time (~4,250 ticks): Map-first below it, Clock-first above it,
with the crossover falling between plants of 1,000 and 5,000 exactly as
predicted.

Two consequences:

1. **The v6 nulls are informative.** When the unplanted model reports
   Clock-first in ≈1% of runs, that is a genuine measurement of the
   model's dynamics, not a blind instrument. Per the pre-registered
   decision rule, **the correction note stands as written and requires
   no softening.**
2. **The measurement is not biased toward Map-first.** That was the
   obvious objection to the ≈1% figure. Planting the ordering flips the
   measurement to 100% Clock-first, so the ≈1% reflects the dynamics,
   not a directional defect in the method.

## Caveats, stated rather than buried

**Thinning at large plants.** The "both predicates fired" column falls
from 38/40 (no plant) to 17/40 (plant = 14,000): larger plants leave
less run-time for S to recover and cross, so fewer runs contribute.
Q1's ρ is computed on 200 of 280 runs, and the largest-plant cells are
the thinnest. This does not threaten the verdict — the flip is 2.6% vs
100%, nowhere near a decision boundary — but the effective N is smaller
than the headline.

**The plant is not perfectly orthogonal.** Noted before running:
suppressing S also suppresses the S-linked metabolic bonuses, which
changes population dynamics and shifts when CV becomes computable
(seed 0: `phase_B` moved 5100 → 3500 under the plant). This is why both
crossings are measured *within each run* and ordering is judged on that
run's own two numbers, never against an assumed Clock time. A plant that
altered only the Map channel would require decoupling S from metabolism,
which would change the model under test.

**What this does not show.** It shows the measurement works. It does
not show the model's unplanted dynamics are physically realistic, and
it says nothing about whether Clock→Map holds in real protocells.

## Evaluation criteria used

- Thresholds (+0.8, 20%, 80%, 90%) fixed in the pre-registration and
  not adjusted after seeing data.
- Ordering judged per run from that run's own `ungated_B_tick` and
  `ungated_C_tick`; runs where either never fired are excluded and the
  exclusion count is reported per condition.
- One run of the experiment, as committed. No parameter adjustment.
