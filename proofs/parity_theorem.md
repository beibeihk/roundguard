# Exact parity-extrema compression for line-versus-total rounding

Independent mathematical audit, 2026-10-03. The results below are `PROVED` in the ordinary mathematical sense: complete proofs are supplied. They are not proof-assistant mechanizations and are not labelled `MACHINE-CHECKED`. This theorem strengthens the cyclic-residue algorithm in `theorems.md`; that earlier algorithm remains correct as a baseline. No firstness or general-complexity lower-bound claim is made.

## 1. Premises, signs, and observation

Normalize the shared output quantum q>0 to one. Physical input tick quanta are absorbed into the exact rational coefficients. Each independent line is

    y_i(x_i)=a_i*x_i+c_i,    x_i in {L_i,...,U_i},

with exact rational a_i,c_i and a finite nonempty integer interval. A constant line has a_i=0 and may be treated as a dummy one-point interval. The domain is the Cartesian product of these independent intervals; there are no cross-line feasibility constraints. For each line a fixed rounding operation R_i selects an integer, and the outer R_0 likewise selects an integer. Define

    k_i=R_i(y_i) in Z,      f_i=y_i-k_i in Q,
    K=sum_i k_i,            F=sum_i f_i,
    P_line=K,               P_total=R_0(K+F),
    delta=P_total-P_line.

The core permits FLOOR, CEILING, and HALF_EVEN for local and outer operations on signed arguments. The nonnegative extension permits all six documented modes, provided every raw y_i is nonnegative throughout its original interval. The prototype may impose the stricter condition of a single common mode.

Independent finite local choices among integer-output modes also fit the proofs if their admissibility is a product family and local witnesses include the chosen mode. A generic no-round IDENTITY choice does **not** fit: its normalized output y_i need not be integer, so k_i modulo two is not defined. One may separately admit an identity choice only after proving that all its permitted raw values are integral. Arbitrary correlated placement families and shared raw inputs require additional state or another exact method.

Signed discrepancy here is total minus lines. The earlier aggregation lemma's line-minus-total quantity has the opposite sign; maximum absolute discrepancy is unchanged. Original monetary units multiply every reported delta by q.

## 2. The monotone terminal maps

Let kappa=K mod 2 in {0,1}. Define a terminal function g_kappa(F) for every rational F:

    outer FLOOR:       g_kappa(F)=floor(F),
    outer CEILING:     g_kappa(F)=ceil(F),
    outer HALF_EVEN:   g_kappa(F)=he(F+kappa)-kappa.

For the certified nonnegative extension define

    outer HALF_UP:     g_kappa(F)=floor(F+1/2),
    outer DOWN:        g_kappa(F)=floor(F),
    outer UP:          g_kappa(F)=ceil(F).

For modes other than HALF_EVEN, the parity argument is irrelevant, though retaining two states is harmless. Crucially the last three displays use the indicated floor/ceiling extensions on F even if F<0. They are not calls to the conventional signed HALF_UP/DOWN/UP functions on F.

**Lemma P1 — PROVED.** Every terminal function above is monotone nondecreasing in F. In its stated mode/sign scope,

    R_0(K+F)-K=g_(K mod 2)(F).

**Proof.** Integer translation gives floor(K+F)-K=floor(F) and similarly for ceiling. For HALF_EVEN, write K=2j+kappa with integer j, including negative K. Even-integer translation gives

    he(K+F)-K=he(F+kappa)-kappa.

For the nonnegative extension, every raw line is nonnegative, so S=K+F=sum_i y_i is nonnegative. On this actual total, HALF_UP is floor(S+1/2), DOWN is floor(S), and UP is ceil(S). Subtracting integer K from these expressions yields their displayed terminal maps, without requiring F to be nonnegative.

Floor and ceiling are nondecreasing, as is their argument-shifted HALF_UP extension. To prove nearest-even monotonicity, suppose u<=v yet he(u)=k>l=he(v). The nearest-integer condition gives u>=k-1/2>=l+1/2>=v. Combined with u<=v, all inequalities must be equalities, so u=v at the shared half tie and k=l+1. The deterministic tie rule cannot assign two different values to the same u=v; contradiction. Thus he is nondecreasing. Adding/subtracting a fixed kappa preserves monotonicity. QED.

**Parity is necessary for HALF_EVEN.** A local FLOOR output at y=1/2 has k=0,f=1/2 and outer HALF_EVEN discrepancy zero. At y=3/2 it has k=1,f=1/2 and discrepancy one. F alone does not determine the discrepancy. In a homogeneous HALF_EVEN example, operands (1/4,1/4) and (5/4,1/4) also have F=1/2 but K parities zero and one, giving discrepancies zero and one.

**Signed residual evaluation is unsafe for positive sign-sensitive policies.** A single y=1/2 with local and outer HALF_UP has k=1,F=-1/2 and true discrepancy zero. Conventional signed HALF_UP(-1/2) is -1; the correct map floor(F+1/2) is zero. A single y=2/5 with local and outer UP has k=1,F=-3/5 and true discrepancy zero; signed UP(F)=-1 but ceil(F)=0. With local UP and outer DOWN on the same y, the true discrepancy is -1; signed DOWN(F)=0 but floor(F)=-1.

## 3. Local feasible extrema without a common-denominator residue state

For each line define

    T_i=den(a_i/2),

where den is the positive reduced denominator and den(0)=1. Neither a joint least common multiple nor the denominator of c_i is needed for this period. Let

    H_i={L_i,...,L_i+min(T_i,U_i-L_i+1)-1}.

For each locally attainable parity b in {0,1}, retain the minimum ell_i(b) and maximum u_i(b) of f_i over H_i and the allowed local choices, with a valid input/mode witness for each endpoint. Absent parities are unreachable. Retaining endpoints does not assert that intervening values are attainable.

**Lemma P2 — PROVED.** These retained local extrema are exactly the attainable extrema conditional on k_i mod 2=b over the entire original interval. The stored witnesses are genuine original-domain witnesses.

**Proof.** By the denominator definition, a_i*T_i is an even integer. In the signed core, translating y_i by any integer multiple of a_i*T_i translates k_i by the same even integer, by integer covariance for FLOOR/CEILING and even covariance for HALF_EVEN. Consequently its parity and residual f_i=y_i-k_i are unchanged. Reduce x_i to

    x'_i=L_i+((x_i-L_i) mod T_i).

As in the bounded-box reduction proof, x'_i is in H_i and x_i-x'_i is a multiple of T_i. Thus the pair (k_i mod 2,f_i) at x_i also occurs at x'_i. Conversely H_i is a subset of the original interval.

In the nonnegative extension, y_i at x_i and x'_i is nonnegative because both inputs lie in the original interval. HALF_UP, DOWN, and UP agree there with floor(y+1/2), floor(y), and ceil(y), respectively. These agree under the integer translation between the two nonnegative arguments; k_i changes by the same even integer and f_i is again unchanged. The argument holds separately for each independent allowed local mode. Therefore every attainable local pair occurs in H_i, proving exact extrema and witness validity. QED.

Exact nonnegativity is checked by min(a_i*L_i+c_i,a_i*U_i+c_i)>=0, including a constant line. Merely nonnegative input ticks do not prove a nonnegative raw line.

## 4. Two-state prefix recurrence

Define V_j^-(b),V_j^+(b) as the minimum/maximum attainable total residual sum over the first j lines conditional on sum_{i<=j}k_i mod 2=b. Initialize only parity zero as reachable:

    V_0^-(0)=V_0^+(0)=0.

Update using XOR addition of parities:

    V_j^-(b)=min_(s xor t=b) (V_(j-1)^-(s)+ell_j(t)),
    V_j^+(b)=max_(s xor t=b) (V_(j-1)^+(s)+u_j(t)),

with only reachable states participating. Store an endpoint's predecessor parity and the chosen local endpoint witness. Use exact rational values without a B-indexed residue table. Rational summation may still create large internal common denominators; their bit costs are excluded from the arithmetic-operation count.

**Lemma P3 — PROVED.** The recurrence computes exact attained prefix residual extrema conditional on total output parity.

**Proof.** At j=0 only the empty assignment exists, with integer sum zero and residual zero. Every feasible j-line assignment decomposes into an independently feasible (j-1)-line assignment and a feasible local input/mode for line j. Conversely any such pair combines, because domains and mode choices are independent. Their residuals add, while integer-output parities add modulo two, which is XOR. At fixed predecessor/local parities the least attainable sum is the sum of the two attained least endpoints; similarly for the greatest sum. Taking the minimum or maximum over the at most two parity decompositions proves the displayed recurrence and attainment. Induction completes the proof. QED.

## 5. Exact discrepancy and witnesses

**Theorem P4 — PROVED.** Under the premises above,

    delta_min=min_reachable_b g_b(V_n^-(b)),
    delta_max=max_reachable_b g_b(V_n^+(b)).

Both extrema are attained by reconstructible inputs in the original box (and declared local choices if applicable). Equivalence over that box/product family holds exactly when delta_min=delta_max=0. The exact maximum absolute discrepancy is max(-delta_min,delta_max).

**Proof.** Lemma P1 expresses every feasible discrepancy as g_b(F), where b is the sum-of-local-output parity. Lemma P3 supplies the attained least and greatest F at each reachable b. Monotonicity implies

    g_b(V_n^-(b)) <= g_b(F) <= g_b(V_n^+(b))

for every feasible assignment with that parity. Each endpoint value is attained by the assignment attaining its corresponding F endpoint, even when g_b has flat regions. Taking minimum/maximum over reachable parity states proves the formulas and attainment. A nonempty set of discrepancies is identically zero exactly when its attained minimum and maximum are zero. Its maximum absolute value is achieved at an attained endpoint and equals the stated expression.

At each prefix endpoint, retain its predecessor parity and the selected local endpoint's input/mode. Follow these records backward from the final parity attaining the desired delta endpoint. Lemma P3's induction guarantees the chain ends at the initial parity zero. Lemma P2 guarantees every reconstructed local input lies in its original interval; independent combination gives a feasible full assignment. Every optional mode witness belongs to its declared independent local set. The reconstructed input thus attains the reported signed/absolute endpoint. QED.

This theorem preserves exact attained extrema and the zero test; it does not represent the entire attainable discrepancy value set.

## 6. Enumeration and storage bound

**Proposition P5 — PROVED for the enumerative algorithm.** Put w_i=U_i-L_i+1 and h_i=min(T_i,w_i). With a fixed constant-size set of allowed integer-output modes, the algorithm uses

    O(sum_i h_i+n)

exact arithmetic operations, O(1) auxiliary working endpoint values, and O(n) witness/backpointer records, excluding the parsed input and operand bit costs. For a single fixed local mode, exactly h_i tick representatives are evaluated at line i. A common-denominator state space is unnecessary.

**Proof.** Streaming the h_i representatives and a constant number of allowed local modes retains at most two local parities, each with a minimum and maximum endpoint and witness. This costs O(h_i) operations and constant-size local storage. Each prefix has at most two reachable parities. Each min/max update examines at most four predecessor/local combinations, hence constant work and constant working values per line. Retained trace records number at most four per prefix, so O(n) records. Final terminal evaluation involves at most four endpoint values; backward reconstruction takes O(n) steps. Summing gives the bound. QED.

These are arithmetic-operation bounds, not unit-cost statements about large integer/rational arithmetic. Individual T_i may be exponential in binary coefficient size, so this enumerative implementation is not claimed to be polynomial in binary input length. This is not an inherent hardness or lower-bound claim for the mathematical problem; different local optimizers may avoid representative enumeration. Denominators introduced by rational sums influence bit costs, but they do not enlarge the two-state recurrence or its local representative domains.

For slopes 1/p_i with distinct prime p_i and zero offsets, safe local periods are 2p_i. The local work is additive in those periods. The former cyclic method uses M=2*lcm_i(p_i), creating a much larger state space; a guard based solely on that joint M is not a valid resource rationale for rejecting the new parity algorithm. Large offset denominators alone likewise do not enlarge T_i.

## 7. Relationship to the previous cyclic baseline

The cyclic method tracks the total raw numerator residue and extrema of d_i=B*k_i-B*y_i. The parity method instead tracks the integer rounded-output phase and extrema of f_i=y_i-k_i. Both terminal identities are exact in their stated scope, but parity monotonicity discards information unnecessary for extrema. Thus the two methods must return identical signed and absolute extrema on every shared supported instance. The cyclic method also has a theoretical IDENTITY/no-round extension with noninteger outputs; that extension is not automatically shared by parity compression.

The new compression neither permits correlated inputs nor extends generic signed mode covariance. It strengthens the specialized algorithm's computational representation, not the analysis contract or legal policy admissibility.

## 8. Equivalent elementary parity correction

**Corollary P6 — PROVED.** The prefix maximization can also be solved by independent local maxima and, if required, one cheapest parity flip. For each line choose a parity s_i attaining its larger local maximum u_i(s_i), choose an arbitrary tie deterministically, and let H=sum_i u_i(s_i), b*=xor_i s_i. Then the maximum for b* is H. If an opposite-parity assignment is feasible, its maximum is

    H-min_flexible_i (u_i(s_i)-u_i(1-s_i)).

If no line has both parities attainable, opposite parity is unreachable. Minima follow the same argument with the smaller ell_i(s_i) and the smallest increase ell_i(1-s_i)-ell_i(s_i).

**Proof.** Every assignment with chosen output parities t_i has residual at most sum_i u_i(t_i), with equality attainable independently. Relative to the independently maximizing s_i, changing line i's parity incurs a nonnegative loss u_i(s_i)-u_i(1-s_i). To change global XOR parity, an odd nonempty set of flexible lines must change. The sum of its nonnegative losses is at least the smallest available individual loss. Flipping precisely one line attaining that smallest loss gives the opposite parity and attains the bound. For b*, no flips attain H and no assignment can exceed the sum of independent maxima. The minimum statement uses nonnegative increases analogously. QED.

This corollary emphasizes that the parity recurrence is an elementary separable optimization pattern; no novelty claim is attached to two-state DP or cheapest-parity correction itself.

## 9. Verification ledger

| Item | Status | Qualification |
|---|---|---|
| Monotone terminal maps and parity identity | PROVED | Integer normalized local outputs; correct sign-sensitive extension |
| Local pair representative reduction | PROVED | T_i=den(a_i/2), exact rational slopes, original-domain sign condition if needed |
| Two-state attained prefix extrema | PROVED | Independent lines and independent declared mode choices |
| Exact signed/absolute discrepancy and witnesses | PROVED | Fixed common output grid; all stated mode/box premises |
| Enumerative arithmetic/storage bound | PROVED | Operand bit costs and parsed input storage excluded |
| Greedy parity-flip equivalence | PROVED | Elementary optimization; not an originality claim |
| Generic noninteger no-round placements | NOT INCLUDED | Integer-output premise may fail |
| Proof-assistant verification | NOT PERFORMED | Never MACHINE-CHECKED |
| Firstness or inherent complexity lower bound | NOT ESTABLISHED HERE | Requires separate literature/complexity analysis |

## 10. Independent bounded implementation evidence

`scripts/proof_sanity.py --implementation` completed on 2026-10-03 and saved its exact reports to `sanity_checks.json`. The default self-contained script uses a separately defined integer/remainder quantizer and never imports project semantics. It compares the direct-Fraction parity recurrence, the cyclic recurrence, and full Cartesian enumeration on 160 signed-core cases (21,629 assignments) and 160 certified-nonnegative six-mode cases (12,828 assignments), with independent local integer-output mode choices and nonterminating rational coefficients. Both signed endpoint witnesses are independently replayed. Nine explicit tie/phase/negative-residual regressions and the identity/sign-premise rejection checks pass.

The optional implementation audit imports the project algorithms only after constructing independent expected values. Both `dp_batch` (parity) and `cyclic_batch` pass the previous 80 signed and 80 nonnegative cases against 5,533 and 4,975 assignments. This audit checks nonunit tick/output grids, negative slopes, constants, local period/count metadata, maximum absolute discrepancy, and independent replay of both parity signed witnesses. Coprime slope cases with four and eight lines also pass, as does a narrow signed-domain case with offset denominators 1009 and 1013. Those succeed under the parity representative budget while the cyclic joint-denominator budget rejects them.

Code inspection of `analysis.py` found that the implemented shared-mode canonical batch contract matches the theorem's premises and terminal identities. A successful written proof and these bounded checks remain distinct: none of this evidence is a proof-assistant verification of Python, its parser, or external solver correctness.
