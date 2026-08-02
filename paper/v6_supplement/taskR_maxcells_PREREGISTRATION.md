# Task R — Is the barely-dividing limit structural, or a parameter choice?

**Pre-registered before running.**

## Why this matters more than it looks

The v6 audit's central *methodological* claim is that ~50% of cells in
every condition barely divide (<2 divisions), so division-perturbation
effects cannot be isolated in this model **at all** — described as "a
property of the simulation class, not of one study."

If that fraction is instead a consequence of `MAX_CELLS = 100` plus
resource limits, then it is a **parameter choice**, the limit is not
structural, and the methods paper's central claim must be softened.

## Mechanism, stated before testing

At `MAX_CELLS = 100` the population saturates the cap and then competes
for a fixed resource pool. Many cells sit near the death threshold,
grow slowly, and divide rarely. Lowering the cap gives each cell more
resource → faster growth → more divisions each → **fewer barely-dividing
cells**.

**I therefore expect the fraction to drop.** Recording that in advance
because it is the outcome that forces me to weaken a claim already
published in this repository, and I do not want to be able to reinterpret
it afterwards.

## Design

- `MAX_CELLS` ∈ {20, 50, 100 (baseline)}
- 40 seeds each, **40,000 ticks** (double the standard run, so cells have
  more opportunity to accumulate intervals)
- Natural geometric division
- Measure over the steady-state window (last 20%, all cells):
  fraction with <2 divisions, fraction with <4, mean divisions per cell

## Pre-registered predictions

| | criterion |
|---|---|
| **R1 structural** | barely-dividing fraction stays **≥ 40%** at `MAX_CELLS = 20` |
| **R2 parameter** | fraction drops **below 25%** at `MAX_CELLS = 20` |
| **R3 dose** | the fraction decreases monotonically as `MAX_CELLS` decreases |

## Decision rule, fixed now

| outcome | consequence |
|---|---|
| **R1 holds** | The limit is structural. The methods paper's claim stands as written. |
| **R2 holds** | The limit is a **parameter choice**. The claim must be softened to "a property of this parameterisation", and the ordering question may be testable in silico after all — which would reopen work already reported as closed. |
| Neither (25–40%) | Partial. Report the dose-response and describe the limit as parameterisation-dependent without claiming either extreme. |

## Commitments

1. One run. No adjustment if the result is inconvenient.
2. Thresholds (40%, 25%) fixed now.
3. If R2 holds, the correction note and the methods scaffold are both
   revised, and the revision is reported prominently rather than folded
   quietly into a later commit.
