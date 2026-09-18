# Independent QA retest plan — QA-F-COV-01

## Identity, selection and authorization

- Plan/run identity and intent: independent `retest`, explicitly selected by the user after a separate `$dev` remediation.
- Automatic continuation: once the parent supplies a frozen corrected candidate and complete dev handoff, this already-authorized retest proceeds without another confirmation.
- Planning status: `READY`; the developer released the frozen 53-file corrected candidate and complete metric/delivery package for independent execution.
- Execution status: `COMPLETED`; the final results and evidence are recorded in `qa-report.md` and `case-results.json`.
- Project: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`, native Windows x64, PowerShell, Windows-local filesystem.
- Evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260916T003840Z-retest`.
- Selected contracts: DFF-WORKER-FEAS-01 v1.0.0, DFF-WORKER-NATIVE-01 v0.1.0 and DFF-WORKER-PREFLIGHT-01 v0.1.0 at the hashes in `input-bindings.json`.
- Defect lifecycle: `QA-F-COV-01` is `VERIFIED_FIXED` by the completed independent retest; the original failing measurement remains retained.
- Original failure: `2,852/3,103 = 91.91105381888495004834031582%`, a valid complete Windows x64 coverage measurement below the mandatory 95% floor.
- Corrected candidate: 53-file manifest `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T003840Z-dev\candidate-manifest.json`, SHA-256 `c27d8ce1742ba7cd0955f0bd18aded8de5f14c898c989654d7298835c3256f9e`, with exact snapshot and final developer handoff. Independent admission matched 53/53 live and snapshot files plus 11 bound inputs.
- Allowed effects: read-only inspection, QA-owned helpers/fixtures, local offline Rust compilation/tests/instrumentation, raw evidence/report writes and bounded cleanup of QA-owned disposable state.
- Excluded effects: product/test/specification repair; operational-copy/cache/configuration/credential/startup changes; installation/deployment; Codex app-server or model launch; installed-profile collection; WN-01/WN-02; authority implementation/provisioning or protected acceptance.

## Output and checkpoint binding

The literal destination and role map are in `context.md`. `checkpoint.json` records all pending prerequisites, attempts, owned processes/fixtures and the next safe action. Final report/fix/candidate paths will not be invented before their bytes exist. A non-circular `handoff-manifest.json` will bind the final plan, report, optional fix and checkpoint; `artifact-manifest.json` will index retained evidence and exclude only itself plus disposable non-coverage Cargo outputs.

## Acceptance inventory and independent oracles

The complete case inventory is in `case-matrix.json`; the candidate-bound readiness revision is `case-matrix-readiness.json`. It covers:

1. `QA-F-COV-01`: all first-party executable Rust under the frozen package `src/`, with no production exclusion.
2. Every compiled Rust unit and integration test in the corrected manifest, including all newly added remediation tests.
3. WF-01..WF-20 as 20 unique parents, with every specification-listed subfixture required within its parent.
4. F-01 blocked-write/deadline/cancellation/tree-cleanup and F-02 typed-field/privacy regressions.
5. The affected offline NI-T05 and NI-T07..NI-T10 validation, policy, inventory, protocol and denial behavior. Synthetic evidence receives no live Codex credit.
6. Formatting and Clippy for the exact frozen bytes.

Independent oracles:

- A fresh package manifest is compared byte-for-byte with the dev freeze before and after every command.
- Source coverage is resolved from the corrected manifest's exact `src/**/*.rs` inventory; llvm-cov paths are normalized before inclusion so lexical paths cannot move tests into the production denominator.
- Physical Rust test attributes, Cargo's executable test list and dev's requirement-to-test map are reconciled. New tests are inspected for meaningful assertions, distinct contract stimuli and coverage of previously unexecuted behavior; duplicated cases do not inflate any denominator.
- The policy oracle derives exact ordered argv and the 35-feature disable set directly from the selected preflight contract, independent of product validators.
- WF trace review requires all specified variants and real Windows process evidence for WF-13..WF-16; a support peer never earns native Codex credit.
- The F-02 oracle injects private canaries, requires contract exit/category behavior and scans retained journal/stdout/stderr bytes for absence while approved typed fields remain.
- No setup result, passing build, test count or Python helper result constitutes framework acceptance.

## Environment and capability matrix

| Host | Tools | Capability | Readiness |
| --- | --- | --- | --- |
| Native Windows 10.0.26200 x64 | Cargo/rustc 1.97.1, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4, Python 3.10.11 | Locked/offline build, Rust suite, Windows process tests, static checks and line coverage | `PASS` for the selected offline defect retest |
| Installed Codex profile/native model | Deliberately not probed in this retest | WN-01/WN-02 and live portions of NI-T05/09/10 | Outside selected retest effects; remains separate `NOT_RUN`/`BLOCKED` evidence |
| Protected compiled-Rust authority | Not selected or provisioned | Framework acceptance | `NOT_EVALUATED` |

## Integrity inspection before execution

After freeze and before the first product command, QA will enumerate every candidate file and inspect all first-party Rust implementation, tests, support binaries, Cargo declarations and QA helpers. The inspection resolves Rust attributes, macros, aliases/re-exports and dependency declarations; searches are only locators. It checks prohibited mock-generating attributes, ignored/skipped tests, vacuous or same-logic assertions, swallowed errors, unconditional success, fake integration/native claims, retry inflation, unjustified coverage suppression, source omission and stale evidence binding.

A confirmed mock decorator or result gaming is `INTEGRITY_FAILURE` and stops the entire run. An unresolved dynamic region is a prerequisite gap and prevents PASS for dependent claims. QA helpers are inspected before use and again after any bounded QA-owned correction.

## Denominators declared before execution

- Eligible source: every frozen first-party Rust file under package `src/`; embedded policy/identity JSON has no executable-line denominator of its own but its compiled consumers remain included. No first-party source or line is excluded because it is uncovered. Tests, support binaries, fixtures, dependency/vendor/generated sources and QA helpers are outside the product source denominator.
- Required unit denominator: every unique executable library/unit test in Cargo's frozen `--list --format terse` output. Failed, errored, ignored, skipped, blocked and unexecuted required tests are nonpasses.
- Required project-suite denominator: every unique executable Rust test in the same complete list, reported separately from the unit rate. New remediation tests are included once.
- WF denominator: exactly 20 parents; every required variant must pass and any failed/missing variant fails its parent. The base contract requires all 20, even though numeric floors are also reported.
- F-01/F-02 denominator: exactly 2 mandatory regression groups, both required.
- New requirement-test denominator: every distinct dev-returned test mapped to previously unexecuted contract behavior, frozen before execution and counted once. It supplements, rather than inflates, WF/NI groups.
- Coverage: executed eligible lines divided by all eligible executable lines from one complete `cargo llvm-cov --locked --offline --all-targets` collection. Branch data is reported separately if supported.
- Effective floors: first-party line coverage `>=95%` and required unit pass rate `>=95%`, both at full precision. The repository's all-required-case floor `>=95%` is also reported for the complete declared suite. Passing percentages cannot waive any failed mandatory WF, F-01/F-02 or authority/security invariant.

`source-denominator.json` and `test-denominator.json` will be generated and read back after freeze and before the respective metric commands. A partial/crashed collection has no final percentage. Attempts never alter denominators.

## Planned execution order

All commands use `record.py`, unique attempt directories, a QA-owned `CARGO_TARGET_DIR`, and `WF_TEST_EVIDENCE` where needed. Each receipt records exact argv/cwd/environment overrides, executable path/hash, UTC and monotonic timing, PID, native exit, timeout/containment, byte-exact raw streams and candidate manifests before/after.

1. Verify corrected manifest, snapshot, selected specifications, handoff and resolution map with `freeze_audit.py`.
2. Run and semantically review `integrity_locators.py`; reconcile every candidate file, Rust attribute/macro/dependency and new assertion. No product test starts before this decision.
3. Capture `cargo test --locked --offline --all-targets -- --list --format terse`; freeze unit/full/new-test denominators.
4. Execute `cargo test --locked --offline --all-targets` once with a bounded 420-second supervisor. Verify WF parent/subfixture artifacts, F-01/F-02 evidence and new requirement-derived tests.
5. Execute the independent policy oracle and focused F-02 byte-canary check against binaries from the same candidate/build identity, if no terminal stop has occurred.
6. Execute `cargo fmt --all -- --check`.
7. Execute `cargo clippy --locked --offline --all-targets -- -D warnings` using its own QA target tree.
8. Execute one complete fresh `cargo llvm-cov --locked --offline --all-targets --json --output-path <QA evidence>/coverage/coverage.json` using its own target/profraw tree, then independently analyze the raw JSON against the frozen source denominator.
9. If the valid complete coverage or unit measurement is below 95%, stop immediately. Do not repair, repeat, shrink the denominator or launch another check to improve the metric.
10. Perform final candidate/spec readback, report, defect-state decision and evidence sealing. No native trial follows from this retest.

## Stop, continuation and cleanup

- `INTEGRITY_FAILURE`, valid complete `METRIC_FAILURE`, or `CRITICAL_PRODUCT_DEFECT` stops the entire campaign immediately. Only bounded containment, evidence preservation/readback, assessment and reporting follow.
- Another mandatory product defect records FAIL but permits safe independent checks to continue.
- Harness/setup/tool gaps block only dependents; they are not product failures without evidence.
- Candidate/specification drift is an execution-safety blocker. QA will not silently rebind the plan or restore older bytes.
- Timed-out QA-owned command processes are contained through the recorded PID tree. No native Codex process is expected or authorized.
- Product source, developer tests, old evidence and non-QA state are never cleaned or rewritten by QA.

## Entry, exit and handoff

Entry requires an exact corrected manifest/snapshot/handoff, successful input/freeze readback, finalized denominators and a clean or explicitly bounded integrity assessment. PASS for this retest requires `QA-F-COV-01` to be independently `VERIFIED_FIXED`, both numerical floors and the full-suite floor to pass, all affected mandatory offline regressions to pass, and no unresolved selected-scope gap. Native readiness and framework acceptance remain separate and cannot be inferred from this result.

On FAIL, QA publishes `qa-report.md`, `qa-fix.md` and a resolved manual `$dev` prompt. On INCOMPLETE, QA names the precise prerequisite owner. On PASS, QA publishes the selected-scope verdict and downstream state without granting release, native qualification or protected acceptance.
