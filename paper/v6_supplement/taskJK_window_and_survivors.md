# v6 Tasks J & K — what the note is entitled to claim

Two corrections to the claims in the correction note, using data already
on disk. Neither is a new audit.

---

## Task J — Which temporal measure did the completed A1 use?

**Answer: the windowed measure. The temporal window WAS matched.**

`results_v6/taskA1_obs.csv` contains **271,089 observations across 21
distinct ticks**, spanning 16,000–20,000 — exactly the last 20% of each
20,000-tick run, which is the grid's `steady_S` window. Mean 602
observations per run. It is not a final-tick snapshot.

Verified numerically: reconstructed `steady_S` versus the grid's, over
450 matched runs, mean |Δ| = **0.000024**, max **0.000050**.

The earlier v2 build *did* use a final-tick snapshot and was discarded
for exactly the lockstep-phase reason. The completed A1 is the third
build.

### The residual, addressed specifically

Matching the window is necessary but not sufficient. The window is 4,000
ticks, so its coverage of a division cycle depends on the period:

| condition | cycles spanned | phase coverage |
|---|---|---|
| T = 3200 | 1.25 | **complete** |
| T = 6400 | 0.62 | **incomplete** |

At T = 6400 a CV=0 population is sampled over only 62% of its division
cycle, so the lockstep-phase mechanism is **not** fully neutralised
there. This is the specific concern, and it is testable: if lockstep
phase were manufacturing ρ(CV,S) > 0, the effect must be **larger** where
coverage is incomplete.

| condition | ρ(CV, cell-S) | ρ(CV, run steady_S) |
|---|---|---|
| T = 3200 (complete) | **+0.1591** (n = 164,350) | **+0.4521** (p = 9.9e-13) |
| T = 6400 (incomplete) | +0.1035 (n = 106,739) | +0.1756 (p = 0.0083) |

The effect is **larger where the artifact cannot operate** and smaller
where it can. The lockstep-phase mechanism therefore does not explain
the result; it works against it.

**Consequence for the note.** A1's measure is sound, and the temporal
window is *not* a reason A1 cannot adjudicate. The sole reason remains
the barely-dividing fraction (44.0% → 56.2%, a 12.3 pp range against a
pre-registered 10 pp threshold). The note should not list a second
independent reason, because there isn't one.

---

## Task K — Are three survivors one result?

**Yes — but the check came out stronger than anticipated. It is one
result confirmed by TWO measures, not three, because the third is
withdrawn for having the wrong sign.**

### ρ(T_div, S) stratified

| stratum | n | ρ | p |
|---|---|---|---|
| LIPID_SUPPLY = 0.008 | 100 | **−0.5970** | 5.6e-11 |
| LIPID_SUPPLY = 0.015 | 100 | **−0.7396** | 1.5e-18 |
| LIPID_SUPPLY = 0.025 | 100 | **−0.7537** | 1.5e-19 |
| pooled (as published) | 300 | **+0.4278** | 8.9e-15 |

It does not collapse toward zero. It **reverses**. Lipid supply moves
both variables at once, so they covary positively across conditions;
within a fixed supply, slower-dividing runs reach *lower* S. A Simpson's
paradox. ρ = +0.43 is therefore withdrawn, not merged — its published
sign is opposite to the within-condition association.

Corroborated independently by Task 3, which imposed division timing with
no lipid confound and no detector in the path, and found the same
negative direction inside the physical window (T=3200 → S 0.780;
T=6400 → S 0.665).

### Phase-D is a thresholded restatement

Phase D requires generational depth ≥ 5 **and** sustained S̄ > 0.35
**and** CV < 0.3. High lipid wins on two of the three criteria:

| | low lipid | high lipid | favours |
|---|---|---|---|
| mean_max_gen (need ≥5) | 4.74 | **4.87** | high |
| final CV (need <0.3) | 0.075 | **0.046** | high |
| final S (need >0.35) | **0.823** | 0.644 | low |
| **Phase-D attained** | **90%** | 79% | low |

High lipid satisfies depth and CV more easily yet attains D less often,
so the **S criterion is what binds**. Phase-D attainment is a
thresholded restatement of the S drop, not independent corroboration.

### How the note must present it

> **One result, confirmed by two measures:** higher lipid supply →
> faster division → lower pattern stability. Measured as final *S*
> 0.823 → 0.644, and restated in thresholded form as Phase-D attainment
> (direction only; the rates are gate-conditioned). The pooled
> ρ(T_div, S) = +0.43 previously offered as a third measure is withdrawn:
> stratified, it is −0.60 to −0.75.

Presenting these as three surviving results would repeat, in structure,
the 1,845-denominator error — counting one shared quantity several times.

---

## Evaluation criteria used

- Task J: "window matched" = observations span the grid's steady-state
  window at more than one tick, verified by tick distribution and by
  numerical agreement of reconstructed `steady_S` with the grid.
- Task J residual: lockstep phase is excluded as a cause iff the effect
  is not larger where phase coverage is incomplete.
- Task K: "same finding" = one causal chain surfacing in multiple
  summaries. Stratified ρ computed per condition from the archived
  per-run ablation files, n = 100 each, Spearman throughout.
