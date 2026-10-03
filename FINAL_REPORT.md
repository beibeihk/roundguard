# Final report

## Paper
**RoundGuard: Exact Attainable Discrepancies in Monetary Rounding Policies** — Kun Huang, Economics and Management School, Wuhan University. 14 pages, one figure and three tables.

## Main contribution
- Feasible structural representatives for common-drift exact rounding policies.
- At most two parity states suffice for attained independent-line discrepancy extrema; witnesses and explicit sign conditions are proved.
- Runnable Python/Z3 rule analyzer, with the cyclic-residue implementation retained as an ablation.
- Independent ground truth for 66 small programs, 24 scaling cases and six denominator-stress cases; 360 actual timing executions.

## Files
- Paper PDF: `paper/main.pdf`
- Source: `paper/main.tex`
- Submission archive: `arxiv/arxiv_submission.tar.gz`
- Submission metadata: `arxiv/metadata.json`

## Code
https://github.com/beibeihk/roundguard (public).

## Reproduce
From the repository root:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/reproduce_all.ps1
```
Remote clean-clone execution and exact record comparisons are recorded in `artifact/clean_clone_report.json`. Wall times and SMT completion outcomes may differ. Docker is provided but untested.

## Tests and review
107 tests passed. Both exact methods matched every exhaustive label and maximum. All 30 larger-case maxima have independent upper bounds and feasible attaining replay certificates. Three independent internal reviewers checked the proofs, citations and experiments; two major revisions corrected validation defects and improved the sufficient-state theorem. Proofs are ordinary rigorous proofs, not proof-assistant mechanizations. The paper and extracted archive compile cleanly with embedded fonts and resolved references. Novelty is a restricted application-specific formulation and sufficient-state analysis; no broad priority claim is made.

## arXiv
**Not submitted — login required.** No submission ID or public arXiv ID has been assigned. Proposed category: cs.PL; license: arXiv perpetual, non-exclusive, matching the previous project.

## Human action required
Log in on the preserved arXiv page. After login, the prepared upload and submission workflow can continue.

Automatic approval review rejected launching the existing Chrome executable, with the stated reason “blocked by policy”. The in-app login page is preserved.
