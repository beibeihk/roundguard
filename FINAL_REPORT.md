# Final delivery

Paper: **RoundGuard: Exact Attainable Discrepancies in Monetary Rounding Policies** — Kun Huang. The 13-page English manuscript is a restricted exact-analysis report; general periodicity and min/max-plus DP are attributed to prior work.

Main contributions:
- Feasible structural representatives for common-drift monetary rounding policies.
- Exact attained-extrema residue DP for independent affine lines, with witness reconstruction and explicit parity/sign/denominator premises.
- Runnable six-mode JSON analyzer with bounded SMT fallback and honest partial/UNKNOWN diagnostics.
- Public synthetic/canonical/rule-derived benchmarks, independent oracles, actual baselines/ablations and reviewed proofs.

Files: [paper PDF](paper/main.pdf), [LaTeX](paper/main.tex), [source archive](arxiv/arxiv_submission.tar.gz), [submission preview](arxiv/submission_preview.pdf), [literature audit](literature/reference_audit.csv), [reviews/revision](notes/internal_review.md).

Code: [beibeihk/roundguard](https://github.com/beibeihk/roundguard). The actual publication and clean-clone evidence are recorded in artifact/clean_clone_report.json after verification.

Reproduce on Windows from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/reproduce_all.ps1
```

Tests/evidence: 88 tests passed. Both exact methods matched all 66 exhaustive-oracle programs; all 24 scaling maxima have independent envelope/replay certificates.216 timing runs were executed. Ordinary proofs underwent three independent adversarial reviews and one substantive major revision. Paper and extracted source archive clean-build with embedded fonts and resolved references. Docker is supplied but untested.

arXiv: **NOT SUBMITTED — login required**. No submission or arXiv ID assigned; no moderation or public-announcement claim. Metadata, source and preview are ready, and the login page is preserved. Intended category cs.PL and prior perpetual, non-exclusive license.

Human action required: **Sign in to arXiv in the preserved browser.** After login the authorized submission workflow can continue; any subsequently required endorsement or personal declaration will be handled as an actual separate gate.

Automated approval review rejected launching Chrome, reporting it was blocked by policy. The browser connector also could not reach its session; the in-app login handoff is retained.
