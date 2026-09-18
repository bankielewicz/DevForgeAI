# Native Windows remediation context

Selected project: `C:\Projects\DevForgeAI\devforgeai`, native Windows, no Git metadata. User selects QA-D01 and QA-D02 remediation under the index-service MVP specification, followed by independent QA retest. No operational skills, installation, deployment, startup/systemd changes, remote synchronization, or WSL invocation are selected.

## Bound output destination

- selected_evidence_value: `C:\Projects\DevForgeAI\docs\plan\index-service-remediation\20260914T1950304158791Z`
- selection_source: selected specification section 10 requires a distinct `docs/plan/` run; this run's pre-write commentary selects the complete path above. The user-supplied QA evidence directory is an immutable input, not a new output destination.
- resolved_evidence_root: `C:\Projects\DevForgeAI\docs\plan\index-service-remediation\20260914T1950304158791Z`
- Normalization: relative commentary path resolved against the selected Windows workspace; components compared before first write.
- Output mapping: `context.md` (context, decisions, slices and traceability), `inputs.json`, `initial-source-manifest.json`, `record.py`, `executions.jsonl`, `attempts/<unique attempt>/{source-manifest.json,receipt.json,stdout.txt,stderr.txt}`, `coverage-<attempt>.json`, `delivery.md`, `source-manifest.json`, `changed-files.json`, `runtime-artifacts.json`, `handoff-manifest.json`, and checkpoints when needed. All beneath the exact root above.

## Verified intake

Selected spec `docs/plan/devforgeai-index-service-mvp-spec.md`: SHA256 `52d33c84435da8f3442c6b1dc4c5370113ff0eb93ee5cd2801903741900c89c4`, read completely. QA input root: `C:\Projects\DevForgeAI\docs\plan\index-service-qa\20260914T184442947070Z\executions\20260914T191133863776Z`.

Handoff manifest SHA256 `7681571d0e61f71b857fb57bf1bb466f902781a52a3e2c3fbf4d8f3794a2398b`. Exact entries verified required path = actual path, bytes and SHA256 for qa-report.md, qa-fix.md, dev-handoff.md. Source manifest SHA256 `43b63b5a9496b9d5374996d274cf5b852e2301ba23a87490717c786f71790343`; all 48 listed files match, no material drift or Git metadata. Current root AGENTS.md and operational dev skill/references read; no nested application AGENTS.md found. Capture is bounded to application, selected spec, current rules, and QA handoff/evidence; unrelated workspace files excluded.

## Decisions, reuse and slices

Architecture, Rust, state ownership and protocol remain as specified in DS-001..026. Index observations have no acceptance authority. Query extension and protected authority-service implementation are not selected. Current Cargo manifest/lock and bundled grammar versions are reused unchanged. Windows cargo/rustc 1.97.1 and cargo-llvm-cov 0.8.4 were discovered, with cargo at `C:\Users\bryan\.cargo\bin\cargo.exe`. Python 3.10 is an evidence recorder only.

| Selected obligation | Existing implementation and reuse decision | Planned verification |
| --- | --- | --- |
| QA-D01 / DS-025 | Extend `src/tray.rs::status_text`; `src/tray_windows.rs::apply_update` already assigns this output to STATUS. Reuse actual index.status fields from service.rs; preserve jobs, counters, asynchronous worker. | Original two QA oracles unchanged, developer known/unknown/changing-field cases, native control readback and screenshot. |
| QA-D02 / section 1.4, DS-A19 | Extend existing Rust tests over measured CLI/service/index/platform/tray gaps; inspect each uncovered path before adding checks. No coverage suppressions or excluded first-party files. | Fresh native baseline, meaningful positive/negative/recovery tests, final full suite and integer coverage counts, formatting/Clippy/release build. |
| Output identity and preservation | SHA256 manifests with exact native paths, original source/evidence retained. | Input rehash, changed-file comparison, candidate/build/evidence readback. |

Order: reproduce original QA failures and measured coverage; add tray behavior tests before implementation; minimal formatter correction; test coverage characterization additions and any discovered behavioral fixes through separate red/green; refactor only when justified; integrated native QA. Existing characterization tests may pass initially; never manufacture a failing product to claim red. The coverage threshold failure is the test-suite deficiency red result.

## Measurement declared before execution

Executed-line denominator: every compiled first-party `devforgeai/src` file, including all three binaries and Windows native adapters. Exclude only tests, examples, fixtures, third-party dependencies and generated code. Same filename exclusion as QA: `[/\\](tests|examples|fixtures)[/\\]`. No removal of first-party behavior to raise the percentage. Threshold 95% without upward rounding. Branch collector not selected: NOT_RUN.

Required Windows regression set: discovered product Cargo tests plus unchanged 12 QA oracles and newly authored scoped repair tests, each counted once on the final candidate; setup-only harness/benchmark fixture tests reported separately. Two explicitly ignored WSL cases remain unexecuted and are reported separately as well as nonpasses in the full declared Cargo inventory. Unit classification follows QA's 18-case original declaration; new tests are separately identified, never used to conceal the original two failed units. Full required-platform acceptance inventory is not established by this repair.

Ubuntu and WSL final candidate tests/coverage are NOT_RUN in this native Windows-only scope. Existing QA-G01..05 remain separate obligations: startup/systemd effects prohibited; alternate-principal, full race/crash/overflow/UI/benchmark/integrity qualification remains with independent QA. External framework acceptance NOT_EVALUATED. QA findings cannot be self-closed by this run.

## Additional concrete output bindings and execution decisions

Before final writes, extend the output mapping beneath the same original root with `attempts/coverage-final/profiles/`, `attempts/coverage-final/profile-manifest.json`, `attempts/coverage-final/instrumented-binaries.json`, `candidate/` (retained corrected source/tests/config), `runtime/` (retained release binaries), `candidate.diff`, `metrics.json`, `test-inventory.json`, `tools.json`, `preservation.json`, `verification.json`, and `checkpoint.md`. Paths remain native Windows descendants of the originally selected root; no destination component changed.

The first sandbox native run failed ACL/IPC prerequisites; separate approved native attempts are retained. Pure component subsets run in the sandbox and do not count skipped native tests as passes. Controlled Rust subprocess fixtures validate the Windows bridge without invoking WSL. Temporary application preferences are exercised with `launch=None`; no Windows startup registry entry is written. Native settings dialogs are cancelled before committing preferences. Test-only junctions and named pipes belong to synthetic fixtures.

Production refactors preserve behavior: CLI bridge accepts an internal executable boundary with the public wrapper still fixed to wsl.exe; host response handling accepts an internal dispatch-task boundary to check timeout/panic envelopes; the watcher callback is separated to verify access filtering, failure invalidation and expired ownership deterministically. All other production-file additions are cfg(test) module bindings. QA-D01 adds the two fields to the existing shared formatter. These are product tests and evidence, not independent QA closure.

Retained harness failures: first invalid glob fixture was actually a supported literal pattern; corrected to the invalid descending range `[z-a]`. Data-root test fixture needed a canonical native path. A focused parser command matched zero tests, then was corrected with the exact full test name. An invalid process-handle fixture used the valid current-process pseudo-handle value and was corrected to null. The native dialog test now waits for modal closure before issuing the next command. No product assertion was weakened; original QA oracle bytes remain unchanged.

Before the next full run, bind `coverage-final-002.json`, `attempts/coverage-final-002/` and its retained profile/binary manifests beneath the same selected root. The earlier `coverage-final` attempt is retained with its actual 3284/3486 (94.205393%) failed coverage threshold.

An explicitly approved `startup-registry-native` test passed using a GUID-owned volatile registry leaf and process-local HKCU redirection in a dedicated single-test executable. It verifies the actual Run value's original type and bytes through an unredirected handle, restores HKCU, checks the original value again, removes the owned fixture, and verifies removal. Application startup settings are unchanged. This isolates registry behavior; it does not qualify sign-in launch, real startup installation, or systemd. The subsequent full suite includes the same bounded fixture under the existing authorization.

Final output accounting also includes `windows-process-readback.json`, `write_delivery.py`, and `seal_handoff.py` at this same root. The final integrated run executed 90/90 Windows product cases, two setup cases, and left the two original WSL cases ignored. Coverage is 3314/3486 (95.06597819850832%). Release build, formatting and Clippy use the same source manifest. Final native screenshot was inspected: both provenance fields are visible and readable. No DevForgeAI processes remained in the recorded process readback.
