# v6 Task I — Machine-wide search for the sibling-paper source

Task B established the Vesicle Division and Engine/Negentropy code is
not in the git repository (all branches, full history). This searches
the machine, in case it exists on disk having never been version
controlled.

## Method

```
find ~ -name "*.py"  | xargs grep -l -i "hedges\|negentrop\|vesicle"
find ~ -name "*.ipynb" | xargs grep -l -i ...
find ~ -maxdepth 4 -type d -iname "*vesicle*" -o -iname "*negentrop*" ...
mdfind -onlyin ~ "negentropy" / "vesicle division" / "hedges_g"
```

Spotlight (`mdfind`) used alongside `find` because it is content-indexed
and reaches files a name-based search misses.

## What was found

**Papers and outputs — yes.**

| artifact | path |
|---|---|
| Vesicle Division paper (PDF) | `~/Downloads/Vesicle Division Simulation_….pdf` |
| Trinity/framework paper (PDF) | `~/Desktop/Mix papper/The Physical Origins of Biological Agency….pdf` |
| SSRN copies | `~/Downloads/ssrn-6135006*.pdf`, `ssrn-6593781*.pdf` |
| **Vesicle results data** | `~/Desktop/VVV/Fondation/PS/Vesicle_Division_Results.csv` |
| spreadsheets mentioning `hedges_g` | `~/Downloads/supp-1.xlsx`, `Paper3_master_API_20250810_133800.xlsx` |

**Source code — no.**

- No `.py` file anywhere on the machine outside `genesis-engine`
  mentions `hedges`, `negentrop` or `vesicle`.
- No `.ipynb` notebooks matching.
- No directory named for the Vesicle, Engine, Negentropy, Trinity or
  Protocell work containing source.
- `~/Desktop/VVV/Fondation/PS/` holds the Vesicle paper's manuscript,
  figures and results CSV, but **no code**: `find … -name "*.py"`
  returns nothing under `~/Desktop/VVV`.
- The only `hedges_g` implementation on the machine is
  `genesis-engine/analyze_results.py`.

## The Vesicle results file does not close the question

`Vesicle_Division_Results.csv` has columns:

```
Ccrit, k, m, Num Divisions, Mean S/V, Std S/V
```

It records surface-to-volume statistics per parameter triple. It
contains **no division-interval series and no CV column**, so the
published CV = 0.06 cannot be recomputed or traced from it, and whether
CV was used there as a detector or only as a descriptive statistic
cannot be determined. The file is an output summary, not the
measurement.

## Conclusion

**The sibling-paper source is not on this machine.** Both papers exist
as PDFs and one has a results CSV, but neither has recoverable code.

Therefore:

- **Engine paper, Hedges' *g* = 4.07 — UNVERIFIABLE from available
  source.** The concern stands and cannot be resolved: the Genesis paper
  explains its own *g* = 9.41 versus 4.07 as "reflecting the tightened
  coupling," which concedes the effect size tracks the coupling
  constants. Whether *g* = 4.07 shares the circularity and the
  group-size problem cannot be checked without the code.
- **Vesicle paper, CV = 0.06 — UNVERIFIABLE, risk remains LOW.** The
  only visible use in the Genesis paper is benign (a final-tick
  descriptive statistic over 5–12 intervals per cell). Nothing found
  raises that assessment, and nothing found closes it.

This closes the item as specified: the correction states that the Engine
paper's *g* = 4.07 could not be verified from available source.

## What would close it properly

The scripts that produced each paper's published numbers. Two greps
each: whether CV is used as a detector or transition marker, and what
the Hedges' *g* dependent variable and group sizes are. If those scripts
no longer exist, the two figures are permanently unverifiable and should
be described that way in any future citation of them.

## Evaluation criteria used

- "Present" = a source file on this machine that computes the published
  quantity, not a PDF or an output artifact.
- Both name-based (`find`) and content-indexed (`mdfind`) search, since
  either alone has known blind spots.
- `genesis-engine` excluded from the source search, having been settled
  in Task B.
