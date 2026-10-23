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
**Incomplete draft — cs.PL endorsement pending.** Current dedicated draft: **8226643**, expiring **2026-10-28**. Historical draft 8174837 is no longer the ID to use for this paper because another local task also references it; that draft was preserved. No public arXiv ID exists. A fresh account visit on 2026-10-23 confirmed submission access, but the actual Start POST still returned the missing-endorsement error. The October 5 request to Raphaël Monat and the October 14 request to Aymeric Fromherz were verified in Sent. No related reply or bounce was found in the latest complete inbox/spam/trash enumeration. Source upload, server PDF verification and final submission remain outstanding; this paper has not entered moderation.

## Human action required

**Complete the previously requested official arXiv login in the Edge RoundGuard group**. A fresh account visit on 2026-10-24 now also redirected to login without autofilled credentials; the official endorser-eligibility lookup still required login. This adds no separate author step, so the existing login request is not repeated. No credentials were entered and no login or Start POST was submitted in this check. The last actual Start result, on October 23, required cs.PL endorsement. Existing agreement and license authorization remains in force.

Agent Mail sender verification was completed and confirmed on the fresh official profile page on 2026-10-18. The three authorized, individually tailored requests to Jonathan Protzenko, Eva Darulova and Pavel Panchekha were sent that day. Following a further direct request on October 20, requests were sent to Zachary Tatlock and Max Willsey at 21:04:42 and 21:05:19 Hong Kong time. All five new Sent records and complete 375585-byte PDF attachments were verified. Together with the two earlier requests, seven distinct researchers have been contacted. The latest two recipients' public contact details were checked on October 20; their official cs.PL qualification was last observed on October 18, and the refresh required login. No related reply or bounce was found in the latest complete inbox/spam/trash enumeration. The earliest further unattended batch is 2026-10-23 21:05:19 Hong Kong time, with at most two new eligible contacts. Private correspondence, request codes and duplicate-prevention records remain outside Git.

On 2026-10-23 the next unattended outreach window opened. Two candidate request drafts were prepared, and neither was sent. The official current-endorser lookup redirected to a separate login page without autofilled credentials, even though normal account access and the actual Start POST were authenticated. Current cs.PL eligibility must be observed before any new request; one candidate's public contact also needs a successful refresh. The seven existing requests were checked in Sent and were not repeated.

## Follow-up
A local heartbeat is ACTIVE and checks every six hours for relevant replies, actual endorsement and submission progress. It stays quiet while the state is unchanged and stops after public announcement and record updates. This follows the original request to continue through publication; it does not guarantee that a prospective endorser will agree.
