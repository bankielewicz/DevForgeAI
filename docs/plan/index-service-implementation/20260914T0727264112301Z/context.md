# Index service implementation context

Recorded 2026-09-14 UTC. Selected project: `C:\Projects\DevForgeAI` on the native Windows filesystem. User request: `$dev docs/plan/devforgeai-index-service-mvp-spec.md`. Scope is application implementation through QA; no installation, startup changes, operational skill edits, or protected acceptance. Git metadata is absent and `devforgeai/` was empty at inspection.

## Evidence destination binding

- selected_evidence_value: `docs/plan/index-service-implementation/20260914T0727264112301Z`
- selection_source: selected specification section 10, "Retain run evidence under a distinct `docs/plan/` run directory." The concrete unused child above was chosen under that rule before the first write.
- resolved_evidence_root: `C:\Projects\DevForgeAI\docs\plan\index-service-implementation\20260914T0727264112301Z`
- Normalization: project-relative forward slashes become native separators; no component renaming. Compared against section 10 and the selected project before writing.
- Outputs beneath this root: `context.md`, `inputs.json`, `traceability.md`, `slices.md`, `executions.jsonl`, `attempts/`, timestamped `checkpoint-*.md`, `delivery.md`, and `readback.json`. Product source, tests, schemas, documentation and binaries belong under `devforgeai/`.

## Decisions and capture bounds

The selected service specification owns management protocol, indexing, storage, lifecycle, isolation, WSL and Windows GUI. The companion query specification is reference-only for forward-compatible record/generation ownership; implementing its query operations is unselected. The enforcement design sections 1, 3, 4, 5 and 6 establish a separate protected service: index observations and these evidence records have no acceptance authority. Legacy implementations were not inspected.

Selected requirements: DS-001 through DS-026, all DS-A01 through DS-A19 scenarios, and unnumbered section 1.4 engineering, section 9 benchmark and section 10 delivery obligations. Three required platforms: Windows 11 x64, Ubuntu 24.04 x64 and Ubuntu 24.04 WSL2. Native visual evidence is additionally required for the Windows tray. Missing hosts/checks are NOT_RUN.

Routine layout decision: one initial Cargo workspace package with separate Rust library modules for protocol, client, platform, index and scheduler, plus the three specified binaries. This preserves logical ownership without introducing an unnecessary package boundary. Dependencies will be pinned with Cargo.lock. No source configuration is written into indexed roots.

Capture includes the selected spec, companion contract, repository AGENTS.md, enforcement design, and operational dev skill plus its references/templates. Inputs are pinned in `inputs.json`. Source reuse inspection is bounded to the selected empty application directory and current repository manifests, not old evidence fixtures or prohibited legacy repositories. User-supplied AGENTS.md matches the inspected repository guidance. No missing product requirement is supplied from memory.

## Observed tooling and host

PowerShell on Windows build 26200, display version 25H2, x64 Rust target. Registry ProductName retains the Windows 10 Pro compatibility label; exact native OS qualification remains to verify. `cargo`, `rustc`, `rustup` resolve beneath `C:\Users\bryan\.cargo\bin`. rustc 1.97.1 (8bab26f4f 2026-07-14), cargo 1.97.1 (c980f4866 2026-06-30); active stable-x86_64-pc-windows-msvc. Rustfmt, Clippy and LLVM tools installed; cargo-llvm-cov 0.8.4 available. Linker execution is not yet established.

WSL inventory initially failed with sandbox E_ACCESSDENIED. The approved read-only retry found Ubuntu running under WSL2 and docker-desktop stopped. No Linux executable was launched and no distribution was started. Ubuntu release and native Linux qualification remain unverified. A separate Linux checkout is not selected.

Initial discovery was interactive terminal evidence; exact start/end times and stream files for those discovery calls were not retained and must not be reconstructed. All subsequent execution attempts use the evidence recorder, which is development observation tooling only.

## QA scope declared before measurement

Executed-line denominator: all first-party executable Rust application source beneath `devforgeai/src`, including binaries and platform adapters. Exclude external dependencies, generated grammar source and fixtures/tests; never exclude uncovered application behavior. Report branches separately when supported. Required executed-line coverage and required-case pass rate each >=95% per required platform. Acceptance scenarios remain mandatory regardless of aggregate metrics. Tests will be enumerated against the final candidate; all 19 selected scenario obligations remain tracked even when unexecuted. Compilation, focused unit tests and Python/PowerShell evidence collection do not qualify service or GUI behavior.

## User-directed qualification handoff (2026-09-14)

The user requested a note that WSL is tested and standalone Linux is not, plus a methodical HTML test playbook whose exported results can be returned for evaluation. Standalone Ubuntu remains NOT_RUN; WSL evidence is not substituted for it. No standalone host selection is pending after this direction.

Before first write, bind the new requested artifact to `docs/plan/index-service-validation-playbook.html`, resolved as `C:\Projects\DevForgeAI\docs\plan\index-service-validation-playbook.html`. The accompanying platform note is `docs/plan/index-service-implementation/20260914T0727264112301Z/platform-status.md`. The playbook is an offline evidence organizer; its results and calculations do not issue framework acceptance. Existing source implementation scope and unresolved coverage/acceptance gaps remain visible.
