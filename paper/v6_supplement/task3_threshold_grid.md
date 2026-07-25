# v6 Task 3 — Threshold grid ablation

**Zero new simulation.** Precondition verified: the archived runs log `mean_cv` and `mean_s` timeseries at 50-tick resolution, so the entire grid is post-hoc re-thresholding of existing data.

## Why this grid was needed

The published paper ablates four physics parameters (`LIPID_SUPPLY`, `RD_NOISE`, `GROWTH_PERTURB`, `STAB_WINDOW`) but never ablates the two numbers the ordering result actually depends on: `PHASE_B_CV = 0.25` and `PHASE_C_S = 0.25`. These are two different metrics on different natural scales that happen to share a threshold value.

## Method note (important)

Ordering is computed from **ungated** first crossings:

```
t_clock = first tick with 0 < mean_cv < CV_th
t_map   = first tick with     mean_s  > S_th
```

The published gated detector **cannot** be used for this grid: it latches Map only after Clock has latched at a strictly earlier tick, so it returns Clock-before-Map = 100% in every cell by construction and carries no information. Verified in Task 1.

---

## 1D — Clock-before-Map %, ungated (n≈150 runs)

Rows = CV threshold (Clock), columns = S threshold (Map). Published cell is CV 0.25 / S 0.25.

| CV\\S | S=0.15 | S=0.25 | S=0.35 |
|---|---|---|---|
| **CV=0.15** | **0.0%** | **0.7%** | **2.1%** |
| **CV=0.25** | **0.0%** | **0.7%** * | **2.1%** |
| **CV=0.35** | **0.0%** | **0.7%** | **2.1%** |

\* = published threshold pair

Median delay (t_map − t_clock), ticks; negative = Map first:

| CV\\S | S=0.15 | S=0.25 | S=0.35 |
|---|---|---|---|
| **CV=0.15** | -3750 | -3000 | -2150 |
| **CV=0.25** | -3650 | -2900 | -2000 |
| **CV=0.35** | -3650 | -2900 | -2000 |

- Range of Clock-before-Map across the 9 cells: **0.0% – 2.1%**
- Published detector reports **100%** in every cell (by construction).

## 2D — Clock-before-Map %, ungated (n≈150 runs)

Rows = CV threshold (Clock), columns = S threshold (Map). Published cell is CV 0.25 / S 0.25.

| CV\\S | S=0.15 | S=0.25 | S=0.35 |
|---|---|---|---|
| **CV=0.15** | **0.0%** | **0.0%** | **0.0%** |
| **CV=0.25** | **0.0%** | **0.0%** * | **0.0%** |
| **CV=0.35** | **0.0%** | **0.0%** | **0.0%** |

\* = published threshold pair

Median delay (t_map − t_clock), ticks; negative = Map first:

| CV\\S | S=0.15 | S=0.25 | S=0.35 |
|---|---|---|---|
| **CV=0.15** | -8000 | -7875 | -7700 |
| **CV=0.25** | -4575 | -3700 | -3525 |
| **CV=0.35** | -4550 | -3650 | -3500 |

- Range of Clock-before-Map across the 9 cells: **0.0% – 0.0%**
- Published detector reports **100%** in every cell (by construction).

---

## Evaluation criteria used

- Ordering judged on ungated first crossings only; the gated detector is uninformative here (returns 100% everywhere).
- A run contributes only if BOTH predicates cross within the archived record; otherwise counted as incomplete.
- Archived 50-tick timeseries; no re-simulation, no tuning.
- Note the CV metric is undefined (pinned at 1.0) until a cell completes four divisions (Task 1 companion), which floors `t_clock` in every cell of this grid. The grid therefore tests threshold-sensitivity, not the underlying ordering.
