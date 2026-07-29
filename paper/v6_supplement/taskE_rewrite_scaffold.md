# v6 Task E — Rewrite scaffold

Target: *Artificial Life* (MIT Press). Methods-cautionary.
Section outline, title and abstract only. No prose drafted.

---

## Proposed title

> **The Detector Was the Result: How Eight Measurement Artifacts
> Produced a 100% Ordering Law in a Protocell Model**

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
> tracked the point at which its statistic became computable, not a
> change in the system. We document eight such defects, each sufficient
> alone to produce the headline. Measured without the detector, the
> ordering holds in ≈1% of runs. We then tested the underlying physical
> hypothesis directly, imposing division regularity as a control
> variable across 1,350 runs, and find it can be neither confirmed nor
> refuted within this design. We argue the general lesson is
> methodological: conceptual peer review reads arguments, and none of
> our reviewers — human or machine — ran the detector against itself. We
> release an automated checklist that recovers all eight defects from
> source.

---

## Section outline

**1. Introduction**
- 1.1 The result as originally obtained; why it looked strong
      (perfect separation, ablation robustness, cross-geometry replication)
- 1.2 Thesis: reproducibility is not validity — a number can reproduce
      exactly and be a number of the wrong thing
- 1.3 Contributions: eight documented defects; a direct test of the
      underlying hypothesis; an automated detector-audit tool

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

**4. Testing the hypothesis directly**
- 4.1 Design: division timing imposed externally; regularity becomes a
      control variable; no detector, no CV estimator in the path
- 4.2 Results: 1,350 runs; the association runs opposite to prediction
- 4.3 Confound analysis: three of four pre-registered checks pass; the
      barely-dividing fraction fails by 2.3 pp
- 4.4 **Verdict: neither confirmed nor refuted.** Why we do not claim
      refutation, and why we did not move the threshold after seeing it
- 4.5 Design limitation: only two physically valid periods; the
      "too fast to organize" regime is untestable here

**5. Why review did not catch this**
- 5.1 What review did catch — three rounds found real problems
      (overreach, missing citations, an unasked question about
      back-reaction) and produced genuine improvements
- 5.2 What it could not catch: conceptual review reads the *argument*.
      Every defect here lived in the *instrument*
- 5.3 The auditor repeated the failure: three results were placed in the
      survivor column during this audit and later withdrawn, each time
      by confirming a number reproduced without checking its reference
      point
- 5.4 Implication: adversarial review of claims is not a substitute for
      mechanical audit of instruments

**6. `detector_audit.py`**
- 6.1 The seven checks and what each encodes
- 6.2 C7: every reported quantity must declare its reference point
- 6.3 Results: 30 findings, 15 critical; all eight defects recovered
      from source with no audit knowledge encoded
- 6.4 Limits: three checks are regex-based; a floor, not a ceiling

**7. What survives**
- §5.2's generalization argument; two §5.3 results as arithmetic only;
  the lipid-supply finding as one result measured two ways; the
  a-priori timescale anchor; extinction under forced fast division
- Explicit statement of what is *not* claimed

**8. Discussion**
- 8.1 Perfect separation as a warning sign, not a strength
- 8.2 Pre-registering detector validation, not just analyses
- 8.3 Why we published the retraction with the data rather than quietly
- 8.4 Cost: what this would have taken to catch before submission
      (one afternoon; the tool runs in seconds)

**9. Data and code availability**
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
