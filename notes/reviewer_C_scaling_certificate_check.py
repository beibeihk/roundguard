"""Independent audit of the saved scaling family; no RoundGuard imports.

This reconstructs local envelopes and replays saved witnesses with a separate
integer implementation of nonnegative nearest-even rounding. It does not rerun
the solver or certify an arbitrary benchmark parser.
"""
import csv
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def nearest_even(value):
    assert value >= 0
    quotient, remainder = divmod(value.numerator, value.denominator)
    twice = 2 * remainder
    return quotient + int(twice > value.denominator or
                          (twice == value.denominator and quotient % 2))


def main():
    records = json.loads((ROOT / "results/scaling_ground_truth.json").read_text())
    checked = []
    for record in records:
        rule = json.loads((ROOT / "benchmarks/scaling" /
                           (record["case"] + ".json")).read_text())
        assert rule["batch"]["mode"] == "HALF_EVEN"
        raw, rounded = [], []
        lower, upper = Fraction(0), Fraction(0)
        periods = []
        for line in rule["batch"]["lines"]:
            match = re.fullmatch(r"(x\d+)/(\d+)", line)
            assert match, line
            name, denominator = match.group(1), int(match.group(2))
            bounds = rule["variables"][name]
            assert bounds["min"] == 0 and bounds["quantum"] == "1"
            # Shifting x by 2d moves x/d by an even integer.
            period = 2 * denominator
            periods.append(period)
            local = [Fraction(nearest_even(Fraction(x, denominator))) -
                     Fraction(x, denominator)
                     for x in range(min(bounds["max"] + 1, period))]
            lower += min(local)
            upper += max(local)
            tick = record["counterexample"][name]
            assert type(tick) is int and 0 <= tick <= bounds["max"]
            value = Fraction(tick, denominator)
            raw.append(value)
            rounded.append(nearest_even(value))
        assert set(record["counterexample"]) == set(rule["variables"])
        envelope = max(-lower, upper) + Fraction(1, 2)
        integral_bound = envelope.numerator // envelope.denominator
        attained = abs(nearest_even(sum(raw)) - sum(rounded))
        assert lower == Fraction(record["local_lower"])
        assert upper == Fraction(record["local_upper"])
        assert integral_bound == Fraction(record["integral_upper_bound"])
        assert attained == integral_bound == Fraction(record["ground_truth"])
        universal = nearest_even(Fraction(len(raw), 2))
        checked.append(dict(case=record["case"], local_periods=sorted(set(periods)),
                            independently_replayed=attained,
                            integral_upper_bound=integral_bound,
                            universal_bound=universal,
                            universal_gap=universal - attained))
    accuracy = list(csv.DictReader((ROOT / "results/accuracy.csv").open()))
    auto = [row for row in accuracy if row["method"] == "auto"]
    diagnostic = json.loads((ROOT / "results/diagnostics.json").read_text())
    dispatch = Counter(row["result"]["method"] for row in diagnostic
                       if row["method"] == "auto")
    report = dict(review_date="2026-10-03", solver_reexecution=False,
                  roundguard_imports=False, scaling_cases=len(checked),
                  witness_and_bound_mismatches=[],
                  universal_strict_gap_cases=sum(row["universal_gap"] > 0 for row in checked),
                  effectiveness_assignments=sum(int(row["domain_size"]) for row in auto),
                  group_counts={group: dict(cases=sum(r["group"] == group for r in auto),
                      sensitive=sum(r["group"] == group and r["truth"] == "SENSITIVE" for r in auto))
                      for group in sorted({r["group"] for r in auto})},
                  auto_dispatch=dict(dispatch), cases=checked)
    path = ROOT / "notes/reviewer_C_scaling_certificate_check.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "cases"}, indent=2))


if __name__ == "__main__":
    main()
