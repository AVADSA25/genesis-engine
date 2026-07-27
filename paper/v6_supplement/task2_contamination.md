# v6 Task 2 — Contamination audit of §5.3

Which of the four §5.3 results survive once the broken anchors
(sequential gate, sampling interval, CV definedness floor, growing-n CV
estimator) are removed.

---

## 2a. Damköhler / "Clock speed limit" — **DELETED**

§5.3 defines τ_pattern as the mean Phase B→C interval. Task 1
established that this interval *is* the sampling interval.

Recomputed per ablation condition from `ablation_summary.csv`:

| statistic | value |
|---|---|
| τ_pattern across all 12 conditions | **77.2 – 196.5 ticks** (median 102.6) |
| expressed in sampling intervals | **1.5 – 3.9** |
| true S-consolidation time (archived, first S>0.25) | **~1300–1400 ticks** |

τ_pattern is therefore the gated B→C delay, i.e. the measurement
interval, and is ~10x smaller than the time patterns actually take to
consolidate. Da = T_div / τ_pattern is T_div divided by roughly two
sampling intervals and carries **zero** pattern-consolidation
information. The Damköhler framing is withdrawn.

**Surviving measurements underneath (these never touched the gate):**

| quantity | low lipid | high lipid |
|---|---|---|
| final pattern stability S | 0.823 | 0.644 |
| Phase-D success rate | 90% | 79% |
| Spearman ρ(T_div, final S) | \+0.43 (p = 8.9e-15) | |

These are direct measurements of S and population outcomes against
lipid supply. They stand. Only the Damköhler *interpretation* is
deleted. Task 3 replaces it with a properly anchored version.

---

## 2b. Δ-CV back-reaction — **1D SURVIVES, 2D DOES NOT**

### The estimator concern, and its actual direction

The production `mean_cv` uses every interval a cell has accumulated
(≥3, capped at 12), so sample size grows over a run. `numpy.std()`
defaults to **ddof=0**, biased LOW at small n. Therefore:

```
small n -> std underestimated -> CV underestimated
large n -> bias shrinks       -> CV estimate rises
=> the estimator alone pushes Delta-CV (late - early) POSITIVE
```

This is the opposite of the direction assumed when the test was
commissioned. It means a **negative** published Δ-CV cannot have been
manufactured by this artifact, while a **positive** one is exactly what
the artifact produces.

### Control

Recompute Δ-CV with a fixed-n estimator (exactly the last N intervals
from cells having at least N), holding sample size constant. N=3 matches
the production minimum, so definedness is identical and the test is
fully powered.

### 1D — survives

| estimator | n | mean Δ-CV | median | sign +/− | p |
|---|---|---|---|---|---|
| production (growing n) | 57 | −0.21046 | −0.22158 | 0/57 | 1.39e-17 |
| **fixed n=3** | 57 | **−0.22166** | −0.23664 | 0/57 | 1.39e-17 |
| per-run shift | 57 | **−0.01120** | | 48/57 more negative | 1.52e-07 |

Production reproduces the published −0.215 exactly. The estimator
contributes only −0.011 of bias, in the direction that was
**understating** the effect. **The 1D back-reaction is dynamical.**

### 2D — does not survive

| estimator | n | mean Δ-CV | median | sign +/− | p |
|---|---|---|---|---|---|
| production | 57 | +0.04498 | −0.00035 | 28/29 | **1.0** |
| **fixed n=3** | 57 | **+0.02415** | −0.02134 | 25/32 | **0.427** |
| shift | | **−0.02083** | | | |

Not significant under either estimator, and the fixed-n control moves it
toward zero by −0.021 — precisely the ddof=0 direction. The published
2D value (+0.057, sign-test p=0.025, n=157) does not replicate.

**Supporting diagnostic.** At N=5 the fixed estimator was defined in the
2D early window in only **1/99** runs, versus 85/99 in the late window.
Sample size demonstrably grows between the published windows, which is
the precondition for the artifact.

**Consequence:** the claim that the 2D back-reaction is 22.8% of the
0.25 latch threshold is withdrawn along with the effect itself.

---

## 2c. Phase-E — **SURVIVES**

Phase-E asks whether the Engine filters against Maps that destabilise
the Clock. It compares Δ-CV between runs reaching Phase D (G_D) and
runs stalling at Phase C (G_C). Recomputed on fixed-n CV:

| estimator | G_D | G_C | difference |
|---|---|---|---|
| production | +0.10190 (n=32) | −0.02788 (n=25) | **+0.12978** |
| **fixed n=3** | +0.08856 (n=32) | −0.05831 (n=25) | **+0.14687** |

Published difference: +0.1253. The differential **reproduces and is
slightly larger** under the control. Engine-reaching runs still show
*more* back-reaction than stalled runs, so the original conclusion —
that Phase-E selection is **not** an emergent property of the model and
would have to be evolved — stands.

Note this is a statement about the *difference between groups*, which is
robust, not about the absolute 2D Δ-CV, which is null (2b).

---

## Summary

| §5.3 result | verdict |
|---|---|
| Damköhler / speed-limit framing | ❌ **Deleted** (τ_pattern = sampling interval) |
| ↳ S and Phase-D measurements underneath | ✅ **Survive** |
| 1D Δ-CV back-reaction (−0.215) | ✅ **Survives** (fixed-n: −0.222) |
| 2D Δ-CV back-reaction (+0.057) | ❌ **Does not survive** (p=0.427) |
| Phase-E null | ✅ **Survives** (+0.147 fixed-n) |

Two of four survive; one survives with its framing deleted but its
measurements intact; one is withdrawn.

## Evaluation criteria used

- **Survives** = same sign and p < 0.05 under the fixed-n estimator, on
  paired runs where both estimators are defined.
- N=3 chosen to match the production minimum so definedness is
  identical and the comparison is paired, not selected.
- Windows held at the published values; no window, threshold, seed or
  parameter was tuned.
- Requires re-simulation (archived timeseries store only population-mean
  CV, not per-cell interval histories), which is a stated deviation from
  "zero new simulation". Sampling stayed at the production 50-tick
  interval.
