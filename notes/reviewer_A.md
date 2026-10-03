# Reviewer A: programming languages and formal-methods audit

Date: 2026-10-03. Scope: manuscript proof/semantic claims, implemented premises, section roles, logical tree, theorem classification, and the mathematical basis of evaluation certificates. Snapshot: `paper/main.tex`, `proofs/theorems.md`, final `src/roundguard/{model,semantics,analysis}.py`, `experiments/run.py`, and benchmark provenance. Bibliographic keys were finalized by a separate reviewer. `evaluation.tex` and `cases_table.tex` were absent at the first snapshot and have since been reviewed in the final re-audit below.

## Recommendation

Initial recommendation: focused major revision before publication. No counterexample to the structural reduction, residue-extrema theorem, nonnegative extension, or sharp nearest-even lemma was found. The implementation matches their stated mathematical premises after the earlier input-quantum and backpointer corrections. Required changes concerned explicit theorem scope, an overly strong value-set sentence, and the self-contained provenance of scaling ground truth. Final re-audit closes A1--A5; no required major correction remains within this review's scope. This is not proof-assistant verification or a judgment of broader literature completeness.

## Required revision checklist

- [x] **A1: state the certified mode domain in the grammar.** Section 3 calls the grammar the certified core, but its displayed production leaves m unrestricted and then documents all six interface modes. Equation (translation) defines p_m only for FLOOR, CEILING, and HALF_EVEN. Add the explicit core restriction m in that three-mode set, and identify the six-mode interface as an extension analyzed by the certified nonnegative DP or unreduced bounded SMT. This premise must be local to the theorem definitions, not only inferable from later exclusions.
- [x] **A2: distinguish extrema preservation from value-set preservation.** The first sentence of the conditional analyzer correctness proof says both specialized paths preserve the exact discrepancy value set. Structural box reduction does preserve that set. The DP intentionally keeps only attained minimum and maximum errors per residue and does not represent every attainable interior value. Replace the sentence with separate statements: box reduction preserves discrepancy value sets; the DP preserves exact attained extrema and the all-zero equivalence criterion. The proposition's conclusions then follow without a stronger unsupported claim.
- [x] **A3: align scaling provenance with the actual independent certificate.** `generate_benchmarks.py` and `benchmarks/MANIFEST.md` still attribute large scaling ground truth to the universal sharp aggregation bound plus a witness. Heterogeneous /2, /4, /5, /10 lines need not attain that universal bound. `experiments/run.py` now uses the appropriate independent local-error envelope, integer upper bound, and Decimal witness replay. Update generated and saved provenance to describe that actual certificate. Do not use the analyzed DP value alone as ground truth.
- [x] **A4: correct the local-period coverage premise and independently check witness feasibility.** The ground-truth comment says the individual nearest-even periods divide 20; they are 4, 8, 10, and 20. Every one is at most 20, so a first-20-tick local table covers its period; divisibility by 20 is unnecessary and false for /4. State the correct reason. Before Decimal replay, independently assert that every witness tick is an integer in the original declared bounds. Upper-bound equality plus replay certifies attainability only for a feasible witness.
- [x] **A5: complete and review the final evaluation artifact.** The first review snapshot contained unresolved input files for the Evaluation and case-result table. Populate them from the completed saved runs and independently check all counts, completion classifications, timing summaries, and table values. No final empirical verdict is issued from an absent section. This is a pending-stage requirement rather than evidence of fabricated completed results.

## Theorem classification and premises

| Manuscript result | Classification | Audit verdict and exact premises |
|---|---|---|
| Common-drift reduction | Ordinary mathematical proposition; background-derived certificate | Correct for exact rational affine/quantizer expressions, the three globally covariant modes, equal erased tick-slope vectors, fixed rational zero-anchored grids, and a Cartesian finite integer box. Constants may differ. Periods are sufficient, not minimal. |
| Exact batch discrepancy | Ordinary mathematical theorem; specialized extrema algorithm | Correct for independent scalar affine lines with a shared normalized output grid, a common integer denominator B, and fixed covariant local/outer modes. The prototype is stricter: one active variable per line and one common mode. Prefix extrema are attained, and backpointers reconstruct actual in-box inputs. |
| Nonnegative sign-sensitive extension | Ordinary mathematical proposition | Correct when every raw normalized line is nonnegative throughout its whole original interval. Exact endpoint checks establish that premise. Actual line arguments, representatives, and totals remain nonnegative. Signed unsupported modes are not thereby admitted to the generic shift theorem. |
| Conditional analyzer correctness | Conditional algorithmic correctness proposition | Correct conclusion under faithful operators and sound successful solver answers; completed detection/optimization must be distinguished from UNKNOWN and incomplete maxima. Correct A2 so the proof invokes exactly the invariants established by the preceding results. This does not verify Python, the parser, or Z3. |
| Sharp aggregation envelope | Elementary ordinary lemma; not an originality claim | Correct for n>=1 arbitrary rational operands and one homogeneous mode shared by local/total rounding. HALF_EVEN gives he(n/2), including the n congruent to 1 modulo 4 exception. FLOOR/CEILING give n-1. Restricted domains can have smaller extrema. |
| Scaling certificate | Benchmark-specific mathematical upper bound plus independent executable witness | Correct when local error extrema cover each line's period, the objective is integral, and the independently replayed witness lies in the original box. The fixed rate set must be recorded; the first-20-tick coverage is not a theorem for arbitrary rational rates. |
| Decimal/property/enumeration checks | Bounded executable evidence | Useful independent checks of implementations on stated grids. Not unbounded proofs, parser verification, or proof-assistant certificates. |

No result should be classified as proof-assistant mechanization or MACHINE-CHECKED. The manuscript's explicit implementation/solver assumptions and its warning about shared parser dependence are appropriate. The sharp stage comparison is signed line-minus-total in its derivation, while the batch theorem is signed total-minus-line; the text consistently uses an absolute envelope when linking the two. No sign reversal bug was found.

## Logical tree

1. A monetary policy prescribes observable rounding stages. Exact rational intermediates alone do not settle stage placement.
2. The analysis contract supplies exact grids, a finite box, and declared policies; legal admissibility is external to the tool.
3. The general certified fragment has rational erased affine drift. Quantizer covariance provides computable shifts. Equal drift cancels in differences, giving exact feasible box representatives.
4. General representative products can remain large. Independent affine lines enable additive local errors conditional on cyclic total residue.
5. Min/max-plus convolution preserves attained prefix extrema. The terminal correction is affine in total local error at a fixed residue, so those two endpoints suffice for exact discrepancy extrema.
6. Full-domain nonnegative certificates permit sign-sensitive modes on the specialized path. Other modes, coupled expressions, branches, and rejected DP cases use unreduced bounded SMT, while eligible core families may use residue-reduced SMT.
7. A faithful encoder and successful solver answers produce conditional exact diagnostics; unknown or interrupted search remains incomplete.
8. Bounded independent oracles and correctly scoped upper-bound/witness certificates evaluate implementation behavior, not the validity of law or defect prevalence in deployed systems.

The central implication chain is coherent. The main structural risk is overstating the boundary between a value-set theorem and an extrema-compression theorem (A2), followed by hiding a mode premise in prose rather than the core grammar (A1).

## Section-role audit

| Section | Role in the argument | Verdict |
|---|---|---|
| Abstract | Contract, technique, complexity, sign restrictions, evaluation scope | Faithful qualitative summary; empirical completion remains contingent on A5. |
| Introduction | Monetary stage problem, prior work, narrowed attainability question | Appropriately disclaims novelty of periodicity, monetary semantics, and counterexample generation. |
| Examples and analysis contract | Observable example and quantified diagnostic target | Correct; finite-family completeness and legal-admissibility boundaries are explicit. |
| Language and exact semantics | Input interpretation, modes, parser scope | Correct operator definitions and type-label limitations; requires A1. |
| Structural shifts | Background certificate and feasible representative theorem | Complete ordinary induction and box argument; no efficiency or minimality overclaim. |
| Attainable extrema | Main specialized algorithm, witness proof, pseudo-polynomial complexity | Sound independence and parity handling; code backpointers support the stated record bound. |
| SMT fallback | Completeness behavior and conditional diagnostic guarantee | Honest timeout classification and implementation assumptions; requires A2. |
| Evaluation | Measured implementation evidence | Pending A5; provenance requires A3 and A4. |
| Public-rule-derived fragments | Motivate small authored comparisons | Properly distinguishes counterfactual policies, illustrative parameters, and genuine public source rules. |
| Related work | Limit firstness/novelty claim to the chosen application | Positioning is appropriately restrained; reference verification belongs to the literature reviewer. |
| Limitations and validity | Generalization and trusted components | Correctly exposes shared inputs, piecewise cases, denominators, machine scope, per-check timeouts, and parser sharing. |
| Conclusion | Restate achieved restricted analysis | No new unproved generality claim. |
| Appendix | Universal comparison envelope | Sound elementary lemma with its restricted-attainability caveat. |

## Implementation match and previous remediation

The inspected implementation measures slopes in integer ticks including input quantum, uses the reduced-denominator period contribution den(a/(p*q)), keeps signed Euclidean residues, rejects affine line sharing, and conditions sign-sensitive DP on exact raw-line endpoint minima. It uses genuine per-layer predecessor maps and separate minimum/maximum trace records. Integer-grid SMT optimization uses a fixed output denominator and sound absolute-error/range upper envelopes; incomplete search never reports an established maximum.

The earlier concrete numeric-JSON quantum hazard was corrected by strict exact field parsing. The earlier O(n)-size path copy at each successful update was replaced by predecessor records. These initial findings and their remediation are documented in `proofs/theory_review.md`; they are not unresolved defects. Reproducible implementation checks are provided by `scripts/proof_sanity.py --implementation`.

## Revision re-audit

A1--A5 were re-inspected and are closed. The grammar explicitly restricts certified modes; the conditional proof separates value-set reduction from extrema preservation; generated and saved provenance describe the local-envelope/integrality/feasible-witness certificate. `experiments/run.py` states periods 4, 8, 10, 20 with individual period at most 20, and explicitly checks witness key sets, integer types, and original bounds. The final `evaluation.tex` correctly states that the sufficient individual periods are at most 20 ticks; the false divisibility sentence has been removed.

The final reproduction's evaluation numbers were independently checked against saved CSV/JSON and every generated `result_macros.tex` value. `notes/reviewer_A_numeric_checks.json` records agreement for 66 programs, 19,940 exhaustive assignments, group labels 37/48, 8/12, 5/6 sensitive, dispatch counts 22/19/25, program-size statistics, and 216 scaling runs. Final completed counts are 72 DP, 35 reduced SMT, and 19 full-grid SMT; reduced-SMT UNKNOWN/partial counts are 25/12 and full-grid SMT counts are 36/17. Earlier wall-time snapshots are superseded. Automatic/full-grid effectiveness medians are 9.77/14.30 ms; the largest DP case median is 101.94 ms. All generated medians, completion counts, and incomplete-status counts were recomputed from their raw records. All 24 scaling certificates were independently recomputed by directly reading the declared x_i/d_i affine lines, using exact Fraction arithmetic and a separate integer/remainder nearest-even function, checking original tick bounds, summing local error envelopes, and replaying the attaining assignment. This scaling replay used neither the analyzer parser nor its quantizer. It confirms 32-line maxima 14/15 cents, 64-line maxima 27/30 cents, and ten cases strictly below the universal bound.

The reviewer reran `scripts/proof_sanity.py --implementation`; all theorem sanity checks and 160 implementation cases pass, and `proofs/sanity_checks.json` again retains the signed and nonnegative implementation-check records. No new critical theoretical or implementation mismatch was found. The final review is ordinary mathematical review plus bounded checks, not mechanized verification or an endorsement of deployability.

The main agent subsequently completed a full reproduction with 88 tests and regenerated the saved records using the stricter Decimal oracle. This reviewer inspected the strict exact-conversion/rounding-trap implementation and verified final saved labels, macros, and scaling certificates; this statement does not claim an additional independent rerun of the whole 88-test suite. Separate scoped copies of this same Reviewer A evidence are saved under the run's `number-check`, `logic-check`, and `section-role-check` directories. They are three views of one independent review, not three distinct reviewers.

## Later central parity theorem: final mathematical re-audit

The preceding numeric reproduction snapshot belongs to the cyclic algorithm and the 24-case scaling suite. It is historical evidence; subsequent parity/coprime runtime records require their own current numeric audit. A1--A4's semantic/provenance corrections remain valid.

The main manuscript's Section 5 was subsequently replaced by the stronger parity-extrema theorem. A final read-only audit of that theorem, its full proof, arithmetic/storage paragraph, nonnegative extension, and the limitation paragraph's two-variable integer-programming observation found no required mathematical correction. Complete independent proofs are in `proofs/parity_theorem.md`. The new theorem has ordinary mathematical status `PROVED`; it is not MACHINE-CHECKED.

The invariant is the integer local output parity together with attained residual endpoints, rather than raw-sum cyclic residue. The normalized local output must be integral. The terminal map is monotone in residual sum at fixed aggregate parity; FLOOR/CEILING need only one state. Certified nonnegative HALF_UP/DOWN/UP use the floor/ceiling extensions even when residual sum is negative. Each local period is den(a_i/2), with the offset denominator irrelevant to representative count. Independent input boxes are essential. The prototype's common-mode restriction and generic optional-placement enumeration are disclosed. Equivalence and attained signed endpoints follow from these exact invariants, without a claim that compressed state represents all interior values.

The work bound O(sum_i min(T_i,width_i)+n), constant working endpoints, and O(n) witness records is correct as an arithmetic-operation bound with rational bit costs excluded. Individual representative enumeration can be exponential in coefficient bit length. The two-variable fixed-parity ILP observation is sound: x and t determine k=2t+b, affine residual constraints have rational endpoints, strict endpoints can be integerized, and fixed-dimensional ILP offers an alternative local optimizer. The paper appropriately does not claim an inherent pseudo-polynomial lower bound or an implemented Lenstra path.

The independent script's latest `--implementation` run is saved in `proofs/sanity_checks.json`. The added parity/cyclic/brute comparisons pass 320 cases over 34,457 Cartesian assignments; both signed witnesses are independently replayed. Nine explicit phase/tie/negative-residual regressions and integer-output/sign-premise rejection checks pass. The prior 160 implementation cases now test BOTH parity and cyclic APIs, with independent replay of BOTH parity signed endpoint witnesses. Coprime four/eight-line cases and large-offset-denominator cases also pass. Inspection of the final `dp_batch` found no critical mismatch with the new theorem within the canonical loaded-Rule contract. This remains independent ordinary proof/code review plus bounded executable evidence.


