# v6 Task G addendum — ρ(T_div, S) = +0.43 is a Simpson's paradox

## Challenge

The survivor list carried three lipid-supply results: Phase-D 90→79%,
final S 0.823→0.644, and ρ(T_div, S) = +0.43. These are probably one
result measured three ways. §5.3 describes ρ as pooled across
conditions, so it may be dominated by between-condition variance.
One check settles it: compute ρ within each lipid condition.

## Result — it does not collapse toward zero, it REVERSES

| stratum | n | ρ(T_div, final S) | p |
|---|---|---|---|
| LIPID_SUPPLY = 0.008 | 100 | **−0.5970** | 5.56e-11 |
| LIPID_SUPPLY = 0.015 | 100 | **−0.7396** | 1.51e-18 |
| LIPID_SUPPLY = 0.025 | 100 | **−0.7537** | 1.45e-19 |
| **pooled (as published)** | 300 | **+0.4278** | 8.91e-15 |

This is a textbook Simpson's paradox. Within every stratum the
association is strongly **negative** (−0.60 to −0.75). Pooling reverses
its sign.

Mechanism: lipid supply moves both variables at once. Higher supply
shortens T_div *and* lowers final S, so across conditions the two
covary positively. Within a condition, where supply is fixed, runs whose
cells happen to divide more slowly reach **lower** S.

## Corroboration from an independent experiment

Task 3 imposed division timing directly, with no lipid-supply confound
and no phase detector in the path. Within the physically valid window it
found the same negative direction:

| imposed T | mean steady-state S |
|---|---|
| 3200 | 0.7798 |
| 6400 | 0.6653 |

Two independent routes — stratified archived data and imposed-timing
simulation — agree that longer division period goes with *lower*
pattern stability. The published pooled ρ asserts the opposite.

## Disposition

**ρ(T_div, S) = +0.43 is WITHDRAWN.** It is not a third result to be
merged with the other two; it is a pooling artifact whose sign is
opposite to the within-condition association.

The remaining lipid-supply finding is **one result, measured two ways**:

> Higher lipid supply → faster division → lower pattern stability.
> Measured as: final S 0.823 → 0.644 across conditions, and as a
> thresholded restatement of the same drop in Phase-D attainment
> (direction only — the rates are gate-conditioned, see Part 1).

Phase D requires generational depth ≥5 *and* sustained S > 0.35 *and*
CV < 0.3. High lipid satisfies the depth and CV criteria more easily
(4.87 vs 4.74; CV 0.046 vs 0.075) yet attains D less often, so the S
criterion is what binds. Phase-D attainment is therefore a thresholded
restatement of the S drop, not independent corroboration of it.

Presenting these as three surviving results would repeat, in structure,
the 1,845-denominator error: counting one shared quantity several times.

## Evaluation criteria used

- Stratified ρ computed per condition from
  `results/ablations/per_run/LIPID_SUPPLY_*.csv`, n=100 each.
- T_div estimated as `final_pop × 50,000 / total_divisions`, identical
  to the published method.
- Spearman rank correlation throughout, matching the published statistic.
- "Same finding" = one causal chain (supply → period → S) surfacing in
  multiple summaries, not multiple independent measurements.
