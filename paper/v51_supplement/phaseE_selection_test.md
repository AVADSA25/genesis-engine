# Phase-E selection hypothesis test (v5.3 supplement)

## Question

Gemini Deep Think (3rd review, May 2026) raised the deepest Unasked
Question of the series:

> If the Map physically destabilizes the Clock (already confirmed in
> 2D: Δcv = +0.057), the Engine must filter for Maps that do not
> suicide the Clock. Otherwise the protocell commits evolutionary
> suicide. This implies an unstated **Phase E: "The Map Controls
> the Clock."**

The argument: real biology (MinCDE positioning, septation rings) shows
that successful cells have spatial chemistries that *assist* division.
Therefore the Engine must select for Map-Clock harmony.

## Direct empirical test

For each 2D run that reached Phase C, compute the per-run Δcv
(same windows as v5.1c clean back-reaction test) and split runs by
whether they also reached Phase D (Engine activation):

| Group | n | mean Δcv | median Δcv | sd |
|---|---|---|---|---|
| **G_D**: reached Phase D | **96** | **+0.1009** | +0.1174 | 0.088 |
| **G_C**: stalled at Phase C | **84** | **−0.0244** | −0.0267 | 0.032 |

**If Phase-E selection were operating, G_D should have LESS
back-reaction than G_C (Engine filtering for Map-Clock harmony).**

## Result — Phase-E hypothesis EMPIRICALLY REFUTED in this direction

- Difference in means (G_D − G_C) = **+0.1253**, NOT negative
- Bootstrap 95% CI: **[+0.1064, +0.1436]** — excludes zero by a wide
  margin, but in the OPPOSITE direction from Phase-E selection
- Mann–Whitney U (two-sided): the difference is overwhelmingly
  significant; one-sided in the G_D < G_C direction returns p = 1

Engine-reaching runs have *more* Map→Clock back-reaction than stalled
runs, not less.

## Interpretation — a more interesting story than confirmation

The result is initially surprising but mechanistically straightforward:

1. The **Phase-D criterion** is based on pattern stability *S*
   reaching a threshold. Reaching Phase D requires a *strong* Map.
2. A **strong Map** in 2D produces a **larger back-reaction** on the
   Clock (consistent with the v5.1c finding that 2D back-reaction is
   geometry-mediated).
3. Therefore back-reaction is **a consequence of successful pattern
   formation**, not a side effect that selection has acted against.
4. The basic thermodynamic Engine in our model **does not filter
   against** the back-reaction. Map-Clock harmony is not an
   auto-emergent property of coupled dissipative systems.

## Why this enriches the framework rather than weakens it

Gemini's MinCDE example is precisely the point: MinCDE is a *highly
evolved* protein-level selection mechanism. It is not a primordial
property of vesicle physics. The empirical absence of Phase-E
selection in our model is therefore **consistent with the biology
Gemini cited**, not in conflict with it:

| Stage | What this captures |
|---|---|
| **Primordial (pre-selection)** | Strong Map ⇒ strong back-reaction. No filter. | ← our model |
| **Evolved (selection layer added)** | MinCDE-style proteins emerge that select Maps assisting division | ← future biology |

The Phase-E selection layer is therefore an **evolved adaptation,
not a physical constraint** — and the gap between our model and real
biology is precisely the gap natural selection had to fill.

## Concrete v6 prediction following from this

A v6 simulation that adds an explicit selection layer (e.g., a
fitness penalty proportional to Δcv after Map latching) should
predict the dissipative cost of evolving the Phase-E mechanism: how
strong a selection pressure is required, and over how many
generations, to convert the primordial regime (G_D mean Δcv ≈ +0.10)
into a MinCDE-style regime (G_D mean Δcv ≈ 0).

## Caveats

- Sample sizes (n=96 vs n=84) are imbalanced but the Mann–Whitney
  test handles unbalanced groups robustly.
- The 2D simulations run for only 10 000 ticks, so "Phase D reached"
  vs "stalled at Phase C" is a coarse binary. A longer-run v6 with
  fine-grained Engine activity might reveal sub-classes within G_D.
- The 1D data was not analyzed here because 1D shows essentially
  zero back-reaction (all 480 runs Δcv < 0), making the
  Phase-E split-by-outcome test underpowered.
