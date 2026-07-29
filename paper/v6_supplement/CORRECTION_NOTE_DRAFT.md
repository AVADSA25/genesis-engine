# Correction to "Sequential Assembly of Biological Agency"

**SSRN abstract 6593781 · Correction dated 29 July 2026 · Farina**

**DRAFT FOR REVIEW — NOT POSTED**

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
   cell completes four divisions. The tick it becomes computable
   coincides with the reported latch: 4250 vs 4250 (1D), 4950 vs 4975 (2D).
4. **The mean delay is three runs.** 243 ± 2,319 ticks is carried by
   seeds 171, 294, 361 (69.0% of delay mass); excluding them, 75.7.
   `paper_data.json` already held `median = 50.0` beside the mean.
5. **The denominator double-counts.** In a one-at-a-time ablation the
   baseline is genuinely shared across parameter groups, and printing it
   in all four rows is standard. The error was summing all twelve rows:
   1,845 → **1,554** distinct runs.
6. **Both effect sizes are invalid, twice over.** Hedges' *g* uses
   `final_pop` grouped by stability *S*, which multiplies uptake,
   efficiency and maintenance — so *g* measures my own coupling
   constants. In 2D the comparison is 198 vs **2** runs, none between
   thresholds. §4.3 explained the lower 2D *g* as "more spatial degrees
   of freedom": a physical story invented for an artifact.
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

**The hypothesis was then tested directly** — 1,350 runs with regularity
imposed as a control variable, no detector or CV estimator in the path.
The association ran opposite to prediction but failed one of four
pre-registered confound checks (barely-dividing cells vary by 12.3
percentage points; threshold 10). It can be **neither confirmed nor
refuted** here. The valid window holds only two division periods, leaving
the "too fast to organize" regime untestable.

**Also withdrawn:** the Damköhler framing (τ_pattern was the sampling
interval) and the 2D back-reaction (*p* = 0.427). A v5.1c figure of
"roughly 4%" should have read 22.8% — moot, as the result is withdrawn.

**What stands:** §5.2's generalization argument; the 1D Δ-CV (−0.222)
and Phase-E differential (+0.147), as arithmetic only; final *S*
0.823 → 0.644 with lipid supply; the timescale anchor (15.8–38.3 min,
bracketing *E. coli*, fixed a priori); and extinction under forced fast
division (32.4% at T=200, zero at T ≥ 1600; 27.3% at CV=0 vs ≤4% at
CV ≥ 0.1).

The sibling Engine paper's *g* = 4.07 is unverified; its source is absent
from the public repository.

Found by my own re-analysis; the repository was public throughout and the
evidence sat in the paper's own data files. Full audit:
`paper/v6_supplement/`. The audit is ongoing — further findings will be
recorded in the repository, not issued as further retractions.
