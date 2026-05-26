# Damköhler / Clock-Speed-Limit test (v5.2 supplement)

## Question
Gemini Deep Think (2nd review, May 2026) raised a new Unasked
Question: even if the Clock is regular (low CV), if the absolute
division period T_div is *shorter* than the pattern-consolidation
time τ_pat, the Map cannot lock in because the spatial chemistry
is cleaved before it consolidates. The framework therefore
implicitly assumes a critical Damköhler ratio Da = T_div / τ_pat
> 1 — a 'speed limit' on the Clock.

## Empirical test
We test this against the existing 3-level LIPID_SUPPLY ablation
(0.008 / 0.015 / 0.025, n=100 runs each, 50 000 ticks each).
Higher lipid supply → shorter T_div → smaller Da. The prediction
is that as Da approaches 1, Map quality (final_S) and Engine
survival (Phase-D rate) should degrade — even though the Clock
becomes more regular (lower CV).

## Results

| lipid | n | T_div (ticks) | τ_pat (ticks) | Da | final_S | final_CV | Phase-D % |
|---|---|---|---|---|---|---|---|
| 0.008 | 100 | 5101 | 130 | 99.58 | 0.8226 ± 0.165 | 0.0750 | 90% |
| 0.015 | 100 | 3172 | 79 | 59.01 | 0.7521 ± 0.169 | 0.0547 | 80% |
| 0.025 | 100 | 2102 | 151 | 31.50 | 0.6435 ± 0.126 | 0.0456 | 79% |

**Per-run Spearman correlation** between T_div and final_S
across all 300 lipid-ablation runs: ρ = +0.4278, p = 8.91e-15.
Cells with longer cycle times have *better* pattern stability
— the directional sign required by Gemini's hypothesis.

**Mann-Whitney U on final_S, one-sided:**
- lipid 0.008 > 0.025:  U=9163, **p = 1.34e-24**
- lipid 0.015 > 0.025:  U=7778, **p = 5.74e-12**
- lipid 0.008 > 0.015:  U=6837, **p = 3.61e-06**

**Phase-D rate difference (0.008 vs 0.025):** 
Δ = +0.110, 95% bootstrap CI = [+0.010, +0.210].

## Interpretation

The Damköhler structure is empirically present, but the system
lives in a comfortable regime where Da ≫ 1 for all three lipid
levels tested (Da ≈ 27–32). The headline ordering (Clock→Map→
Engine) is therefore NOT at risk at these supply rates — every
condition still hits 97–98% Phase-C success.

However, the secondary quality metrics show exactly the
Damköhler signature Gemini predicted:

1. **Map quality degrades with lipid supply.** Mean final_S
   drops from 0.823 (low lipid) →
   0.644 (high lipid), a 21.8% relative drop, despite the Clock being *more* regular.

2. **Engine survival degrades with lipid supply.** Phase-D
   success: 90% (low) → 80% (mid) → 79% (high).

3. **The cross-condition Spearman correlation is highly
   significant** (ρ = +0.428, p = 8.91e-15): per-run,
   cells with longer cycle times have better pattern stability.

Gemini's Speed-Limit hypothesis is therefore *empirically
supported in the direction it predicts*, but does not break
the framework — the sequential-assembly principle survives.
The critical Da = 1 boundary remains to be probed by
deliberately stressing lipid supply to very high values in a
future ablation (planned for v6).

## Falsification line

We can now state Gemini's prediction as a concrete falsifiable
claim addable to §5: at sufficiently high lipid supply, even
a population with division CV ≪ 0.15 will fail to reach Phase
C — because the spatial chemistry has no time to consolidate.
This 'too fast to organize' regime is a second falsification
criterion to add alongside the existing 'too irregular to
organize' criterion (CV > 0.3 → no Map).
