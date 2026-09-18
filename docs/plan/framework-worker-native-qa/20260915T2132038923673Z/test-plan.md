# Independent QA Test Plan

## Identity, selection and authorization

- Plan/run identity and invocation intent: `framework-worker-native-qa/20260915T2132038923673Z`; ordinary full `run`, paused before executable work by the root-agent concurrent-Cargo hold.
- Automatic-continuation eligibility and basis: continue without a second user selection after the root agent confirms that the developer Cargo/coverage process has ended. All selected QA effects are local builds, test instrumentation, synthetic fixtures, and fresh evidence already authorized by the assignment.
- Execution status: `NOT_STARTED`. No Cargo command, product test, Codex process, login, credential read, configuration change, installation, native trial, or authority operation has been launched by QA.
- Planning status: `NEEDS_INPUT` only for the temporary root-agent Cargo greenlight. Candidate identity, selected requirements, independent oracles, output paths, and allowed effects are otherwise resolved.
- Project identity, host, shell and filesystem: `C:\Projects\DevForgeAI`; Windows-native PowerShell; candidate on the native `C:` NTFS checkout. Exact OS/tool versions will be recorded by `QA-ENV-01` before build execution.
- Selected scope: independent Windows QA of the frozen exact-executable-identity and schema-version-2 fail-closed intake slice in `devforgeai\experiments\codex-worker-probe`, plus preservation of all original offline tests/regressions and fresh full-source coverage.
- Specification inputs:
  - `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-feasibility-v1.md`, expected SHA-256 `7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23` from the development input manifest; QA will rehash before execution.
  - `C:\Projects\DevForgeAI\docs\specs\framework\runtime\codex-worker-native-readiness-v1.md`, expected SHA-256 `c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d`; QA will rehash before execution.
  - `C:\Projects\DevForgeAI\AGENTS.md` and `C:\Projects\DevForgeAI\docs\prompt\qa.md` as repository and QA rules.
- Candidate identity: developer manifest `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-implementation\20260915T2118427272409Z\candidate-manifest.json`, SHA-256 `73ecd4a115b34f824e3e9eef3083866d89c5715cf0053919f9456ee8a4bbb7a8`, 36 entries. QA readback at planning time found all 36 paths, byte counts, and SHA-256 values matching.
- Build/package identity and source correspondence: no QA build exists yet. Each build/test receipt will recheck the 36-entry manifest before and after execution and bind resulting executable hashes.
- Dependencies/locks: standalone package `Cargo.toml` and `Cargo.lock` are in the 36-file candidate. Offline locked resolution is required. No dependency installation or lockfile regeneration is authorized.
- Development handoff and supplied claims: `docs\plan\framework-worker-native-implementation\20260915T2118427272409Z\context.md` is ownership context only. Developer-reported formatting/Clippy results and the in-flight 62-test coverage run are not independent QA evidence and will not be reused as QA results.
- Requested effects and authorization: read source and machine identity, create QA evidence, use QA-owned synthetic files/junctions, compile/test the frozen package offline, and collect coverage into fresh QA output. Candidate source, developer tests, historical evidence, installed Codex, operational copies, user configuration, credentials, and startup settings are immutable.
- Explicit exclusions: no Codex/app-server launch; no WN-01/WN-02; no login/logout/read-credentials; no `CODEX_HOME`, config, plugin, MCP, hook, model, provider, policy, installation, or startup change; no authority implementation/decision; no Linux/tray qualification.

## Output and checkpoint binding

- `selected_evidence_value`: `docs/plan/framework-worker-native-qa/<fresh timestamp>/`, supplied by the assignment.
- Resolved evidence root: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-qa\20260915T2132038923673Z`.
- Role-to-path map:
  - plan: `test-plan.md`
  - candidate checkpoint: `candidate-binding.json`
  - QA helper source: `qa-identity-harness\` or `qa-independent-copy\tests\support\identity_cases.rs`, finalized and inspected before use
  - environment/tool receipt: `environment.json`
  - case receipts/logs: `receipts\`
  - exact-Cargo target: `target\`
  - raw coverage: `coverage.json`
  - normalized coverage assessment: `coverage-assessment.json`
  - test inventory/results: `test-inventory.json` and `test-results.json`
  - findings: `findings.json`
  - QA report/fix/checkpoint: `qa-report.md`, `qa-fix.md` only on FAIL, and `checkpoint.json`
  - final noncircular bindings: `artifact-manifest.json`
- Plan digest binding: the final SHA-256 of this plan will be stored in `artifact-manifest.json`; a self-hash is deliberately absent.
- Checkpoint and next safe action: wait for root Cargo greenlight, revalidate candidate/spec identities, discover tools, finalize and inspect QA-owned helper bytes, then execute READY cases in stop-rule order.

## Acceptance inventory and risks

| Source-qualified criterion | Required behavior | Mandatory | Cases | Independent oracle | Current readiness |
| --- | --- | --- | --- | --- | --- |
| Native amendment NI-01.1 | Only the pinned physical executable path/digest is admitted; alias is never launched; no path fallback | yes | `QA-NI01-A`, `QA-NI01-B` | specification constants, direct filesystem identity, independent hashes, no process creation | READY after Cargo hold |
| Native amendment NI-01.2 | Exactly two specified directory junctions, exact targets/type/order; reject target/type/reparse substitution and another location with same bytes | yes | `QA-NI01-A`, `QA-NI01-C` | Windows reparse observations plus QA-owned synthetic chains and outside sentinels | READY after Cargo hold |
| Native amendment NI-01.3 / NI-T05 | Recheck mapping and bytes immediately before spawn; drift rejects before spawn and preserves evidence | yes | `QA-NI01-D1`, `QA-NI01-D2` | independently changed synthetic bytes/target for library recheck; real pre-spawn path requires qualified NI-02 | D1 READY; D2 BLOCKED |
| Native amendment NI-01.4 / NI-T04 | Fixture/run/review/profile paths retain strict reparse rejection, including through approved launcher junctions | yes | `QA-NI01-C`, `QA-REG-01` | QA-owned reparse roots and sentinels; original negative tests | READY after Cargo hold |
| Native amendment NI-02 schema compatibility | Schema 2 is native-only and closed, requires both policy identity fields; v1 native and v1 peer behavior remain distinct | yes | `QA-S2-01`, `QA-S2-02` | independently authored JSON variants and exact parser outcomes | READY after Cargo hold |
| Native amendment current maturity | Because policy/version/effective behavior is unqualified, schema-2 review/launch fails closed before any spawn | yes | `QA-S2-03` | all-true but unqualified review must yield exit 3 `profile_unqualified`, with no `spawn_intent`/`server_started` and no child process | READY after Cargo hold |
| Native amendment NI-T06 and base section 8 | WF-01..20 and all original supplemental/regression/F-01/F-02 behavior remain valid | yes | `QA-REG-01` | fresh exact-candidate `cargo test --all-targets`; developer claims are not reused | READY after Cargo hold |
| Base section 9 and AGENTS | Executed first-party line coverage and required test pass rates are each at least 95%; all mandatory cases pass | yes | `QA-MET-01` | fresh LLVM JSON, normalized paths, inventory-bound arithmetic | READY after Cargo hold |
| Native NI-T07..10 | Restrictive argv, policy/version, effective integration inactivity, and complete profile preflight | yes for full readiness | `QA-BLOCK-POLICY` | pinned-version key/effective behavior proof | BLOCKED: policy is deliberately unimplemented/unqualified |
| Native NI-T11..12 / WN-01..02 | Real native completion/cancellation with qualified profile and stopped tree | yes for native qualification | `QA-BLOCK-NATIVE` | actual native trial only | NOT_RUN/BLOCKED; no native execution authorized |
| Compiled-Rust authority | Qualified authority independently accepts evidence | separate requirement | `QA-BLOCK-AUTH` | actual qualified authority decision | NOT_EVALUATED/NOT_RUN; authority prerequisite absent |

- Inventory completeness: the selected executable slice covers NI-T01 through NI-T06, schema-2 fail-closed behavior, original offline inventory, test integrity, formatting/static analysis, and coverage. NI-T07 through NI-T12 remain explicitly accounted for as blocked outside the executable slice.
- Ambiguity: no ambiguity is resolved by QA. The policy specification itself says its concrete argv is proposed and not qualified; QA will not invent approved arguments.
- Principal risks: machine-specific identity drift; a test seam passing while the real runner pre-spawn path is unreachable; coverage misclassifying `src/../tests/support/identity_cases.rs`; schema-2 values being accepted by deserialization but accidentally authorizing launch; original regression loss.

## Environment and capability matrix

| Platform | Tools | Capability | Effects | Readiness |
| --- | --- | --- | --- | --- |
| Windows x86_64, native `C:` checkout | `rustc`, `cargo`, `rustfmt`, `clippy`, `cargo-llvm-cov`, PowerShell; exact versions pending `QA-ENV-01` | offline locked build/tests, Windows junction/Job Object tests, LLVM coverage | QA-owned target, logs, temp/synthetic fixtures only | READY after concurrent-Cargo hold |
| Installed Codex 0.154.0 identity | filesystem/read-only metadata and SHA-256 only | identity observation; no `--version` or app-server launch is needed for QA identity proof | none | READY |
| Native Codex profile/model | intentionally unavailable for this campaign | WN-01/WN-02 and real NI-T05 pre-spawn effect | prohibited | BLOCKED |
| Compiled authority | not supplied/qualified | framework acceptance | none | NOT_EVALUATED |

## Required case inventory

| Stable case ID | Category | Criteria | Platform | Provenance | Readiness |
| --- | --- | --- | --- | --- | --- |
| `QA-ID-01` | setup | exact candidate/spec identity | Windows | independent QA | READY |
| `QA-ENV-01` | setup | host/tool binding | Windows | independent QA | READY after Cargo hold |
| `QA-INT-01` | integrity | mock-decorator/result-gaming inspection | Windows/source | independent QA | READY |
| `QA-NI01-A` | static/filesystem | NI-01 exact compiled record and actual mapping | Windows | independent QA | READY |
| `QA-NI01-B` | compiled library | exact physical identity, wrong digest/adapter/alternate path | Windows | independent QA | READY after Cargo hold |
| `QA-NI01-C` | compiled filesystem | exact synthetic chain; changed target/type/order, loop, extra reparse, strict other-path rejection | Windows | independent QA | READY after Cargo hold |
| `QA-NI01-D1` | compiled filesystem | synthetic repeated verification catches byte/target drift | Windows | independent QA | READY after Cargo hold |
| `QA-NI01-D2` | native pre-spawn | actual runner second check prevents a native spawn | Windows/native Codex | independent QA | BLOCKED by NI-02; must not be inferred from D1 |
| `QA-S2-01` | parser | valid exact-identity schema 2 intake only | Windows | independent QA | READY after Cargo hold |
| `QA-S2-02` | negative parser | peer-v2, v1 policy extension, missing/null/unknown/injected policy fields | Windows | independent QA | READY after Cargo hold |
| `QA-S2-03` | compiled runner fail-closed | unqualified schema 2 never spawns | Windows | independent QA | READY after Cargo hold |
| `QA-REG-01` | regression | complete frozen 62-test inventory, including WF/F-01/F-02 | Windows | developer tests independently executed by QA | READY after Cargo hold |
| `QA-QUAL-01` | format/static | rustfmt and Clippy `-D warnings` | Windows | independent QA | READY after Cargo hold |
| `QA-MET-01` | coverage/metrics | exact source denominator and declared test inventories | Windows | independent QA | READY after Cargo hold |
| `QA-BLOCK-POLICY` | policy/native readiness | NI-T07..10 | Windows | required future evidence | BLOCKED |
| `QA-BLOCK-NATIVE` | native | NI-T11..12/WN-01..02 | Windows | required future native evidence | NOT_RUN/BLOCKED |
| `QA-BLOCK-AUTH` | authority | protected framework acceptance | Windows | qualified Rust authority | NOT_EVALUATED |

### Procedures and oracles

- `QA-ID-01`: hash the two specifications and candidate manifest; recalculate all 36 candidate byte counts/hashes. Any drift stops affected execution as `EXECUTION_SAFETY_BLOCKER`.
- `QA-INT-01`: enumerate every in-scope Rust attribute/import/dependency/macro path and inspect assertions, early returns, ignored/skipped tests, evidence counting, and coverage exclusions. Search is only a locator; source resolution is required. Any confirmed mock decorator or result gaming is terminal `INTEGRITY_FAILURE`.
- `QA-NI01-A`: compare the compiled JSON record to the selected constants; query each exact reparse point without following arbitrary caller paths; verify junction tag/targets/order, alias resolution, physical file size/hash, and that no process was started.
- `QA-NI01-B/C/D1`: use a QA-owned disposable package copy that preserves every frozen `src/` byte and replaces only the existing `#[cfg(test)]` helper at `tests/support/identity_cases.rs` with independently authored cases. This uses the candidate's existing private-test seam without changing production source. Fixtures use unique QA-owned directories, exact Windows junction creation, independent sentinel/hash checks, and explicit cleanup limited to QA-owned reparse points.
- `QA-S2-01/02`: use a separate QA test harness with the frozen package as a path dependency for public parser behavior. Expected accept/reject classes come from the amendment, not the implementation. Invalid cases assert exact error class and absence of run/process effects.
- `QA-S2-03`: create one unique synthetic fixture at the product-mandated `docs/plan/framework-worker-trials/<qa-run-id>/fixture` path, provide a closed all-true but unqualified schema-2 review, run only the local harness, and require exit 3/reason `profile_unqualified`, no spawn records, no child process, unchanged fixture, and retained evidence. The physical Codex is identified but never launched.
- `QA-REG-01`: after exact identity recheck, run `cargo test --locked --offline --all-targets` from the package root with `CARGO_TARGET_DIR` under this QA root and retained stdout/stderr/exit status. The declared frozen inventory is 62 unique Rust test functions: 9 library unit tests and 53 integration tests. All original 50 plus 9 private identity tests and 3 new integration tests are required; no retry changes the denominator.
- `QA-QUAL-01`: run fresh `cargo fmt --all -- --check` and `cargo clippy --locked --offline --all-targets -- -D warnings`; keep developer results separately as supplied evidence.
- `QA-MET-01`: run a fresh exact-candidate `cargo llvm-cov --locked --offline --all-targets --json --output-path <QA-root>\coverage.json` after the test inventory is terminal. Normalize every coverage filename to an absolute resolved path before membership. Include all executable lines in the nine `src/*.rs` files. Exclude test code and fixtures, including any raw spelling such as `src/../tests/support/identity_cases.rs`, only after normalization proves the actual path is under `tests/`. Do not exclude uncovered production behavior.
- Retry rule: zero silent retries. A QA harness setup error may be corrected once within QA-owned evidence while retaining the first attempt and re-inspecting helper bytes. Product failures are not repaired or rerun in this campaign. Each required case is counted once.

## Test-integrity inspection

- Scope: all 36 frozen files, with detailed source review of changed `src/native_identity.rs`, `src/request.rs`, `src/runner.rs`, `src/native-executable-identity.json`, `tests/native_identity.rs`, `tests/support/identity_cases.rs`, `src/lib.rs`, and manifest-defined evidence accounting.
- Planning-time observation: Cargo dependencies contain no mocking framework or proc-macro test-double package. Enumerated Rust attributes in the frozen tree are `test`, `derive`, `serde`, `cfg(test)`, and `path`; no mock decorator mechanism was observed. This remains a preliminary inspection until the freeze-bound inventory/readback is retained.
- Existing changed tests contain behavioral assertions for exact accepted paths, exact error class, no run directory before runner use, no spawn/server-start event, junction setup success, hash equality for the alternate path, and drift rejection. They are developer-provided evidence and do not replace the independent QA cases above.
- The included `#[path = "../tests/support/identity_cases.rs"]` is a private test seam. Its lines are test code even if LLVM reports a lexical path beginning with `src/..`; normalized membership controls exclusion.
- No clean integrity conclusion will rely on text search alone. Unresolved dynamic/procedural macro behavior would leave affected claims INCOMPLETE.

## Metrics and accounting declared before execution

- Executed-line source denominator: every LLVM executable region in `src/journal.rs`, `src/lib.rs`, `src/main.rs`, `src/native_identity.rs`, `src/oracle.rs`, `src/process_windows.rs`, `src/protocol.rs`, `src/request.rs`, and `src/runner.rs`. `src/native-executable-identity.json` is data. `lib.rs` may contribute zero executable lines but remains in the inventory.
- Exclusions: third-party/generated dependency code and resolved files under `tests/` (test drivers, support, fixtures). There are no first-party production exclusions.
- Required unit-test denominator: 9 frozen library unit tests under `native_identity::tests`; each skipped, errored, failed, blocked, or unexecuted required unit test is a nonpass once the complete unit collection is terminal.
- Required project-wide Rust test denominator: 62 unique frozen test functions, reported separately from the unit ratio. Required offline WF denominator remains 20 parent cases, with every required subfixture passing for its parent to pass. Original regression inventory remains 50 unique functions.
- Independent QA case denominator: 9 executable QA groups (`QA-NI01-A/B/C/D1`, `QA-S2-01/02/03`, `QA-REG-01`, `QA-QUAL-01`) plus setup/integrity and coverage obligations reported separately. `QA-NI01-D2`, policy, native, and authority rows remain blocked/NOT_RUN and prevent a full native-readiness PASS.
- Collection completion: coverage is valid only after all 62 exact-candidate tests contributing to it have terminal results and LLVM emits usable JSON for the complete nine-file source inventory. Partial/crashed collection has no final percentage.
- Floors: executed-line coverage >=95%, required unit-test pass rate >=95%, project-wide required test pass rate >=95%, and all mandatory WF/identity/security cases passing. A valid completed subthreshold result triggers immediate terminal stop.
- Branch coverage: report separately only if the installed collector provides it without unapproved options; absence is `NOT_RUN`, not line-coverage failure.
- Current measurements: `NOT_RUN`. Developer measurements are not QA measurements.

## Stop classification and final disposition rules

- Confirmed mock decorator/result gaming, a valid complete metric below 95%, or a critical authorization/security/data-preservation defect stops the entire campaign immediately. Only containment, safe cleanup, evidence preservation, assessment, and reporting follow.
- Ordinary mandatory failures retain final `FAIL` while safe independent checks continue. Candidate drift or unsafe ownership blocks affected checks and yields `INCOMPLETE` unless another confirmed failure establishes `FAIL`.
- A passing offline identity/fail-closed slice cannot qualify NI-T07..12, WN-01/02, a real NI-T05 pre-spawn effect, or protected framework acceptance.
- Product verdict for the overall selected native-readiness specification cannot be `PASS` while those mandatory prerequisites remain unresolved. The final report will distinguish the bounded offline slice result from overall `INCOMPLETE`/`FAIL`.
- Source/plan drift policy: stop, retain attempts, compare the changed path to the frozen 36-entry manifest, and request a new candidate freeze; never silently rebind.
- Framework acceptance: `NOT_EVALUATED`. Release/deployment authorization: not granted.
