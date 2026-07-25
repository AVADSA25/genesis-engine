# v6 Task 1 (companion) — the Clock latch is a measurement floor

**No new simulation.** This is a re-reading of the archived 50-tick timeseries that back the published results.

## Mechanism under test

In `genesis_engine.py` the population division CV is computed as:

```python
cvs = []
for c in cells:
    if len(c.division_times) >= 3:      # needs 3 INTERVALS
        ...
mean_cv = np.mean(cvs) if cvs else 1.0  # undefined -> 1.0
```

and `division_times` is appended only from the **second** division onward (`if c.last_div_age > 0`, line 384). A cell therefore needs **four completed divisions** before it contributes to CV at all. Until that happens `mean_cv` is pinned at 1.0 — above every candidate threshold — so the Clock predicate *cannot* fire, regardless of the dynamics.

The Map statistic `S` has no equivalent floor: `pattern_s` is an EMA over RD snapshots taken every `STAB_WINDOW` (=40) ticks and rises within a few hundred ticks.

**Prediction if this is a measurement artifact:** the first tick at which CV becomes computable should coincide with the reported `phase_B_tick`.

---

## 1D (n = 120 archived runs)

| quantity | median | IQR | min | max |
|---|---|---|---|---|
| first tick CV is **computable** (<1.0) | **4250** | [3800, 4800] | 3450 | 5650 |
| published `phase_B_tick` ("Clock emerges") | **4250** | [3800, 4800] | 3450 | 9600 |
| first tick S > 0.25 ("Map") | **1400** | [1300, 2250] | 400 | 4400 |

- S crosses its threshold **before CV is even computable** in **115/116** runs (99.1%).

- Median first-CV-defined tick (4250) vs median reported Clock latch (4250): difference **0 ticks** — i.e. they coincide.

## 2D (n = 120 archived runs)

| quantity | median | IQR | min | max |
|---|---|---|---|---|
| first tick CV is **computable** (<1.0) | **4950** | [4250, 5300] | 3350 | 6200 |
| published `phase_B_tick` ("Clock emerges") | **4975** | [4250, 5350] | 3350 | 9550 |
| first tick S > 0.25 ("Map") | **1300** | [450, 1350] | 300 | 2350 |

- S crosses its threshold **before CV is even computable** in **118/118** runs (100.0%).

- Median first-CV-defined tick (4950) vs median reported Clock latch (4975): difference **25 ticks** — i.e. they coincide.

---

## Conclusion

The reported Clock latch time is **not a dynamical transition**. It coincides with the first tick at which the CV statistic becomes computable, which is set by the metric's requirement of four completed divisions per cell — not by when division timing actually becomes regular.

The Map predicate is already satisfied roughly 3,000 ticks earlier, in essentially every run, in both geometries.

Combined with the sequential gate in `detect_phase()` (which forbids C from latching before B by construction), the published Clock-before-Map ordering is fully accounted for by two measurement artifacts and requires no dynamical explanation.

## Evaluation criteria used

- **Coincide** = median first-CV-defined tick within one sampling interval (50 ticks) of median `phase_B_tick`.
- Thresholds held at published values (CV < 0.25, S > 0.25). No tuning.
- Archived data only; the published runs are re-read, not re-run.
