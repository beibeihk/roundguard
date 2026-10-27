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

**SUBMITTED — ON HOLD**, confirmed on October 27, 2026. After actual cs.PL endorsement authorization, source upload, successful server compilation, complete server-PDF review and metadata verification, the final Submit action returned "Article submitted." The expected account lists internal submission 8226643 with the exact RoundGuard title and status "on hold." No public arXiv ID or public paper page has been observed; submission success is not an announcement.

The server used main.tex, pdflatex and TeX Live 2025. All 14 server-generated PDF pages were visually inspected, and normalized text matches the local final manuscript on every page. The final preview confirmed title, Kun Huang authorship, abstract, comments, cs.PL and the accepted non-exclusive license. No cross-list, DOI or journal reference was added.

All new endorsement outreach is stopped. Seven earlier requests have verified Sent records and complete PDF attachments; the two candidate requests prepared on October 23 were never sent. No further author action is required by the currently observed page. The active heartbeat now checks the submitted record and relevant correspondence until a real public paper page appears. It does not create another submission or repeat the final Submit action.

The historical draft 8174837 belongs to shared history with another local task and remains untouched. Private correspondence, request codes, browser evidence and the authenticated server PDF remain outside Git. See arxiv/SUBMISSION_STATUS.md for the submission audit. No research or experiment was rerun.
