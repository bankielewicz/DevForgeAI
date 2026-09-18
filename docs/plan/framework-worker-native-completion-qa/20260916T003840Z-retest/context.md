# Independent QA retest context

- Invocation intent: `retest`, explicitly selected by the user after the separate `$dev` remediation for `QA-F-COV-01`.
- Selected project: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Required host: native Windows x64, PowerShell, Windows-local filesystem at `C:\Projects\DevForgeAI`.
- Selected evidence value and resolved destination: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260916T003840Z-retest`, supplied by the parent QA assignment before the first write.
- Selected specifications: `codex-worker-feasibility-v1.md`, `codex-worker-native-readiness-v1.md`, and `codex-worker-preflight-v1.md`, bound in `input-bindings.json`.
- Selected defect: `QA-F-COV-01`, original valid coverage failure `2,852/3,103 = 91.91105381888495004834031582%`.
- Scope: independently verify a frozen corrected candidate; inspect integrity; enumerate every compiled Rust test; run the complete locked/offline all-target suite; verify all WF-01..20 parents/subfixtures, F-01, F-02 and all new requirement-derived tests; run rustfmt, Clippy and one complete fresh first-party line-coverage collection; apply both 95% floors independently.
- Native exclusion: no installed-profile source collection, Codex app-server/model process, WN-01 or WN-02 launch is authorized in this retest. Their state remains separate from closure of the offline metric defect.
- Authority exclusion: this QA run cannot issue protected framework acceptance. Framework acceptance remains `NOT_EVALUATED` unless the separate qualified compiled-Rust authority actually decides it.
- Candidate state: development is in progress. All product execution and candidate integrity conclusions are blocked until the parent supplies the corrected manifest, snapshot, dev handoff and freeze statement.
- Git identity: absent in the selected workspace according to repository instructions; the corrected candidate will therefore be bound by a complete scoped source manifest and SHA-256 hashes.
- Existing evidence: original FAIL evidence is preserved and used only as historical defect evidence. It cannot qualify changed bytes.
- Operational constraints: do not edit product source/tests/specifications or operational copies; do not install, deploy, change configuration, credentials, cache, startup state or thresholds; do not run native trials; preserve every attempt and stop immediately after a valid complete sub-95 metric, confirmed gaming/mock attribute, or critical security/data-preservation violation.

## Environment discovered during preparation

- OS: Microsoft Windows 10.0.26200, X64.
- Shell: PowerShell 7.6.6.
- Working directory: `C:\Projects\DevForgeAI`.
- Cargo: 1.97.1; rustc 1.97.1, `x86_64-pc-windows-msvc`, LLVM 22.1.6.
- cargo-llvm-cov: 0.8.4; rustfmt: 1.9.0-stable; Clippy: 0.1.97; Python: 3.10.11.
- Filesystem type is not independently established during preparation. The selected path is Windows-local and no Linux/WSL evidence is substituted.

## Bound output roles

- Plan: `qa-plan.md`.
- Input identities: `input-bindings.json`.
- Candidate/freeze identities: `candidate-bindings.json`, written only after development freeze.
- Requirements/cases: `case-matrix.json`.
- Denominators: `source-denominator.json` and `test-denominator.json`, written after freeze and before metric execution.
- QA helpers: `record.py`, `freeze_audit.py`, `integrity_locators.py`, `coverage_analysis.py`, and `seal_manifest.py`.
- Raw command attempts: one uniquely named child directory per attempt with `stdout.bin`, `stderr.bin`, candidate before/after manifests and `receipt.json`.
- Coverage: `coverage/coverage.json`, QA-owned target/profraw tree and independent analysis receipt.
- Runtime checkpoint: `checkpoint.json`.
- Final report: `qa-report.md`; `qa-fix.md` only if this retest fails.
- Final external binding: `handoff-manifest.json`; immutable evidence index: `artifact-manifest.json`.

