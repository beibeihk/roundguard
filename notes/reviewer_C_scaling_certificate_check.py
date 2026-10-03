"""Independent audit of saved scaling/denominator certificates; no RoundGuard imports.

This reconstructs local envelopes and replays saved witnesses with a separate
integer implementation of nonnegative nearest-even rounding. It does not rerun
the solver or certify an arbitrary benchmark parser.
"""
import csv
import hashlib
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
    records = []
    sources = []
    for family, name in [("scaling", "scaling_ground_truth.json"),
                         ("denominators", "denominator_ground_truth.json")]:
        path = ROOT / "results" / name
        sources.append(path)
        records += [(family, record) for record in json.loads(path.read_text())]
    checked = []
    for family, record in records:
        path = ROOT / "benchmarks" / family / (record["case"] + ".json")
        sources.append(path)
        rule = json.loads(path.read_text())
        assert rule["batch"]["mode"] == "HALF_EVEN"
        raw, rounded = [], []
        lower, upper = Fraction(0), Fraction(0)
        periods = []
        for line in rule["batch"]["lines"]:
            match = re.fullmatch(r"(x\d+)/(\d+)", line)
            assert match, line
            name, denominator = match.group(1), int(match.group(2))
            bounds = rule["variables"][name]
            assert bounds["min"] >= 0 and bounds["quantum"] == "1"
            # Shifting x by 2d moves x/d by an even integer.
            period = 2 * denominator
            periods.append(period)
            local = [Fraction(nearest_even(Fraction(x, denominator))) -
                     Fraction(x, denominator)
                     for x in range(bounds["min"], bounds["min"] +
                                    min(bounds["max"] - bounds["min"] + 1, period))]
            # The older scaling certificates store rounding-minus-raw errors;
            # denominator certificates store raw-minus-rounding residuals.
            # Both conventions give the same absolute envelope and replay.
            if family == "denominators":
                local = [-value for value in local]
            lower += min(local)
            upper += max(local)
            tick = record["counterexample"][name]
            assert type(tick) is int and bounds["min"] <= tick <= bounds["max"]
            value = Fraction(tick, denominator)
            raw.append(value)
            rounded.append(nearest_even(value))
        assert set(record["counterexample"]) == set(rule["variables"])
        envelope = max(-lower, upper) + Fraction(1, 2)
        integral_bound = envelope.numerator // envelope.denominator
        attained = abs(nearest_even(sum(raw)) - sum(rounded))
        assert lower == Fraction(record["local_lower"]), record["case"]
        assert upper == Fraction(record["local_upper"]), record["case"]
        assert integral_bound == Fraction(record["integral_upper_bound"])
        assert attained == integral_bound == Fraction(record["ground_truth"])
        universal = nearest_even(Fraction(len(raw), 2))
        checked.append(dict(case=record["case"], family=family, local_periods=sorted(set(periods)),
                            local_sign_convention=("raw-minus-rounded" if family == "denominators"
                                                   else "rounded-minus-raw"),
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
                  review_phase="final parity release",
                  roundguard_imports=False,
                  scaling_cases=sum(row["family"] == "scaling" for row in checked),
                  denominator_cases=sum(row["family"] == "denominators" for row in checked),
                  witness_and_bound_mismatches=[],
                  universal_strict_gap_cases=sum(row["family"] == "scaling" and
                                                 row["universal_gap"] > 0 for row in checked),
                  effectiveness_assignments=sum(int(row["domain_size"]) for row in auto),
                  group_counts={group: dict(cases=sum(r["group"] == group for r in auto),
                      sensitive=sum(r["group"] == group and r["truth"] == "SENSITIVE" for r in auto))
                      for group in sorted({r["group"] for r in auto})},
                  auto_dispatch=dict(dispatch), cases=checked,
                  source_sha256={str(path.relative_to(ROOT)).replace("\\", "/"):
                                 hashlib.sha256(path.read_bytes()).hexdigest() for path in sources})
    path = ROOT / "notes/reviewer_C_scaling_certificate_check.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items()
                      if key not in {"cases", "source_sha256"}}, indent=2))


if __name__ == "__main__":
    main()
