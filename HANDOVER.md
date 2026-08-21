# Genesis Engine — HANDOVER (3 Aug 2026; status verified 21 Aug 2026)

## 1. WHAT THIS SESSION WAS FOR

Correct a published paper (SSRN 6593781) whose central result was produced by
measurement artifacts, and publish the audit as a standalone methods paper.
Goal: get both documents factually correct and publicly posted.

---

## 2. WHAT SHIPPED

All committed and pushed to `github.com/AVADSA25/genesis-engine` (public),
HEAD = `2f325af`. Working tree clean except one untracked scratch file
(`paper/v6_supplement/SSRN_NEW_PAPER_ABSTRACT.txt` — superseded, safe to delete).

**The new paper — WORKING, not yet published**
- `paper/submission/detector_paper_farina_2026.tex` / `.pdf`
- 27pp, compiles clean with `tectonic`, 25 refs, 2 figures.
- Title: *The Detector Was the Result: Eight Measurement Artifacts, and a
  Question That Cannot Be Asked This Way*

**Corrected SSRN upload — BUILT, upload state unverified**
- `paper/submission/genesis_paper_v6_corrected.tex` / `.pdf` (32pp, 6.1 MB)
- 5pp correction front matter + v5.3 included byte-identical via `pdfpages`,
  all 27 original pages stamped "CENTRAL RESULT WITHDRAWN".
- Mickael was uploading this to SSRN 6593781 when the session ended.
  **I did not see it confirmed. Verify before assuming it is live.**

**Abstract text for SSRN 6593781**
- `paper/v6_supplement/SSRN_FULL_ABSTRACT.txt` — correction + original
  abstract already combined, 3,534 chars. This is the one to paste.
- Two older variants exist (`SSRN_ABSTRACT_PREPEND.txt`, `SSRN_PASTE_THIS.txt`).
  Ignore them; they caused confusion.

**Task S archive — WORKING, verified**
- `experiment_v6_taskS_symmetric.py` → `results_v6/taskS_symmetric.csv`
- Buffer sweep → `results_v6/taskS_buffer_sweep.csv` (4 arms × 40 seeds, 40k ticks)
- Out-of-sample confirm → `results_v6/taskS_buffer_confirm.csv` (seeds 40–79)
- `analysis_v6_taskS.py`, `analysis_v6_taskS_sweep.py` regenerate the results docs.

**detector_audit.py — WORKING, verified this session**
- `tools/detector_audit.py` → 31 findings, 16 critical (re-run and confirmed)
- `tools/test_detector_audit.py` → 5/5 pass (re-run and confirmed)

**Figures — WORKING**
- `make_figures.py` → `paper/submission/figures/fig1_positive_control.pdf`,
  `fig2_definedness.pdf`. Regenerate from the archived CSVs.

**Bibliography — WORKING, verified**
- `paper/submission/refs.bib` (25 entries), `verify_refs.py` → 25/25 verified
  against CrossRef by DOI.

---

## 3. WHAT IS HALF-DONE

**Nothing. Both papers are published.** Verified live on SSRN 21 Aug 2026.

**A. SSRN 6593781 correction — LIVE.** Last revised 3 Aug 2026, 32 pages
(= `genesis_paper_v6_corrected.pdf`), licence CC-BY 4.0. The public abstract
opens with `*** CORRECTION, 3 AUGUST 2026: THE CENTRAL RESULT OF THIS PAPER IS
WITHDRAWN. ***` and retains the original abstract beneath it. Cleared
moderation.

**B. New paper — LIVE.** https://papers.ssrn.com/abstract=7224298, posted
10 Aug 2026, 26 pages, CC-BY 4.0, declaration of interest and ethics statement
both displayed. Mickael finished steps 5–7 himself after the session ended.
(The handover previously said 27pp; the PDF is 26 — SSRN and the local file
agree, md5 `5b3366d7…`.)

---

## 4. DECISIONS MADE

- **Correct SSRN in place, do not withdraw.** The original's text and data are
  the evidence for the correction; removing it makes the defects unverifiable.
- **Original included byte-identical, not rewritten.** Same reason.
- **Stamp every page**, not just page 1 — loose pages circulate.
- **Keep the old abstract below the correction.** A correction that deletes the
  claim it corrects is a substitution, not a correction.
- **New paper is standalone, not a replacement.** Different document, own SSRN entry.
- **Paper affiliation → "Independent Researcher, Marbella, Spain"** (was AVA
  Digital L.L.C.) — keeps business context out of research. NOTE: his SSRN
  *account* still says AVA Digital, so PDF and SSRN metadata disagree. Unresolved.
- **License CC-BY** for both papers — the paper argues publishing the code is
  the only reason the defects were findable; a no-reuse license contradicts that.
  → **Appended to `~/.claude/DECISIONS.md`.**
- **Tool reports six of eight defects recovered**, not all eight — stated in
  the paper rather than fixed by adding checks (scope creep, unasked).
- **Preprint first, journal after.** Artificial Life remains the eventual target.

---

## 5. WHAT BROKE / WHAT I GOT WRONG

**The 22-error fact-check.** An adversarial pass over the revised draft checked
196 numeric claims and confirmed 22 errors. Several were introduced by the
revision that fixed the previous round. Do not assume the current draft is clean
— every pass so far has found new errors, including errors created by fixes.

**C3 could not fail.** `tools/detector_audit.py` computed
`si = sample_interval or int(med)` with `sample_interval` always None, so the
"sampling interval" was defined to be the median it was compared against. It
fired on any integral median and could never pass — the paper's Defect 1
reproduced inside the tool built to detect it. Fixed (GCD-inferred grid) and
negative controls added. **Lesson: every check needs an input on which it must
stay silent.**

**A disclosure note blinded the tool.** The `#` staleness header on
`web/results/summary.csv` made `csv.DictReader` read the comment as the header;
every check's `if not rows or KEY not in rows[0]: continue` guard fired and two
real findings vanished silently. Count moved 30→29 and read as improvement.
Fixed via `read_csv`/`want_cols`.

**I invented a mechanism.** Added a survivorship explanation for the
non-monotone S(CV) point, citing 27.3% extinction. That table excludes every
period where those extinctions occur; in-window extinction is 0/675. Withdrawn,
now §6.3 entry (7).

**Seven CrossRef searches returned the wrong record** — a book reprint for
Turing 1952, preprints for Nosek/Marshall, a Faculty Opinions stub for Munafò,
an unrelated 1954 paper for Gabor. All looked plausible in a result list.
**Never accept CrossRef's first search hit; resolve by DOI.**

**The ~3,170-tick "natural period" was an artifact** of a hardcoded 50,000-tick
divisor applied to 40,000-tick runs. The earlier "different configurations"
reconciliation was itself invented. Both figures are ~2,540.

**Dead ends / failures:**
- Browser `file_upload` returns an error but the file may still attach. It did.
  Screenshot before believing the error.
- `~/Downloads` and the session scratchpad are both rejected by `file_upload`.
- SSRN date fields strip typed slashes → "Invalid date". Use `form_input`.
- SSRN's rich-text abstract counts markup, not visible chars. Hard-wrapped text
  pasted from a file blows the 5,000 limit. Paste unwrapped, `Cmd+Shift+V`.
- SSRN auto-extracts the abstract from the PDF and pulls in the running header.
  Always replace it manually.
- `hq.ssrn.com/submissions/CreateNewSubmission.cfm` is a 404. Use
  `hq.ssrn.com/submission.cfm`.
- I told Mickael the upload was blocked when it wasn't. Verify before reporting
  a blocker.

---

## 6. OPEN THREADS

- **Title metadata bug on 7224298 (open).** SSRN stored the title with raw HTML
  in it — the page `<title>` reads literally
  `<div> The Detector was the Result: </div> <div> Eight Measurement Artifacts,
  and a Question that cannot be asked this Way </div>`. Two problems: the `div`
  tags, and the casing ("was", "cannot be asked this Way") against the paper's
  own `The Detector Was the Result: Eight Measurement Artifacts, and a Question
  That Cannot Be Asked This Way`. Cause: the title field was pasted as rich
  text. Fix = a metadata-only revision on the title field, paste unformatted.
- **7224298 shows "0 References".** SSRN did not extract the 25-entry
  bibliography (6593781 shows 46). Cosmetic — no reference linking or
  citation-graph presence. Probably not worth a revision on its own; fold it
  into the title fix if a revision happens.
- **No running jobs, no crons, no PRs, no deploys.** All experiments finished.
- `genesis-engine.lucyvpa.com` dashboard is live and untouched.

---

## 7. NEEDS MICKAEL

- Decide whether to file a metadata revision on 7224298 to fix the HTML-in-title
  bug (see §6). It is a public-record change, so it needs his go-ahead.
- Decide whether to align his SSRN *account* affiliation (AVA Digital L.L.C.)
  with the paper's (Independent Researcher, Marbella, Spain). Both currently
  show on the author page.
- Decide whether to submit to *Artificial Life* (MIT Press) and when.

---

## 8. FIRST THREE MOVES

1. **Read §5 before touching either paper.** The error rate across revisions
   never converged to zero. Both papers are now public; any change is a
   revision to the public record.
2. **Re-run the three verifiers before trusting any number.** Last run
   21 Aug 2026, all green:
   `python3 tools/detector_audit.py` → 31 findings / 16 critical
   `python3 tools/test_detector_audit.py` → 5 passed, 0 failed
   `cd paper/submission && python3 verify_refs.py` → 25/25 against CrossRef.
   (`verify_refs.py` lives in `paper/submission/`, not `tools/`.)
3. **If a revision is authorised**, it is metadata only — the title field on
   7224298, pasted with Cmd+Shift+V. Do not re-upload the PDF.

---

## KEY FACTS (so the next session does not re-derive them)

- Withdrawn: Clock precedes Map in 1,845/1,845, p = 8.01e-146. It was the gate.
- Corrected: ~1% of runs. Reverse also unestablished.
- Definedness: S at ~150 ticks, CV at ~4,450, valid clock_r at ~24,000 (160×).
- A valid regularity metric needs ~9 division periods of buffer
  (rho = -0.4565, p = 0.0031 on held-out seeds 40–79).
- Distinct runs 1,554 not 1,845: 97 baseline runs counted 4× = 291 redundant.
- Nine of 19 reported quantities were detector-dependent, a tenth indirectly.
- Both extinction survivors occur ONLY at imposed periods <=800, which the
  model treats as unphysical. Zero extinctions at T>=1600.
- Two companion papers (Vesicle CV=0.06, Engine g=4.07) are UNVERIFIABLE —
  no source survives on any machine.
