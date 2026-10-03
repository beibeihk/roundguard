# RoundGuard

**Exact attainable discrepancies in monetary rounding policies.** RoundGuard checks explicitly declared rounding variants on finite integer input grids. It returns SAFE, SENSITIVE with a replayed input, or UNKNOWN. A completed maximum is attained on the supplied grid. A warning does not decide which financial policy is legally correct.

The specialized residue dynamic program handles independent affine line items with a shared quantum and mode. General bounded expressions use Z3, with structural residue reduction where its premises hold. All six decimal rounding conventions are supported; sign-sensitive modes require nonnegative raw lines for the DP. Large denominator moduli, shared line dependencies, and piecewise expressions use the fallback. This is a JSON rule analyzer, not an analyzer for arbitrary Python source.

## Install

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e '.[reproduce]'
```

On Linux, use `.venv/bin/python` instead.

## Quick start

```powershell
.venv/Scripts/roundguard.exe analyze benchmarks/canonical/tax_per_line.json
.venv/Scripts/roundguard.exe analyze benchmarks/canonical/placements.json --json
```

The first example reports a one-cent attained discrepancy. Inputs are integer ticks; a variable's exact `quantum` maps them to monetary units. Constants and quanta use integers or strings such as `"0.062"` or `"1/3"`. Floating-point literals and JSON floating-point quanta are rejected. See [rule format](docs/rule_format.md) for syntax and limits.

## Reproduce the paper

Install a TeX distribution providing `latexmk`, `pdflatex`, `bibtex`, Latin Modern fonts, and `pdffonts` (Poppler). The research run used Python 3.11.5, TeX Live 2022, and the package versions in [environment.json](results/environment.json).

From the repository root, on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/reproduce_all.ps1
```

This creates a virtual environment if needed, installs pinned research dependencies, runs tests and proof sanity checks, regenerates benchmarks, executes experiments, generates tables and figures, audits their consistency, compiles the paper, and clean-builds the extracted arXiv archive. On Linux: `python scripts/reproduce_all.py`. An optional Dockerfile supplies these dependencies (`docker build -t roundguard .` then `docker run --rm roundguard`). Docker is provided but has not been executed in the original Windows study.

Seeds determine program generation and testing configuration. Exact oracle labels and discrepancy values should reproduce; wall times and solver timeout outcomes can vary. Timings in the manuscript are generated from the saved execution records. The main experiment takes several minutes, depending on solver behavior.

## Benchmark and evidence

- 48 synthetic, 12 canonical, and six public-rule-derived programs, independently checked by exhaustive Decimal evaluation.
- 24 scaling cases, three repetitions per method. Their maxima have independent local-error upper bounds and Decimal replay of feasible attaining inputs.
- Full-grid SMT, reduced-grid SMT ablation, random testing, Hypothesis search, and simple independent intervals.
- Ordinary mathematical proofs and bounded executable checks, with explicit classifications in [proofs/theorems.md](proofs/theorems.md).
- [Literature matrix](literature/related_work_matrix.csv), [citation audit](literature/reference_audit.csv), and [review/revision record](notes/internal_review.md).

See [benchmark provenance](benchmarks/MANIFEST.md). The public-rule examples are independently authored fragments and counterfactual comparisons, not production bug reports or complete legal calculators. The small oracle shares the parsed AST, so it independently checks arithmetic after parsing rather than independently validating every parser translation.

## Paper and citation

[Paper PDF](paper/main.pdf) · [LaTeX source](paper/main.tex) · [arXiv source archive](arxiv/arxiv_submission.tar.gz)

Kun Huang. *RoundGuard: Exact Attainable Discrepancies in Monetary Rounding Policies*. Research manuscript, 2026. See [CITATION.cff](CITATION.cff). No arXiv identifier is claimed until one is assigned; [STATUS.md](STATUS.md) records the actual submission state.

## License

Source code, scripts, benchmarks, and original data are MIT licensed. The manuscript has a separate [paper copyright notice](PAPER_LICENSE.md); the intended arXiv license matches the author's prior perpetual, non-exclusive arXiv license. Downloaded third-party papers and browser/authentication materials are excluded from the repository.

