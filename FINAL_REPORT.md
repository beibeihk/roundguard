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

**Incomplete draft — endorsement reported, official verification pending.** A previously contacted researcher reported completing endorsement on October 27, 2026. All new outreach has stopped; the two candidate requests prepared on October 23 were never sent. All seven earlier requests have verified Sent records and complete PDF attachments. Private correspondence stays outside Git.

The recorded dedicated draft is **8226643**, with a **2026-10-28** expiry last confirmed on October 23. Historical draft 8174837 is also referenced by another local task and was preserved. The last actual Start POST on October 23 returned the missing-endorsement error; it predates the new report. No later Start result or official endorsement approval is claimed. Source upload, server PDF verification and final submission remain outstanding. The paper has not entered moderation and has no public arXiv ID.

## Human action required

The previously requested official arXiv login in the Edge RoundGuard group remains pending. A fresh account visit on October 26 redirected to login without autofilled credentials, and the official qualification query displayed "Login Required." Browser control was unavailable on October 27, so current authentication and official endorsement have not been checked. The existing agreement and license authorization remains in force.

## Follow-up
The existing local heartbeat remains ACTIVE to verify the endorsement report through actual arXiv Start and complete submission/publication. New contact outreach is stopped. It stays quiet without a meaningful change and ends after a real public paper page and release/record updates. The endorsement report is not proof of completed submission or announcement.
