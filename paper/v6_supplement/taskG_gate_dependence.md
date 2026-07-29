# v6 Task G — Phase-D success, and a full gate-dependence audit

## Part 1 — Is Phase-D success gate-contaminated? **No.**

Concern: Phase D is gated on C, which is gated on B, which is the CV
definedness floor. Higher lipid supply → faster divisions → CV
computable earlier → B/C/D latch earlier → more remaining run time to
reach D. The gate would then interact with the ablated variable.

The mechanism is real, but the direction is wrong.

| LIPID_SUPPLY | mean B | mean C | post-C ticks (of 50,000) | Phase-D % |
|---|---|---|---|---|
| 0.008 (low) | 7752 | 7911 | 42,089 | **90.0%** |
| 0.015 (base) | 4416 | 4519 | 45,481 | 80.0% |
| 0.025 (high) | 2785 | 2862 | **47,138** | **79.0%** |

High lipid does latch earlier and does get **+5,049 more post-C ticks
(+12.0%)** — and reaches Phase D **less** often (79% vs 90%).

The confound predicts more post-C time → higher Phase-D success. The
observed effect is the opposite, so the confound cannot be producing it;
if anything it was **suppressing** it.

**Verdict: Phase-D success 90% → 79% SURVIVES.** It stays in the
survivor column.

The other two lipid-supply results are direct measurements with no gate
in the path and also stand:
- final S 0.823 → 0.644 (population mean of `pattern_s`)
- ρ(T_div, final S) = +0.43 (T_div from `final_pop`/`total_divisions`)

---

## Part 2 — Gate-dependence audit of every headline quantity

"Gate-dependent" = the computation path touches `phase_B_tick`,
`phase_C_tick`, `phase_D_tick`, or the latched phase state.

| # | reported quantity | touches gate? | status |
|---|---|---|---|
| 1 | Clock-before-Map 1,845/1,845 (100%) | **yes** — both ticks | withdrawn |
| 2 | Binomial p = 8.01e-146 / 2.49e-60 | **yes** | withdrawn (unreachable null) |
| 3 | Wilcoxon W = 116,403, p = 1.66e-98 | **yes** | withdrawn (unreachable null) |
| 4 | 1D delay 243 ± 2,319 ticks | **yes** | withdrawn (= sampling interval) |
| 5 | 2D delay 56 ± 41 ticks | **yes** | withdrawn (= sampling interval) |
| 6 | Phase B/C/D tick medians | **yes** | withdrawn (definedness floor) |
| 7 | Damköhler Da, τ_pattern | **yes** — B→C interval | withdrawn |
| 8 | Hedges' g = 9.41 (1D) | no | withdrawn — circular, n=18 arm |
| 9 | Hedges' g = 3.27 (2D) | no | withdrawn — circular, **n=2 arm** |
| 10 | Phase-D success 90% → 79% | indirect | **survives** (confound runs opposite, Part 1) |
| 11 | final S 0.823 → 0.644 | no | **survives** |
| 12 | ρ(T_div, final S) = +0.43 | no | **survives** |
| 13 | per-cell CV 0.045 ± 0.023 | no — final tick | **survives** (descriptive) |
| 14 | timescale anchor 15.8–38.3 min | no | **survives** |
| 15 | 1D Δ-CV back-reaction −0.222 | **yes** — windows anchored on `phase_C_tick` | **measurement survives, interpretation withdrawn** (below) |
| 16 | Phase-E differential +0.147 | **yes** — groups split on `phase_D_tick` | **measurement survives, interpretation withdrawn** (below) |
| 17 | Task 3 imposed grid (ρ(CV,S)) | no — forced division, steady-state S | **survives** |
| 18 | extinction 32.4% @ T=200 | no | **survives** |
| 19 | §5.2 generalization argument | no — conceptual | **survives** |

### Items 15 and 16 — a demotion I did not previously make

Both §5.3 results I placed in the survivor column have gate-dependent
computation paths, verified in source:

- `analysis_v51b.py:51` reads `phase_C_tick` and anchors **both** Δ-CV
  windows at `phc + offset`.
- `analysis_v53_phaseE.py:51,87` reads `phase_D_tick` and defines the
  G_D / G_C split as `reached_D = phd > 0`.

What this does and does not invalidate:

- **The measurements stand.** Population CV really does decline between
  the two windows (1D, fixed n=3: −0.222, p = 1.4e-17), and the two
  groups really do differ (+0.147). Those are arithmetic on recorded
  timeseries.
- **The causal readings do not.** Item 15 was reported as a
  *Map → Clock back-reaction*, i.e. an effect of Map latching. But
  `phase_C_tick` is not when the Map latched; Task 1 established it is
  one sampling interval after CV became computable. So the measured
  decline is CV drift after an artifact-defined time zero, not a
  consequence of pattern consolidation. Item 16's "Engine-reaching
  runs" is likewise a gated label, not an established physical state.

Neither result is *wrong as arithmetic*; both are **mislabelled as
physics**. They move from "survives" to "survives as measurement,
interpretation withdrawn."

## Evaluation criteria used

- "Touches gate" determined by reading the computation path in source
  for each quantity, not inferred from the manuscript text.
- Phase-D confound assessed by direction: a confound that predicts the
  opposite sign to the observed effect cannot be generating it.
- Post-C time computed as 50,000 − mean_C_tick from
  `results/ablations/ablation_summary.csv`.
- All figures recomputed from archived data; no re-simulation.
