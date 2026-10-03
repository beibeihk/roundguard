"""Reproducible finite checks for theorems.md and parity_theorem.md.

These checks are independent exact-Fraction enumerations, not proof-assistant
verification. Run with any Python 3.11+:
    python scripts/proof_sanity.py
To also audit the project implementation, use its environment:
    .venv/Scripts/python.exe scripts/proof_sanity.py --implementation
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import tempfile
from fractions import Fraction as F
from math import gcd, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COVARIANT = ["floor", "ceil", "he"]
ALL_MODES = COVARIANT + ["half_up", "down", "up"]


def independent_round(y: F, mode: str):
    """No project semantics imports: direct integer/remainder definitions."""
    k = y.numerator // y.denominator
    f = y - k
    if mode == "floor":
        return k
    if mode == "ceil":
        return k + (f != 0)
    if mode == "id":
        return y
    if mode == "down":
        return k + (y < 0 and f != 0)
    if mode == "up":
        return k + (y > 0 and f != 0)
    tie_up = k % 2 != 0 if mode == "he" else y >= 0
    return k + (f > F(1, 2) or (f == F(1, 2) and tie_up))


def independent_dp(a, c, bounds, choices, outer):
    B = lcm(*(v.denominator for v in a + c))
    M = 2 * B
    states = {0: (0, 0)}
    for ai, ci, (lo, hi), options in zip(a, c, bounds, choices):
        A = int(B * ai)
        T = M // gcd(abs(A), M)
        local = {}
        for x in range(lo, lo + min(T, hi - lo + 1)):
            y = ai * x + ci
            z = int(B * y)
            for mode in options:
                d = int(B * independent_round(y, mode) - z)
                r = z % M
                old = local.get(r, (d, d))
                local[r] = (min(old[0], d), max(old[1], d))
        updated = {}
        for s, (low, high) in states.items():
            for t, (dl, dh) in local.items():
                r = (s + t) % M
                candidate = (low + dl, high + dh)
                old = updated.get(r, candidate)
                updated[r] = (min(old[0], candidate[0]), max(old[1], candidate[1]))
        states = updated
    minimum = min(
        F(B * independent_round(F(r, B), outer) - r - high, B)
        for r, (low, high) in states.items()
    )
    maximum = max(
        F(B * independent_round(F(r, B), outer) - r - low, B)
        for r, (low, high) in states.items()
    )
    return minimum, maximum


def direct_values(a, c, bounds, choices, outer):
    local = [
        [(ai * x + ci, mode) for x in range(lo, hi + 1) for mode in options]
        for ai, ci, (lo, hi), options in zip(a, c, bounds, choices)
    ]
    result = []
    for assignment in itertools.product(*local):
        exact = sum((y for y, mode in assignment), F(0))
        rounded_lines = sum((independent_round(y, mode) for y, mode in assignment), F(0))
        result.append(independent_round(exact, outer) - rounded_lines)
    return result


def parity_terminal(residual: F, parity: int, outer: str):
    """The total-minus-lines identity, including positive-policy extensions."""
    if outer == "he":
        return independent_round(residual + parity, "he") - parity
    if outer == "half_up":
        return independent_round(residual + F(1, 2), "floor")
    if outer == "down":
        return independent_round(residual, "floor")
    if outer == "up":
        return independent_round(residual, "ceil")
    return independent_round(residual, outer)


def independent_parity_dp(a, c, bounds, choices, outer):
    """Independent exact-Fraction parity recurrence with real backpointers.

    This uses no B-indexed residue table and no project semantics. Exact
    Fraction sums can still create internal common denominators.
    Unlike the cyclic baseline, its contract excludes generic IDENTITY choices.
    """
    if outer not in ALL_MODES or any(not set(options) <= set(ALL_MODES) or not options
                                    for options in choices):
        raise ValueError("Parity compression requires integer-output modes")
    signed_modes = {"half_up", "down", "up"}
    if outer in signed_modes or any(signed_modes.intersection(options) for options in choices):
        if any(min(ai * lo + ci, ai * hi + ci) < 0
               for ai, ci, (lo, hi) in zip(a, c, bounds)):
            raise ValueError("All raw lines must be nonnegative")
    low = high = {0: F(0)}
    low_trace, high_trace = [], []
    periods, counts = [], []
    for ai, ci, (lo, hi), options in zip(a, c, bounds, choices):
        period = (ai / 2).denominator
        count = min(period, hi - lo + 1)
        periods.append(period)
        counts.append(count)
        local = {}
        for x in range(lo, lo + count):
            y = ai * x + ci
            for mode in options:
                k = independent_round(y, mode)
                assert isinstance(k, int)
                f, b = y - k, k % 2
                if b not in local:
                    local[b] = (f, f, (x, mode), (x, mode))
                else:
                    fl, fh, wl, wh = local[b]
                    local[b] = (min(fl, f), max(fh, f),
                                (x, mode) if f < fl else wl,
                                (x, mode) if f > fh else wh)
        new_low, new_high, ptr_low, ptr_high = {}, {}, {}, {}
        for state, updated, pointers, minimize in (
                (low, new_low, ptr_low, True), (high, new_high, ptr_high, False)):
            for s, value in state.items():
                for t, (fl, fh, wl, wh) in local.items():
                    b = s ^ t
                    candidate = value + (fl if minimize else fh)
                    if b not in updated or (candidate < updated[b] if minimize else candidate > updated[b]):
                        updated[b] = candidate
                        pointers[b] = (s, wl if minimize else wh)
        low_trace.append(ptr_low)
        high_trace.append(ptr_high)
        low, high = new_low, new_high

    pmin = min(low, key=lambda b: parity_terminal(low[b], b, outer))
    pmax = max(high, key=lambda b: parity_terminal(high[b], b, outer))

    def reconstruct(b, traces):
        chosen = []
        for pointer in reversed(traces):
            b, witness = pointer[b]
            chosen.append(witness)
        assert b == 0
        return list(reversed(chosen))

    return dict(minimum=parity_terminal(low[pmin], pmin, outer),
                maximum=parity_terminal(high[pmax], pmax, outer),
                minimum_witness=reconstruct(pmin, low_trace),
                maximum_witness=reconstruct(pmax, high_trace),
                periods=periods, representative_counts=counts, states=len(low))


def independent_witness_value(a, c, bounds, choices, outer, witness):
    """Replay only exact rational affine forms and integer rounding definitions."""
    total, lines = F(0), 0
    assert len(witness) == len(a)
    for ai, ci, (lo, hi), options, (x, mode) in zip(a, c, bounds, choices, witness):
        assert isinstance(x, int) and lo <= x <= hi and mode in options
        y = ai * x + ci
        total += y
        lines += independent_round(y, mode)
    return independent_round(total, outer) - lines


def parity_checks(nonnegative=False):
    seed = 1003202601 if not nonnegative else 1003202602
    rng = random.Random(seed)
    assignments = 0
    for trial in range(160):
        n = rng.randint(1, 4)
        a = [F(rng.randint(-7, 7), rng.randint(1, 7)) for _ in range(n)]
        c = [F(rng.randint(-7, 7), rng.randint(1, 7)) for _ in range(n)]
        bounds = [(rng.randint(-5, 0), rng.randint(1, 5)) for _ in range(n)]
        bounds = [(lo, min(hi, lo + rng.randint(0, 4))) for lo, hi in bounds]
        if nonnegative:
            c = [ci - min(ai * lo + ci, ai * hi + ci)
                 + F(rng.randint(0, 4), rng.randint(1, 7))
                 for ai, ci, (lo, hi) in zip(a, c, bounds)]
        modes = ALL_MODES if nonnegative else COVARIANT
        choices = [rng.sample(modes, rng.randint(1, 2)) for _ in range(n)]
        outer = rng.choice(modes)
        observed = direct_values(a, c, bounds, choices, outer)
        expected = min(observed), max(observed)
        got = independent_parity_dp(a, c, bounds, choices, outer)
        assert (got["minimum"], got["maximum"]) == expected, (nonnegative, trial)
        assert independent_dp(a, c, bounds, choices, outer) == expected, (nonnegative, trial)
        for endpoint in ("minimum", "maximum"):
            assert independent_witness_value(a, c, bounds, choices, outer,
                                             got[endpoint + "_witness"]) == got[endpoint]
        assert got["states"] <= 2
        assignments += len(observed)
    return dict(random_seed=seed, cases=160, brute_force_assignments=assignments,
                parity_cyclic_brute_extrema_matched=True,
                both_endpoint_witnesses_in_original_domain_and_replayed=True,
                independent_mixed_integer_output_choices=True,
                nonterminating_rational_coefficients_included=True,
                raw_line_nonnegativity_certified=nonnegative)


def parity_regressions():
    cases = [
        # Equal residual sum, unequal integer phase: HALF_EVEN needs parity.
        ("phase_even", [F(0)], [F(1, 2)], [["floor"]], "he", F(0)),
        ("phase_odd", [F(0)], [F(3, 2)], [["floor"]], "he", F(1)),
        ("homogeneous_phase_even", [F(0), F(0)], [F(1, 4), F(1, 4)],
         [["he"], ["he"]], "he", F(0)),
        ("homogeneous_phase_odd", [F(0), F(0)], [F(5, 4), F(1, 4)],
         [["he"], ["he"]], "he", F(1)),
        # Positive raw values can have negative residuals; terminal extension matters.
        ("negative_half_up_residual", [F(0)], [F(1, 2)], [["half_up"]], "half_up", F(0)),
        ("negative_up_residual", [F(0)], [F(2, 5)], [["up"]], "up", F(0)),
        ("negative_down_terminal", [F(0)], [F(2, 5)], [["up"]], "down", F(-1)),
        ("odd_half_even_five", [F(0)] * 5, [F(1, 2)] * 5, [["he"]] * 5, "he", F(2)),
        ("negative_integer_phase", [F(0)], [F(-1, 2)], [["floor"]], "he", F(1)),
    ]
    for name, a, c, choices, outer, expected in cases:
        got = independent_parity_dp(a, c, [(0, 0)] * len(a), choices, outer)
        assert got["minimum"] == got["maximum"] == expected, (name, got, expected)
    try:
        independent_parity_dp([F(0)], [F(1, 2)], [(0, 0)], [["id"]], "he")
    except ValueError:
        pass
    else:
        raise AssertionError("Noninteger IDENTITY must not enter parity compression")
    try:
        independent_parity_dp([F(1)], [F(0)], [(-1, 1)], [["half_up"]], "half_up")
    except ValueError:
        pass
    else:
        raise AssertionError("Signed HALF_UP raw domain requires fallback")
    return dict(cases=[row[0] for row in cases], identity_premise_rejected=True,
                uncertified_signed_raw_domain_rejected=True, all_passed=True)


def half_even_bounds():
    pool = [F(k, 4) for k in range(-3, 4)]
    local = [independent_round(v, "he") for v in pool]
    report = []
    for n in range(1, 7):
        maximum = 0
        for indices in itertools.product(range(len(pool)), repeat=n):
            delta = sum(local[i] for i in indices) - independent_round(
                sum((pool[i] for i in indices), F(0)), "he"
            )
            maximum = max(maximum, abs(delta))
        sharp = independent_round(F(n, 2), "he")
        assert maximum == sharp, (n, maximum, sharp)
        report.append(dict(n=n, tuples=len(pool) ** n, observed_maximum=maximum, formula=sharp))
    return report


def general_dp_checks():
    rng = random.Random(20261003)
    assignments = 0
    for trial in range(120):
        n = rng.randint(1, 4)
        a = [F(rng.randint(-5, 5), rng.randint(1, 6)) for _ in range(n)]
        c = [F(rng.randint(-5, 5), rng.randint(1, 6)) for _ in range(n)]
        bounds = [(rng.randint(-4, 1), rng.randint(1, 4)) for _ in range(n)]
        bounds = [(lo, min(hi, lo + 3)) for lo, hi in bounds]
        choices = [rng.sample(COVARIANT + ["id"], rng.randint(1, 2)) for _ in range(n)]
        outer = rng.choice(COVARIANT)
        observed = direct_values(a, c, bounds, choices, outer)
        assert independent_dp(a, c, bounds, choices, outer) == (min(observed), max(observed)), trial
        assignments += len(observed)
    return dict(random_seed=20261003, cases=120, brute_force_assignments=assignments,
                all_extrema_matched=True, dimensions="1 through 4",
                modes=["FLOOR", "CEILING", "HALF_EVEN", "IDENTITY"],
                includes_negative_coefficients_and_signed_inputs=True)


def nonnegative_dp_checks():
    rng = random.Random(6102026)
    assignments = 0
    for trial in range(120):
        n = rng.randint(1, 4)
        a = [F(rng.randint(-5, 5), rng.randint(1, 6)) for _ in range(n)]
        bounds = [(rng.randint(-4, 1), rng.randint(1, 4)) for _ in range(n)]
        bounds = [(lo, min(hi, lo + 3)) for lo, hi in bounds]
        c = [F(rng.randint(0, 5), rng.randint(1, 6)) - min(ai * lo, ai * hi)
             for ai, (lo, hi) in zip(a, bounds)]
        assert all(min(ai * lo + ci, ai * hi + ci) >= 0
                   for ai, ci, (lo, hi) in zip(a, c, bounds))
        choices = [rng.sample(ALL_MODES + ["id"], rng.randint(1, 2)) for _ in range(n)]
        outer = rng.choice(ALL_MODES)
        observed = direct_values(a, c, bounds, choices, outer)
        assert independent_dp(a, c, bounds, choices, outer) == (min(observed), max(observed)), trial
        assignments += len(observed)
    return dict(random_seed=6102026, cases=120, brute_force_assignments=assignments,
                all_extrema_matched=True, raw_line_nonnegativity_certified=True,
                includes_all_six_modes_and_identity=True,
                includes_negative_slopes_and_signed_input_ticks=True)


def implementation_checks(nonnegative=False):
    sys.path.insert(0, str(ROOT / "src"))
    from roundguard.model import Rule, Variable, Node, parse, add_nodes
    from roundguard.analysis import dp_batch, cyclic_batch
    from roundguard.semantics import evaluate, tick_env

    seed = 3102026 if not nonnegative else 33102026
    rng = random.Random(seed)
    assignments = 0
    names_by_mode = {"floor": "FLOOR", "ceil": "CEILING", "he": "HALF_EVEN",
                     "half_up": "HALF_UP", "down": "DOWN", "up": "UP"}
    for case in range(80):
        n = rng.randint(1, 4)
        names = [f"x{i}" for i in range(n)]
        vs = [Variable(name, rng.randint(-5, 0), rng.randint(1, 3),
                       rng.choice([F(1, 4), F(1, 2), F(1), F(2)])) for name in names]
        vs = [Variable(v.name, v.lo, min(v.hi, v.lo + 3), v.quantum) for v in vs]
        q = rng.choice([F(1, 2), F(1), F(2)])
        key = rng.choice(ALL_MODES if nonnegative else COVARIANT)
        mode = names_by_mode[key]
        a = [F(rng.randint(-4, 4), rng.choice([1, 2, 4])) for _ in names]
        c = [F(rng.randint(0 if nonnegative else -4, 4), rng.choice([1, 2, 4])) for _ in names]
        if nonnegative:
            c = [ci - min(ai * v.quantum * v.lo, ai * v.quantum * v.hi)
                 for ai, ci, v in zip(a, c, vs)]
        raw = [f"rat({ai.numerator},{ai.denominator})*{name}+rat({ci.numerator},{ci.denominator})"
               for name, ai, ci in zip(names, a, c)]
        if case % 9 == 0:
            raw.append("rat(3,4)" if nonnegative else "rat(-3,4)")
        es = [parse(s, set(names)) for s in raw]
        variants = {"per_line": add_nodes([Node("round", (e,), (q, mode)) for e in es]),
                    "total": Node("round", (add_nodes(es),), (q, mode))}
        rule = Rule(f"audit_{case}", vs, variants, {}, dict(lines=raw, quantum=str(q), mode=mode))
        # Independent oracle uses affine forms and direct integer/remainder rounding.
        physical_a = [ai * v.quantum / q for ai, v in zip(a, vs)]
        normalized_c = [ci / q for ci in c]
        normalized_bounds = [(v.lo, v.hi) for v in vs]
        if case % 9 == 0:
            physical_a.append(F(0))
            normalized_c.append(F(3 if nonnegative else -3, 4) / q)
            normalized_bounds.append((0, 0))
        observed = [q * z for z in direct_values(physical_a, normalized_c, normalized_bounds,
                                               [[key]] * len(physical_a), key)]
        assignments += len(observed)
        for method in (dp_batch, cyclic_batch):
            got = method(rule)
            assert (F(got["minimum_signed"]), F(got["maximum_signed"])) == (min(observed), max(observed)), (method.__name__, case)
            assert F(got["maximum_discrepancy"]) == max(abs(min(observed)), abs(max(observed)))
            if method is dp_batch:
                assert got["local_periods"] == [(ai / 2).denominator for ai in physical_a]
                assert got["local_representatives"] == sum(
                    min((ai / 2).denominator, hi - lo + 1)
                    for ai, (lo, hi) in zip(physical_a, normalized_bounds))
                assert got["active_states"] <= 2
                # Audit both signed endpoint witnesses against this independent oracle.
                for endpoint in ("minimum", "maximum"):
                    witness = got[endpoint + "_counterexample"]
                    assert all(isinstance(witness[v.name], int) and v.lo <= witness[v.name] <= v.hi for v in vs)
                    chosen = [(witness[name], key) for name in names]
                    if case % 9 == 0:
                        chosen.append((0, key))
                    replay = q * independent_witness_value(
                        physical_a, normalized_c, normalized_bounds,
                        [[key]] * len(physical_a), key, chosen)
                    assert replay == F(got[endpoint + "_signed"]), (endpoint, case)
            witness = got.get("counterexample")
            if witness:
                assert all(v.lo <= witness[v.name] <= v.hi for v in vs)
                env = tick_env(rule, witness)
                assert abs(evaluate(variants["total"], env) - evaluate(variants["per_line"], env)) == F(got["maximum_discrepancy"])
    return dict(random_seed=seed, cases=80, direct_assignments=assignments,
                all_signed_extrema_matched=True, nonunit_input_and_output_quantum=True,
                negative_slopes=True, signed_input_ticks=True, negative_constants=not nonnegative,
                constant_lines=True, raw_line_nonnegativity_certified=nonnegative,
                algorithms=["parity-dp", "cyclic-dp"],
                both_parity_signed_endpoint_witnesses_independently_replayed=True,
                parity_local_period_and_representative_counts_checked=True)


def coprime_parity_checks(implementation=False):
    """Joint lcm and offset denominators must not govern parity enumeration.

    For the large-domain cases, elementary residual envelopes plus attained
    endpoint witnesses supply the expected optimum, without a product oracle.
    """
    primes = [17, 19, 23, 29, 31, 37, 41, 43]
    report = []
    for n in (4, 8):
        a, c = [F(1, p) for p in primes[:n]], [F(0)] * n
        bounds = [(0, 10**9)] * n
        got = independent_parity_dp(a, c, bounds, [["he"]] * n, "he")
        # |F| <= n/2, and |HE(K+F)-K| <= |F|+1/2; the
        # integral discrepancy is therefore at most n/2 for these even n.
        bound = n // 2
        assert got["minimum"] == -bound and got["maximum"] == bound
        for endpoint in ("minimum", "maximum"):
            assert independent_witness_value(a, c, bounds, [["he"]] * n, "he",
                                             got[endpoint + "_witness"]) == got[endpoint]
        joint_modulus = 2 * lcm(*primes[:n])
        report.append(dict(lines=n, joint_cyclic_modulus=joint_modulus,
                           local_periods=got["periods"],
                           representatives=sum(got["representative_counts"]),
                           exact_maximum_absolute_discrepancy=bound,
                           independent_envelope_and_attained_witness_certificate=True))
    # Offset denominators do not enter safe periods, even with signed raw values.
    a, c, bounds = [F(1, 17), F(-1, 19)], [F(1, 1009), F(-1, 1013)], [(-2, 3), (-3, 2)]
    got = independent_parity_dp(a, c, bounds, [["he"], ["he"]], "he")
    observed = direct_values(a, c, bounds, [["he"], ["he"]], "he")
    assert (got["minimum"], got["maximum"]) == (min(observed), max(observed))
    assert got["periods"] == [34, 38] and got["representative_counts"] == [6, 6]
    large_offset = dict(offset_denominators=[1009, 1013], local_periods=got["periods"],
                        representatives=12, brute_force_assignments=len(observed), all_extrema_matched=True)
    if implementation:
        sys.path.insert(0, str(ROOT / "src"))
        from roundguard.model import Rule, Variable, Node, parse, add_nodes
        from roundguard.analysis import dp_batch, cyclic_batch, NotCertified

        def make_rule(slopes, offsets, intervals):
            names = [f"x{i}" for i in range(len(slopes))]
            variables = [Variable(name, lo, hi, F(1)) for name, (lo, hi) in zip(names, intervals)]
            raw = [f"rat({ai.numerator},{ai.denominator})*{name}+rat({ci.numerator},{ci.denominator})"
                   for name, ai, ci in zip(names, slopes, offsets)]
            expressions = [parse(s, set(names)) for s in raw]
            variants = {"per_line": add_nodes([Node("round", (e,), (F(1), "HALF_EVEN")) for e in expressions]),
                        "total": Node("round", (add_nodes(expressions),), (F(1), "HALF_EVEN"))}
            return Rule("coprime_audit", variables, variants, {},
                        dict(lines=raw, quantum="1", mode="HALF_EVEN"))

        cases = [([F(1, p) for p in primes[:row["lines"]]], [F(0)] * row["lines"],
                  [(0, 10**9)] * row["lines"], (-row["lines"] // 2, row["lines"] // 2))
                 for row in report]
        cases.append((a, c, bounds, (min(observed), max(observed))))
        for slopes, offsets, intervals, expected in cases:
            rule = make_rule(slopes, offsets, intervals)
            actual = dp_batch(rule)
            assert (F(actual["minimum_signed"]), F(actual["maximum_signed"])) == expected
            assert actual["local_periods"] == [(v / 2).denominator for v in slopes]
            for endpoint in ("minimum", "maximum"):
                w = [(actual[endpoint + "_counterexample"][f"x{i}"], "he") for i in range(len(slopes))]
                assert independent_witness_value(slopes, offsets, intervals, [["he"]] * len(slopes),
                                                 "he", w) == F(actual[endpoint + "_signed"])
            try:
                cyclic_batch(rule)
            except NotCertified:
                pass
            else:
                raise AssertionError("The retained cyclic cap should reject this joint denominator")
        large_offset["implementation_parity_succeeded_while_cyclic_budget_rejected"] = True
        for row in report:
            row["implementation_parity_endpoints_and_witnesses_matched"] = True
    return dict(coprime_large_domains=report, large_offset_denominators=large_offset)


def quantum_input_guard_checks():
    sys.path.insert(0, str(ROOT / "src"))
    from roundguard.model import load_rule

    reports = []
    for field in ("input", "batch"):
        request = dict(name="decimal_quantum_audit", variables={"x": dict(min=10, max=10)},
                       variants={"a": 'Q(x,1,"CEILING")', "b": "1"})
        if field == "input":
            request["variables"]["x"]["quantum"] = 0.1
        else:
            request["batch"] = dict(lines=["1"], quantum=0.1, mode="FLOOR")
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "r.json"
            path.write_text(json.dumps(request), encoding="utf-8")
            try:
                rule = load_rule(path)
            except ValueError:
                reports.append(dict(field=field, numeric_decimal="rejected"))
            else:
                value = rule.variables[0].quantum if field == "input" else rule.variants["total"].value[0]
                assert value == F(1, 10), (field, value)
                reports.append(dict(field=field, numeric_decimal="parsed as exact 1/10"))
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation", action="store_true")
    args = parser.parse_args()
    report = dict(date="2026-10-03", status="BOUNDED_SANITY_CHECKS_ONLY",
                  proof_assistant_checked=False, half_even_aggregation=half_even_bounds(),
                  residue_dp=general_dp_checks(), nonnegative_residue_dp=nonnegative_dp_checks(),
                  parity_signed_core=parity_checks(),
                  parity_nonnegative_six_modes=parity_checks(nonnegative=True),
                  parity_phase_and_signed_residual_regressions=parity_regressions())
    if args.implementation:
        report["implementation_signed_covariant"] = implementation_checks()
        report["implementation_nonnegative_six_modes"] = implementation_checks(nonnegative=True)
        report["quantum_input_guard"] = quantum_input_guard_checks()
    else:
        report["implementation_checks"] = "not requested; use --implementation"
    report["parity_coprime_and_offset_denominators"] = coprime_parity_checks(args.implementation)
    output = ROOT / "proofs" / "sanity_checks.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
