# Rust native-denial diagnostic development delivery

Development status: **COMPLETE for the selected bounded implementation and independent offline QA handoff**. Independent QA is **NOT_RUN**. No native Codex preflight/trial or installed source collection was launched. Framework acceptance is **NOT_EVALUATED**. The original native failure remains unexplained until a separately selected diagnostic launch.

## Candidate and environment

- Package: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
- Final 58-file manifest: `C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics\20260916T181820Z-dev\candidate-v2-manifest.json`, SHA256 `419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540`. The corresponding candidate-v2-snapshot contains the exact source/test/config/README bytes.
- Original 56-file candidate was preserved in baseline-snapshot and verified against historical manifest `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`. The initial diagnostic candidate and attempts remain preserved separately; only candidate-v2 is delivered for QA.
- Native Windows x64 10.0.26200, PowerShell 7.6.6, C: NTFS; Rust/Cargo 1.97.1, rustfmt 1.9.0, Clippy 0.1.97, cargo-llvm-cov 0.8.4. No Git metadata. No WSL or alternate checkout.
- Built diagnostic executable: `C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics\20260916T181820Z-dev\target\debug\devforgeai-codex-worker-probe.exe`, SHA256 `54ecb9ce6967b941e60139c418b5b7995a30df8d9d2e670b5f788b8090adf7c8`, 2307584 bytes. This is a development artifact, not an approved native-launch selection or installation.

## Implemented behavior and traceability

| Requirement | Implementation and evidence | Development result |
| --- | --- | --- |
| D1 / handoff 1: derive closed non-sensitive contract before implementation | diagnostic-contract-initial.md; final diagnostic-contract.md; typed Rust enums in diagnostic.rs | PASS |
| D2a / handoff 2: post-spawn source verification stage | runner/Session source_review observations at post_spawn and post_preflight; real missing-review verifier tests and dispatch wiring | PASS, offline scope |
| D2b / handoff 2: initialize/config process accounting | one existing held-job query returns total/active; exact 1/1 success, 2/1 exited-descendant rejection, 1/0 stopped-worker rejection; initialize/config/checkpoint tags | PASS |
| D2c / handoff 2: closed config rejection categories | same validator, same predicate order/values; section/predicate markers; 22 literal mutation cases, missing/duplicate session-layer and path/precedence subfixtures | PASS |
| D2d / handoff 2: privacy and failed RPC stage | closed serialized events; sentinel/unknown-field tests for config, layer, origin, RPC errors and server requests; no untrusted values in diagnostic constructors | PASS |
| D3a / handoff 1,3: preserve denial, all-false review, fixed launch, identities, cleanup and no-work behavior | unchanged protected source/data bindings; all original 123 tests plus ten diagnostic tests; source checks fail closed; actual local process and journal tests | PASS |
| D3b / handoff 3: regression, negative paths, format, Clippy, full first-party coverage and both floors | final attempts listed below, all bound to final manifest | PASS |
| D4 / current user: independent offline QA handoff and exact readback | qa-handoff.md, final-readback.json, artifact-index.json | Prepared; independent QA NOT_RUN |
| Deferred / handoff 4,5 | fresh native fixture/request/review/inventory digests, separate single no-work launch selection, then use observed predicate to classify issue | NOT_RUN; requires separate selection after independent QA PASS |

Changed/added package files (nine existing files, two new files):

- `README.md`
- `src/diagnostic.rs`
- `src/effective_profile.rs`
- `src/lib.rs`
- `src/process_windows.rs`
- `src/protocol.rs`
- `src/runner.rs`
- `tests/effective_profile.rs`
- `tests/profile_protocol.rs`
- `tests/support/diagnostic_cases.rs`
- `tests/support/profile_peer.rs`

No policy, source/executable identity record, Cargo manifest/lock, request/review predicate, baseline fixture, journal schema, operational installation, credential setting, startup setting or qualification threshold was changed. Final pre-spawn ordering and terminal cleanup/error mapping remain intact. The diagnostic label correction RC-01 does not change result strings.

## Exact validation

All commands ran from `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe` using `C:\Users\bryan\.cargo\bin\cargo.exe`. Attempts record scoped CARGO_TARGET_DIR, per-attempt CARGO_LLVM_COV_TARGET_DIR and WF_TEST_EVIDENCE; all other environment variables were inherited, and no credential values were collected or changed. The final normal and coverage campaigns used separate targets/fixtures and overlapped; both completed without failures.

| Attempt | Exact Cargo command | Exit | Elapsed |
| --- | --- | ---: | ---: |
| 19-final-clippy | `cargo clippy --locked --offline --all-targets -- -D warnings` | 0 | 1.031 s |
| 20-final-inventory | `cargo test --locked --offline --all-targets -- --list` | 0 | 5.984 s |
| 21-final-offline | `cargo test --locked --offline --all-targets` | 0 | 164.953 s |
| 22-final-coverage | `cargo llvm-cov --locked --offline --all-targets --json --output-path C:/Projects/DevForgeAI/docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/final-coverage.json` | 0 | 174.625 s |
| 23-final-fmt-check | `cargo fmt --all -- --check` | 0 | 0.281 s |
| 24-final-doc-tests | `cargo test --locked --offline --doc` | 0 | 0.281 s |
| 25-final-build | `cargo build --locked --offline --bins` | 0 | 0.125 s |

- Required complete suite: **133/133 (100%)**, including **40/40 unit tests**, original WF-01..WF-20 and subfixtures, offline NI/SI cases, F-01/F-02 and ten added diagnostic tests. Zero failed/errored/skipped/ignored/unexecuted required tests in the final candidate campaign. The instrumented campaign independently executed the same 133/133; it does not double the denominator.
- Full first-party executed-line coverage: **3335/3497 = 95.36745782098941950243065485%**, floor 95%. All 13 src/*.rs files are accounted for, lib.rs 0/0; zero first-party exclusions. Raw final-coverage.json and final-coverage-analysis.json bind each file/count.
- Branch coverage: **NOT_RUN**; no branch floor was selected. Documentation tests: command passed with **0 discovered**, not invented documentation coverage.
- Red/Green: attempts 01/03 demonstrate initial absent diagnostics then the corrected exact-count Green; 16/17 demonstrate the misleading generic RPC label then its correction. Refactor was rustfmt only; current all-target campaigns reran affected code. Initial 02 and 05 fixture/oracle mistakes remain documented in review-notes.md, not concealed as product defects or successful Red results.
- Final code/test review found no ignored/should_panic/mock framework/coverage-suppression additions. Config/identity/launch predicate comparison and literal output oracles support preservation; this is developer review, not independent QA.

## Limits and remaining work

Independent offline QA must use fresh, disjoint evidence and assess the final frozen bytes. Native installed-profile behavior, Pro authentication, gpt-6-astra/high availability, hooks/plugins/apps/MCP/network isolation and custom-provider runtime behavior remain unqualified. WN-01/WN-02 remain 0/2 NOT_RUN here. Local synthetic peers are not Codex trials. Accounting-query OS failure is handled with null counts/query_failed but was not forcibly induced; private source-boundary tests do not claim end-to-end native runner execution. No authoritative framework decision was requested or issued.

Only after independent offline QA PASS may a separate task prepare exact fresh fixture/request/all-false review/inventory digests and select one bounded no-work native diagnostic launch. Refresh source bindings after any host permission change. Preserve each attempt; dispatch no thread/turn and generate no true operator findings. Any resulting repair, policy/contract amendment or operational change needs its own selection.

Output destination is the original context-selected `C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics\20260916T181820Z-dev`. Final-readback.json verifies the promised files at this root, 58/58 current/snapshot candidate bindings, all bound input/historical evidence files, and unchanged fixed policy/identity/request sources. Artifact-index.json supplies external report bindings without a self-hash. These Python records summarize observations only; they grant no mutation, phase or framework acceptance authority.
