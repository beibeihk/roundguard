# Final independent novelty gate

search_date: 2026-10-03  
reviewer_role: independent literature, claim and logic auditor  
decision: PASS FOR A RESTRICTED REPRODUCIBLE RESEARCH REPORT UNDER THE STATED PREMISES  
strong_originality_certified: NO

## Q1: Is there a real, unaddressed research problem?

**There is a concrete restricted problem worth investigating; the broad problem is already addressed by existing mathematics and tools.** Given fixed rounding policies, finite rational affine amount grids and independently varying line items, compute attainable signed discrepancy extrema and exhibit valid inputs attaining them. Universal rounding envelopes can be strictly unattainable on those grids. General integer/SMT reasoning expresses this problem already; a specialized residue-state implementation can reduce the cost of solving this particular family.

The search did not find the same bounded-grid, fixed-policy invoice formulation with this exact local-residue/extrema interface. This is a scoped search result, not a proof that no such result exists. The proposed recurrence is ordinary min/max-plus dynamic programming. Periodic affine drift, rational ceiling trees, exact legal monetary encoding, counterexample generation and proof certificates are existing foundations.

The final basis for proceeding is therefore **a specialized formulation, explicit attainability proof and an auditable implementation/evaluation**, with modest originality language. A first-tool claim, a new general periodicity theory, a polynomial-time claim in binary coefficient size, or a strong theoretical-novelty claim fails this gate.

## Closest overlap and the actual distinction

| Source | Established overlap | Remaining narrow distinction |
|---|---|---|
| Williams 2011, author working paper 2010, pp. 21–23 | Nested Chvátal rounding trees, affine average gradient and explicit shift periodicity | Mixed-mode feasible box representatives and the specialized implementation are additional engineering/formulation work |
| Basu et al. 2019, Definition 2.2 and Section 3 | Rational affine ceiling trees, exact mixed-integer representability and elimination | The particular independent-line attainable-extrema interface is not supplied in the inspected sections |
| isl and Woods 2015 | Exact integer/quasi-affine reasoning and broader Presburger structure | A reusable exact framework can already express the problem; specialization must earn its practical relevance |
| Date arithmetic 2024, Sections 3–4 | Relational comparison of alternative rounding semantics for law | Calendar ambiguity differs from monetary residue optimization |
| CUTECat 2025, Sections 2–4 | Rational monetary rounding, sign-aware nearest ties-away SMT encoding, generated tests and backend discrepancy findings | No inspected exact global invoice-extrema residue algorithm; CUTECat otherwise handles a richer language |
| Skala 2017, preliminary author draft, Sections 2–3 | Financial line-versus-total rounding and optimization on total forests | Chooses rounded node values for one fixed report; RoundGuard fixes policies and searches feasible input grids |
| Sadakane et al. 2001 | Compact rounding-state graphs and optimization over a given sequence | Selects rounding outputs for fixed data rather than worst input under fixed monetary rules |
| Fluctuat, Daisy, FPTaylor, Gappa, PRECiSA and Flocq | Numerical error bounds, fixed-point reasoning, explicit rounded operators and/or proof-assistant certificates | Attainable policy discrepancies differ from a conservative approximation-error bound against ideal real semantics |
| Modern min-plus convolution work | Established dynamic-programming primitive, including sophisticated structured accelerations | Arbitrary cyclic residue tables need not meet monotone or near-convex acceleration premises |

Verified direct links and per-source limitations are in [related_work_matrix.csv](related_work_matrix.csv) and [reference_audit.csv](reference_audit.csv); the detailed rejection argument is in [novelty_independent_review.md](novelty_independent_review.md). The closest theory sources are [Williams](https://personal.lse.ac.uk/williahp/pubs/WP%2010-118.pdf) and [Basu et al.](https://arxiv.org/html/1711.07028v1). The closest exact legal-encoding source is [CUTECat](https://rmonat.fr/data/pubs/2025/2025-05-03_esop_cutecat.pdf). The closest financial-total draft is [Skala](https://ansuz.sooke.bc.ca/professional/rounding.pdf).

## Conditional pass requirements

1. Restrict the global shift proposition explicitly to FLOOR, CEILING and HALF_EVEN. HALF_EVEN requires even shifts. Sign-sensitive modes require the proved nonnegative raw-line premises or the unreduced fallback. Input nonnegativity alone does not establish intermediate nonnegativity.
2. Keep independence and one active tick variable per supported affine line visible. Shared wages, total constraints and shared discounts do not inherit the independent convolution guarantee.
3. State the lcm/denominator dependence, arithmetic-operation convention and potential exponential binary encoding size. The current (O(nM^2)) path is pseudo-polynomial.
4. Preserve exact witnesses and independently checked numerical evidence. Numerical enumeration validates finite cases; it does not mechanize the mathematical proof or establish parser correctness.
5. Attribute all foundations and include Skala's preliminary-draft status and different objective. No claim may rest on the excluded wrong Rosa fetch.
6. Distinguish completed exact maxima, sensitive-but-incomplete results and UNKNOWN. Scale-test repetitions are not additional independent workloads.
7. Keep public-rule-derived fragments explicitly partial and partly counterfactual. They are evidence for a declared arithmetic contract, not legal compliance or a validated production calculator.
8. Correct the scaling-certificate prose: local nearest-even periods 4, 8, 10 and 20 are all at most 20, but do not all divide 20. The actual tables cover these periods; an independent integer-arithmetic replay confirms all 24 certificates.

The current manuscript's main drift and independent-line DP arguments satisfy the mathematical restrictions when read with the stated covariance premises. The revised grammar explicitly restricts the certified core to the three globally covariant modes. Skala's distinct objective is now attributed. The completed empirical prose distinguishes exact completion from sensitivity and UNKNOWN and agrees with the saved 66 small oracle cases. A separate audit reconstructs envelopes and replays witnesses for all 24 scaling cases without importing RoundGuard; all witnesses attain the independently derived upper bounds. This specific verification is not a solver rerun or a general implementation proof. The local-period prose is now correct. No outstanding mathematical or reference blocker was found at this review point. The gate permits completion of a truthful report, not an assessment that a selective venue will accept it.

## Strongest rejection argument

After clearing denominators, keep the total remainder and the least/greatest accumulated error. This is a natural finite-state compression followed by a standard semiring DP. The proofs are short, broad exact solvers already express the problem, and the present realistic cases are deliberately small fragments. A skeptical reviewer can therefore judge the contribution as an incremental application with limited practical validation. Stronger evidence would be an independently sourced workload where attainability matters and the specialization repeatedly provides a useful result that generic exact reasoning cannot obtain at comparable cost. A larger synthetic domain alone does not resolve this objection.

## Search and access audit

The audit used targeted web searches, exact DOI lookups through Crossref, publisher records, arXiv abstracts/full text, author/institution-hosted PDFs, current research-group publication pages, official library documentation and official government policy pages. Search families included computational law and monetary rounding; date rounding and concolic execution; affine Chvátal/quasi-affine/Presburger structure; exact/finite-precision error analysis; financial sequence/total rounding; fixed-point verification; and min/max-plus dynamic programming. The 2026 check included Monat/Huttner, probabilistic floating-point analysis and deterministic monotone min-plus work.

No direct Google Scholar session, Scopus or Web of Science search is claimed. Search result snippets were leads; paper methods were checked against primary material. This is a targeted evidence audit rather than an exhaustive PRISMA systematic review of every paper before the cutoff.

The matrix has 29 entries: 28 research papers or identified preprints plus one explicitly segregated unpublished financial-rounding draft. Fifteen research-paper rows have targeted core-section readings. This does not mean all pages or all proofs of those papers were read. Rhodes/Williams is publisher extract only; Woods is abstract/definitions; the isl conference paper is abstract plus a separate official manual reading; QuickCheck is original DOI metadata plus the authors' original tool documentation, not a full-paper reading. Scallop was read to disambiguate its neurosymbolic, non-legal scope.

Access limitations are preserved: some ACM publisher requests failed, so exact DOI metadata and author PDFs were used; an initial Daisy PDF path returned 404 and was not treated as read; the initial Flocq path was repaired using an actual author-page link; the fixed-point PDF download had an SSL failure and its reading depth is limited to primary available text; Skala's current blog returned 403 while the author PDF was available. The alleged Rosa download at arXiv 1301.5341 is a superconducting-wire paper and is rejected in [rejected_fetches.csv](rejected_fetches.csv). No missing full text was represented as a successful read.

