# v6 Task E — Rewrite scaffold

Target: *Artificial Life* (MIT Press). Methods-cautionary.
Section outline, title and abstract only. No prose drafted.

---

## Proposed title

> **The Detector Was the Result: Eight Measurement Artifacts, and a
> Question That Cannot Be Asked This Way**

Alternates:
- *Reproducible and Wrong: A Self-Audit of a Perfect Simulation Result*
- *What 1,845 out of 1,845 Actually Measured*

Recommendation: the first. It states the finding and the number, and
"the detector was the result" is the transferable lesson in five words.

---

## Proposed abstract (~200 words)

> We report a simulation result, its retraction, and the audit that
> produced both. A protocell model of 1,845 Monte Carlo runs appeared to
> show that division regularity precedes spatial organization without
> exception — 100% consistency, binomial *p* ≈ 10⁻¹⁴⁶. The result was
> reproducible, survived a twelve-condition parameter ablation, and
> passed three rounds of external adversarial review. It was an
> artifact. The phase detector latched the second predicate only after
> the first, so no other outcome was reachable; the reported delay
> equalled the sampling interval; the first predicate's latch time
> tracked when its statistic became computable, not a change in the
> system. We document eight such defects, each sufficient alone to
> produce the headline. We then validate the corrected measurement by
> planting a known ordering in the physics and recovering it
> (ρ = +0.96), so that the corrected figure — the ordering holds in ≈1%
> of runs — is a measurement rather than a blind spot. Three attempts to
> rescue the hypothesis follow. The third is the result: a Clock metric
> built to have no definedness floor becomes defined *later* than the
> one it replaces, because measuring the regularity of a ~2,500-tick
> periodic process requires observing several of its periods, while
> spatial correlation over a ~40-tick field is measurable in ~150. The
> asymmetry that produced the original artifact is therefore partly a
> time-frequency constraint, not an implementation error, and the
> ordering question is malformed as posed: comparing first-crossing
> times measures the ratio of two intrinsic timescales, not the
> dynamics. Such claims must be tested by intervention instead. We
> release an automated checklist that recovers all eight defects from
> source, and note that its authors reproduced the same class of error
> five times while writing this paper.

---

## Section outline

**1. Introduction**
- 1.1 The result as originally obtained; why it looked strong
      (perfect separation, ablation robustness, cross-geometry replication)
- 1.2 Thesis: reproducibility is not validity — a number can reproduce
      exactly and be a number of the wrong thing
- 1.3 Contributions: eight documented defects; a validated corrected
      measurement; the demonstration that the question is malformed as
      posed; an automated detector-audit tool

**2. The model and the original claim**
- 2.1 Protocell dynamics (membrane growth, Gray-Scott RD, geometric division)
- 2.2 The Clock / Map / Engine phase predicates
- 2.3 The published result and the confidence attached to it
- *No new content; needed so the audit is legible*

**3. The audit**
- 3.1 Method: re-run under instrumentation, not re-read
- 3.2 **Defect 1 — the gate.** `detect_phase()` cannot emit a violation;
      both p-values test unreachable nulls
- 3.3 **Defect 2 — the delay is the sampling interval.** 50 ticks at
      50-tick sampling; 1 tick at 1-tick sampling
- 3.4 **Defect 3 — the latch time is a definedness floor.** CV needs four
      divisions; latch coincides with computability
- 3.5 **Defect 4 — three runs carry the mean.** Seeds 171, 294, 361 =
      69.0% of delay mass
- 3.6 **Defect 5 — the denominator.** Shared OAT baseline summed across
      twelve rows: 1,845 → 1,554
- 3.7 **Defect 6 — the effect sizes, and the story told about them.**
      *Centrepiece.* `final_pop` grouped by the variable that determines
      it; the 2D comparison arm is n = 2; §4.3 explained the resulting
      number with "more spatial degrees of freedom." An artifact appeared
      and we reached for physics instead of checking `len()`
- 3.8 **Defect 7 — gate dependence is systematic.** 7 of 19 quantities;
      all four §5.3 results withdrawn or demoted
- 3.9 **Defect 8 — a sign reversal.** ρ = +0.43 pooled, −0.60 to −0.75
      within every stratum
- 3.10 The corrected figure: ≈1% by two independent methods

**4. Validating the corrected instrument** *(new — do this before any null)*
- 4.1 Why a null from an unvalidated instrument is worthless — the same
      error as the original paper, pointed the other way
- 4.2 Planting a known ordering in the physics (not the detector);
      ρ = +0.96 recovery, Clock-first 2.6% → 100% across the plant sweep
- 4.3 Consequence: the ≈1% figure is a measurement, not a blind spot

**5. Three attempts to rescue the hypothesis, and what the third revealed**
- 5.1 *Intervention.* Impose regularity as a control variable (1,350
      runs). Association runs opposite to prediction; survives three of
      four pre-registered confounds, fails the fourth. Neither confirmed
      nor refuted
- 5.2 *Reformulation.* Minimum-interval floor instead of regularity.
      Fails — and the pooled ρ = +0.38 that looked like support is the
      third Simpson's paradox in the project
- 5.3 *Redesign.* Build a Clock metric with no definedness floor. **It
      arrives at tick 6,000 — later than the metric it replaces**
- 5.4 **The finding.** You cannot measure the regularity of a
      ~2,500-tick periodic process without observing several periods;
      spatial correlation over a ~40-tick field needs ~150. The
      asymmetry is a time-frequency constraint, not a defect. Defect 3
      is only half ours
- 5.5 **Therefore the question is malformed as posed.** First-crossing
      comparison between a slow periodic process and a fast field
      process measures their timescale ratio, not their dynamics. This
      explains why every approach failed identically
- 5.6 The constructive replacement: ordering claims must be tested by
      *intervention*, not timing — and §5.1 is that test

**6. Why review did not catch this**
- 6.1 What review did catch — three rounds found real problems
      (overreach, missing citations, an unasked question about
      back-reaction) and produced genuine improvements
- 6.2 What it could not catch: conceptual review reads the *argument*.
      Every defect here lived in the *instrument*
- 6.3 The auditor repeated the failure, five times, in two distinct
      forms. **Wrong reference point** (×3): results placed in the
      survivor column, each later withdrawn after confirming a number
      reproduced without checking what it was a number *of*. **Wrong
      scope** (×2): a correct number generalised past its domain — "~50%
      of cells barely divide in every condition" was true of one forced-
      division design and false of the model, and a pre-registered
      decision rule returned the right verdict for the wrong reason
- 6.4 Implication: adversarial review of claims is not a substitute for
      mechanical audit of instruments — and the auditor needs the same
      mechanical checks as the author

**7. `detector_audit.py`**
- 7.1 The eight checks and what each encodes
- 7.2 C7: every reported quantity must declare its reference point
- 7.3 C8: pooled statistics must survive stratification — added after
      three Simpson's paradoxes slipped past C1–C7
- 7.4 Results: 30 findings, 15 critical; all eight defects recovered
      from source with no audit knowledge encoded
- 7.5 Limits: three checks are regex-based; a floor, not a ceiling

**8. What survives**
- §5.2's generalization argument; two §5.3 results as arithmetic only;
  the lipid-supply finding as one result measured two ways; the
  a-priori timescale anchor; extinction under forced fast division
- Explicit statement of what is *not* claimed

**9. Discussion**
- 9.1 Perfect separation as a warning sign, not a strength
- 9.2 Pre-registering detector validation, not just analyses
- 9.3 Why we published the retraction with the data rather than quietly
- 9.4 Cost: what this would have taken to catch before submission
      (one afternoon; the tool runs in seconds)

**10. Data and code availability**
- Repository public throughout, including during the period the claim
  was live; `paper_data.json` already contained `median = 50.0`
  beside the reported mean

---

## Notes on framing

- **Do not** frame as heroic self-correction. The tone that works is
  flat and specific: here is what we did, here is why it was wrong, here
  is the tool.
- **Do** keep §5.3 (auditor repeated the failure). It is the difference
  between a retraction notice and a methods paper.
- The 1,845 → 1,554 denominator and the n = 2 group are the two details
  reviewers will remember. Give each its own subsection rather than
  burying them in a list.
- Length target ~6,000 words; *Artificial Life* accepts methods and
  perspective pieces of this scale.
