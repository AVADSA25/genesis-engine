# Genesis Engine — HANDOVER (3 Aug 2026)

## STATE: audit complete, correction drafted, NOT POSTED

The one outstanding action is yours: post the correction to SSRN
abstract 6593781. Everything else is done and pushed.

`paper/v6_supplement/CORRECTION_NOTE_FINAL.md` — paste-ready.

---

## THE HEADLINE

The paper's central claim (Clock precedes Map, 1,845/1,845, 100%,
p = 8.01e-146) is **withdrawn**. It was produced by measurement
artifacts, not by the dynamics.

Corrected figure: **Clock precedes Map in ~1% of runs.**

---

## EIGHT DEFECTS IN THE PUBLISHED PAPER

1. The detector could not fail — `detect_phase()` latched Map only after
   Clock, so 100% was the only reachable output; both p-values test
   unreachable nulls
2. The reported delay IS the sampling interval — 50 @50-tick, exactly
   1 @1-tick
3. The Clock latch coincides with when CV first becomes computable
   (partly physical — see below)
4. The 243-tick mean is carried by 3 seeds (171, 294, 361 = 69% of mass)
5. Denominator double-counted the shared OAT baseline: 1,845 -> 1,554
6. Effect sizes invalid three ways — circular DV, an n=2 arm in 2D, and
   a "combined" g = 6.34 that is just (9.41+3.27)/2
7. Gate dependence systematic — 9 of 19 quantities directly, a 10th
   indirectly; all four sec 5.3 results withdrawn or demoted
8. rho(T_div,S) = +0.43 has the WRONG SIGN (-0.60 to -0.75 stratified)

---

## THE DEEPEST FINDING (this is the new paper)

The ordering question is **malformed as posed**.

Asking "which metric crosses first" compares a slow periodic process
(division regularity, ~2,500 ticks, needs several periods to measure)
against a fast field process (spatial correlation, ~40 ticks, measurable
by ~150). A Clock metric built to have NO definedness floor came out
defined at tick 6,000 — LATER than the one it replaced. The buffer
sweep then showed it was not even a valid metric until ~9 periods
(24,000 ticks), so the honest figure is 160x, not 40x.

Time-frequency constraint, not an implementation error. No simulation
redesign removes it. **Defect 3 is only half ours.**

Consequence: ordering claims of this kind must be tested by
INTERVENTION, not timing. That test was run (1,350 runs, imposed CV) and
found no support for the theory.

---

## WHAT SURVIVES

- sec 5.2 generalization argument (S measures persistence, not Turing)
- Timescale anchor: 15.8-38.3 min, brackets E. coli, fixed a priori
- ONE lipid-supply result, two measures: higher supply -> lower pattern
  stability (S 0.823 -> 0.644). MECHANISM NOT IDENTIFIED — the
  'via faster division' chain is refuted by the stratified data.
- Extinction findings: 32.4% at T=200, zero at T>=1600; and 27.3% at
  CV=0 vs <=4% at CV>=0.1 (lockstep division starves whole populations)
  — BOTH confined to imposed periods <=800, which the model treats as
  unphysical. Zero extinctions anywhere at T>=1600.
- 1D dCV (-0.222) and Phase-E (+0.147) as ARITHMETIC ONLY
- The measurement itself is validated: planting a known ordering,
  rho = +0.96 recovery, Clock-first 2.6% -> 100%

---

## MY OWN ERRORS, PUBLISHED TO THIS REPO AND LATER WITHDRAWN

SEVEN, in four classes. All are in the repo history and in sec 6.3 of
the paper. (6) validating clock_r by eye from an insignificant
correlation; (7) inventing a survivorship explanation refuted by the
same grid. Both were found only by re-running with saved outputs.

WRONG REFERENCE POINT (x3) — confirmed a number reproduced without
checking what it was a number OF:
 1. Called the 2D back-reaction "the most interesting surviving number
    in the project". It does not replicate (p = 0.427).
 2. Corrected "roughly 4%" to 22.8% — correct arithmetic applied to a
    result that should have been withdrawn entirely.
 3. Put 1D dCV and Phase-E in the survivor column. Both anchored on
    detector outputs; the causal readings are not licensed.

WRONG SCOPE (x2) — a correct number generalised past its domain:
 4. "~50% of cells barely divide in every condition, so
    division-perturbation effects cannot be isolated in this model at
    all." True of ONE forced-division design (44-56%); false of the
    model under natural division (11-13%).
 5. Claimed a timescale-separation mechanism from a comparison of an
    unphysical condition against a physical one.

Also: a pre-registered decision rule returned the RIGHT verdict for the
WRONG reason (Task R), which is its own failure mode.

---

## PUBLIC ARTIFACTS

- SSRN 6593781 — **STILL UNCORRECTED. This is the open action.**
- Dashboard genesis-engine.lucyvpa.com — corrected, banner live,
  KPIs marked WITHDRAWN, stale CSV disclosed. Static files served via
  cloudflared -> localhost:3001 -> LaunchAgent. Edit files in
  ~/genesis-engine/web/, no restart needed.
- README — corrected, banner + claim-by-claim table
- Repo — public throughout, all audit data and scripts pushed

---

## TOOLS PRODUCED

`tools/detector_audit.py` — 8 checks. 31 findings, 16 critical on this
repo. Recovers SIX of the 8 defects (not all 8 — see final audit round
below). C7 and C8 were added because C1-C6 missed my own errors.
`tools/test_detector_audit.py` — negative controls, 5/5. Run these
before trusting any audit count; C3 shipped unfalsifiable.

`paper/v6_supplement/LAB_PROTOCOL.md` — 5 wet-lab experiments, one
counterintuitive (synchrony fragility), one that can settle the ordering
question a simulation structurally cannot.

---

## TASK S IS NOW ARCHIVED — AND IT CHANGED (2 Aug 2026)

Task S had been run inline; no script, no CSV. Re-run and archived as
`experiment_v6_taskS_symmetric.py` -> `results_v6/taskS_symmetric.csv`
(40 seeds x 2 parameterisations, 20k ticks), analysed by
`analysis_v6_taskS.py`, which regenerates the results document.

Definedness result HOLDS and is the paper's spine:
  S = 150, CV = 4450, clock_r = 6000. The floor-free metric arrives
  last. Note 4450, not the 4825 previously in prose — definedness lies
  on a 50-tick grid, so 4825 was a median over an even run count.

Validity result CHANGED, against the paper:
  rho(clock_r, CV) = -0.2364 is exactly seeds 0-9 and was NEVER
  significant (p = 0.511). At n = 40 it is -0.0822 (p = 0.614).
  The long parameterisation fails the same validity check the short one
  fails. The paper quotes the correlation without its p-value, which
  presents an unvalidated metric as a working one.

=> Do not describe clock_r as a metric that "works but arrives late."
   It arrives late AND was never shown to measure regularity.

OPEN: buffer sweep running (`V6_SWEEP=1`, 4 spans x 40 seeds, 40k
ticks -> `results_v6/taskS_buffer_sweep.csv`) to establish whether
validity is reachable at ANY buffer length. Sample count held at 120 so
only span varies — a curve, not a search for a length that works.

## FINAL AUDIT ROUND (3 Aug 2026) -- 22 MORE ERRORS

An adversarial fact-check of the revised draft checked 196 numeric
claims and confirmed 22 errors; 6 alleged ones were dismissed on
verification. Several were introduced by the revision that fixed the
previous round. All 22 applied; paper recompiles at 27pp.

Two worth remembering:

C3 COULD NOT FAIL. `si = sample_interval or int(med)` with
sample_interval always None => the grid was defined to be the median,
and the second clause is true by the definition of a median. The check
fired on any integral median and could never pass. That is Defect 1
(a predicate that cannot emit a violation) reproduced inside the tool
built to detect it. Fixed: grid now inferred as the GCD of delays,
median must equal one step with a majority exactly on it. Negative
controls added in tools/test_detector_audit.py -- 5/5. RUN THEM.

INVENTED MECHANISM. The revision explained the non-monotone S(CV) point
by survivorship, citing 27.3% extinction at CV=0. That table excludes
every period where those extinctions happen; in its own window
extinction is 0/675. Entry (7) of section 6.3 now.

Also: the tool recovers SIX of eight defects, not all eight -- no check
reads results/ablations/ (both data checks glob "summary.csv", the file
is "ablation_summary.csv"), and C8 finds Defect 8's class on a different
quantity. If you want 8/8, add a check that reads the ablation summary
and recomputes rho(T_div,S) over the lipid strata. NOT done here: adding
checks changes the tool's described identity and was not asked for.

The ~3,170 "natural period" was an artifact of a hardcoded 50,000-tick
divisor applied to 40,000-tick runs. The earlier "different
configurations" reconciliation was itself invented; both figures are
~2,540.

## NEXT STEPS

1. Post the SSRN correction (yours) -- CORRECTION_NOTE_FINAL.md is now
   consistent with the revised paper (sweep result, ~2,540 period,
   extinction scope). It was NOT consistent before this round.
2. Write the methods paper from `taskE_rewrite_scaffold.md` — target
   Artificial Life (MIT Press)
3. Consider promoting detector_audit.py to a CODEC skill (caveat:
   C1/C2/C5 are regex-based, a floor not a ceiling)
4. Sibling papers: Vesicle CV=0.06 and Engine g=4.07 are UNVERIFIABLE —
   no source exists on any machine. Two greps each would settle them if
   the code resurfaces.
