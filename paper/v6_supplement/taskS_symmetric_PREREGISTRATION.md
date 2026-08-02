# Task S — Symmetric metrics: can the ordering question be answered at all?

**Pre-registered before running.**

## The problem this addresses

Every failure to answer the ordering question traces to one design fault:
**Clock and Map are measured by instruments with different definedness
properties.**

- **Map** (`S`) is a temporal autocorrelation over RD snapshots. Defined
  after `STAB_DEPTH × STAB_WINDOW` = 5 × 40 = **200 ticks**, regardless
  of division.
- **Clock** (`CV` of division intervals) requires ≥3 intervals, i.e.
  **four completed divisions** — median tick ~4,250.

A ~4,000-tick asymmetry in when the two instruments switch on. Any
comparison of their first-crossing times measures that asymmetry.
This is Defect 3, and no amount of re-analysis fixes it because it is
in the measurement design.

## The redesign

Replace the Clock metric with one that has **no definedness floor**.

**`clock_r`** — normalised autocorrelation of the cell's own radius
trajectory. A regularly dividing cell traces a sawtooth (linear growth,
sharp drop at division); a regular sawtooth autocorrelates strongly at
its period, an irregular one weakly. Computed as the maximum normalised
autocorrelation over a lag window, from a rolling radius buffer.

Crucially it is defined **as soon as the buffer fills**, on the same
timescale as `S`, and requires **no divisions at all**.

## Pre-registered checks, in order

**S1 — definedness symmetry (the precondition).**
Median tick at which each metric first becomes defined must agree within
**20%**. If they do not, the redesign has not achieved symmetry and
nothing downstream is interpretable.

**S2 — positive control on the NEW instrument.**
The old measurement was validated in Task Q by planting an ordering and
recovering it. The new one must pass the same bar before its nulls mean
anything: with `PLANT_MAP_DELAY = 10000`, Clock-first must exceed **80%**.

**S3 — the ordering result.**
Only if S1 and S2 pass. Report Clock-first rate on natural dynamics
across a **grid of threshold pairs**, so the answer cannot be an
artifact of one arbitrary threshold choice.

## Decision rule, fixed now

| outcome | conclusion |
|---|---|
| S1 fails | Redesign failed; the asymmetry persists; the ordering question remains unanswerable in silico. Report and stop. |
| S1 passes, S2 fails | New instrument is blind. Its results carry no information. Report and stop. |
| S1 and S2 pass | **S3 is a real answer** — the first genuine in-silico measurement of the ordering in this project. Report the grid, whatever it shows. |

## Commitments

1. S3 is not computed or looked at until S1 and S2 are evaluated.
2. Thresholds (20%, 80%) fixed now.
3. If S3 shows Clock-first, that is a positive result for the original
   theory and will be reported as such — **with the same scrutiny
   applied to every negative result in this audit**, including
   stratification by division count (three Simpson's paradoxes so far)
   and a check that the reference point of each crossing is what it
   claims to be (four scope/reference errors so far).
4. A positive result does **not** resurrect the published paper. That
   result was produced by a gate that could not fail. A new measurement
   would be new evidence, reported as such, not a reinstatement.
