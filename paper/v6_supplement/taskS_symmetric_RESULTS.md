# v6 Task S — symmetric-metrics redesign (archived re-run)

Regenerated from `results_v6/taskS_symmetric.csv` by
`analysis_v6_taskS.py`. The original execution of this task was done
inline and its outputs were never written to disk; the numbers below
supersede any earlier prose figures.

**Design.** Replace CV — undefined until a cell completes four
divisions — with `clock_r`, the autocorrelation of a cell's own radius
trajectory, which needs no divisions. If the Clock/Map definedness
asymmetry were purely an artifact of the CV estimator, `clock_r`
should become defined much earlier than CV.

**Runs.** 40 seeds x 2 parameterisations, 20000 ticks each, 1D engine.

## Definedness (median first tick defined; -1 runs excluded)

| parameterisation | buffer | Map: S | Clock old: CV | Clock new: clock_r |
|---|---|---|---|---|
| `long` | 6000 ticks | 150 (n=38) | 4450 (n=40) | 6000 (n=40) |
| `short` | 400 ticks | 150 (n=38) | 4450 (n=40) | 400 (n=40) |

## Validity check: rho(clock_r, CV) at steady state

A genuine regularity metric must correlate **negatively** with CV
(more regular -> higher autocorrelation, lower CV).

| parameterisation | buffer | median division period | rho | p | n | verdict |
|---|---|---|---|---|---|---|
| `long` | 6000 ticks | 2625 ticks | -0.0822 | 0.6142 | 40 | INVALID |
| `short` | 400 ticks | 2625 ticks | -0.1897 | 0.2411 | 40 | INVALID |

## Reading

The short buffer spans 400 ticks against a division period
of ~2625 ticks: it cannot contain even one period, and the
validity check confirms it measures nothing about regularity
(rho = -0.1897, p = 0.241). It is reported here only
to document that the first parameterisation was invalid.

The long buffer spans 6000 ticks, ~2.3
division periods, and is the one that can work.

**The result.** `clock_r` was built specifically to have no
definedness floor. It becomes defined at a median tick 6000, later than the CV metric
it replaces (4450), and far later than the spatial metric
S (150).

**Why this is not fixable by a better estimator.** `clock_r` is
defined only once a cell's radius buffer is full, i.e. once that
cell has lived 6000 ticks. Shortening the buffer is what
the `short` row does, and it destroys validity. The floor is
therefore bounded below by the requirement to observe several
division periods — a time-frequency constraint on measuring the
regularity of a slow periodic process, not an implementation
choice. Any Clock metric faces it; the spatial metric does not,
because its correlation length is set by a ~40-tick field
relaxation rather than by the division cycle.

**Selection caveat (stated explicitly).** Because the buffer is
per-cell and daughters are constructed fresh (`Cell.create`, empty
`radius_hist`, `age = 0`) while mothers retain theirs, `clock_r` at
any tick is an average over the subpopulation of cells old enough
to have filled a 6000-tick buffer. This is age-selected by
construction. It does not rescue the metric: a cell too young to
have a full buffer is precisely a cell whose period has not been
observed. The selection is a restatement of the constraint, not a
confound that hides it.

**Conclusion.** The Clock/Map definedness asymmetry that produced
defect 3 is only partly an implementation error. The specific
four-division CV floor is ours. A floor of order several division
periods is physical, and it means comparing first-crossing times
between these two metrics measures their timescale ratio rather
than the dynamics. The ordering question is malformed as posed.

---

Raw data: `results_v6/taskS_symmetric.csv`. 
Regenerate: `python3 analysis_v6_taskS.py`.
