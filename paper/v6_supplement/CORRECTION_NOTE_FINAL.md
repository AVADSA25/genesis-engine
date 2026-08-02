# Correction to "Sequential Assembly of Biological Agency"

**SSRN abstract 6593781 · Correction dated 29 July 2026 · Farina**

---

I withdraw this paper's central result. Re-analysis of my own code and
data shows the reported Clock→Map ordering was produced by measurement
artifacts, not the dynamics it was attributed to.

**Withdrawn:** that division regularity (Clock) preceded spatial
organization (Map) in 1,845/1,845 runs (100%), binomial
*p* = 8.01 × 10⁻¹⁴⁶.

**Eight defects.**

1. **The detector could not fail.** `detect_phase()` latches Map only if
   Clock latched strictly earlier, so 100% was the only reachable
   outcome; both p-values test unreachable nulls.
2. **The delay is the sampling interval.** Median 50 ticks at 50-tick
   sampling; exactly 1 at 1-tick sampling (93.8% of runs, N=100).
3. **The Clock latch is a definedness floor.** CV is undefined until a
   cell completes four divisions; the tick it becomes computable
   coincides with the reported latch (4250 vs 4250 in 1D, 4950 vs 4975
   in 2D). A later experiment showed this is only half an error: the
   *specific* four-division floor is ours, but a floor of order several
   division periods is **physical** — measuring the regularity of a
   ~2,500-tick process requires observing several of its periods, while
   the spatial metric needs ~150 ticks. See below.
4. **The mean delay is three runs.** 243 ± 2,319 ticks is carried by
   seeds 171, 294, 361 (69.0% of delay mass); excluding them, 75.7.
   `paper_data.json` already held `median = 50.0` beside the mean.
5. **The denominator double-counts.** In a one-at-a-time ablation the
   baseline is genuinely shared across parameter groups, and printing it
   in all four rows is standard. The error was summing all twelve rows:
   1,845 → **1,554** distinct runs.
6. **The effect sizes are invalid three ways.** Hedges' *g* uses
   `final_pop` grouped by stability *S*, which multiplies uptake,
   efficiency and maintenance — so *g* measures my own coupling
   constants. In 2D the comparison is 198 vs **2** runs, none between
   thresholds. And the repository's "combined" *g* = 6.34 is exactly
   (9.41 + 3.27)/2 — the arithmetic mean of two effect sizes, which is
   not a valid pooling under any convention, one of whose inputs has
   n = 2. §4.3 explained the lower 2D *g* as "more spatial degrees of
   freedom": a physical story invented for an artifact.
7. **Gate dependence is systematic.** Seven of 19 reported quantities
   depend on detector outputs. Phase-D rates (90%/79%) are withdrawn;
   only the direction survives, and only because two confounds predict
   the opposite sign. **All four §5.3 results are withdrawn or demoted —
   §5.3 does not survive as physics;** two remain as arithmetic with
   their causal readings withdrawn.
8. **ρ(T_div, S) = +0.43 has the wrong sign.** Within each lipid
   condition it is −0.60 to −0.75. Pooling reverses it: a Simpson's
   paradox.

**Corrected figure.** Without the gate, Clock precedes Map in **≈1%** of
runs (1.0%, 1-tick resample N=100; 0.7%, threshold grid N=150; 0.0% in
2D across all nine cells).

**The inverse is also unestablished.** The Map-first signal is partly the
same definedness floor; this model cannot adjudicate the ordering either
way.

**The corrected measurement was itself validated.** Planting a known
ordering in the physics (280 runs), the ungated method recovered it:
ρ = +0.96 between planted and measured, with Clock-first moving from
2.6% to 100% as the plant crossed the natural Clock time. The ≈1% figure
is a real measurement, not a blind instrument, and the method is not
biased toward either direction.

**The hypothesis was then tested directly** — 1,350 runs with regularity
imposed as a control variable, no detector or CV estimator in the path.
The association ran opposite to prediction and survived three of four
pre-registered confound checks, including a matched-interval control
that excludes the obvious alternative. It failed the fourth:
barely-dividing cells rise from 44.0% to 56.2% across the range
(threshold 10 pp). It can therefore be **neither confirmed nor refuted**
by that experiment.

**The original question is malformed as posed.** Asking which metric
crosses its threshold first compares a slow periodic process (division
regularity, period ~2,500 ticks, requiring several periods to measure at
all) against a fast field process (spatial correlation, ~40 ticks,
measurable by ~150). An attempt to build a Clock metric with no
definedness floor produced one defined at tick 6,000 — *later* than the
metric it was built to replace. This is a time-frequency constraint, not
an implementation choice, and no simulation redesign removes it.
Ordering claims of this kind must be tested by **intervention**, which
is what the imposed-regularity experiment above did.

**Also withdrawn:** the Damköhler framing (τ_pattern was the sampling
interval) and the 2D back-reaction (*p* = 0.427). A v5.1c figure of
"roughly 4%" should have read 22.8% — moot, as the result is withdrawn.

**What stands:** §5.2's generalization argument; the 1D Δ-CV (−0.222) and
Phase-E differential (+0.147), as arithmetic only; the timescale anchor
(15.8–38.3 min, bracketing *E. coli*, fixed a priori); extinction under
forced fast division (32.4% at T=200, zero at T ≥ 1600; 27.3% at CV=0 vs
≤4% at CV ≥ 0.1); and **one** lipid-supply result confirmed by two
measures — higher supply → faster division → lower pattern stability,
seen as final *S* 0.823 → 0.644 and restated in thresholded form by
Phase-D attainment. These are not three findings; ρ was the third and it
is withdrawn.

**On reproducibility.** Two of the three companion papers cannot be
reproduced from surviving materials: no Vesicle Division code exists on
any machine I control, and its results file has no CV column, so the
published CV = 0.06 cannot be traced; no Engine code exists either, so
*g* = 4.07 cannot be checked for the same circularity found here. Genesis
Engine published its code. That is the only reason these eight defects
were findable, and correctable, at all.

Found by my own re-analysis; the repository was public throughout and the
evidence sat in the paper's own data files. Full audit:
`paper/v6_supplement/`. The audit is ongoing — further findings will be
recorded in the repository, not issued as further retractions.
