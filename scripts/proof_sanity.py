"""Reproducible finite sanity checks accompanying proofs/theorems.md.

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
    from roundguard.analysis import dp_batch
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
        got = dp_batch(rule)
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
        assert (F(got["minimum_signed"]), F(got["maximum_signed"])) == (min(observed), max(observed)), case
        assignments += len(observed)
        witness = got.get("counterexample")
        if witness:
            assert all(v.lo <= witness[v.name] <= v.hi for v in vs)
            env = tick_env(rule, witness)
            assert abs(evaluate(variants["total"], env) - evaluate(variants["per_line"], env)) == F(got["maximum_discrepancy"])
    return dict(random_seed=seed, cases=80, direct_assignments=assignments,
                all_signed_extrema_matched=True, nonunit_input_and_output_quantum=True,
                negative_slopes=True, signed_input_ticks=True, negative_constants=not nonnegative,
                constant_lines=True, raw_line_nonnegativity_certified=nonnegative)


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
                  residue_dp=general_dp_checks(), nonnegative_residue_dp=nonnegative_dp_checks())
    if args.implementation:
        report["implementation_signed_covariant"] = implementation_checks()
        report["implementation_nonnegative_six_modes"] = implementation_checks(nonnegative=True)
        report["quantum_input_guard"] = quantum_input_guard_checks()
    else:
        report["implementation_checks"] = "not requested; use --implementation"
    output = ROOT / "proofs" / "sanity_checks.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
