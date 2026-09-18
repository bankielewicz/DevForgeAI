# Scoped logging remediation context

Record: 20260917T102726Z-dev-qa-fixes. Project and shell: `C:\Projects\DevForgeAI`, native Windows PowerShell 7.6.6, Windows 10.0.26200 x64, native C: filesystem. No Git metadata exists at the project or application root. No subordinate AGENTS.md was found at the selected source/evidence ancestors.

Authorization is the current user request: remediate QA-LOG-01 and QA-LOG-02 only; create `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes`. Preserve the failed candidate, original/snapshot, prior evidence, unrelated bytes, and `Start-CodexAppServerDiagnostic.ps1`. Native Codex, operational changes, installation/deployment, independent QA invocation and finding closure are excluded. This is development evidence, not framework acceptance.

## Bound destinations and inputs

- Original corrected-source selection: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging-qa-fixes`, from the user's literal request. Resolved destination is identical; no component renaming. It was absent at preflight.
- selected_evidence_value: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging`.
- selection_source: established evidence family in the verified QA handoff, together with AGENTS.md's requirement for distinct new evidence. The old QA run is read-only.
- resolved_evidence_root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-logging\20260917T102726Z-dev-qa-fixes`.
- Pre-write comparison: absolute native paths under the selected project; evidence and source are disjoint. No separator or name normalization was needed.
- Concrete output mapping: context.md (this record), plan.md (slices/traceability/declared metrics), intake-verification.json, input-bindings.json, attempts/<unique-id>/{receipt.json,source-manifest.json,stdout.txt,stderr.txt,fixtures/}, execution-record.jsonl, coverage.json, metrics.json, candidate-manifest.json, build-manifest.json, changed-file-manifest.json, candidate.patch, resolution-map.json, delivery.md, checkpoint.json, preservation-readback.json, handoff-manifest.json and final-readback.json. Build/coverage intermediates remain in this run's build-target/coverage-target directories.

The handoff manifest SHA256 is `0c6949f4379e7c469643f34ad6d4b1f664f48177f8865d12dfedd7cbe901019e`. All its bound entries verified. Initial readback found zero drift among 67 candidate files, 37 inputs, 8 specifications and 116 preserved original/snapshot files. No old source is restored: the new directory starts from the verified current failed candidate. Full current file membership is compared before copying. Input bindings retain the exact eight selected specification identities plus current instructions and development skill references. The bound qa-report.md and qa-fix.md were read; both findings remain OPEN in QA custody.

## Decisions and limits

Rust 2024 / minimum 1.97.1, existing Cargo.toml/Cargo.lock and dependencies are retained. The isolated package already implements stream capture, mandatory process_exit, diagnostic validation and historical inspection. Inspection is the only runtime responsibility needing extension. Capture::validate currently checks shape/conditional drain consistency; journal::inspect discards typed capture and post-stop code. Reuse these components and extend their success consistency checks. Do not change request, wire, launch-policy, process lifecycle or optional logging contracts.

The selected amendments resolve precedence: logging-contract LG-01..08 defines current capture/request-schema behavior; logging design and investigation clarify lifecycle/privacy; diagnostic v1 owns closed observations; base feasibility owns inspection and offline WF cases; native-readiness/preflight/source-identity companions retain offline regression obligations. No missing specification decision blocks these two repairs. Broader authority/index/native deliverables are unselected.

Discovered native tools: Cargo/Rust 1.97.1, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4, LLVM 22.1.6, resolved from `C:\Users\bryan\.cargo\bin`; PowerShell is `C:\Program Files\PowerShell\7\pwsh.exe`. Installed toolchains are stable and 1.93 Windows MSVC; no nightly. Collector help labels branch coverage unstable, so branch measurement is NOT_RUN. No installation is selected. Commands use locked offline dependencies and fresh targets. The record helper retains executable hashes, argv, source identity, environment overrides, times and exit codes.

Capture is scoped to this package, selected contracts, bound preservation inputs and new evidence. No credential/environment values or unrelated repository contents are captured. Historical reports provide requirements and reproduction pointers, not current test credit. Saved memory supplied no task-specific requirement or result.
