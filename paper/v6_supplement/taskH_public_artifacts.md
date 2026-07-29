# v6 Task H — Public artifacts still asserting withdrawn claims

Two public surfaces carried the withdrawn headline. One is fixed; the
other is **proposed only and awaiting confirmation** — no deploy action
was taken, per instruction.

---

## 1. Repository README — **FIXED AND PUSHED**

Version-controlled and reversible, so edited directly.

### Claims found

| line | claim | status |
|---|---|---|
| 22 | "1,165 of 1,165 runs (**100 %**; combined binomial *p* < 10⁻²⁰⁰; Hedges' *g* = 6.34)" | withdrawn |
| 33 | "Clock always precedes Map. 1,165 / 1,165 = 100 %. Zero violations." | withdrawn |
| 35–36 | 1D *p* = 8.01 × 10⁻¹⁴⁶, *g* = 9.41; 2D *p* = 2.49 × 10⁻⁶⁰, *g* = 3.27 | withdrawn |
| 37 | Combined *p* < 10⁻²⁰⁰, *g* = 6.34 | withdrawn |

**New finding.** The README reports a *third* effect size, **Hedges'
*g* = 6.34 "combined"**, which does not appear in the manuscript. A
pooled effect size across two geometries inherits both underlying
defects (DV determined by the grouping variable; the 2D arm is n = 2)
and additionally pools the double-counted denominator. It is withdrawn
with the rest. Logged here rather than opened as a new investigative
thread, per the stop-loss.

### Applied

1. A dated correction banner immediately after the H1, stating the
   withdrawal, the corrected ≈1% figure, the neither-confirmed-nor-
   refuted outcome of the direct test, and links to
   `paper/v6_supplement/`, the correction note, and
   `tools/detector_audit.py`.
2. The Key Result box struck through and replaced with a
   claim-by-claim table of what each figure actually was.
3. An inline HTML comment at the abstract marking the withdrawal with
   its reason, leaving the published text otherwise intact.

The original text is retained unaltered beneath the banner. The record
is corrected, not rewritten.

---

## 2. Dashboard at `genesis-engine.lucyvpa.com` — **PROPOSED, AWAITING CONFIRMATION**

Serving the withdrawn 100% headline since May 2026. **No file was
modified and nothing was deployed.**

### Claims found

| location | claim |
|---|---|
| `web/index.html:242` | KPI "BINOMIAL p — 8.01 × 10⁻¹⁴⁶" |
| `web/index.html:244` | KPI "MEAN C − B DELAY — 243 ticks" |
| `web/index.html:245` | KPI "HEDGES' g — 9.41" |
| `web/index.html:252` | narrative: "…100 %; binomial test p = 8.01 × 10⁻¹⁴⁶… mean delay 243 ± 2316 ticks… Hedges' g = 9.41" |
| `web/index.html:353–355` | the same p and g repeated in prose |
| `web/results/summary.csv` | **a stale copy of the withdrawn data that the page reads** |

### The dashboard is not just a display problem

`tools/detector_audit.py` (check C3) flagged `web/results/summary.csv`
independently: the dashboard serves **its own copy** of the archived
results, not a live read. So a banner alone leaves the withdrawn numbers
being computed and rendered from stale data underneath it. Either the
copy carries a header note, or the page repoints at `results/`.

### Proposed changes

1. **Correction banner** (exact HTML in `/tmp/dashboard_banner.html`,
   reproduced in the commit message) inserted immediately after
   `<body>`: dated, states the withdrawal and the ≈1% corrected figure,
   links to the audit. Styled to be unmissable without breaking the
   existing dark theme.
2. **KPI values** replaced: `8.01 × 10⁻¹⁴⁶` → "WITHDRAWN";
   `243 ticks` → "= sampling interval"; `9.41` → "WITHDRAWN (n=2 in 2D)".
3. **Narrative paragraphs** (252, 353–355) struck through with a link to
   the audit.
4. **`web/results/summary.csv`** — decide between a header note and
   repointing at `results/`.

**Minimum acceptable** is item 1. Items 2–4 prevent a reader who scrolls
past the banner from reading withdrawn numbers as current.

### Awaiting

Confirmation before any edit or deploy. The service was not restarted,
redeployed or taken down.

---

## Evaluation criteria used

- "Public-facing claim" = rendered to a visitor or shown on the repo
  landing page, not merely present in a source file.
- README treated as reversible (version-controlled, `git revert` restores
  it); dashboard treated as irreversible (live service, explicit
  instruction to propose-and-wait).
- Inventory by grep for the specific withdrawn figures (100%, 1845,
  1165, 8.01, 2.49, 243, 9.41, 3.27, 6.34), not by reading for sense.
