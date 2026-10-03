# Independent audit of the parity-state revision

search_date: 2026-10-03
scope: independent mathematical and adjacent-prior-art audit, not a manuscript edit
decision: MATHEMATICALLY SOUND UNDER THE STATED PREMISES; MODEST ORIGINALITY ONLY
implementation_and_new_experiment_review: PENDING

## The compression and its premises

Normalize one common monetary quantum to one. Each local prescribed rounding output must be an integer: k_i=R_i(y_i). Put f_i=y_i-k_i, K=sum k_i and F=sum f_i. Then the signed total-minus-lines difference is R_0(K+F)-K.

For globally covariant outer FLOOR and CEILING, this is floor(F) and ceil(F), respectively. Only the attainable minimum and maximum F are needed. For outer HALF_EVEN, write K=2t+kappa, kappa in {0,1}. The difference is g_kappa(F)=HE(F+kappa)-kappa. Each g is monotone, so attained min/max F at each total parity suffice. Independent local domains allow the extrema to combine; no interior-error attainability assumption is needed. Local witnesses and O(n) backpointers attain the final extrema. The statement is also meaningful for negative inputs and negative slopes with the globally covariant modes.

For nonnegative raw-line domains, outer HALF_UP, DOWN and UP use floor(F+1/2), floor(F), and ceil(F). F itself can be negative: these are translated extensions of the outer rule, not signed rounding applied directly to F. One line y=1/2 with local HALF_UP has K=1,F=-1/2 and actual difference zero; signed HALF_UP(F) would incorrectly give -1. With local UP at y=1/5 and outer DOWN, the correct difference is -1=floor(-4/5), while truncation would give zero.

The two states are genuinely necessary in the stated general class. Two HALF_EVEN lines y_1=1/2 (constant) and y_2=x, x in {0,1}, always have F=1/2 but have discrepancies zero and one. An F-only endpoint table would lose the tie-parity distinction.

Unsupported generalizations remain: shared/coupled inputs, unequal output quanta, a nonintegral unrounded local output, an arbitrary sign-sensitive outer rule on signed totals, or multiple policies outside this exact line/total contract. Identity/no-round locals fit only when their outputs are integral. Source-level optional rounding interfaces do not automatically fit the parity theorem.

## A still simpler equivalent combination

The two-state min/max-plus recurrence is elementary and admits a separable description. For a maximum, choose each line's larger attainable parity endpoint, producing total parity kappa*. To get the other parity, switch exactly one flexible line with the smallest loss. Any assignment of the opposite parity switches an odd number of lines; each switch has nonnegative loss, so it cannot beat the cheapest single switch. The minimum uses the smallest increase. Equal-cost endpoints allow a zero-cost flip; if no line has both parities, the opposite total parity is unreachable. Witnesses use the selected endpoint ticks.

This is equivalent to the two-state recurrence and has the same O(n) combination cost. It strengthens the rejection argument against presenting the DP mechanism itself as a new combinatorial algorithm. Keeping the DP implementation for clarity is reasonable.

## Denominator dependence and a polynomial-bit alternative

A sufficient local period is T_i=den(a_i/2), with T_i=1 for zero slope. The shift changes y_i by an even integer, preserving local parity and error. Offset denominators do not affect this period. Enumeration requires only min(T_i,U_i-L_i+1) feasible ticks per line. Thus the precise arithmetic-operation bound is O(sum_i min(T_i,width_i)+n); rational bit costs are excluded. There is no need for a joint common-denominator state space. Slopes 1/p and 1/q require periods 2p and 2q even when a common denominator would be pq. A guard solely on the old joint modulus can reject otherwise cheap parity instances unnecessarily.

An individual period can still be exponential in its coefficient's binary encoding. However, this is a property of the enumerative prototype, not an inherent lower bound for the independent-line problem. At fixed parity b, write k=2t+b and f=ax+c-2t-b. Local FLOOR constrains f to [0,1), CEILING to (-1,0], and HALF_EVEN to [-1/2,1/2] for b=0 or (-1/2,1/2) for b=1. Optimizing f involves only integer variables x,t. Strict rational inequalities can be converted to non-strict integer inequalities after clearing denominators. Fixed-dimension integer feasibility plus threshold search gives polynomial-bit extrema and witnesses. This application is an inference from [Lenstra's fixed-dimension theorem](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf), not a monetary algorithm explicitly supplied there. The prototype does not implement this alternative.

## Adjacent primary sources checked in this revision

- **Yap and Yu (2009), Foundations of Exact Rounding**, WALCOM/LNCS 5431, pp.15-31, DOI [10.1007/978-3-642-00202-1_2](https://link.springer.com/chapter/10.1007/978-3-642-00202-1_2). Primary Section 2 defines general rounding grids, directed modes and parity-based tie conventions. Its focus is correctly rounding elementary functions from arbitrary-precision approximation, rather than policy discrepancy over independent monetary grids. [Primary PDF](https://cs.nyu.edu/~exact/doc/exactround.pdf). Reading: Section 2 and problem definitions; not all transcendence proofs.
- **Aswal, Perumal and Prasanna (2012), On Basic Financial Decimal Operations on Binary Machines**, IEEE Transactions on Computers 61(8), pp.1084-1096, DOI 10.1109/TC.2012.89. Sections 3-5 model financial transactions, use transaction-error tables, and construct sequences with recurring capitalization errors after financial rounding. The compared semantics are binary computation versus correct decimal execution, not two prescribed exact policies on independent bounded inputs. It nevertheless rules out broad first-worst-case-monetary-analysis claims. [Institution-hosted primary PDF](https://www.iiitb.ac.in/csl/documents/abhilashaFP.pdf). Reading: targeted Sections 3-5, not all implementation/performance details.
- **Kis and Horvath (2022; online 2021), Ideal, non-extended formulations for disjunctive constraints admitting a network representation**, Mathematical Programming 194, pp.831-869, DOI [10.1007/s10107-021-01652-z](https://link.springer.com/article/10.1007/s10107-021-01652-z). Section 5.5 treats the classical parity polytope and cites Jeroslow's 1975 description. This establishes adjacent parity-constrained optimization infrastructure; it does not supply the proposed monetary state identity or the cheapest-flip argument above. Reading: primary abstract and Section 5.5, not the entire general formulation proof.
- **Lenstra (1983), Integer Programming with a Fixed Number of Variables**, Mathematics of Operations Research 8(4), pp.538-548, DOI [10.1287/moor.8.4.538](https://pubsonline.informs.org/doi/abs/10.1287/moor.8.4.538). The abstract, input model and introductory main-result discussion support fixed-dimension polynomial feasibility. The full geometry-of-numbers proof was not independently checked. [Author-hosted primary PDF](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf).

Exact DOI metadata were checked through Crossref against publisher/primary headers. Aswal's third author is taken from the paper header because the Crossref name fields repeat part of the name. No search-engine crawl date was treated as publication year. Additional targeted queries covered parity optimization, sum/line financial rounding, fractional-part extrema, and modular arithmetic progression optimization. No direct Google Scholar or exhaustive database search is claimed.

## Revised gate

The parity reduction is a worthwhile correction to an unnecessarily large internal cyclic state space. The strongest credible claim is an exact specialized formulation with one/two combination states, feasible witnesses and a reproducible implementation comparison against the larger cyclic baseline and SMT. Generic parity, monotone rounding, separability, dynamic programming and polynomial fixed-dimension integer reasoning are established foundations. The narrowed report passes the mathematical audit; release-level implementation, refreshed experiments and manuscript alignment must be reviewed after this revision. It is not a first-ness certification or a publication-acceptance prediction.
