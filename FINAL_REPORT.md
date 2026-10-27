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

**Submitted — on hold**, confirmed on October 27, 2026. Internal submission number: **8226643**. The actual final Submit action returned **"Article submitted"**; the expected author's account lists the exact RoundGuard title with status **"on hold."** No public arXiv ID or public paper page has been observed. Submission is complete; public announcement remains pending.

Actual Start verified cs.PL authorization. The correct source archive was uploaded, and the server successfully compiled main.tex using pdflatex and TeX Live 2025. All 14 server-generated PDF pages were visually reviewed; normalized page text matches the local final manuscript on every page. Final metadata, category and license were verified. No cross-list, DOI or journal reference was added.

Seven earlier endorsement requests were verified in Sent. All new outreach is stopped; the two candidate drafts prepared on October 23 were never sent. Historical draft 8174837 was preserved and not used for this submission. Private correspondence and authenticated browser/PDF evidence remain excluded from Git.

## Human action required

None on the currently observed page. The author already accepted the same Submission Agreement and license and expressly requested direct publication. No additional declaration or consent was fabricated.

## Follow-up

The existing heartbeat remains ACTIVE to check this submitted record and relevant correspondence until actual public announcement. It must not create a replacement draft, repeat Submit or resume endorsement outreach while the record is on hold. Once a real public RoundGuard page appears, update README, citation metadata, reports and the release, then stop the heartbeat. No publication date or moderation outcome is assumed.
