# v6 Task 4 — Blast radius on the sibling papers

## Scope limit, stated up front

Four sibling preprints are cited by this paper:

| key | title (short) | venue |
|---|---|---|
| `farina2025trinity` | The Physical Origins of Biological Agency | SSRN |
| `farina2025engine` | Organized Dissipative Structures Drive Fitness | SSRN |
| `farina2025rd` | Reaction-Diffusion Turing Pattern Formation | SSRN |
| `farina2025vesicle` | Vesicle Division Simulation | SSRN |

**None of their source repositories are present on this machine.** Only
`~/genesis-engine` exists. Direct code inspection — which is what the
task asks for — is therefore not possible here. What follows separates
(a) what is determinable from this paper's own text, from (b) what
requires the sibling repos and remains open.

---

## 4a. Vesicle Division paper (`farina2025vesicle`, CV = 0.06)

### What is determinable

This paper describes exactly how it computes its own comparable CV
(line 220 of the manuscript):

> CV = 0.045 ± 0.023, "computed per cell from its `division_times`
> series and averaged across all cells present at the **final tick** of
> each run — typically 30–45 cells per run, yielding population-level
> CVs based on **5–12 division intervals per cell**"

This is the **benign** use of the statistic:

- measured at the final tick, i.e. at steady state, not during a transient
- based on 5–12 intervals per cell, not the 3-interval minimum
- reported as a descriptive summary, **not** used as a detector or a
  transition marker

The CV = 0.06 from the Vesicle paper is invoked only as a steady-state
value for numerical comparison against this steady-state value. A
steady-state-to-steady-state comparison does not inherit the defect
found in Task 1.

### Why the Task 1 defect does not automatically propagate

The Task 1 defect is **not** "CV is computed wrongly". The production CV
formula is fine as a descriptive statistic. The defect is that CV was
used as a **phase detector**, where its definedness floor (undefined
until a cell completes four divisions) became the measured transition
time. Any use of CV that is not a detector is unaffected by that finding.

### What remains open (requires the repo)

1. Does the Vesicle paper use CV anywhere as a **detector, threshold, or
   transition marker** — e.g. "regular division is achieved at tick T"?
   If yes, that claim inherits the definedness-floor defect and must be
   corrected.
2. Does it compute CV with `numpy.std()` at **ddof=0** over a *growing*
   number of intervals? If the reported CV = 0.06 is a steady-state
   value over 5–12 intervals, the residual bias is small and the number
   stands. If it is measured early or over a drifting n, it is biased low.

**Assessment: LOW risk**, on the evidence available. The one use visible
from here is benign. Confirmation requires the repo.

---

## 4b. Engine paper (`farina2025engine`, Hedges' g = 4.07)

### What is determinable

The Genesis paper cites g = 4.07 from the Engine paper and describes its
own g = 9.41 as larger, "reflecting the **tightened coupling** in the
Genesis Engine implementation."

That sentence is itself the finding. It concedes that the effect size
tracks the **strength of the S→fitness coupling constants**, not an
independently discovered effect. This is precisely the circularity
established for this paper in Task 4c: g is computed on `final_pop`,
grouped on `final_mean_s`, while S multiplies uptake, efficiency and
maintenance directly (UPT_BONUS 0.12, EFF_BONUS 0.70, MAINT_BONUS 0.35).

If the Engine paper computes g the same way — grouping on an
organization measure and measuring a fitness/population outcome that the
same measure causally drives — then g = 4.07 is circular for the same
reason, and the Genesis paper's comparison of 9.41 against 4.07 is a
comparison of two coupling-constant choices rather than of two
measured effects.

The phrase "tightened coupling" is strong circumstantial evidence that
both numbers are coupling-determined, because it explains the difference
between them *by* the coupling strength.

### What remains open (requires the repo)

1. What is the dependent variable behind g = 4.07?
2. Is the grouping variable causally upstream of that dependent variable
   in the Engine model's code?
3. Are the comparison groups balanced? (Here they were 482 vs 18.)

**Assessment: MEDIUM-HIGH risk.** The paper's own explanation for the
difference between 9.41 and 4.07 presupposes the coupling-dependence
that makes both numbers uninterpretable as discovered effects.

---

## 4c. `farina2025trinity` and `farina2025rd`

Not assessed. `farina2025rd` is cited but uncited in the body
(it appears in `references.bib` without a `\cite` in the text).
`farina2025trinity` is the framework paper this one extends; whether it
makes independent quantitative claims that depend on the phase detector
cannot be determined without its source.

---

## Consequence for the SSRN correction note

The correction should:

- **State plainly** that the defect is specific to CV-as-detector, and
  that steady-state descriptive uses of CV are unaffected. This prevents
  over-broad reading of the retraction.
- **Flag the Hedges' g circularity as likely shared** with the Engine
  paper, and commit to checking it, rather than asserting either that it
  is or is not affected.
- **Not** claim the sibling papers are clean, because that has not been
  verified.

## Evaluation criteria used

- "Affected" = the claim depends on CV as a detector/transition marker,
  or on an effect size whose dependent variable is causally determined
  by its grouping variable.
- "Unaffected" = descriptive steady-state use with adequate sample size.
- Determinations made only from text present in this repository; no
  claim is made about code that was not read.

## To close this task

Clone the sibling repos and grep for: `division_times`, `detect_phase`,
threshold constants on CV, and the `hedges_g` call site with its
dependent variable. Two greps per repo would settle both questions.
