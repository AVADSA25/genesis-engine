# Physical-time calibration (tick → seconds)

Using oleic-acid vesicle lipid-diffusion anchor (cell ≈ 1.5 μm, D_lipid 1–10 μm²/s).

| Regime | D (μm²/s) | 1 tick | Full 10 000-tick run | 2D Clock→Map gap (56 t) | 1D Clock→Map gap (243 t) |
|---|---|---|---|---|---|
| slow (D=1) | 1.0 | 2.25 s | 6.2 h | 2.1 min | 9.1 min |
| typical (D=5) | 5.0 | 450 ms | 1.2 h | 25.20 s | 1.8 min |
| fast (D=10) | 10.0 | 225 ms | 37.5 min | 12.60 s | 54.68 s |

**Interpretation for wet-lab translation:** the Clock→Map delay falls in the **seconds-to-minutes** regime under typical lipid kinetics — i.e. observable live, not on geologic timescales. The 1D gap of 243 ticks (~109 s at D=5) and the 2D gap of 56 ticks (~25 s at D=5) are both well within the time-resolution of standard fluorescence microscopy of Rh-DHPE-doped vesicles.