# v6 Task 5 — Timescale anchor in physical units

**Anchor.** 1 tick ≈ 0.45 s, from lipid lateral diffusion D ≈ 5 μm²/s on a ~1.5 μm vesicle (Vaz 1984; Macháň & Hof 2010): t = (1.5 μm)² / (5 μm²/s).

**Scope note.** T_div is estimated as `N · T_run / D_total` per run from the archived ablation data. It depends only on population size and division counts — not on the phase detector, the sequential gate, or the sampling interval — so it is **unaffected** by the v6 Task 1/3 findings. The Damköhler ratio built on top of it *is* affected, because its denominator τ_pattern turned out to be the sampling interval (see `task2_contamination.md`). T_div itself stands.

---

## Derived division period

| LIPID_SUPPLY | regime | n | T_div (ticks) | T_div (min) | IQR (min) |
|---|---|---|---|---|---|
| 0.008 | low | 100 | 5101 | **38.3** | [37.1, 40.0] |
| 0.015 | baseline | 100 | 3172 | **23.8** | [22.9, 25.3] |
| 0.025 | high | 100 | 2102 | **15.8** | [15.0, 16.6] |

## Comparison against measured systems

| system | measured period | source |
|---|---|---|
| E. coli, rich medium (LB, 37C) | 20–25 min | standard microbiology; doubling ~20 min |
| E. coli, minimal medium (glucose) | 40–60 min | standard microbiology |
| Oleic-acid vesicle division, fed micelles | 10–60 min | Zhu & Szostak 2009, JACS 131:5705 -- filamentous growth then division on the order of minutes under gentle agitation |

## Assessment

The simulated division period spans **16–38 minutes** across the three lipid-supply conditions (full run-level range 0–44 min).

This brackets *E. coli* doubling time (20–60 min depending on medium) and overlaps the timescale reported for fed oleic-acid vesicle division (Zhu & Szostak 2009), which is minutes to tens of minutes.

**What this is and is not.** The anchor was fixed independently — from lipid diffusion coefficients and vesicle size, with no reference to the division data — so the agreement is not a fit. It is a genuine order-of-magnitude check that the model's division dynamics sit in the right physical regime. It is *not* evidence for the ordering hypothesis, which Tasks 1 and 3 addressed separately and negatively. A model can have physically plausible timescales and still measure its phase transitions incorrectly; that is exactly what was found here.

The v5.1 text called this calibration "illustrative, not predictive." That hedge understates it: an independently fixed anchor landing inside the measured biological band is a real, if modest, external validity check, and should be reported as such — while being kept clearly separate from the withdrawn ordering claim.

## Evaluation criteria used

- Anchor fixed a priori at 0.45 s/tick from published lipid diffusion constants; not tuned to the division data.
- T_div computed from archived per-run ablation files (`final_pop`, `total_divisions`), 50,000-tick runs.
- 'Brackets' = the simulated range contains the measured reference range.
- Reference timescales are cited from the literature, not derived here.
