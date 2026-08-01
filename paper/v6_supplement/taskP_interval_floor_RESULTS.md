# Task P — interval-floor hypothesis: RESULTS

Evaluated against the pre-registration committed at `3e7eb4a` **before** this experiment ran. Thresholds were fixed in advance and have not been moved.

**H1:** a cell's own *minimum* recent division interval predicts its own pattern stability; regularity matters only insofar as it produces short intervals.

| prediction | threshold |
|---|---|
| P1 | ρ(min_interval, S) > +0.25 and > 0.22 |
| P2 | highest − lowest bin gap ≥ 0.15 |
| P3 | CV effect attenuates > 50% controlling min_interval (arm B) |
| P4 | threshold within 2× of 1350 ticks (675–2700) |

---

# natural division (PRIMARY)

## Arm A — n = 153,133 cell-observations

- ρ(min_interval, cell_S) = **+0.3844** (p = 0)
- min_interval range: 357 – 3979 ticks (median 1889)
- cell_S range: 0.000 – 1.000 (median 0.959)

### S by min-interval quintile

| bin | min_interval range | n | mean S | median S |
|---|---|---|---|---|
| 1 | 357–1168 | 30,497 | **0.7825** | 0.9121 |
| 2 | 1168–1350 | 30,715 | **0.7639** | 0.8714 |
| 3 | 1350–2042 | 30,625 | **0.8458** | 0.9723 |
| 4 | 2042–3185 | 30,657 | **0.8730** | 0.9811 |
| 5 | 3185–3979 | 30,639 | **0.9054** | 0.9954 |

- Gap (highest bin − lowest bin): **+0.1229**

### Confound check — stratified by n_intervals

Pre-registered risk: a cell with few divisions has few intervals to minimise over, so its minimum is biased upward. An effect present only in low-n cells is an artifact.

| n_intervals | n obs | ρ(min_interval, S) | p | mean S |
|---|---|---|---|---|
| 1–2 | 28,266 | **+0.0918** | 5.61e-54 | 0.9077 |
| 3–4 | 25,745 | **-0.1525** | 9.15e-134 | 0.8733 |
| 5–8 | 50,375 | **-0.0495** | 1.04e-28 | 0.8427 |
| 9+ | 48,747 | **-0.0840** | 4.9e-77 | 0.7619 |

- ρ among well-divided cells (5+ intervals): **-0.0667**
- If this is near zero while the pooled ρ is not, the effect is the n-bias artifact.


# forced division (secondary)

## Arm B — n = 139,715 cell-observations

- ρ(min_interval, cell_S) = **-0.1484** (p = 0)
- min_interval range: 1 – 18651 ticks (median 3081)
- cell_S range: 0.000 – 1.000 (median 0.981)

### S by min-interval quintile

| bin | min_interval range | n | mean S | median S |
|---|---|---|---|---|
| 1 | 1–2028 | 27,936 | **0.8493** | 0.9923 |
| 2 | 2028–2873 | 27,893 | **0.8533** | 0.9854 |
| 3 | 2873–3200 | 22,876 | **0.8360** | 0.9785 |
| 4 | 3200–4418 | 33,054 | **0.8224** | 0.9785 |
| 5 | 4418–18651 | 27,956 | **0.5466** | 0.8114 |

- Gap (highest bin − lowest bin): **-0.3027**

### Confound check — stratified by n_intervals

Pre-registered risk: a cell with few divisions has few intervals to minimise over, so its minimum is biased upward. An effect present only in low-n cells is an artifact.

| n_intervals | n obs | ρ(min_interval, S) | p | mean S |
|---|---|---|---|---|
| 1–2 | 102,125 | **-0.1871** | 0 | 0.7700 |
| 3–4 | 32,268 | **-0.1424** | 8.84e-146 | 0.8197 |
| 5–8 | 5,305 | **-0.3463** | 2.63e-149 | 0.7563 |

- ρ among well-divided cells (5+ intervals): **-0.3463**
- If this is near zero while the pooled ρ is not, the effect is the n-bias artifact.


---

# Verdict

- **P1 (pooled)** ρ = +0.3844 vs required > +0.25: passes on the pooled statistic
- **P1 (stratified, pre-registered disqualifier)** ρ among cells with 5+ intervals = -0.0667: **FAIL**
- **P1 overall**: **FAIL**
- **P2** gap = +0.1229 vs required ≥ 0.15: **FAIL**

## NOT SUPPORTED

Neither pre-registered prediction passed. The interval-floor reformulation does not rescue the theory within this model. The ordering question goes to the laboratory untested — which is where the v6 audit already placed it.

## Evaluation criteria used

- Thresholds fixed in the pre-registration and not adjusted.
- Arm A (natural geometric division) is the primary test; it contains none of the Task 3 forcing artifacts.
- Only cells with ≥1 completed interval are included, since min_interval is undefined otherwise.
- Stratification by n_intervals reports whether the effect is the pre-registered n-bias artifact.
- Spearman rank correlation throughout.

---

## Arm B corroborates arm A, in the opposite direction to H1

Arm B (forced division) gives ρ(min_interval, S) = **−0.1484** pooled,
and it **strengthens under stratification** rather than collapsing:
−0.187 (1–2 intervals), −0.142 (3–4), **−0.346 (5–8)**. The bin gap is
**−0.3027** — the highest min-interval bin has the *lowest* S.

This is the mirror image of arm A's artifact and it matters:

- In arm A, the pooled ρ was **positive** and vanished under
  stratification → artifact.
- In arm B, the pooled ρ is **negative** and grows stronger under
  stratification → not an artifact.

Both arms therefore agree on the substantive point: **longer minimum
intervals do not produce more stable patterns.** Arm B says they
produce *less* stable ones, most strongly among the best-divided cells.

## Three independent analyses now point the same way

| analysis | statistic | direction |
|---|---|---|
| Task 3 imposed-CV grid | ρ(CV, S) = +0.22 | irregular slightly *better* |
| Task G stratified lipid | ρ(T_div, S) = −0.60 to −0.75 | longer period *worse* |
| Task P arm B stratified | ρ(min_int, S) = −0.35 | longer minimum *worse* |

None is individually strong enough to claim a reversal of the theory,
and each has caveats. But no analysis, from any angle attempted, has
produced support in the theory's predicted direction.

## What this closes

The interval-floor reformulation was the strongest remaining candidate
for rescuing the Clock→Map ordering inside this model. It fails on the
primary arm and is contradicted on the secondary arm. **No further
reformulation is warranted without new data**; continuing to rename the
independent variable until something clears a threshold is exactly the
practice this audit exists to document.

The ordering question is open and belongs at the bench.

## A structural note for the methods paper

This is the **third Simpson's paradox** found in this project:

1. ρ(T_div, S): +0.43 pooled, −0.60 to −0.75 within lipid conditions
2. The 1,845 denominator: a shared OAT baseline summed across rows
3. ρ(min_interval, S): +0.38 pooled, −0.07 within division-count strata

They share a cause. Nearly every quantity in this model is entangled
with how many times a cell has divided — S is disrupted by division, CV
requires divisions to be defined, minimum interval is taken over a
division-count-dependent sample. Pooling across division count
therefore produces sign reversals as a matter of course.

That is a general hazard for agent-based models of dividing populations,
not a quirk of this codebase, and it is the most transferable technical
finding in the audit.
