# v6 Task 4 — Statistics correction

## 4a. The delay summary is a mean of a floor-censored, heavy-tailed distribution

| geometry | n | published summary | median | IQR | min | max | % at 50-tick floor |
|---|---|---|---|---|---|---|---|
| 1D | 482 | 243 ± 2319 | **50** | [50, 50] | 50 | 38400 | **434/482 = 90.0%** |
| 2D | 198 | 56 ± 41 | **50** | [50, 50] | 50 | 450 | **193/198 = 97.5%** |

The median equals the sampling interval and the IQR has **zero width** in both geometries. `paper/paper_data.json` already contained `delay_C_minus_B/median = 50.0` alongside the mean; the manuscript sentence reported only the mean.

The same file records the 2D pilot as `mean=50, median=50, min=50, max=50` — every run at exactly the sampling interval, zero variance.

## 4b. Which runs carry the 1D mean

Total 1D delay mass: **117,100 ticks** across 482 runs.

| rank | seed | delay | share of total mass | cumulative |
|---|---|---|---|---|
| 1 | 171 | 38,400 | 32.8% | **32.8%** |
| 2 | 294 | 32,000 | 27.3% | **60.1%** |
| 3 | 361 | 10,450 | 8.9% | **69.0%** |
| 4 | 202 | 900 | 0.8% | **69.8%** |
| 5 | 219 | 700 | 0.6% | **70.4%** |
| 6 | 5 | 650 | 0.6% | **71.0%** |

**Three runs out of 482 carry 69.0% of the entire delay mass.** Removing them changes the mean from 242.9 to 75.7 ticks — i.e. to within 25.7 ticks of the sampling floor.

The reported SD (2319) is roughly **10x its own mean** (243). That is not a summary statistic; it is a description of three lineages.

## 4c. Hedges' g — dependent variable and circularity

Located at `analyze_results.py:147-151`:

```python
organized    = [r["final_pop"] for r in data if r["final_mean_s"] > 0.3]
disorganized = [r["final_pop"] for r in data if r["final_mean_s"] < 0.1]
g = hedges_g(np.array(organized), np.array(disorganized))
```

**The dependent variable is `final_pop`** — final population count — with groups split on `final_mean_s`. This is named nowhere in the manuscript, Table 1, Table 2, or `paper_data.json`.

**The effect is substantially circular.** In `genesis_engine.py` the same S that defines the grouping multiplies three fitness terms directly (lines 356-359):

```python
uptake = E_UPTAKE * (1 + UPT_BONUS  * S) * resource_frac   # UPT_BONUS  = 0.12
eff    = E_EFFICIENCY * (1 + EFF_BONUS * S)                # EFF_BONUS  = 0.70
maint  = E_MAINTENANCE * (1 - MAINT_BONUS * S)             # MAINT_BONUS= 0.35
```

High S raises uptake and efficiency and lowers maintenance, which raises energy, which lowers death rate, which raises `final_pop`. Grouping on S and measuring `final_pop` therefore largely measures the magnitude of `EFF_BONUS`, `MAINT_BONUS` and `UPT_BONUS` — constants chosen by the modeller — rather than a discovered thermodynamic effect.

Group sizes are also severely imbalanced: **n_organized = 482 vs n_disorganized = 18** (from `paper_data.json`), so the pooled SD is dominated by one arm.

## 4d. Wilcoxon signed-rank — tie structure and what it tests

- Input: 1D delays, n = 482
- Tied at exactly 50: **434/482 = 90.0%**
- Distinct values in the whole sample: **15**
- Minimum value: 50 (= the sampling interval)

Published: `W = 116403, p = 1.66e-98`, `alternative='greater'`, i.e. H0: median delay <= 0.

**The test is uninformative, for a reason more basic than the ties.** The gate in `detect_phase()` cannot emit C at or before B, so every delay is >= one sampling interval by construction. The null (delay <= 0) is not merely false, it is *unreachable* — no possible run could have produced a value inconsistent with it. A p-value against an unreachable null carries no evidence.

Separately, 90.0% of the input is a single repeated value, so the signed-rank statistic is computed over 15 distinct levels; the normal approximation behind the reported p-value is not appropriate at this tie fraction.

---

## Proposed replacement for the manuscript sentence

Current (`paper_data.json:/mc_1d/manuscript_sentence`):

> In N = 500 independent simulations ... the Clock preceded the Map in 482 of 482 runs (100 %; binomial test p = 8.01e-146). The mean Clock → Map delay was 243 ± 2319 ticks (Wilcoxon signed-rank W = 116 403, p = 1.66e-98). Populations that achieved stable patterns (S > 0.3, N = 482) outperformed disorganized populations (S < 0.1, N = 18) with Hedges' g = 9.41.

Corrected:

> Across 482 runs in which both predicates latched, the gated detector reported Clock before Map in 482/482 cases. This proportion is not evidence: the detector latches Map only if Clock latched at a strictly earlier tick, so no other outcome was reachable, and the associated binomial and Wilcoxon tests are computed against unreachable nulls. The measured delay has median 50 ticks (IQR [50, 50]; 90.0% of runs at exactly the 50-tick sampling interval); the mean of 243 ticks is carried by three runs holding 69.0% of total delay mass. Under ungated first-crossing measurement the ordering reverses (Clock first in 0.7% of 1D and 0.0% of 2D runs). The reported Hedges' g = 9.41 is computed on final population count grouped by pattern stability S, a quantity S multiplies directly through the efficiency, uptake and maintenance terms; it therefore reflects the chosen coupling constants rather than a discovered effect.

## Evaluation criteria used

- All figures recomputed from `results/summary.csv` and `results_2d/summary.csv`; no re-simulation.
- 'On the floor' = delay <= the 50-tick sampling interval.
- Circularity judged by tracing whether the grouping variable appears in the causal chain producing the dependent variable.

---

## 4e. Denominator inflation (found by the v6 audit, verified independently)

The headline "1,845 runs" pools three studies: 482 (1D main) + 1,165
(ablation grid) + 198 (2D). The ablation grid sweeps four parameters at
three levels each, and in each sweep one level IS the baseline value.
Those four baseline conditions are therefore the same configuration.

Verified from `results/ablations/ablation_summary.csv` — all four
baseline rows are identical to the last decimal place:

| parameter | value | mean_B_tick | mean_C_tick | mean_final_S | mean_pop |
|---|---|---|---|---|---|
| LIPID_SUPPLY | 0.015 | 4416.0 | 4518.556701030928 | 0.7521093934 | 37.89 |
| RD_NOISE | 0.004 | 4416.0 | 4518.556701030928 | 0.7521093934 | 37.89 |
| GROWTH_PERTURB | 0.15 | 4416.0 | 4518.556701030928 | 0.7521093934 | 37.89 |
| STAB_WINDOW | 40 | 4416.0 | 4518.556701030928 | 0.7521093934 | 37.89 |

Distinct statistical signatures among the four: **1**.

- Ablation runs counted: 1,165 → **874 distinct**
- Duplicate-counted: **291**
- Headline denominator 1,845 → **1,554 distinct runs**

The ablation grid also reuses seeds 0–99 in every condition, so even the
non-baseline conditions are not independent of one another; they are the
same 100 initial states re-run under different parameters. Any pooled
test treating the 1,845 as independent Bernoulli trials is invalid on
this ground alone, before the unreachable-null problem is considered.
