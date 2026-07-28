# v6 Task B — Sibling-paper code: resolved

## Question

Task 4 was left open because the Vesicle Division (Farina 2025c,
CV = 0.06) and Engine/Negentropy (Farina 2025a, Hedges' g = 4.07) code
could not be found. The author states all code is combined in the
genesis-engine repository. This resolves it directly.

## Method

Searched the **entire repository across all branches and all history**,
not just the working tree:

```
git branch -a
git log --all --pretty=format: --name-only --diff-filter=A | sort -u
grep -rn "hedges_g" . --exclude-dir=.git
grep -rn "4\.07" . --exclude-dir=.git
```

## Result — the sibling code is NOT in this repository

- Branches: `main` only (plus its remote tracking ref). No other branch.
- Every `.py` file ever **added** in history (29 files) belongs to the
  Genesis Engine: the two engines, mesh utils, the MC/ablation runners,
  the v51–v53 analyses, the v6 analyses, the paper scripts, `web/server.py`.
- Files matching `vesicle|negentrop|dissipativ|trinity`: **none**, in the
  working tree or anywhere in history.
- `hedges_g` is **defined once** (`analyze_results.py:46`) and **called
  once** (`analyze_results.py:167`), on `final_pop`.
- The value `4.07` appears **only** as a citation inside the Table 1
  caption (`genesis_paper_farina_2026.tex:217` and the markdown
  original). It is **not computed anywhere in this repository.**

**Conclusion.** The Vesicle Division and Engine papers were produced by
code that is not in this repository. Their claims cannot be audited
from here, and the earlier "all code is combined" understanding does not
hold for them.

## What is needed to close the sibling audit

For each of the two papers, the source that produced its published
numbers. Two greps then settle it:

1. **Vesicle (CV = 0.06):** is CV used anywhere as a *detector,
   threshold, or transition marker*, or only as a steady-state
   descriptive statistic? Only the former inherits the Task 1 defect.
2. **Engine (g = 4.07):** what is the dependent variable, and is the
   grouping variable causally upstream of it (as `final_mean_s` is of
   `final_pop` here)? What are the two group sizes?

## Risk assessment, unchanged in substance but now firmly bounded

- **Vesicle — LOW.** The only visible use is benign: this paper's own
  comparable CV is computed at the final tick over 5–12 intervals per
  cell as a descriptive statistic (manuscript line 220). The Task 1
  defect is CV-as-detector, not CV-as-statistic.
- **Engine — MEDIUM-HIGH, unresolved.** The Genesis paper explains its
  own g = 9.41 versus 4.07 as "reflecting the tightened coupling in the
  Genesis Engine implementation." That sentence concedes the effect size
  tracks the S→fitness coupling constants. If g = 4.07 is computed the
  same way, it is circular for the same reason. This cannot be confirmed
  or refuted from this repository.

---

## Incidental finding — a SIXTH defect, in this paper

While locating the effect-size code, the group sizes behind both
reported Hedges' g values were recomputed from the archived summaries:

| geometry | organized (S̄ > 0.3) | disorganized (S̄ < 0.1) | g | paper |
|---|---|---|---|---|
| 1D | n = 482 | **n = 18** | 9.4124 | 9.41 ✓ |
| 2D | n = 198 | **n = 2** | 3.2737 | 3.27 ✓ |

Both reproduce exactly. The **2D effect size rests on a comparison group
of two runs** (seeds 65 and 114, both with `final_mean_s` = 0.0000). No
2D run falls in the interval [0.1, 0.3], so the split is degenerate
rather than merely unbalanced.

A Hedges' g reported against an n = 2 arm is not an interpretable effect
size. This is independent of, and additional to, the circularity already
established in Task 4c, and it was not in the five-defect list. It
belongs in the correction.

## Evaluation criteria used

- "Present in repo" = appears in `git log --all --diff-filter=A`, i.e.
  was added at some point on any branch, not merely present now.
- Group sizes recomputed from `results/summary.csv` and
  `results_2d/summary.csv` using the Methods thresholds
  (organized S̄ > 0.3, disorganized S̄ < 0.1) and this repo's own
  `hedges_g`, reproducing both published values to 2 dp.
