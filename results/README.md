# Result records

All records come from executed scripts. Exact numerical strings are reduced rational values in each rule's declared output units (cents in the published monetary fragments). Wall times and solver completion depend on the machine and scheduling.

| File | Meaning |
|---|---|
| ground_truth.json | Exhaustive independent Decimal labels, attained maximum, first attaining tick input and evaluated assignment count for 66 small programs. |
| diagnostics.json | Every method's returned result on those programs, including concrete policy outputs and any completion indicator. |
| accuracy.csv | One row per program/method; false-warning/missed counts, UNKNOWN, time, domain size, variables, AST node counts and oracle time. |
| benchmark_profile.csv | Program composition and root-to-leaf AST depth, counting repeated nodes separately across variants. |
| summary.json | Grouped method counts and median time across the heterogeneous small corpus; timings are single runs per case/method. |
| scaling.csv | 24 cases × 4 methods × 3 repetitions. `complete=True` establishes an exact optimum. SENSITIVE without completion is a witnessed disagreement with an unresolved maximum; UNKNOWN establishes neither detection nor equivalence. |
| scaling_ground_truth.json | Independent local Decimal error bounds, integer upper bound and feasible attaining replay witness for all 24 scaling maxima. |
| denominators.csv | Six cases × four methods × three repetitions. Coprime denominators or large individual periods with narrow feasible windows. Cyclic rejection is its implementation cap, not a runtime failure. |
| denominator_ground_truth.json | Independent integer quotient/remainder local residual bounds and attaining witness replay for six nonterminating-rational cases. |
| paper_facts.json | Generated summaries and manuscript macros. |
| environment.json | Seed, measured runtime/package versions, system description and per-check solver timeout. |
| integrity_audit.json | Executed consistency checks and source/data hashes; not a general software verification or exhaustive novelty proof. |
| latex_build.json | Final log/font checks. |

`exact_truth` is independently certified in the corresponding ground-truth file; the DP value alone is not the oracle. `parity_states` and `local_representatives` describe the new sufficient-state method; `cyclic_states` describes the larger ablation. `transitions` is method-specific and empty for SMT. `universal_bound` is the unrestricted nearest-even aggregation envelope; `bound_gap` subtracts the exact grid-specific maximum. The independent scaling envelope is tight in these 24 saved cases, not guaranteed for every program.

Naive interval warnings can be false positives because each variant loses input correlation. Random/Hypothesis misses are failure to find a witness, not proofs of safety. Hypothesis's `max_examples=64` is a configuration parameter, with additional shrinking behavior; it is not an equal strict evaluation or wall-time budget.

The original-machine records are published. A reproduction run regenerates these files, tables, macros and figures in its own checkout. It should preserve exact labels and maxima; timing-derived fields may change. Internal independent reviewer snapshots preserve their actual audit point, including pre-release newline normalization. The release integrity report records the final source format.
