# v6 Task A1 — does the refutation survive its confounds?

Task 3 reported ρ(CV, S) = +0.2196 (p = 2.56e-06) on the physically valid conditions: steady-state pattern stability **rises** with imposed division irregularity, contrary to the paper's physical hypothesis. This tests whether that is real.

---

## 0. Measure validity (checked before anything else)

This analysis must adjudicate the grid's `steady_S`, so it must measure the same thing. Two earlier versions did not:

- v1 logged only cells with ≥2 divisions, excluding ~42% of the population — precisely the barely-dividing cells the confound concerns.
- v2 logged all cells but only at the **final tick**. That is CV-dependent by construction: at CV=0 every cell divides in lockstep, so at any single tick all cells sit at the same phase of their division cycle; if that phase is a post-division low-S moment the entire CV=0 group is depressed. That artifact alone manufactures ρ(CV,S) > 0 — the same direction as the effect under test.

This version samples all cells across the last 20% of each run, matching the grid's population and temporal window.

Reconstructed `steady_S` vs the grid's, over 450 matched runs: mean |Δ| = **0.000024**, max |Δ| = **0.000050**.

✅ The reconstruction reproduces the grid's measure; this analysis is entitled to adjudicate it.

## 1. Are high-CV populations carried by cells that stopped dividing?

| imposed CV | % cell-obs with <2 divisions | % with <4 | mean realized interval |
|---|---|---|---|
| 0.0 | 44.0% | 84.6% | 3946 |
| 0.05 | 45.0% | 86.5% | 3974 |
| 0.1 | 45.6% | 87.9% | 3964 |
| 0.15 | 46.7% | 87.6% | 3909 |
| 0.2 | 46.9% | 87.2% | 3908 |
| 0.3 | 47.7% | 86.4% | 3687 |
| 0.5 | 48.8% | 85.0% | 3504 |
| 0.8 | 53.1% | 85.2% | 3377 |
| 1.0 | 56.2% | 85.0% | 3236 |

- Range of <2-division fraction across CV: **12.3 pp** (44.0% at CV=0.0 → 56.2% at CV=1.0)
- Range of <4-division fraction across CV: **3.3 pp**

## 2. Within-condition: does a cell's own realized interval predict its own S?

| imposed CV | imposed T | n obs | ρ(own interval, own S) | p |
|---|---|---|---|---|
| 0.0 | 3200 | 11169 | +nan | nan |
| 0.0 | 6400 | 3396 | +nan | nan |
| 0.05 | 3200 | 12198 | +0.0160 | 0.0781 |
| 0.05 | 6400 | 3866 | -0.1632 | 1.76e-24 |
| 0.1 | 3200 | 12320 | -0.0068 | 0.448 |
| 0.1 | 6400 | 3849 | -0.0992 | 6.85e-10 |
| 0.15 | 3200 | 12238 | +0.0158 | 0.0813 |
| 0.15 | 6400 | 3602 | -0.0223 | 0.181 |
| 0.2 | 3200 | 12139 | -0.0428 | 2.4e-06 |
| 0.2 | 6400 | 3685 | -0.0886 | 7.21e-08 |
| 0.3 | 3200 | 12164 | -0.0189 | 0.037 |
| 0.3 | 6400 | 3504 | -0.1731 | 5.52e-25 |
| 0.5 | 3200 | 12180 | -0.0093 | 0.304 |
| 0.5 | 6400 | 3498 | -0.0330 | 0.051 |
| 0.8 | 3200 | 10719 | -0.0127 | 0.188 |
| 0.8 | 6400 | 4304 | -0.1999 | 4.65e-40 |
| 1.0 | 3200 | 9775 | -0.0274 | 0.00668 |
| 1.0 | 6400 | 5109 | -0.1731 | 1.22e-35 |

Median within-condition ρ(own interval, own S) = **+nan** (range +nan to +nan).

## 3. Does CV retain explanatory power once realized interval is controlled?

Matched-bin comparison: within bins of realized interval, does mean cell-S still rise with imposed CV?

| interval bin | CV=0.0 | CV=0.05 | CV=0.1 | CV=0.15 | CV=0.2 | CV=0.3 | CV=0.5 | CV=0.8 | CV=1.0 | ρ(CV,S) within bin | p |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1–2601 | — | — | 0.862 | 0.875 | 0.881 | 0.854 | 0.833 | 0.863 | 0.852 | **+0.1366** | 9.3e-117 |
| 2601–3163 | — | 0.821 | 0.863 | 0.868 | 0.861 | 0.863 | 0.866 | 0.862 | 0.869 | **+0.1240** | 2.24e-96 |
| 3163–3403 | 0.783 | 0.815 | 0.850 | 0.876 | 0.861 | 0.834 | 0.811 | 0.835 | 0.896 | **+0.1527** | 1.08e-145 |
| 3403–5144 | — | 0.793 | 0.835 | 0.840 | 0.820 | 0.781 | 0.807 | 0.842 | 0.855 | **+0.1070** | 4.81e-72 |
| 5144–18651 | 0.481 | 0.429 | 0.461 | 0.508 | 0.458 | 0.501 | 0.710 | 0.776 | 0.825 | **+0.1627** | 3.64e-165 |

- Unconditional ρ(CV, cell-S) on the same observations: **+0.1691** (p = 0, n = 139715)
- Median ρ(CV, cell-S) **within** interval bins: **+0.1366**
- Attenuation: **19%**

---

## Verdict

**CANNOT CURRENTLY ANSWER.**

The fraction of cells completing <2 divisions varies by 12.3 pp across the CV sweep, so the comparison is partly between populations that divide and populations that largely do not.

**This does not restore the original claim.** It is a weaker and different statement: with this model and this design, the physical hypothesis can be neither confirmed nor refuted. The correction must say that rather than claiming refutation.

## Stated limitation (for the correction)

The physical window contains only **two** period values (T = 3200 and 6400), both at or above the model's natural period (~3,170 ticks). Below that, forcing division splits cells before they have grown — 79.4% premature at T=1600, rising to 100% at T=200. The **'too fast to organize' regime is therefore unphysical by construction in this model and cannot be tested with it.** That is a limitation of the design, not a finding.

## Evaluation criteria used

- Measure validity checked numerically against the grid before drawing conclusions (mean |Δ| reported above).
- 'Survives' requires BOTH: median within-bin ρ > +0.05, AND <2-division fraction varying by < 10 pp across the CV sweep. Both thresholds fixed before running.
- Interval bins are quintiles of the pooled realized-interval distribution, so bins are equally populated.
- Physical conditions only (T ∈ {3200, 6400}); zero extinctions in this window, so no survivorship correction.
