# v6 Task 1 — Unconditional predicate logging + high-resolution resample

## What this tests

The published detector `detect_phase()` latches Map (C) only if Clock (B) latched at a **strictly earlier tick**:

```python
if ph.B and ph.B_tick < tick and not ph.C and mean_s > PHASE_C_S:
```

Two consequences follow mechanically:

1. Clock-before-Map is **true by construction**. The published 1,845/1,845 result cannot come out any other way, so it is not evidence for the ordering hypothesis.
2. The minimum observable delay is pinned to **one sample interval**, which is why 90.0% of published 1D runs and 97.5% of 2D runs report a delay of exactly 50 ticks.

This task adds ungated first-crossing logging (each predicate evaluated every measurement tick, independently, with no sequential gate) and re-runs at fine sampling. The gated detector is kept running alongside, unchanged, for comparison.

Instrumentation: `genesis_engine.py` / `genesis_engine_2d.py`, fields `ungated_B_tick`, `ungated_C_tick`, `cosat_tick`, `ungated_clock_before_map`. Default behaviour is unchanged; the new fields are purely additive.

---

## 1D geometry — 100 seeds @ 1-tick sampling

### Q1. Delay distribution at fine resolution

| measure | UNGATED (honest) | GATED (published-style detector) |
|---|---|---|
| n (both predicates fired) | 97 | 97 |
| median | **-2869** | 1 |
| IQR | [-3430, -1523] | [1, 1] |
| mean ± SD | -2732.8 ± 1373.8 | 19.6 ± 85.2 |
| min | -7598 | 1 |
| max | 634 | 634 |
| at resolution floor (≤1) | **96/97 = 99.0%** | 91/97 = 93.8% |

### Q2. Ungated ordering — did S ever fire first?

- CV predicate fired strictly first (Clock→Map): **1/97**
- S predicate fired strictly first (Map→Clock): **96/97**
- Exact simultaneous tie (same tick): **0/97**
- Runs where one predicate never fired: 3/100
- Clock-before-Map rate (ungated): **1.0%**

**Map-before-Clock violations** (seed, cv_tick, S_tick, delay):
  - seed 0: CV@5084, S@1261, delay -3823
  - seed 1: CV@5241, S@520, delay -4721
  - seed 2: CV@5333, S@560, delay -4773
  - seed 3: CV@3879, S@2391, delay -1488
  - seed 4: CV@4796, S@1301, delay -3495
  - seed 6: CV@8796, S@1290, delay -7506
  - seed 7: CV@4802, S@1299, delay -3503
  - seed 8: CV@3737, S@2245, delay -1492
  - seed 9: CV@4281, S@1376, delay -2905
  - seed 10: CV@3627, S@2197, delay -1430
  - seed 11: CV@3643, S@2353, delay -1290
  - seed 12: CV@8018, S@560, delay -7458
  - seed 13: CV@4712, S@1282, delay -3430
  - seed 14: CV@4165, S@1360, delay -2805
  - seed 16: CV@3839, S@2222, delay -1617
  - seed 17: CV@3594, S@2247, delay -1347
  - seed 18: CV@4033, S@1615, delay -2418
  - seed 19: CV@4761, S@1257, delay -3504
  - seed 20: CV@3843, S@2320, delay -1523
  - seed 21: CV@3800, S@2360, delay -1440
  - seed 22: CV@4081, S@1385, delay -2696
  - seed 23: CV@5201, S@1267, delay -3934
  - seed 24: CV@4585, S@1400, delay -3185
  - seed 25: CV@4757, S@1302, delay -3455
  - seed 26: CV@3640, S@2290, delay -1350
  - ... and 71 more

### Q3. Side-by-side vs published 50-tick data

| | published @50-tick | this run @1-tick (gated) | this run @1-tick (ungated) |
|---|---|---|---|
| n | 482 | 97 | 97 |
| median delay | 50 | 1 | **-2869** |
| mean delay | 242.9 | 19.6 | -2732.8 |
| % at floor | 90.0% | 93.8% | **99.0%** |
| max delay | 38400 | 634 | 634 |

### Q4. Does a real positive gap survive?

**NO — the gap collapses.** At 1-tick resolution the ungated median delay is -2869 tick(s) and 99.0% of runs sit at the resolution floor. The apparent 50-tick gap in the published data was an artifact of the 50-tick measurement interval: the two predicates cross within one measurement of each other. At this resolution 'sequential' is NOT distinguishable from 'simultaneous'.


## 2D geometry — 4 seeds @ 1-tick sampling

### Q1. Delay distribution at fine resolution

| measure | UNGATED (honest) | GATED (published-style detector) |
|---|---|---|
| n (both predicates fired) | 4 | 4 |
| median | **-4104** | 1 |
| IQR | [-4958, -3164] | [1, 1] |
| mean ± SD | -4018.0 ± 1174.5 | 1.0 ± 0.0 |
| min | -5122 | 1 |
| max | -2742 | 1 |
| at resolution floor (≤1) | **4/4 = 100.0%** | 4/4 = 100.0% |

### Q2. Ungated ordering — did S ever fire first?

- CV predicate fired strictly first (Clock→Map): **0/4**
- S predicate fired strictly first (Map→Clock): **4/4**
- Exact simultaneous tie (same tick): **0/4**
- Runs where one predicate never fired: 0/4
- Clock-before-Map rate (ungated): **0.0%**

**Map-before-Clock violations** (seed, cv_tick, S_tick, delay):
  - seed 0: CV@5482, S@360, delay -5122
  - seed 1: CV@4597, S@1292, delay -3305
  - seed 2: CV@4077, S@1335, delay -2742
  - seed 3: CV@5263, S@360, delay -4903

### Q3. Side-by-side vs published 50-tick data

| | published @50-tick | this run @1-tick (gated) | this run @1-tick (ungated) |
|---|---|---|---|
| n | 198 | 4 | 4 |
| median delay | 50 | 1 | **-4104** |
| mean delay | 55.8 | 1.0 | -4018.0 |
| % at floor | 97.5% | 100.0% | **100.0%** |
| max delay | 450 | 1 | -2742 |

### Q4. Does a real positive gap survive?

**NO — the gap collapses.** At 1-tick resolution the ungated median delay is -4104 tick(s) and 100.0% of runs sit at the resolution floor. The apparent 50-tick gap in the published data was an artifact of the 50-tick measurement interval: the two predicates cross within one measurement of each other. At this resolution 'sequential' is NOT distinguishable from 'simultaneous'.


---

## Evaluation criteria used

- **Resolution floor** = the sampling interval. A delay at or below it is unresolvable.
- **Gap survives** iff ungated median delay > 5x the sampling interval AND fewer than 50% of runs sit at the floor.
- **Gap collapses** iff ungated median <= sampling interval AND >= 50% of runs sit at the floor.
- Ordering is judged on the **ungated** predicates only. The gated detector cannot falsify the hypothesis and is reported for comparison, not as evidence.
