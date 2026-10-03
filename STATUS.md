# RoundGuard research status

Started: 2026-10-03 (Asia/Hong_Kong).

## Current question
Final question: exact attainable discrepancy between prescribed monetary rounding policies on finite amount grids, with a specialized independent-affine-line algorithm. Title: RoundGuard: Exact Attainable Discrepancies in Monetary Rounding Policies.

## Completed
- Read the complete user request.
- Inspected prior project structure, metadata, compilation/package workflow and actual submission receipt.
- Verified author: Kun Huang; Economics and Management School, Wuhan University; public academic email.
- Prior arXiv license: perpetual non-exclusive. ORCID absent; do not infer.
- Created independent project. Prior paper prose will not be reused.

## Literature gate
CONDITIONAL PASS for a modest restricted report. The initial broad direction overlapped Catala date-insensitivity, CUTECat rational monetary encoding/counterexamples, and established Chvatal/quasi-affine periodicity. The final contribution is a feasible-extrema formulation, proof, implementation and evaluation using ordinary cyclic min/max-plus DP. General periodicity, monetary semantics, counterexamples and decidability are not claimed new. Stronger venue-level novelty is not established. Matrix:29works; sentence-level audit:26usedsources.

## Core contributions / experiments
Ordinary proofs: structural reduction, attained batch extrema, nonnegative extension, conditional analyzer correctness and a sharp elementary envelope. No proof-assistant mechanization. Implemented JSON parser, exact Fraction/Z3 semantics, six quantizers, finite placements, witnesses and CLI.88tests passed.66exhaustive programs (50sensitive,16safe) and24scalingcases with216actualtimedruns. All exact small maxima agree; all scaling optima have independent upper bounds and feasible attaining replay certificates. Final original-machine completions:DP72/72,reducedSMT35/72,fullSMT19/72. These counts are time-dependent.64lines attain27cents on narrow windows or30with full local coverage, versus32unrestricted.

Three independent adversarial reviews and a major revision are complete. Fixed an actual Decimal precision defect with3regressions; corrected overstrong value-set language and inaccurate oracle provenance. Full reproduction succeeded.13-page manuscript and independently extracted source archive compile; fonts embedded, references resolved, no overfull boxes. All pages visually checked through a contact sheet with full-size theorem/figure/bibliography inspection.

## Unresolved
Public repository and clean-clone verification are release steps recorded after execution in FINAL_REPORT.md and artifact/clean_clone_report.json. Scope limits: independent lines, common quantum/mode, capped DP modulus, finite boxes, explicit variants, one-machine microbenchmarks, shared parsed AST. Public-rule cases are partial/counterfactual fragments, not production defects. Docker is supplied but untested.

## Submission
NOT SUBMITTED. In-app arXiv browser reached the login page; no authenticated session was available. Chrome connector reuse failed, and automated Chrome launch was rejected by policy. No submission/arXiv ID assigned. Intended primary category:cs.PL; license:arXiv perpetual,non-exclusive matching the previous submission. Source archive and metadata are prepared in arxiv/.
