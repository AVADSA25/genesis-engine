# Wet-lab protocol — testing what the Genesis Engine simulation could not

**Version 1.0 · 31 July 2026 · Farina**
Companion to the v6 audit (`paper/v6_supplement/`).

---

## Read this first

The simulation that motivated these experiments **failed**. Its headline
result — that division regularity precedes spatial organization —
was produced by measurement artifacts and is withdrawn. A purpose-built
control experiment then found the model cannot adjudicate the ordering
question at all.

Nothing here should be attempted because a simulation predicted it.
Three of the four experiments below test things the simulation got
*wrong* or could not test. They are worth running because the questions
are open, the measurements are tractable with existing methods, and one
of them is counterintuitive enough to be interesting regardless of
outcome.

**Predictions from the original paper that are NO LONGER SUPPORTED and
should not be tested on its authority:** Clock-before-Map ordering; the
CV < 0.15 / CV > 0.3 patterning thresholds; the Clock→Map→Engine
synthetic-cell construction order.

---

## System

**Vesicles.** Oleic acid / oleate giant unilamellar vesicles (GUVs),
prepared by the standard gentle-hydration or electroformation route.
Oleic acid is chosen because growth-and-division under micelle feeding
is already established (Zhu & Szostak 2009, *JACS* 131:5705) and because
the simulation's timescale anchor was calibrated to fatty-acid membranes.

**Feeding.** Oleate micelle addition under a microfluidic chemostat or
programmable syringe pump, so feed rate is a controlled variable rather
than a bolus.

**Imaging.** Time-lapse epifluorescence or spinning-disk confocal,
frame interval ≤ 30 s (see Experiment D for why this bound matters).
Trap or immobilise so individual vesicles can be tracked across
divisions — lineage tracking is essential to three of the four
experiments.

**Labels.**
- Membrane-domain reporter: Rh-DHPE or NBD-PE, ≤ 0.5 mol% to avoid
  perturbing phase behaviour
- Optional aqueous marker for volume/division confirmation

**Domain-persistence metric.** The simulation's *S* is a temporal
autocorrelation of the membrane field with a spatial-complexity gate.
The experimental analogue: compute the autocorrelation of the
fluorescence intensity map around the vesicle circumference across
successive frames. **Do not** simply count visible domains — the
simulation's own §5.2 argument (one of the few parts that survived
audit) is that persistence, not classical Turing patterning, is the
meaningful quantity.

---

## Experiment A — Feed rate → division rate → domain persistence

**The one surviving substantive finding from the simulation.**

Higher lipid supply produced faster division *and* lower pattern
stability (mean *S* 0.823 → 0.644 across a 3× feed range). This is the
only physical result that survived the audit with no detector in its
measurement path.

**Design.** Three feed rates spanning ~3× (e.g. low / medium / high
oleate micelle flux), ≥ 20 tracked vesicles per condition.

**Measure.** (i) division interval per lineage; (ii) domain
autocorrelation over the steady-state period.

**Prediction.** Faster feed → shorter division interval → **lower**
domain persistence.

**Falsified if** domain persistence is flat across feed rate, or rises
with feed rate.

**Note the direction.** This is opposite to the intuition behind the
original theory. Higher throughput does not buy more organization.

---

## Experiment B — The over-feeding cliff

**Design.** Extend Experiment A upward: push feed rate progressively
past the highest rate in A, ≥ 20 vesicles per level.

**Prediction.** A threshold exists beyond which the population
**collapses** — vesicles lyse, fragment, or fail to sustain division —
rather than simply dividing faster.

In simulation, forcing division faster than growth could support was
lethal: 32.4% population extinction at the shortest imposed period,
8.4% at the next, zero at longer periods.

**Falsified if** division rate increases monotonically with feed rate
with no collapse regime up to the solubility limit of the feedstock.

**Why it is worth doing.** The naive expectation is "more food, more
growth." A hard ceiling with a collapse beyond it is a non-obvious,
practically relevant result for anyone trying to sustain artificial
cell populations.

---

## Experiment C — Synchrony fragility (**highest value**)

**The most counterintuitive prediction, and cheap to run.**

In simulation, *perfectly regular* division was **more** lethal than
irregular division under resource limitation: 27.3% population
extinction at CV = 0, versus 1.3–4.0% at CV ≥ 0.1.

Proposed mechanism: synchronised vesicles deplete shared feedstock
simultaneously and starve together; heterogeneity means some are
off-phase when the trough arrives and survive it.

**Design.** Two populations under identical, *limiting* feed:
- **Synchronised** — e.g. size-selected by filtration or sorted to a
  narrow radius distribution, so division events cluster in time
- **Desynchronised** — deliberately broad initial size distribution

Match total lipid mass and vesicle count. Run under feed sufficiently
limiting that competition is real.

**Measure.** Population survival over time; fraction of lineages lost.

**Prediction.** The **synchronised** population is more fragile.

**Falsified if** synchronised populations survive as well as or better
than desynchronised ones.

**Caveat, stated honestly.** This came from a simulation whose central
claim collapsed. It survived the audit because it involves no phase
detector and no CV estimator — it is a bare population-survival count —
but it has not been independently replicated in silico either. Treat it
as a hypothesis worth an afternoon, not a prediction with weight behind
it.

---

## Experiment D — Timescale check (do this first; it is nearly free)

**Design.** Simply measure division periods for fed oleic-acid vesicles
under the Experiment A medium condition.

**Prediction.** **15–40 minutes.**

This comes from an anchor fixed *a priori* — lipid lateral diffusion
D ≈ 5 µm²/s on a ~1.5 µm vesicle gives 0.45 s per simulation tick, with
no reference to any division data. It brackets *E. coli* doubling
(20–60 min) and overlaps published fatty-acid vesicle division times.

**Falsified if** periods are outside ~5–120 minutes.

**Why first.** It is a one-session sanity check on whether the model's
dynamical regime resembles the real system at all. If it fails, treat
A–C with correspondingly more scepticism.

---

## Experiment E — The open question the simulation could not answer

**This is the scientifically important one, and it is genuinely open.**

Does temporal regularity precede spatial organization in real
protocells?

The simulation cannot answer this. Its detector could not emit a
violation; its regularity metric (division-interval CV) is undefined
until a cell has completed four divisions, while its organization metric
is measurable almost immediately. The two quantities are measured by
instruments with different definedness properties, so any comparison
between them is confounded at the design level.

**A laboratory does not have this problem.** Both quantities can be
measured on the same lineage from t = 0:

**Design.** Track individual vesicle lineages from formation. For each:
- Record every division time → running interval regularity
- Record domain autocorrelation continuously

**Measure.** For each lineage, the time at which division regularity
first stabilises and the time at which domain persistence first
stabilises. Compare *within* each lineage.

**Critical design requirements**, learned from the simulation's failure:
1. **No gating.** Score both crossings independently. Do not condition
   one on the other — that is exactly the defect that produced the
   original false result.
2. **Report the distribution, not the mean.** The simulation's headline
   delay was carried by 3 runs out of 482.
3. **Frame interval must be well below the expected gap**, or the
   measured "delay" will be your frame interval. The original result's
   50-tick delay *was* its 50-tick sampling interval.
4. **Stratify by division count.** Nearly every per-cell quantity is
   entangled with how many times a cell has divided; pooling across it
   produced three separate sign-reversing Simpson's paradoxes in the
   simulation data.

**Any outcome is publishable.** Clock-first, Map-first, or simultaneous
within resolution — all three are informative, because nobody currently
knows.

---

## Suggested order and effort

| | experiment | effort | why |
|---|---|---|---|
| 1 | **D** timescale | ~1 session | free sanity check on the whole regime |
| 2 | **C** synchrony | ~1 week | counterintuitive, cheap, interesting either way |
| 3 | **A** feed → persistence | ~2–3 weeks | the surviving simulation result |
| 4 | **B** over-feeding cliff | extends A | practically useful |
| 5 | **E** ordering | ~1–2 months | the real question |

---

## What the simulation contributes, honestly

Not evidence. **Specification.** It produced a physically-plausible
timescale, four measurable quantities, explicit falsification criteria,
and — most usefully — a detailed list of the measurement traps that
destroyed its own result. Requirements 1–4 in Experiment E are the
distilled version of eight documented defects.

A protocol that says "here is how we fooled ourselves, do not do this"
is worth more than one that says "our model predicts X."

Full audit, data and analysis code: `paper/v6_supplement/` and the
public repository.
