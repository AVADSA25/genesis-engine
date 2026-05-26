# Genesis Engine v5.1 supplement — empirical results

Three follow-up analyses on the existing 1D (n=590) and 2D (n=200)
Monte Carlo data, motivated by Gemini Deep Think's external review
(May 2026). **No new simulations were run** — all results are
re-analyses of the data underlying v5.

---

## A) Physical-time calibration

See `calibration.md`. Anchor: lipid lateral diffusion in fluid
bilayers (D ≈ 1–10 μm²/s) on a 1.5 μm vesicle.

**Result:** 1 tick ≈ **0.45 s** (typical D = 5 μm²/s).
Under this anchor, the headline Clock→Map delay is:

| Geometry | Mean delay (ticks) | Physical time @ D=5 |
|---|---|---|
| 1D ring     | 243 | **~1.8 min** |
| 2D icosphere | 56 | **~25 s**    |

Both fall in a regime observable live by standard fluorescence
microscopy of Rh-DHPE-doped vesicles — not geologically slow,
not femto-fast.

---

## B) Map → Clock long-run back-reaction test

**Motivation.** Gemini's "Unasked Question" asked whether Map
latching causes retroactive destabilisation of the Clock through
shared membrane-mechanical substrate. The published model assumes
independence; this is the first direct empirical check.

**Method.** For every run that reached Phase C, compare a stabilised
early-post-latch window against a much later long-run window:

| | early window | late window |
|---|---|---|
| 1D (100 000-tick runs) | phc + 2 000 … + 3 000 | phc + 50 000 … + 60 000 |
| 2D (10 000-tick runs)  | phc +    500 … +1 500 | phc +  3 500 … +  4 500 |

Statistic: Δcv = mean_cv(late) − mean_cv(early), tested per-run with
a two-sided sign test.

**Results.**

| Geometry | n | mean Δcv | median Δcv | sign +/−/0 | sign-test p |
|---|---|---|---|---|---|
| **1D ring**     | 480 | **−0.2151** | −0.2245 | 0 / 480 / 0 |  6.4 × 10⁻¹⁴⁵ |
| **2D icosphere** | 157 | **+0.0573** | +0.0230 | 93 / 64 / 0 |  0.025 |

**Interpretation — dimensional asymmetry.**

- **1D**: the Clock continues to **tighten** indefinitely after the Map
  latches. Every one of 480 runs trended down. There is no evidence
  of any back-reaction on a topologically trivial substrate.
- **2D**: there *is* a small but statistically significant
  Clock **destabilisation** in the long run (mean Δcv = +0.057,
  p = 0.025). The effect is roughly 4 % of the 0.25 latch threshold
  — far from "metabolic cancer," but non-zero.

This is a partial empirical confirmation of Gemini's hypothesis
that operates only in the higher-dimensional regime, consistent
with the geometric prediction that richer spatial topology offers
more coupling channels back into the membrane mechanics driving
the Clock. The published v5 paper's independent-substrate
assumption is **conservative in 1D and very slightly violated in 2D**
within the model's existing dynamics — even though the Map only
acts on Engine in code.

**Robustness controls (`backreaction_2D_shuffle_control.md`).**
We worried that the 2D Δcv = +0.057 could be a generic
"later-in-run population-age drift" rather than a true Phase-C
back-reaction. Two formal controls rule this out:

| Control | Description | Result |
|---|---|---|
| Fixed-tick anchor (T5) | Same absolute-tick windows for every run, ignoring per-run phc | Δcv = **−0.007** (effect vanishes) |
| Permutation null  (N=2000) | Each run's phc replaced by another run's phc | Null mean = −0.107 ± 0.013; **0 / 2000 shuffles produced Δcv ≥ +0.057**; permutation p < 1/2000 |

Both confirm the effect is anchored to each run's actual Phase-C
event — not to absolute simulation time and not to a generic drift.
The pre-latch sanity check (anchor = phc − 3000) gives Δcv = −0.79
across all 184 eligible runs, as expected for the active Clock-
tightening regime.

**Remaining caveat.** The 2D simulations are only 10 000 ticks, so
we cannot test "even-deeper-post-latch" anchors (phc + 2000 leaves
only n=1 eligible run). A dedicated long-run 2D Monte Carlo
(50 000 ticks, planned for v6) would confirm the trend extrapolates
beyond end-of-run.

(See `fig_backreaction_clean_1D.png`, `fig_backreaction_clean_2D.png`
and `backreaction_clean_*.csv`.)

---

## C) Phase-C-onset state characterization

What does the system look like at the exact tick the Map latches?

| Geometry | n | population | mean_cv | mean S | median phc tick |
|---|---|---|---|---|---|
| 1D ring     | 482 | 35.3 cells | 0.161 ✓ | 0.471 | 4 300 |
| 2D icosphere | 198 | 39.8 cells | 0.183 ✓ | 0.557 | 4 975 |

Both geometries latch with the Clock comfortably under the 0.25
threshold (✓) and the population in a tight 20–60 cell band.
Pattern stability S is well above zero but well below the
post-latch ceiling, i.e. the Map latches **while patterns are
still tightening**, not after they have fully consolidated.

(See `fig_phase_c_onset_1D.png`, `fig_phase_c_onset_2D.png`.)

---

## Summary one-liner for the paper

> *Re-analysis of the existing Monte Carlo data shows the Clock→Map
> delay is 25 s – 2 min under typical lipid kinetics, the Map latches
> in a tight 20–60-cell window with division CV ≈ 0.16–0.18, and the
> Clock continues to tighten in the long run on a 1D substrate but
> exhibits a small, robustly-anchored 2D-only back-reaction (mean
> Δcv = +0.057, sign-test p = 0.025; permutation null p < 1/2000;
> survives both phc-shuffle and fixed-tick controls) — a partial
> confirmation of Gemini Deep Think's retroactive-interference
> hypothesis that motivates a fully coupled Map↔Clock v6 model.*
