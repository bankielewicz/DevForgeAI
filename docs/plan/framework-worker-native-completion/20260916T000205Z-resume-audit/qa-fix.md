# QA remediation packet — QA-F-COV-01

## Selection and custody

This is a supplemental, read-only continuation handoff. The original QA report and stopped campaign remain unchanged. The newly selected output root is `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T000205Z-resume-audit`; it holds this packet, the complete manual invocation, current identity readback and their external manifest. No product test, reproduction or repair was launched in this continuation.

- Remediation owner: `dev`; independent closure owner: `qa`.
- Project: `C:\Projects\DevForgeAI`; package: `devforgeai\experiments\codex-worker-probe`.
- Platform: native Windows x64, PowerShell, Windows C: filesystem. Required Linux/tray checks: not applicable to this selected experiment. Filesystem type is unverified.
- Original QA report: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260915T2325371896643Z\qa-report.md`, SHA-256 `0cea59ae0461aec0530ee144d8bae340dba7208bec9ad03c97bb8cd1802d1095`.
- Original fix handoff: adjacent `dev-handoff.md`, SHA-256 `fbb6926a4b3a67433f06a7c12e48a24a013249402c2cc7e1b868eb3e2c4c075c`.
- Original evidence index: adjacent `artifact-manifest.json`, SHA-256 `886f2c630a03183df3557d9fc58a24075b3af440ade7e00c398e5c5a8fa6b1c5`.
- Failed source manifest: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260915T2306060954875Z\candidate-manifest.json`, SHA-256 `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd`.
- Inputs: same directory's `inputs-manifest.json`, SHA-256 `3fafe784e180b37cabaf8e276c8f324ea464fd568dcfa9a05688a55db9e88288`. It binds `AGENTS.md`, `docs\prompt\qa.md`, the three selected worker contracts, architecture context, captured schemas and skill entrypoints.
- Specifications: `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md` (SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23`), `codex-worker-native-readiness-v1.md` (`c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d`), and `codex-worker-preflight-v1.md` (`6e781f23f221d1033896716512e9162579653b529d107e0040d49c499574afd1`) in that same runtime directory.

The current host skill catalog exposes `$dev` and `$qa`. Merely publishing this packet does not invoke them or authorize restarting a terminal QA campaign. The proposed new assignment selects developer tests and any product correction justified by a valid reproduced defect; it excludes installation, deployment, operational copies/configuration/credentials/startup changes, protected authority and policy relaxations.

## Confirmed finding

- ID/state: **QA-F-COV-01 / OPEN**.
- Classification: **METRIC_FAILURE**, terminal; severity: high because it violates a mandatory qualification requirement.
- Requirement: `AGENTS.md`, Mandatory framework quality thresholds; base feasibility quality requirement; every first-party executable Rust line under `src/` stays in the denominator. Coverage must be at least 95%, independently of required test pass rates.
- Actual: **2,852/3,103 = 91.91105381888495004834031582%**. The complete collector exited 0, all 89 test functions passed, and the candidate remained unchanged. This is a valid below-threshold result, not unavailable coverage.
- Expected: at least 95% executed-line coverage over the entire declared first-party executable source, without exclusions or waived mandatory behavior.
- Ownership: application/developer test completeness. No QA-created helper defect or functional product root cause is established by this measurement.
- Affected artifacts: `src/effective_profile.rs` 485/573; `src/profile_sources.rs` 420/462; `src/protocol.rs` 594/627; `src/runner.rs` 145/178; all other per-file counts remain in the raw report. No particular uncovered implementation path is declared defective merely because it was unexecuted.
- Impact: the candidate cannot complete the mandatory QA gate. Native preflight and trials remain unperformed.

## Reproduction evidence and prerequisites

Historical environment: Windows 10.0.26200 x64, PowerShell 7.6.6, rustc/Cargo 1.97.1, rustfmt 1.9.0-stable, Clippy 0.1.97, cargo-llvm-cov 0.8.4. Current tools must be rediscovered before a new assignment; no installation is implied.

Historical working directory: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.

Historical executable: `C:\Users\bryan\.cargo\bin\cargo.exe` (rustup proxy). Historical argv was `llvm-cov --locked --offline --all-targets --json --output-path C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260915T2325371896643Z\08a-coverage\coverage.json`. Environment overrides were `CARGO_TARGET_DIR=C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260915T2325371896643Z\target-coverage` and `WF_TEST_EVIDENCE=C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260915T2325371896643Z\08a-coverage\fixtures`. The outer bound was 360 seconds; actual duration was 169.578 seconds, exit 0. **These are historical values, not an instruction to overwrite them.**

Exact argv/cwd/environment/exits/stream hashes are in that campaign's `08a-coverage\receipt.json`. The raw JSON SHA-256 is `271212ab24ab2939f4a595103c9978c2d451dc826fecfe341da06d5d4c3dc3b8`. `09-coverage-analysis\stdout.bin` binds all 12 declared source files, 11 with executable lines, and 160 retained raw profiles. Test data is the frozen candidate's unit/integration suite and bound fixture sources; their generated observations remain under the historical fixture directory. Root independently recalculated this result from retained JSON; no additional product measurement ran after the stop.

For a new authorized campaign: verify current manifest and specifications; discover native tool versions; declare the new source/case denominator; allocate fresh, nonexisting evidence/target/fixture locations; run the same complete collection scope against the new frozen candidate; retain every terminal outcome. Never reuse the historical output paths or replace the original failure. The first `08-coverage` recorder setup failure launched no Cargo process and is separate from the single successful complete collection.

## Required correction and regression

Add meaningful tests for unexecuted requirement behavior, especially effective-profile rejection/validation, inventory bounds/drift and complete runner/preflight orchestration. Use independent expected values and actual compiled CLI/process boundaries for integration requirements. A test that legitimately exercises already-correct behavior may pass on first run; do not invent a behavioral Red. If a new test reveals a product defect, preserve valid Red and follow Green/refactor/QA for the minimum authorized correction.

Preserve original WF-01..20/all subfixtures, F-01/F-02, identity/review admission, strict source immutability, typed error privacy, no-work preflight, process ownership/deadlines/cancellation and cleanup. No weakened assertions, copied-product oracles, skipped production code, duplicate passing cases, threshold changes or result-erasing retries.

Required return: corrected source/build identity, changed-file manifest, case-to-requirement map, relevant Red/Green/refactor receipts, full regression/static results, current coverage and required-case denominators/raw reports, remaining gaps, and `QA-F-COV-01` resolution map. Development can report **FIX_REPORTED** with evidence; only an explicitly selected independent retest can establish **VERIFIED_FIXED**. That retest must reassess integrity, complete invalidated metrics and affected negative/regression behavior on the returned frozen bytes. A persisting failure is REOPENED with new preserved evidence.

## Stopped work and independent prerequisites

No product work was in flight at the terminal stop; the recorded command handles completed. The frozen candidate and nine bound inputs still match current source in `readback.json`. No cleanup or replay was performed in this continuation.

Final-candidate live source collection, NI-T05's actual prelaunch observation, NI-T09/T10 installed profile observations, WN-01/WN-02 and the additional QA-authored F-02/evidence probes remain NOT_RUN/BLOCKED with stop trigger QA-F-COV-01. Both native trial counters remain zero. The separately observed development-time `chrome/latest` reparse and source-bound operator profile review remain prerequisite decisions. No cache omission, link/configuration edit or assumption of native inactivity is authorized. Native trials retain their existing selected model/version/effort and one-shot limits.

Protected authority remains deferred; framework acceptance is NOT_EVALUATED and is not established.

## End-user invocation and artifact binding

Open the same Windows workspace and use the complete fenced conversation prompt in [dev-invocation.md](dev-invocation.md). It is a proposed separate assignment, not an OS command or automatic dispatch. `handoff-manifest.json`, entries `qa_report`, `qa_fix`, `dev_invocation`, and `identity_readback`, bind required/actual paths and final hashes without a circular digest.
