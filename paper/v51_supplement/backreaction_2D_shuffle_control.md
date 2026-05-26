# 2D back-reaction: shuffle control (Phase-C anchor test)

## Question
Is the observed 2D Δcv = +0.057 specifically caused by Phase-C
latching, or is it a generic 'later-in-run' population-age
drift that would appear at any anchor time?

## Real and diagnostic anchors

| Test | n | mean Δcv | median | sign +/− | p (sign-test) |
|---|---|---|---|---|---|
| T1 real          (anchor = phc) | 157 | +0.05732 | +0.02302 | 93/64 | 0.0251 |
| T3 pre-latch     (anchor = phc - 3000) | 184 | -0.79197 | -0.79915 | 0/184 | 8.16e-56 |
| T4 deeper-post   (anchor = phc + 2000) | 1 | -0.04732 | -0.04732 | 0/1 | 1 |
| T5 fixed-abs     (anchor = 4975 for all runs) | 198 | -0.00734 | -0.00857 | 85/113 | 0.0547 |

## Permutation null (gold-standard control)

For each of N = 2000 permutations, each run's `phc` value was replaced by the `phc` of a different (randomly chosen) run, and Δcv was recomputed at that random anchor.

- Null distribution mean = -0.10737
- Null distribution sd   = 0.01344
- 95% interval = [-0.13353, -0.08146]
- Observed mean Δcv = +0.05732
- **Permutation p (one-sided, real ≥ null) = 0.0000**

## Verdict

**REAL: the 2D back-reaction effect is statistically anchored to Phase C — survives phc-shuffle control.**