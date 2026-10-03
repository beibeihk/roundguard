# Independent theory and logic review

Reviewer task: independently audit mathematical claims, identify counterexamples and scope boundaries, and prove the specialized residue-extrema algorithm. Date: 2026-10-03. Complete proofs and the claim ledger are in `theorems.md`. This review does not certify novelty, code correctness, experiment completion, or a submission-ready paper.

## Main verdict

The proposed rational affine/rounding shift certificate and exact bounded-box reduction are mathematically valid under the explicitly stated semantics. The specialized DP is also valid and gives an exact algorithm without a Cartesian-product domain search for independent affine lines. Its certified nonnegative extension supports all six specified rounding modes; generic signed-domain reduction continues to certify only FLOOR/CEILING/HALF_EVEN. The safe paper claim is an exact, witness-producing residue-extrema algorithm for line-versus-total rounding, supported by a familiar shift-periodicity foundation. Generic periodicity and Presburger encodability must not carry the main novelty claim.

## Required qualifications

1. HALF_EVEN needs parity preservation. The correct period contribution is den(a_child,i/(2q)), not den(a_child,i/q). Doubling the latter is safe but can be larger than necessary. Do not claim the computed period is minimal.
2. A periodic *difference* needs equal erased slopes. Identical erasure implies this but is stronger than necessary. The individual output itself generally has affine drift and is not periodic.
3. The reduced interval begins at the actual lower bound L_i. The map is L_i+((x_i-L_i) mod T_i); this guarantees witnesses remain in the original box, including signed boxes and widths shorter than a period.
4. Large rational denominators can make numeric periods and the DP modulus huge. O(nM^2) is pseudo-polynomial, with M=2B, rather than polynomial in the binary description size. Arithmetic-operation bounds must be distinguished from bit-operation bounds.
5. The DP state holds *attainable extrema*, not an assertion that every error value in the enclosing interval is attainable. Extrema suffice only because the terminal discrepancy is affine in total local error at a fixed total residue.
6. Optional local choices are handled without enumerating their Cartesian product only when their admissibility is independent across lines. An arbitrary declared family, a global placement budget, or other correlated choices needs additional state or explicit enumeration. The witness must include the chosen local operations when optimization includes them.
7. Independent input domains are essential for the DP. A global equality such as sum_i x_i=K makes an arbitrary combination of locally extremal witnesses invalid. Such constraints need additional state, a different exact method, or bounded SMT.
8. The specialized DP concerns R_outer(sum_i y_i) minus sum_i R_i(y_i). Nested quantizers inside affine-line definitions, different per-line grids without normalization, post-aggregation rounding of the line branch, thresholds, and saturation need separate derivations. Do not silently represent them by the same terminal formula.
9. FLOOR/CEILING/HALF_EVEN are the certified signed-domain modes. Conventional HALF_UP (ties away from zero), DOWN (toward zero), and UP (away from zero) fail global translation across zero. Theorem 6b separately proves their DP support when every raw affine line is exactly certified nonnegative on its whole box; sign checks only at tested inputs are insufficient.
10. An exact SMT result is evidence about its encoded query. `unknown`, timeout, or an interrupted optimum is not an equivalence or maximality certificate. Arbitrary bounded testing is not an unbounded proof, and ordinary written proofs are not proof-assistant verification.

## Specialized algorithm: precise useful contribution

After a common grid normalization, choose B clearing affine-line coefficient and constant denominators; z_i=B*y_i is integer and M=2B preserves both fractional parts and HALF_EVEN parity. Each input has sufficient period

    T_i=2B/gcd(|B*a_i|,2B)=den(a_i/2)<=2B.

This means local enumeration itself is bounded by the DP modulus, regardless of the original tick interval width. Store local minimum/maximum d_i=B*R_i(y_i)-z_i conditional on z_i mod M, and retain endpoint witnesses. Independent local errors combine through min-plus and max-plus residue convolution. The final correction C_outer(r)=B*R_outer(r/B)-r depends only on total residue. Therefore global signed extrema are recovered by subtracting the appropriate DP endpoint from that correction. Backpointers recover an input in the actual original box and, where relevant, a valid local operation assignment.

The direct algorithm uses O(nM^2) arithmetic operations, O(M) working values, and O(nM) witness records. Its benefit over the generic theorem is avoiding product_i min(T_i,width_i). This is a real structural improvement in the chosen separable class; whether it is sufficiently novel for publication is a separate literature question. Residue convolution and extrema DP themselves are established algorithmic patterns.

## Elementary bounds that should not be marketed as new

The sharp line-minus-total FLOOR bound is [-(n-1)q,0]; CEILING is [0,(n-1)q]. HALF_EVEN has sharp maximum absolute value q*he(n/2), with the parity exception n congruent to 1 modulo 4: for n=5 the sharp universal bound is 2q, even though ceil(n/2)q is a valid loose bound of 3q. Inputs all equal to q/2 attain the negative HALF_EVEN endpoint. These unrestricted bounds need not be attainable in a given application box; that is a reason to compute exact attainable extrema.

The local interval-error recursion is sound but loses correlation and is generally not tight. It can support a comparison baseline or a quick upper bound, not an exact worst-case claim by itself.

## Counterexamples to retain as regression targets

| Unsafe assumption | Exact counterexample |
|---|---|
| HALF_EVEN shifts by every integer grid tick | he(1/2)=0; he(3/2)=2 |
| Modulus B is sufficient with HALF_EVEN | n=1; y=x+1/2, x in {0,1}; local FLOOR, outer HALF_EVEN; B=2; both local z mod B=1 and d=-1, yet total-minus-lines is 0 and 1 |
| Common input grammar implies periodic pair difference without slope equality | x versus 0 has discrepancy x |
| HALF_UP becomes globally shift-covariant after doubling | ties-away: R(-1/2)=-1, R(3/2)=2; shift 2 produces output drift 3 |
| Toward-zero rounding is globally shift-covariant | R(-1/2)=0, R(1/2)=0; shift 1 produces drift 0 |
| Away-zero rounding is globally shift-covariant | R(-1/2)=-1, R(1/2)=1; shift 1 produces drift 2 |
| Arbitrary min/max preserves affine shift | max(x,0) has different drifts on negative and positive inputs |
| The local extrema imply every interior error is attainable | With B=2, y=1/2, and local choices FLOOR/CEILING, the only errors are -1 and +1; error 0 is absent |
| Finite syntax periods guarantee efficient general enumeration | High denominators and many dimensions make the product representative box huge |

## Positioning against known theory

The closest mathematical foundation is older than this project. H. P. Williams's 2010 survey explicitly describes Chvatal functions built from nested integer round-up and nonnegative combinations as shift periodic, and illustrates a nested example. The present signed rational arithmetic and HALF_EVEN parity handling require precise semantic treatment, but do not justify presenting shift periodicity itself as new. [Williams, The Problem with Integer Programming, LSEOR 10-118 (2010)](https://personal.lse.ac.uk/WILLIAHP/pubs/WP%2010-118.pdf).

Presburger and quasi-affine tools already represent rational affine functions with integer division and piecewise descriptions. The isl tutorial's Chapter 4 expressly relates piecewise quasi-affine expressions to functions representable by Presburger relations; its manual describes exact integer arithmetic and floor/division facilities. The project's linear-integer encoding is an application of this foundation, rather than a new decision procedure. [isl tutorial, Chapter 4](https://libisl.sourceforge.io/tutorial.pdf), [isl manual](https://libisl.sourceforge.io/user.html).

Cluckers proves cell decomposition for Presburger sets, providing relevant broader definability theory. Woods relates Presburger counting functions to piecewise quasi-polynomials and rational generating functions. Those papers are broader than the exact separable rounding optimization proved here; they are context, not evidence that this particular DP has never appeared. [Cluckers, Presburger sets and p-minimal fields](https://arxiv.org/abs/math/0206197), [Woods, Presburger arithmetic, rational generating functions, and quasi-polynomials](https://arxiv.org/abs/1211.0020).

The likely paper burden is therefore to demonstrate a clearly specified application-verification problem, a practically useful specialized exact algorithm, correct treatment of parity/sign/witnesses, and measured gains over exact baselines. A novelty review must additionally inspect accounting/monetary rounding, finite-state integer arithmetic, modular dynamic programming, and exact rounding-error optimization. This file makes no firstness finding for the DP.

## Recommended claim boundaries

Accept: exact equivalence and worst-case discrepancy in the certified grammar via finite representatives; exact pseudo-polynomial specialized DP for independent affine lines; actual in-domain witnesses; automatic complete search over a finite declared placement family or independent product of local choices as separately stated.

Reject unless separately proved: minimal periods; polynomial time in the binary input length; efficient unrestricted dimensional scaling; arbitrary branch/threshold/nonlinear support; unconditional support for all rounding modes; complete search over an unspecified placement universe; proof-assistant verification; first-ever rounding equivalence method; novelty of elementary stage bounds; empirical speedup before measurement.

## Independent bounded sanity checks

The exact-rational check results are saved in `sanity_checks.json` and are reproducible with `scripts/proof_sanity.py`. Exhaustive tuples on the seven-point grid {-3/4,-1/2,-1/4,0,1/4,1/2,3/4} for n=1 through 6 (137,256 tuples total) attain and never exceed the HALF_EVEN sharp formula. A separate 120-case randomized affine-line check, seed 20261003, compares the residue DP extrema against direct Cartesian enumeration of 27,380 input/operation assignments. Cases have one through four lines, rational coefficients/constants with denominators one through six, negative coefficients and signed inputs, and independent choices among FLOOR, CEILING, HALF_EVEN, and IDENTITY. Another 120 exactly nonnegative line cases, seed 6102026, compare 31,036 assignments across all six rounding modes and IDENTITY; these include negative slopes and signed input ticks whose affine offsets maintain nonnegative raw line values. Every compared signed minimum and maximum agrees. These observations are bounded sanity checks only; the full mathematical proofs above establish the stated general claims. The default script is self-contained and does not import `src/`; its optional `--implementation` checks separately compare the project implementation with independent direct enumeration.

## Implementation review observations

Initial review of `src/roundguard/analysis.py`, `model.py`, and `semantics.py` found that exact quantizer semantics, signed HALF_EVEN parity, syntax periods, tick-quantum slope scaling, affine independence rejection, residue correction, bounded-SMT fallback, and integer-grid binary search align with the stated proofs. The implementation's DP currently uses a fixed common mode and does not implement the theorem's independent local-operation-choice extension. That difference is a feature-scope boundary, not a mathematical error.

Two concrete issues were reported to the main agent for remediation. First, path dictionaries copied during successful DP updates can cost O(n) per update, so O(nM^2) cannot describe total running time of that version without qualifying that it counts arithmetic operations only. True layer-indexed predecessor records give the stated update bound with O(nM) witness records. Second, `json.loads` followed by `Fraction` of a numeric JSON decimal can silently change an intended decimal quantum to a binary rational. The reproduced example uses x tick=10, numeric quantum 0.1, and variants `Q(x,1,"CEILING")` versus `1`: the initial parser yields quantum 3602879701896397/36028797018963968 and outputs 2 versus 1, whereas exact decimal quantum 1/10 yields 1 versus 1. Exact quantum fields should reject floating JSON numbers or parse them as exact decimal values before Fraction conversion. Expression floating literals were already rejected. Reinspection and implementation-check outcomes should be recorded after remediation; this paragraph documents the initial findings rather than asserting they remain unresolved.

Reinspection confirms both findings were remediated: `model.exact_field` rejects JSON floating/bool quantum fields, and `dp_batch` stores separate per-layer predecessor maps for its minimum and maximum states. Its nonnegative mode extension checks every normalized raw affine line's exact endpoint minimum before permitting HALF_UP/DOWN/UP. Generic periods still reject those modes. The optional implementation audit in `scripts/proof_sanity.py --implementation`, run using the project `.venv`, passes 80 signed covariant cases against 5,533 direct assignments and 80 certified-nonnegative six-mode cases against 4,975 direct assignments. These cases additionally cover nonunit input/output quanta, negative slopes, constant lines, and genuine in-domain witness replay. Both input-quantum and batch-quantum numeric-decimal guard cases are rejected. No further critical mismatch was found in this inspection; this is independent review plus bounded oracle evidence, not formal software verification.
