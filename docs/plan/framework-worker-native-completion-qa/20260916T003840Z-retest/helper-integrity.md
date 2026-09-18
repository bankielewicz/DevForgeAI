# QA helper integrity review — preparation

Status: prepared helpers are syntactically valid and suitable for use only after the corrected candidate freeze. No product command was launched while reviewing them.

## Inspected helpers and claims

- `record.py` owns raw command capture. It requires the exact frozen candidate-manifest path and digest, refuses launch if live package bytes differ, writes separate byte-exact stdout/stderr, records native exit/timing/PID/containment and compares the complete package before and after. It returns the observed command exit; it does not turn failures into success.
- `freeze_audit.py` independently compares candidate-manifest, live package and snapshot bytes plus caller-supplied input hashes. It performs no repair or source write.
- `integrity_locators.py` enumerates Rust tests and suspicious attributes/patterns from the selected manifest. Its output explicitly says that semantic conclusions are not made by the locator. A human source review remains mandatory before execution.
- `coverage_analysis.py` derives eligible source exclusively from every frozen `src/**/*.rs` entry, rejects live/source/JSON inventory mismatches, applies no first-party exclusion, retains per-file/raw-profraw identities, calculates with Decimal precision and exits nonzero below 95%.
- `independent_policy_oracle.py` uses a literal ordered policy vector and the 35-feature set from the selected preflight specification. It does not call product validation logic.
- `focused_f02.py` holds the harness stdin pipe open while the candidate runs, uses compiled peer/probe executables, requires exact failure exit, scans journal/stdout/stderr for an independent private canary, checks the closed journal envelope and fixture immutability, and retains per-case raw bytes/receipts. Its limited claim is privacy/non-retention; the compiled regression must separately prove approved typed fields remain.
- `seal_manifest.py` indexes delivered evidence and includes raw coverage profiles while excluding disposable non-coverage build products. It does not assess product success.

## Integrity findings

- No mock/patch decorator, generated mock, skip/ignore execution option, retry loop, hardcoded product PASS, coverage omission or threshold reduction exists in the prepared helpers.
- `return 0` locators found during the textual scan belong only to successful helper completion after explicit checks, or to evidence sealing. `integrity_locators.py` intentionally returns success because its result is a locator set, never a clean-integrity verdict.
- The policy digest is specification-pinned; if the corrected candidate legitimately changes policy bytes, the independent oracle fails rather than adapting to product output.
- The helpers create only QA-owned evidence/fixture state. They do not edit the selected package, specifications or operational copies.

## Remaining inspection

After the candidate freeze, QA must inspect the final dev-returned tests and every helper again, bind final helper hashes, reconcile Cargo's executable list with physical attributes and confirm each newly added test has a requirement-derived oracle. This preparation review cannot establish candidate integrity or a QA verdict.
