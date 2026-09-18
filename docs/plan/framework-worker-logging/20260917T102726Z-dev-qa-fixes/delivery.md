# Scoped development delivery: QA-LOG-01 and QA-LOG-02

Both selected defects are **FIX_REPORTED** for independent QA retest. The production correction and all declared offline checks passed. Final publication status is recorded in final-readback.json after actual required-path/hash readback; no QA finding is closed and no framework acceptance is issued.

## Corrected identity and changes

Corrected source is at the user's exact destination, `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes`. It contains 68 files copied from the verified current failed candidate, then changed in exactly three paths:

- src/journal.rs retains typed capture/post-stop evidence, distinguishes an absent exit field from explicit null, and enforces complete capture and matching successful exits for completed/preflight_checked observations.
- tests/inspection_consistency.rs adds ten conjunctive regression tests with public CLI/library observations, fresh real peer controls, both streams, success/failure/history branches, all logging levels and byte-for-byte no-mutation checks.
- README.md identifies this sibling and its remediation evidence and corrects its build command destination.

[candidate-manifest.json](candidate-manifest.json) SHA256: `4a25130c9353ec65553ed8c26cb75e76af5833ce4e2d80e8c62ecd9297b5d7a7`. Path-independent source content identity: `8e2acac92495e8119638d4588df96d7dc91834b196d7bcce1153efcfcc95f697`; its canonical encoding is specified in [source-identity.json](source-identity.json).

Main compiled executable: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T102726Z-dev-qa-fixes\build-target\debug\devforgeai-codex-worker-probe.exe`, 2,545,152 bytes, SHA256 `ec2575bd4cacfce147113eee1b257d69be06b7e3d563d669e15010432e9dc3e5`. [build-manifest.json](build-manifest.json) binds this and the instrumented/test executables to the candidate/toolchain/receipts. [changed-file-manifest.json](changed-file-manifest.json) retains original and corrected hashes; [candidate.patch](candidate.patch) supplies the source/test/documentation diff.

## Executed verification

| Check | Actual result and retained evidence |
| --- | --- |
| Red before production edit | 6 failed / 4 passed; actual invalid successful evidence accepted. 01-red, Cargo exit101. |
| Green | Identical ten tests/assertions pass, 02-green, exit0. |
| Refactor | rustfmt applied; no additional semantic refactor needed. Ten tests pass on formatted bytes, 03-format / 04-refactor. |
| Required package campaign | 162/162 pass, no skips/errors/filtered cases, 08-coverage. Includes every inherited WF case and actual production watchdog, cleanup/descendant, fault/query_failed, source/identity and denial regressions. |
| Inherited supplemental real-pipe case | 1/1 pass, 09-supplemental; literal malformed UTF8/final-line byte hashes and actual Windows child exit/cleanup. |
| Required units | 49/49 = 100%. |
| Overall declared offline suite | 163/163 = 100%; 0 failed, errored, ignored, blocked or unexecuted. |
| Executed-line coverage | 3,871/4,057 = 95.41533152575795%; exact fraction independently exceeds 95%. |
| Formatting / Clippy / build | All PASS, 06-fmt-check / 07-clippy with -D warnings / 10-build. |
| Branch coverage | NOT_RUN; installed cargo-llvm-cov labels branch collection unstable and installed toolchains contain no nightly. |

The package/source/case denominators were declared before the full measurement in [plan.md](plan.md), [declared-cases.json](declared-cases.json) and [coverage-source-inventory.json](coverage-source-inventory.json). Every first-party executable line in all 15 src Rust files is included; declaration-only lib.rs has no executable lines. Tests/support and dependencies are excluded, with no executable first-party exclusion. [coverage.json](coverage.json), [coverage-analysis.json](coverage-analysis.json), [case-results.json](case-results.json) and [metrics.json](metrics.json) retain raw data and independently recomputed arithmetic. The supplemental case is in the suite denominator but does not contribute to package coverage.

Compared with the failed candidate's prior QA measurement, journal.rs changes from 415/426 to 429/442; unchanged protocol.rs measures 678/716 versus prior 679/716. All other file counts match. This run's own 3,871/4,057 is the reported result; historical coverage is not credited to changed bytes and no rerun was used to improve the number.

Windows x64 is the only selected platform; per-platform and overall ratios are identical. The complete full-coverage invocation took 215.653047 seconds. Native PowerShell 7.6.6, OS 10.0.26200, Rust/Cargo 1.97.1, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4 and LLVM 22.1.6 ran from the corrected candidate on native C:. [toolchain.json](toolchain.json) records resolved paths/hashes. [execution-record.jsonl](execution-record.jsonl) and each attempts/*/receipt.json retain exact argv/cwd/environment overrides/timing/exits/source identities and stdout/stderr. All ten execution attempts are terminal; none timed out. There are no pending invocations owned by this session.

## Resolution and remaining ownership

[resolution-map.json](resolution-map.json) maps each defect to the production checks and real red/green/final evidence. [implementation-review.md](implementation-review.md) explains the reuse/refactor decision and independent expected-result oracles. Complete stream hashes, EOF and reader-error checks are preserved. Valid actual nonzero failure, nullable failed observation, cancellation, timeout, cleanup uncertainty and historical schema1/2 controls pass. Inspection preserves all bytes and peer traces. Synthetic preflight journal fixtures exercise interpretation only; they do not prove native preflight.

The five selected obligation groups in plan.md are accounted for: S1/S2 implemented and verified by development; C1 compatibility PASS; R1 full offline regression/metrics PASS; D1 identities and required publication paths are read back by the final seal. Independent QA may retest both findings against this exact candidate and original eight contracts. Development has not invoked QA or set VERIFIED_FIXED.

Original failed candidate, frozen original/snapshot, prior QA artifacts and inputs, source specifications, unrelated bytes and Start-CodexAppServerDiagnostic.ps1 remain preserved. Initial verification found no material drift. [preservation-readback-final.json](preservation-readback-final.json) records final actual hashes, including the old handoff, 67 candidate files, 116 original/snapshot files, 37 inputs and 3,689 prior QA evidence files. The helper's required SHA256 remains `f69da72fb44737127dcfde3607fb0e027e4afeb2463a78ac8f844bc3abfc58a0`.

The first publication helper stopped on an inherited console-observation record that has a different shape from new inspection observations. [publication-attempt-01.json](publication-attempt-01.json), its original helper and completed initial preservation readback are retained. The corrected helper selects the exact inspection record shape, requires all 201 inspection observations per focused/final execution and records other families separately. No product byte changed or product test was rerun for this evidence-only correction.

Native Codex, WN-01/02, NI-T11/12 and installed-profile qualification: **NOT_RUN**. Independent QA retest: **NOT_RUN**, separately selected. Framework acceptance: **NOT_EVALUATED**. No operational configuration change, installation or deployment occurred.

## Literal publication

Original corrected-source destination is unchanged from the user request. Established selected_evidence_value is `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging`; this fresh run is `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T102726Z-dev-qa-fixes`. The original selection and every promised concrete output are in context.md. [handoff-manifest.json](handoff-manifest.json) binds required versus actual absolute paths, lengths and SHA256; final-readback.json records actual literal-path verification after publication. New evidence is separate from the immutable QA run and failed source. No older source or evidence was restored.
