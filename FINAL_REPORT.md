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
The full command passed in a separately installed remote clone at commit `2a4acf343920ffd1bac931ccc976f0a2e97b6a09`: 107 tests, all 66 small exact records, all 24 scaling certificates and all six denominator certificates reproduced identically; the paper and extracted archive compiled. The clone was initially installed from the immediately preceding computation release and rerun after a metadata-only package-version correction. Evidence is in `artifact/clean_clone_report.json`. Full-grid SMT completed 21/72 scaling runs in the final clone versus 22/72 in the published original run; both counts are actual observations, and exact values agree wherever established. Docker is provided but untested.

## Tests and review
107 tests passed. Both exact methods matched every exhaustive label and maximum. All 30 larger-case maxima have independent upper bounds and feasible attaining replay certificates. Three independent internal reviewers checked the proofs, citations and experiments; two major revisions corrected validation defects and improved the sufficient-state theorem. Proofs are ordinary rigorous proofs, not proof-assistant mechanizations. The paper and extracted archive compile cleanly with embedded fonts and resolved references. Novelty is a restricted application-specific formulation and sufficient-state analysis; no broad priority claim is made.

## arXiv
**Incomplete draft — endorsement pending.** Submission ID: **8174837**; no public arXiv ID. Login was restored on 2026-10-05 and the previously authorized agreement accepted again. The official cs.PL request code was generated. arXiv confirmed Raphaël Monat's endorsement eligibility; one request with the full paper and code repository was sent through the authorized Agent Mail account at 12:15 (Asia/Hong_Kong), verified in the sent folder. No endorsement approval has been observed. Source upload, server PDF verification and final submission remain outstanding; the draft has not entered moderation.

## Human action required
NONE currently. Await the external endorser's decision. Private correspondence and request codes are kept outside Git.
