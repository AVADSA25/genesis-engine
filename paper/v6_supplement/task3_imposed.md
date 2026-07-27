# v6 Task 3 — imposed regularity × imposed period

The first direct test of the paper's **physical** hypothesis. Tasks 1/3/4
of the previous pass were measurement findings: they showed the published
ordering was manufactured by a sequential gate and a CV definedness
floor. They did not test the physics. This does.

Division timing is **imposed externally** (Gamma(1/cv², T·cv²), mean T
and coefficient of variation cv exactly; cv=0 deterministic, cv=1
Poisson). Regularity and period are therefore independent **control**
variables, and steady-state S is measured over the last 20% of each run
with no detector, no gate and no CV estimate anywhere in the causal path.

Grid: 9 CV × 6 T × 25 seeds = **1,350 runs** @ 20,000 ticks.
Plateau verified in a pre-check (drift q4→q5 = 0.1–0.5%).

---

## 1. Physicality — half the grid is not a physical regime

Forcing division decouples it from growth, so cells are split before
reaching the size at which they would divide geometrically. Natural
period at baseline lipid supply is **~3,170 ticks**.

| imposed T | % divisions premature (rv ≥ 0.16) | extinct runs | status |
|---|---|---|---|
| 200 | 100.0% | **73/225 (32.4%)** | unphysical |
| 400 | 99.9% | 19/225 (8.4%) | unphysical |
| 800 | 98.2% | 2/225 (0.9%) | unphysical |
| 1600 | 79.4% | 0 | unphysical |
| 3200 | 17.4% | 0 | **physical** |
| 6400 | 6.1% | 0 | **physical** |

Only **T = 3200 and 6400** are physically valid. Everything below splits
cells that had not grown, and at T=200 a third of populations die
outright. This is a hard limit of the experimental design and is
reported, not absorbed into the averages.

---

## 2. Regularity — the hypothesis is REFUTED, not merely unsupported

Steady-state S against imposed CV, **physical periods only** (n=450):

| imposed CV | 0.0 | 0.05 | 0.1 | 0.15 | 0.2 | 0.3 | 0.5 | 0.8 | 1.0 |
|---|---|---|---|---|---|---|---|---|---|
| mean S | 0.760 | 0.664 | 0.687 | 0.710 | 0.700 | 0.702 | 0.726 | 0.773 | 0.781 |

- **Spearman ρ(CV, S) = +0.2196, p = 2.56 × 10⁻⁶**
- Most regular (CV ≤ 0.05): mean S = **0.7122** (n=100)
- Most irregular (CV ≥ 0.80): mean S = **0.7771** (n=100)
- Mann–Whitney, one-sided *regular > irregular*: **p = 1.0**

The hypothesis predicts S falls as division becomes irregular. S
**rises**, significantly. Sweeping regularity across its entire range —
from perfectly periodic to Poissonian — does not degrade pattern
stability; it slightly improves it.

This is a refutation with a significant effect in the wrong direction,
which is stronger than a null.

---

## 3. Period — the apparent effect is largely an artifact

Across all six periods the correlation looks decisive:

- Spearman ρ(T, S) = **+0.7233, p = 2.24 × 10⁻²⁰⁴** (n = 1,259)

**This must not be reported as a timescale-separation result.** It is
driven almost entirely by the four unphysical short-period conditions,
where S is suppressed because cells are being mechanically split before
their pattern can persist — a direct consequence of the forcing, not a
discovered consolidation threshold.

Within the physically valid range the trend **reverses**:

| imposed T | mean S | n |
|---|---|---|
| 3200 | **0.7798** | 225 |
| 6400 | **0.6653** | 225 |

Two points only, and S *declines* with longer period. S peaks near
T ≈ 3200, which is essentially the model's own natural division period
(~3,170 ticks) — a coincidence that warrants suspicion rather than
celebration, since the model's other constants were calibrated in that
regime.

**No timescale-separation conclusion is supported by this grid.** An
earlier reading of the plateau pre-check suggested one; that reading
contrasted T=400 (unphysical) against T=3200 (physical) and was
confounded. It is withdrawn.

---

## 4. Verdict

**The physical hypothesis, as the paper states it, is dead.**

> "Temporal regularity precedes and enables spatial organization."

With regularity under direct experimental control and every broken
instrument removed from the loop, regularity has no beneficial effect on
persistent spatial organization. The measured effect is significant and
**opposite in sign** (ρ = +0.22, p = 2.6 × 10⁻⁶): Poissonian division
supports marginally *higher* steady-state pattern stability than perfect
periodicity.

The remaining period effect cannot be rescued as a substitute mechanism,
because it is confounded with forced premature splitting and reverses
inside the only physically valid window.

### What this does not say

- It does not show that division dynamics are irrelevant to protocell
  organization in general. It shows that **in this model**, with timing
  imposed, regularity is not the operative variable.
- It does not rescue the reverse ordering either. Task 1 established the
  model cannot adjudicate ordering; this establishes that the mechanism
  the ordering was supposed to reflect is absent.
- The physical regime is thin: only two valid period values. A model in
  which division and growth are coupled (so that fast division is
  physically attainable rather than imposed) would be required to probe
  the short-period regime honestly.

---

## Evaluation criteria used

- **Steady-state S** = mean over the final 20% of each run; plateau
  verified beforehand (drift 0.1–0.5%).
- **Direction, not range**, is the test: the hypothesis predicts a
  *decrease* in S with increasing CV. Assessed by Spearman ρ and a
  one-sided Mann–Whitney between the extreme CV groups.
- **Physical** = <50% of divisions premature (rv ≥ CRIT_THRESHOLD_MEAN
  = 0.16). Threshold fixed before analysis.
- Extinct runs (final_pop = 0) excluded from S statistics and reported
  separately; 94/1350 = 7.0% overall, all at T ≤ 800.
- No parameter, threshold, seed or window was tuned. The grid was run
  once.
