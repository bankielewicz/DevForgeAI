# Independent bounded repair review

## Result

No substantiated new production defect found in this focused static review. This is a repair review, not independent skill validation or framework acceptance. No production edits or test executions were performed by this reviewer.

Reviewed source: `src/agents/skills/skill-builder/scripts/authoring.py`, SHA-256 `76dbd505dfadb88cb15fc12f80584aa46fff7e5d3c67c04c122d7dce8ae415b2`.

Compared against retained `before/scripts/authoring.py`, SHA-256 `cb55597715dc2d4d5dcdc4780ebc096eb9c3f137dbf9a853461a61c2c8b7cfc6`, and the original selected revision specification at `docs/plan/skill-validations/skill-builder/20260914T2131571597777Z/revision-spec.md`.

## Observed behavior and scope

- `begin` writes the closed stage receipt after origin readback and validates it before returning STAGED. The receipt binds run/name, the exact origin reference, and a strict boolean mode. A receipt error stays within capture-failure handling.
- `publish` validates stage integrity before design/legacy dispatch or target creation. The reproduced mode downgrade fails the original receipt's mode or origin binding. Missing/malformed origin and inconsistent receipts produce retained BLOCKED failure evidence with no applied paths. A recorded failed attempt cannot be reused by restoring the receipt.
- Existing design checks now also recheck stage integrity at their publication boundaries. A new check after the fault-injection callback and before each changed path rejects first-path drift before target directory creation. Drift after an earlier completed write preserves that applied-path list and produces PARTIAL without reaching successful baseline publication.
- The old B/C/N merge decisions, path guards, destination readback, authored/legacy baseline readers, validator packet fields, and output authority boundaries remain unchanged by the source diff. Late publication failures retain existing failure evidence semantics; successful publication readback remains required by existing baseline consumption.
- Fresh no-design stages receive false-mode receipts and retain the explicit early no-design branch, including ordinary design-shaped JSON inputs. Canonical historical no-marker/no-design stages take the prior legacy path. Marker-bearing stages without receipts receive an explicit fresh-linked-run error.
- Reference documentation changes in authoring.md, evidence-format.md, and regeneration.md describe receipt timing, editable-evidence limits, and the migration consistently. SKILL.md is unchanged. This review does not certify the package manifest or whole-workspace preservation.

## Retained V3 failures and fixture interpretation

Read-only inspection of `regression/v3-authoring-process.json` and stderr found exit 1 with two failures among 133 tests; this attempt must remain failed. V3 adaptive-stage and legacy process receipts report exit 0. No later rerun result is asserted here.

The two failing fault injectors depend on the previous eager target-directory creation:

1. `test_per_path_concurrent_write_is_preserved` writes directly to `target / path` inside before_write. With the repaired ordering, its parent does not exist, so the callback fails before creating competing bytes. Its PARTIAL assertion does not exercise its intended competing-writer condition.
2. `test_unreadable_after_interruption_reports_gap` makes `files(target)` fail but leaves the target absent. Failure capture correctly observes absence without calling files, so its expected unreadable-directory issue is never induced.

Creating the target directory inside each injector is a justified setup correction to establish the intended competing writer or unreadable destination. Retain all existing outcome/preservation assertions and the failed V3 evidence, then execute a fresh attempt. This conclusion follows from inspecting callback code and publication ordering, not from assuming the production change is correct because tests failed.

## Review method and limits

Used `git diff --no-index` for source and reference comparisons, `Get-Content` for the contract, source, failure-injection tests and retained process/stderr artifacts, and `Get-FileHash -Algorithm SHA256` for the two authoring files. Diff exit 1 indicates observed differences. Read/hash commands completed successfully. Local memory was used only to locate historical context; the selected contract and repair were read directly.

The receipt is an editable consistency check. Coherent rewriting of all local custody artifacts is outside its specified protection and was not treated as a defect. No new cross-platform execution, native generated-skill behavior, complete coverage denominator, required-case grading, validator acceptance, or protected Rust authority result is established by this bounded review.
