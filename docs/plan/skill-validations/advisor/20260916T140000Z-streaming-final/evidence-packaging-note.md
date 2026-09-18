# Evidence packaging note

## Scope

This note records an evidence-layout correction made after the advisor source validation was complete. It does not change the candidate, test results, coverage measurements, or QA verdict.

## Preserved failed aggregate audit

The command `observe.py records --run-root <final-run>` returned `MISMATCH`. The run root contains heterogeneous raw evidence, including BOM-bearing Pester JSON and raw coverage/readback manifests, outside the observer's excluded `source/`, `inputs/`, and `trials/` boundaries. The observer recursively interpreted those files as schema-1 validator records and resolved embedded paths against the final-run root. The exact failed output is preserved at `trials/records-audit-001.json`.

This result is an aggregate-record tooling/layout limitation. It is not a product failure and does not supersede the direct source, behavior, coverage, structure, or artifact-digest observations.

## Temporary relocation and restoration

While investigating that observer limitation, raw evidence was temporarily moved to these trial locations:

- `coverage/` to `trials/coverage/`
- `coverage-independent/` to `trials/coverage-independent/`
- `evaluation/` to `trials/evaluation/`
- `independent-cases-001.json`, `independent-cases-002.json`, `independent-cases-003-coverage.json`, `source-readback.json`, and `source-readback-final.json` to `trials/`
- `policy-control.ps1` and the `policy-*` artifacts to `trials/policy/`

That relocation was stopped because existing delivery links and sealed peer evidence already referenced the original paths. Byte-identical copies were restored at every original path. The trial copies and failed audit were retained; no peer artifact was deleted or overwritten.

The restoration readback compared eight load-bearing root/trial pairs: the Python coverage JSON, both independent Pester results, the deterministic evaluation summary, all three independent case summaries, and the final source readback. All eight pairs matched byte-for-byte. A subsequent index readback found every indexed artifact present with its recorded SHA-256.

## Source and execution effect

- Candidate source readback remained `MATCH` for all 19 files.
- Canonical package digest remained `ce037407bfe1bb636b42dc468595a93b5837a2788837fc436c4bfc615f1d033f`.
- No source file or operational skill copy changed.
- No product test, evaluation, coverage run, PowerShell trial, or live Claude call was repeated because of this packaging correction.
- The independent verdict and its 30-case denominator are unchanged.

