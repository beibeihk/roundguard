"""Persist a sentence-level, primary-source-scoped review of used citations.

Descriptions below are reviewer judgments from the inspected primary portions,
not an automated inference from keyword matches. Unused audit rows are preserved.
"""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = {
    "hmrc_vat": "PASS: Sections 17.5-17.6 support the introduction's line/final VAT stages and the fragment's tenth-penny line and final-penny motivation. Trader conditions and the chosen 20% rate/window remain explicit benchmark assumptions; the citation does not certify either alternative's legal applicability.",
    "irs_p15": "PASS: Section 13 supports individual-payroll rounding differences and fractions-of-cents adjustments, with separate 6.2% and 1.45% employee-side rates. The manuscript labels the combined-rate comparison counterfactual and omits caps/additional taxes/reporting adjustments; no claim of a complete payroll calculator is supported.",
    "ssa_rounding": "PASS: POMS RS00601.020 Sections A-D support distinct cent/dime/dollar stages and certain entitlement comparisons before lower-dollar rounding. The manuscript distinguishes illustrative factors/offsets/thresholds from an implemented statutory benefit formula.",
    "fluctuat2011": "PASS: Primary text explicitly includes implemented fixed-point analysis and absolute rounding-error abstraction (Section 2), as well as finite-precision error analysis. It supports both cited source-description sentences; it does not imply exact attainable optima or a RoundGuard proof.",
    "daisy2018": "PASS: Tool paper Section 3 supports finite-precision/fixed-point analysis and sound error-estimation/optimization descriptions in introduction and Related work. Conservative real-semantics accuracy analysis is correctly distinguished from attained monetary-policy discrepancy.",
    "fptaylor2015": "PASS: Section 3 and certificate passages support rigorous roundoff bounds via symbolic Taylor error modeling and rigorous optimization. The Related work describes bounds/certificates without claiming that FPTaylor supplies exact monetary-grid extrema.",
    "catala2021": "PASS: Sections 4.2, 4.5 and 5 support executable legal specifications, default semantics and F*-proved core compiler transformations. The wording 'semantics and verified compilation' is a source description; it does not certify all backends or this artifact.",
    "date2024": "PASS: The paired-rounding relational analysis and semantic properties support insensitivity to alternative calendar rounding in qualifying cases and its relational formulation. The manuscript accurately presents this as prior art rather than a monetary extrema algorithm.",
    "cutecat2025": "PASS: Sections 2-4 support exact rational monetary values, sign-aware nearest ties-away Z3 encoding, concolic tests and a reported Python backend rounding discrepancy. The manuscript's fallback/motivation attribution is supported; no Catala integration or global-optimum result is attributed to CUTECat.",
    "williams2011": "PASS: Author working-paper pp.21-23 show nested Chvatal rounded trees, affine average gradient and explicit shift periodicity. Both foundation citations are appropriately scoped; the manuscript explicitly disclaims new general periodicity.",
    "basu_et_al2019": "PASS: Definition 2.2 and Section 3 formalize rational affine Chvatal binary trees and mixed-integer representability/elimination. These support the foundation and Related work statements, without asserting the proposed heterogeneous-mode invoice DP is present in that source.",
    "verdoolaege2010": "PASS WITH READING LIMIT: Conference abstract plus official manual Section 1.4.13 support exact integer-set infrastructure and quasi-affine expressions with integer division. These support the two library/foundation descriptions; the current manual is distinct from a full reading of the 2010 conference paper.",
    "z32008": "PASS: The four-page tool paper identifies Z3 and its SMT architecture, supporting the solver citation. The manuscript's own integer/rational/tie/parity encoding requires its separate proof and implementation evidence; this source alone does not validate that encoding or current optimization APIs.",
    "cra_cash": "PASS: Official GI-131 states cash nickel rounding after taxes and unchanged GST/HST calculations. The manuscript properly labels early per-component rounding as an intentionally compared alternative, not Canadian policy.",
    "brick_money": "PASS: Maintained README RationalMoney and context sections support exact rational intermediates/deferred rounding and consequences of early rounding. The manuscript declares independently chosen rates and no copied external implementation; no Brick bug or tested adapter is claimed.",
    "skala2017": "PASS: Author PDF introduction supports financial line-versus-total motivation; Section 2 Problem 1/Lemma 2 fixes labels and seeks consistent rounded totals; Section 3 Problem 3/Theorem 4 optimizes maximum node error. The closing author note explicitly disclaims peer review. The objective distinction and rejection as a same-task runtime baseline are valid reviewer inferences.",
    "woods2015": "PASS WITH READING LIMIT: Abstract and foundational definitions support the broad structural treatment of Presburger integer sets/functions, generating functions and counting. The single cited sentence is general and does not rely on unread proof details or attribute the invoice algorithm to this paper.",
    "bringmann_cassis2023": "PASS WITH READING LIMIT: Primary publisher contribution summary supports near-convex min-plus convolution for structured 0-1 knapsack. The manuscript explicitly notes those extra premises need not hold for cyclic residue tables, avoiding an unsupported complexity transfer.",
    "sadakane2001": "PASS WITH READING LIMIT: Publisher abstract and accessible Sections 3-4 excerpt support compact rounding-state graphs and optimization for fixed real sequences. The manuscript correctly distinguishes choosing outputs for fixed data from searching inputs under fixed policies.",
    "gappa2010": "PASS: Sections 2-3 support explicit rounded operators, interval/rewriting bounds and proof-assistant-checkable certificates. The cited sentence describes sound numerical analysis/certificates, without equating certified enclosures with attained monetary extrema.",
    "fixedpoint2013": "PASS WITH READING LIMIT: Primary abstract/problem formulation support fixed-point synthesis and accuracy analysis. Only that limited source-description claim is cited; SSL-limited PDF access is not represented as a full-paper reading.",
    "flocq2011": "PASS: Section III generic formats/rounding predicates support foundational arithmetic proofs in Coq. The manuscript does not claim its own proof is mechanized or automatically follows from Flocq.",
    "herbie2015": "PASS: Sections 4.1-4.3 explicitly use sampled high-precision accuracy estimates, error localization and expression rewriting. The manuscript's description correctly distinguishes heuristic search from guaranteed worst-case policy extrema.",
    "robust2013": "PASS: Long-version Sections 2-3 and 5 treat unstable tests/branch discontinuities through constrained affine sets and discontinuity errors. The cited sentence supports robustness analysis of discontinuous branch changes; published short version and inspected longer primary version are distinguished in the ledger.",
    "codinglaws2026": "PASS: Recommendations 9-10 explicitly advocate arbitrary-precision monetary representation and rigorous lawyer-reviewed test suites. The cited general recommendation sentence is supported; it does not attribute a residue theorem or analyzer to this recommendations article.",
    "fpbench2017": "PASS: Sections 2-3 and 5 support explicit numerical benchmark semantics, measures and provenance for auditable tool comparisons. The manuscript expressly separates its monetary JSON suite from FPBench, avoiding an unsupported extension claim.",
}


def main():
    source_bytes = (ROOT / "paper/main.tex").read_bytes()
    source = source_bytes.decode("utf-8")
    occurrences = {}
    for number, line in enumerate(source.splitlines(), 1):
        for citation in re.findall(r"\\cite\w*\{([^}]+)\}", line):
            for key in citation.split(","):
                occurrences.setdefault(key.strip(), []).append(dict(line=number, text=line))
    assert set(occurrences) == set(CLAIMS), (set(occurrences)-set(CLAIMS), set(CLAIMS)-set(occurrences))
    path = ROOT / "literature/reference_audit.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        rows = list(reader)
    report = []
    for row in rows:
        key = row["citation_key"]
        if key in occurrences:
            lines = ",".join(str(item["line"]) for item in occurrences[key])
            row["manuscript_alignment"] = "Reviewed 2026-10-03 main.tex lines " + lines + ". " + CLAIMS[key]
            report.append(dict(citation_key=key, judgment=CLAIMS[key], occurrences=occurrences[key],
                               reading_depth=row["reading_depth"], supported_claim=row["supported_claim"]))
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    result = dict(review_date="2026-10-03", main_sha256=hashlib.sha256(source_bytes).hexdigest(),
                  used_keys=len(occurrences), unresolved_alignment_items=[], citations=report)
    (ROOT / "notes/reviewer_C_citation_alignment.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(dict(used_keys=len(occurrences), updated_rows=len(report),
                         unused_rows_preserved=len(rows)-len(report))))


if __name__ == "__main__":
    main()
