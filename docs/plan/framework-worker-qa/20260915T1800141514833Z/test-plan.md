# Independent offline worker QA plan

Intent: run. Plan readiness: READY for offline work. Execution: NOT_STARTED.
Selected evidence value: fresh timestamped child of docs/plan/, selected by user repository evidence policy.
Resolved root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z`. Product source: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
Selected manifest SHA-256: `177b5894a236a02c7d322df7f04d647632094a4a3f3998e7f2a150db246e1604` (31 files match).
Contract: DFF-WORKER-FEAS-01 v1.0.0 at `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md`, SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`.
Input identities, 335 contract/schema readbacks and source denominator are adjacent JSON files.

## Scope and obligations

Windows x64, native PowerShell/Cargo on C:. All WF-01..20 and required subfixtures; independent IQ-01..06.
WN-01/WN-02 remain NOT_RUN, separately unselected; no Codex process, live account/config/profile inspection or model launch.
Linux/WSL, index implementation, protected authority, installation and native GUI qualification are not this unit.
The public library test seam permits injected shorter monotonic limits. The production watchdog remains exercised by WF-16.
Parent design constraints do not expand deliverables; Rust controls product behavior, Python records QA evidence only.

## Matrix and measurement

`cases.json` binds requirements, independent expected behavior, readiness, evidence and cleanup for 26 required QA cases.
The specification denominator remains 20 WF cases, each counted once; all subfixtures must pass.
Additional independent case rate is reported separately and overall 26-case rate retains all required nonpasses.
`test-inventory.json` contains all 46 developer test functions: 20 mandatory, 26 supplemental.
Unit-level inventory is the oracle/admission/profile test functions (6); integration/API test binaries remain separate.
Both 95% thresholds apply independently. All mandatory cases must pass even when numeric floors pass.
Coverage: full all-targets suite, no production exclusions; see `source-denominator.json`. IQ exploratory probes are separately assessed, not used to inflate baseline coverage.

## Execution order and commands

1. Inspect all 31 package inputs including all first-party Rust implementation/tests/support, attributes/imports and recorder; freeze fixture hashes and manifests.
2. `python -B -X utf8 C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\record.py test`: Cargo test --locked --offline --all-targets, bound 360s including compilation and production 120s watchdog.
3. `record.py format`, then `record.py clippy`: Cargo fmt --all -- --check; Cargo clippy --locked --offline --all-targets -- -D warnings.
4. `record.py coverage`: Cargo llvm-cov --locked --offline --all-targets --json --output-path C:\Projects\DevForgeAI\docs\plan\framework-worker-qa\20260915T1800141514833Z\coverage.json, bound 360s. Independent collection; preserve raw profiles/output.
5. Build QA-owned Rust peer/driver with path dependency on unchanged package into fresh evidence output; inspect code before launch. Execute IQ cases once per declared subfixture with external bounded process containment. Large server-request ID stays below 1MiB input line and 8MiB cumulative limits; peer stops reading only owned pipe. Expected result lives outside worker fixture.
6. Rehash original candidate and input boundaries; report/fix packet and manual handoff.

No product or developer-test edits. All build outputs/fixtures under this QA root. No downloads or dependency installation; missing cache is a setup gap.
Safety containment uses only current owned subprocess handles/tree; never a historical PID. Preserve failed attempts. Do not silently retry product tests.

## Integrity inspection and stop rules

Reviewed all package test functions and peer/console/crash drivers. Ordinary serde derive/test attributes; no mock-generating decorators, ignores or coverage suppression found. Synthetic external peer is expressly permitted; does not qualify native Codex. Fault injection remains library-only and is not real disk failure evidence.
Reviewed process FFI: job list supplied to CreateProcessW, kill-on-close, only three pipe handles listed, no breakaway. Independent lifecycle observation still required.
Known concern pending independent reproduction: synchronous worker stdin write may block deadline/control loop. No product defect yet inferred from a timeout alone.
Whole-run stop on confirmed integrity failure, complete subthreshold metric, critical security/data-loss defect, or uncontained ownership/identity problem. Ordinary functional defects retain FAIL while safe independent checks continue.
After a stop: containment, evidence readback and reporting only. Remaining required cases stay NOT_RUN with trigger ID.

## Artifact paths

Plan: test-plan.md; criteria: criterion-inventory.json; cases: cases.json; candidate: selected-manifest.json/candidate-before.json;
commands: per-attempt receipt.json/stdout.txt/stderr.txt; findings: qa-report.md/qa-fix.md; checkpoint: checkpoint.json;
final candidate: candidate-after.json; delivery: handoff.md. Report is independent QA assessment, never framework acceptance.
