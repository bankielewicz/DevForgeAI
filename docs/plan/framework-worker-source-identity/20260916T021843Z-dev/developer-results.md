# Developer results: bounded source identity

These are development observations, not independent QA or protected acceptance. The frozen candidate is `devforgeai/experiments/codex-worker-probe`, 56 files, canonical manifest SHA-256 `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`. The snapshot, `changed-files.json`, and `selected-inputs-final.json` bind the delivered bytes and contracts. The plan declared 30 selected required groups before execution: WF-01..20 plus SI-T01..10. Native WN-01/WN-02 remain separately unexecuted.

## Windows results

Native Windows x64, Windows 10.0.26200, PowerShell 7.6.6, C: filesystem; Rust/Cargo 1.97.1, LLVM 22.1.6, rustfmt 1.9.0-stable, Clippy 0.1.97, cargo-llvm-cov 0.8.4. Exact paths/version output are in `01-environment`. No Git metadata, optional package features, new dependencies or installed tools.

| Check | Result | Evidence |
| --- | --- | --- |
| Locked offline build of binaries | PASS | `12-build/receipt.json` |
| rustfmt check | PASS | `11-format-final/receipt.json` |
| Clippy all targets, warnings denied | PASS | `10-clippy-refactor/receipt.json` |
| Full tests | 123/123, 100%; 37 unit + 86 integration, zero failed/ignored | `13-full-tests/stdout.bin`, `receipt.json` |
| Documentation tests | Command PASS; zero tests exist | `15-doc-tests/receipt.json` |
| Full first-party executed-line coverage | 3,191/3,339 = 95.5675351901767%, PASS | `16-full-coverage/coverage.json`, `coverage-summary.json` |
| Required development groups | 30/30, 100% | Matrix below |
| Final candidate/specification readback | Unchanged from freeze | `candidate-readback.json` |
| Installed mapping/control manifest readback | Identical observation bytes | `06-installed-baseline`, `17-installed-final` |

Both baseline and final installed observation stdout have SHA-256 `fb6ff2c9a920d217d444ebb82fc094abd769d778c86de903a1eca7c22b465c59`. This binds fixed-level membership, reparse metadata and the selected physical plugin manifest; it does not claim a byte inventory of all plugin payloads or credentials. No installed file was intentionally written. Full coverage includes all 12 `src/*.rs` paths with no first-party exclusions. `lib.rs` contains declarations only (0 executable lines). Tests/fixtures and third-party dependencies are outside the first-party runtime denominator. Branch coverage is NOT_RUN. Instrumented test executions are not extra cases or retries of failing qualifying tests.

Every command receipt records argv, working directory, executable/recorder identity, start/end, duration, native exit code, streams and before/after candidate manifests. Final qualifying commands all returned native exit 0, without timeout. Raw coverage JSON SHA-256 is `3d56e45cb8c7dc4dcecb2c118ee5c5a9f1d18eb186444fcb2b8a68d85d985dd0`; raw profiles and build artifacts remain under the evidence target directory.

## Requirements-to-evidence results

Specification locations are `codex-worker-feasibility-v1.md` mandatory WF matrix and `codex-worker-source-identity-v1.md` SI-01..05. All selected cases require Windows x64/default features. Subfixtures are conjunctive, counted once per row/group. All runtime results below are present in `13-full-tests/stdout.bin`; full coverage reran the same suite.

| Required group | Expected observable result / fixture | Evidence / test | Status |
| --- | --- | --- | --- |
| WF-01..08 (8 groups) | Handshake, permission/auth denial, malformed/correlated messages, denied server requests, failure category and usage counters preserve every contract oracle | `tests/protocol.rs`, `wf_01`..`wf_08` | PASS, 8/8 |
| WF-09..12 (4 groups) | Replay rejection, crash recovery without redispatch, durable terminal/pagination and corrupt evidence classifications | `tests/recovery.rs`, `wf_09`..`wf_12` | PASS, 4/4 |
| WF-13..16 (4 groups) | Real Windows lifecycle/cancel/deadline/process-tree behavior | `tests/process_windows.rs`, `wf_13`..`wf_16` | PASS, 4/4 |
| WF-17..20 (4 groups) | Invalid paths/IDs reject; independent content oracle, fixture/evidence failure and cancellation/cleanup ordering remain enforced | `tests/contract.rs`, `wf_17`..`wf_20` | PASS, 4/4 |
| SI-T01 | Exact synthetic reviewed junction succeeds with physical hashes, complete selected membership and no duplicate bindings | `si_t01_exact_reviewed_junction_reads_physical_sources_once` | PASS |
| SI-T02 | Changed/same-byte/escaping/missing targets reject | `si_t02_changed_same_byte_escaping_and_missing_targets_reject` | PASS |
| SI-T03 | Symlink/wrong tag/ordinary replacement/missing junction reject | `si_t03_wrong_type_ordinary_and_missing_junction_reject` | PASS |
| SI-T04 | Unlisted, loop, additional reparse and wrong-depth aliases reject | `si_t04_unlisted_loop_nested_reparse_and_wrong_depth_reject` | PASS |
| SI-T05 | Changed physical bytes/membership invalidate inventory; retarget during collection fails final OS recheck | `si_t05_physical_bytes_and_indexed_membership_drift_invalidate_inventory` | PASS |
| SI-T06 | Old schema, forged digest/mapping and unknown/duplicate/malformed fields reject | `si_t06_schema_identity_and_mapping_tampering_reject` and closed inventory tests | PASS |
| SI-T07 | Exact physical review bindings required; stale or alias source paths reject | Six `request::review_v2_cases` tests | PASS |
| SI-T08 | Mutation after initial check/intent reaches final check and prevents child creation | `si_t08_changed_source_after_intent_stops_before_real_process_creation`, missing-review cases | PASS |
| SI-T09 | Existing bounds, credentials, strict paths, native identity/policy and F-01/F-02 regressions retained | All remaining unit/integration tests, including `tests/remediation.rs` and protocol preflight suites | PASS |
| SI-T10 | Candidate/selected inputs unchanged after freeze; only enumerated development changes; installed observation preserved | `changed-files.json`, `candidate-readback.json`, installed before/after receipts | PASS |

Private synthetic policy values exercise actual Windows junction/path operations without editing the installed cache. The SI-T08 private digest callback tests runner ordering; the public production entry always supplies the fixed full review/identity checker. This is component evidence, not actual Codex profile or native-launch proof. The all-targets suite builds the real protocol peer before those tests. Do not run focused library tests without the documented peer build prerequisite.

## Preserved development failures and limitations

- Collector `red-001` and runner `02-runner-red` were setup errors, not behavioral Red. Corrected fixture setup did not weaken assertions. Collector `red-002` and runner `04-runner-red` retain valid expected pre-repair failures; corresponding Green observations passed.
- Child compile attempts and its focused-library missing-peer setup failure remain under `profile-sources-dev`. The final all-targets run satisfies that prerequisite and passed. Added post-collection retarget coverage was part of the collector slice; no separate Red is claimed for that later subfixture.
- `09-clippy` preserves three style failures; minimal borrow/iterator refactoring preceded the final passing Clippy and full tests.
- Discovery retains descriptions of an early PowerShell parse error and unavailable Rust metadata method, but not their original complete console bytes/source revisions. The decisive discovery metadata and Rust directory-type observation were freshly captured in `06-installed-baseline` and `14-role-observation`. This limitation does not affect raw qualifying build/test/coverage outputs.
- Source collection against the installed profile, compiled effective-profile preflight, human findings and WN-01/WN-02 have not been executed in this development campaign. Independent QA must pass before the selected source observation. Native trial count is 0/2; no native success is inferred.
- Authority implementation/provisioning is outside this amendment. Framework acceptance is NOT_EVALUATED and not established.

The independent assessment is recorded separately under `docs/plan/framework-worker-source-identity-qa/20260916T021843Z-retest`; its verdict controls the selected continuation prerequisite. This file records the completed developer checks and does not predict that verdict.
