# Rule interface

```json
{
  "name": "invoice",
  "variables": {
    "x": {"min": 0, "max": 19, "quantum": "1", "type": "Money"},
    "y": {"min": 0, "max": 19, "quantum": "1", "type": "Money"}
  },
  "batch": {"lines": ["x/5", "y/5"], "quantum": "1", "mode": "HALF_EVEN"}
}
```

This generates `per_line` and `total` policies. Alternatively, specify a `variants` object mapping names to expression strings. A `template` using `maybe(expression, quantum, mode, "site")` enumerates round/no-round placements; identical site names share a decision. Ten distinct sites are the maximum.

The input domain is the Cartesian product of inclusive integer tick bounds. The amount denoted by `x` is its tick multiplied by its declared quantum. Bounds must be integers; quanta must be positive exact integers or rational/decimal strings. `Money`, `Decimal`, `Rate`, and `Integer` are representation labels; `Integer` requires unit quantum. Currency typing, dimensional checking, and legal-policy inference are not implemented.

Expressions support exact literals, variable names, addition/subtraction, constant multiplication/division, `rat(n,d)`, `rate("0.062")`, `decimal("0.1")`, `Q(e,q,"MODE")`, `sum([e,...])`, `min(e,e)`, `max(e,e)`, and numeric conditional expressions with `<`, `<=`, `>`, `>=`. Arbitrary calls, attribute access, input-input multiplication, and input-dependent division are rejected. There are no loops, machine overflow, or implicit binary floats.

Modes: `FLOOR`, `CEILING`, `HALF_EVEN`, `HALF_UP` (ties away from zero), `DOWN` (toward zero), and `UP` (away from zero).

`--method auto` uses parity-conditioned attainable residual extrema for independent affine batches when certified, otherwise reduced or unreduced SMT. `dp` uses at most two states, directly enumerates the feasible first local period `den(a_i/2)`, and declines if any line needs more than 400 representatives. It constructs no common-denominator residue table; exact residual sums can still have large denominator bit lengths. `cyclic` retains the exact cyclic-residue ablation, declining if its common-denominator modulus exceeds 400. Both batch paths require exactly the generated `per_line`/`total` family and independent line inputs; additional policies trigger the SMT fallback. Generated batch or placement names are reserved: collisions with explicit variants are rejected rather than overwritten. `residue` uses structural reduction if justified and otherwise the unreduced box. `smt` is the full-box ablation. `--timeout-ms` limits each solver check, not the full analysis. An unfinished optimization can still report SENSITIVE and valid bounds after finding a witness; only `complete: true` establishes the reported exact optimum. `maximum_discrepancy` is null when not established.

Completed `dp` records include signed extrema, separate attaining assignments for both endpoints, `parity_states`, `active_states`, `local_periods`, `local_representatives`, and `transitions`. HALF_EVEN needs two parity states; the remaining common modes use one. HALF_UP, DOWN and UP are supported by this path only when every raw affine line is nonnegative on its box. Their terminal functions are extended floor/ceiling maps, even when the sum of residuals is negative. Enumeration is pseudo-polynomial in individual slope denominators; this is a limitation of the implemented algorithm, not an inherent complexity lower bound.

The Decimal exhaustive oracle is an evaluation aid with an explicit domain-size limit and exactness restrictions. It rejects nonterminating decimal arithmetic, including normalized quantum division such as 1/3 in Q(1,3,...), and insufficient precision rather than approximate. The analyzer itself uses exact Fractions and rational SMT and supports such rational quanta.
