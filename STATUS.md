# RoundGuard research status

Research date: 2026-10-03 (Asia/Hong_Kong). Version 0.2.0.

## Final question and scope
Compute exact attainable discrepancies between declared monetary rounding policies on finite amount grids. Final title: RoundGuard: Exact Attainable Discrepancies in Monetary Rounding Policies. The specialized theorem covers independent affine line items. General bounded expressions use exact SMT.

## Research decisions and novelty gate
The initial broad static-analysis proposal overlapped Catala date-insensitivity, CUTECat rational monetary encoding and established Chvatal/quasi-affine arithmetic. The final restricted contribution is a sufficient-state theorem for attained discrepancy extrema, feasible witnesses, an implementation and independently certified evaluation. Late review replaced a larger cyclic-residue recurrence with at most two parity states, eliminating a common-denominator state space. General rounding semantics, periodicity, parity optimization and decidability are not claimed new. The gate is a conditional pass for this modest report, not a claim of top-venue novelty. The matrix has 33 records; 28 sources are actually cited and audited in the manuscript.

## Completed research
Ordinary proofs cover structural reduction, parity-conditioned attained extrema, nonnegative sign-sensitive modes, conditional analyzer correctness and the elementary sharp aggregation envelope. The cyclic proof remains as an ablation. No proof-assistant mechanization is claimed. The implementation includes exact JSON parsing, Fraction/Z3 semantics, six modes, placement enumeration, attaining witnesses and a CLI. All 107 tests pass.

The 66 exhaustive-oracle programs contain 50 sensitive and 16 safe cases; both exact methods match all labels and maxima. The 24 scaling cases have 288 measured runs and independent Decimal envelope/replay certificates. Original-machine exact completions are parity 72/72, cyclic 72/72, reduced SMT 36/72 and full SMT 22/72. Six denominator-stress cases have 72 runs and independent integer-rounding certificates; parity, reduced SMT and full SMT each complete 18/18, while cyclic rejects 18/18 at its declared cap. Timing and timeout outcomes can vary across reruns. The 64-line maximum is 27 cents on narrow windows and 30 cents with full local coverage, against a universal 32-cent envelope.

Three independent adversarial reviewers and two substantive revisions checked theory, provenance and evaluation. Fixed an actual Decimal precision defect and protected explicit policies from generated-name overwrite. The 14-page paper and freshly extracted source archive compile with embedded fonts, resolved references and no overfull boxes. Final visual and clean-clone records are saved separately.

## Public release and remaining limitations
Public repository: https://github.com/beibeihk/roundguard . The full remote-clone README command passed at commit 2a4acf343920ffd1bac931ccc976f0a2e97b6a09, with 107 tests and identical 66/24/6 exact records. Evidence is in artifact/clean_clone_report.json. The final full-grid SMT scaling completion count was 21/72 in the clone versus 22/72 in the original run; this timing variability is preserved. Limits include independent lines, common quantum/mode in the prototype, at most 400 feasible local representatives per line, finite boxes, explicit policies, one-machine microbenchmarks and a shared parsed AST. Enumeration is pseudo-polynomial; fixed-dimensional ILP offers an unimplemented alternative, so no inherent complexity lower bound is claimed. Public-rule cases are partial or counterfactual fragments, not production defects. Docker is supplied but untested.

## Actual arXiv state

**NOT SUBMITTED — endorsement reported, official verification pending.** On October 27, 2026, one of the seven contacted researchers reported completing endorsement. All new contact outreach has stopped. The two candidate requests prepared on October 23 were never sent and remain on hold. The report has not yet been verified in the live arXiv Start workflow.

The recorded dedicated draft is 8226643, with a 2026-10-28 expiry last confirmed on October 23. The last actual Start POST, also on October 23, returned HTTP 200 with "You are not endorsed for this archive." This predates the endorsement report. No source has been uploaded and the paper has not entered moderation; there is no public arXiv ID. Historical draft 8174837 is also referenced by another local task and must not be used or changed.

A fresh account visit on October 26 redirected to login without autofilled credentials, and the official qualification query displayed "Login Required." The local browser-control endpoint was unavailable on October 27, so no new authentication or Start result is claimed. The previously requested author login remains pending. The existing Submission Agreement and non-exclusive license authorization remains valid.

All seven earlier requests have verified Sent records and complete 375585-byte PDF attachments. Full folder enumeration on October 27 inspected 49 inbox messages and empty spam/trash folders; the relevant reply was recorded once and no related bounce was found. Private correspondence and browser evidence stay outside Git. Detailed observation dates and outreach history are recorded in arxiv/SUBMISSION_STATUS.md.

The next step is actual Start verification, followed by source upload, server compilation and PDF review, checked metadata and authorized final submission. The existing heartbeat continues through actual public announcement and release updates; it will not send additional endorsement requests after the affirmative report. No research or experiments were rerun.
