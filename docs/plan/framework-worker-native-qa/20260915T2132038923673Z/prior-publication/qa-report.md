# Independent QA Report: Codex Worker Native Identity Slice

## Verdict

**INCOMPLETE** for the selected native-readiness specification.

The executed narrow Windows offline slice passed: exact executable identity, schema-2 closed intake and fail-closed profile handling, all original WF/regression cases, formatting, Clippy, and executed-line coverage met their declared requirements. Full native readiness cannot pass because only 5 of 12 NI groups are satisfied: **41.666666666666664%**, below the mandatory 95% required-case floor when blocked and unexecuted groups count as non-passes. NI-T05's real native pre-spawn path is not reachable, NI-T07 through NI-T10 remain blocked on policy/profile prerequisites, NI-T11 and NI-T12 (WN-01/WN-02) remain conditionally selected but blocked on those prerequisites, and protected compiled-Rust authority acceptance was not evaluated.

No confirmed product defect was found in the executed scope. No product repair or QA fix packet is proposed.

## Binding and environment

- QA run: `20260915T2132038923673Z`
- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`
- Frozen candidate manifest: `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-implementation\20260915T2118427272409Z\candidate-manifest.json`
- Manifest SHA-256: `73ecd4a115b34f824e3e9eef3083866d89c5715cf0053919f9456ee8a4bbb7a8`
- Candidate entries: 36
- Specifications: `codex-worker-feasibility-v1.md` and `codex-worker-native-readiness-v1.md`
- Host: Windows 11 Professional 10.0.26200 x86_64, PowerShell 7.6.6, Windows-native `C:` filesystem
- Toolchain: rustc/cargo 1.97.1, rustfmt 1.9.0 stable, Clippy 0.1.97, cargo-llvm-cov 0.8.4
- Network/install/configuration use: none

The final readback checked all 36 manifest entries after execution: 36 matched by path, size, and SHA-256; 0 mismatched. QA did not change candidate source. The QA-built executable is retained at `target-exact\debug\devforgeai-codex-worker-probe.exe`, 1,718,784 bytes, SHA-256 `627f07916eb2197bcc018420d8fcc9730702db0b3bfdb85625b568263e4d12d3`.

## Declared cases and results

| Scope | Passed | Required denominator | Rate | Result |
| --- | ---: | ---: | ---: | --- |
| Frozen candidate library unit tests | 9 | 9 | 100% | PASS |
| Frozen candidate Rust tests, all test-bearing targets | 62 | 62 | 100% | PASS |
| Original WF-01 through WF-20 parent cases | 20 | 20 | 100% | PASS; all required subfixtures passed |
| Independent QA cases, final corrected harness | 7 | 7 | 100% | PASS (identity 5/5; schema-2 2/2) |
| First-party executable line coverage | 1,542 | 1,602 | 96.25468164794007% | PASS against 95% floor |
| Full declared native-readiness required groups | 5 | 12 | 41.666666666666664% | FAILS 95% floor; overall evidence INCOMPLETE |

The 62-test project result comprises 9 library unit tests and 53 integration tests, with 0 failed, 0 ignored, and 0 measured. Those executed-scope rates stand separately from the full declared readiness denominator. NI-T05 is not satisfied and NI-T07 through NI-T12 are blocked, so they count as non-passes in the required-case formula; the resulting 5/12 rate fails the threshold and cannot support a full-readiness PASS.

## Commands and retained streams

All Cargo commands used `--locked --offline` and serialized tests where applicable.

| Purpose | Exact command | Exit | Evidence |
| --- | --- | ---: | --- |
| Independent identity cases, first attempt | `cargo test --locked --offline --lib -- --test-threads=1` | 1 | `receipts/helper-001.txt` |
| Independent identity cases, corrected QA oracle | `cargo test --locked --offline --lib -- --test-threads=1` | 0 | `receipts/helper-002.txt` |
| Independent schema-2 negatives and fail-closed path | `cargo test --locked --offline --test qa_schema2 -- --test-threads=1` | 0 | `receipts/schema2.txt` |
| Frozen-candidate regression | `cargo test --locked --offline --all-targets -- --test-threads=1` | 0 | `receipts/exact-suite.txt` |
| Format | `cargo fmt --all -- --check` | 0 | `receipts/quality.txt` |
| Static analysis | `cargo clippy --locked --offline --all-targets -- -D warnings` | 0 | `receipts/quality.txt` |
| Coverage | `cargo llvm-cov --locked --offline --all-targets --json --output-path C:\Projects\DevForgeAI\docs\plan\framework-worker-native-qa\20260915T2132038923673Z\coverage.json -- --test-threads=1` | 0 | `receipts/coverage-command.txt`; `coverage.json` |

Attempt `helper-001` retained a real harness error: 4 cases passed and 1 failed because the QA assertion compared the same Windows physical path with and without the `\\?\` extended-path spelling. The QA-only assertion was corrected to resolve the expected path before comparison. Candidate source and expected behavior were unchanged. Attempt `helper-002` then passed 5/5. The failed attempt is not counted as a product failure and is not erased from evidence.

## Requirement traceability

| Requirement | Status | Independent evidence and limit |
| --- | --- | --- |
| NI-T01 | PASS | Exact synthetic two-junction chain and the selected observed native identity admitted only the pinned physical executable; Codex was not launched. |
| NI-T02 | PASS | Changed target/order/reparse kind and same bytes at another physical path rejected. |
| NI-T03 | PASS | Missing physical executable, digest mismatch, invalid worker and unsupported adapter rejected without PATH fallback. |
| NI-T04 | PASS | Extra reparse component and loop cases rejected using QA-owned synthetic fixtures; original fixture/run/profile reparse regressions also passed. |
| NI-T05 | NOT_RUN | Synthetic library-level repeated verification detected independent byte and junction-target drift. The full criterion requires the real runner admission-to-pre-spawn path, which remains unreachable while schema-2 profile qualification deliberately blocks before spawn. The synthetic case is not native pre-spawn effect evidence. |
| NI-T06 | PASS | Peer admission, WF-01 through WF-20 with required subfixtures, and original F-01/F-02 remediation regressions all passed. |
| NI-T07 | BLOCKED | No approved pinned-version restrictive argv/policy exists. Schema-2 rejects caller argv/config injection and fails closed. |
| NI-T08 | BLOCKED | The versioned launch-policy/review contract is not qualified; missing, old, null, or mismatched policy fields are rejected. |
| NI-T09 | BLOCKED | Complete effective hook/plugin/MCP/app inactivity and override proof is unavailable. Unknown remains unqualified. |
| NI-T10 | BLOCKED | Exact profile/model/effort/sandbox and credential-risk qualification is incomplete. The supplied all-true synthetic review still returned `profile_unqualified`. |
| NI-T11 / WN-01 | BLOCKED | Trial is conditionally selected, but NI-02/NI-03 prerequisites are blocked. No Codex process or native trial was launched. |
| NI-T12 / WN-02 | BLOCKED | Trial is conditionally selected, but NI-02/NI-03 prerequisites are blocked. No cancellation/native process result exists and no replay was attempted. |
| Protected compiled-Rust authority | NOT_EVALUATED | No qualified authority decision was supplied or invoked. This report is QA evidence, not framework acceptance. |

## Schema-2 fail-closed result

The two independent schema-2 cases proved that schema 2 is closed and native-only: schema-2 peer records, v1 policy extensions, missing/null policy fields, caller argv/config data, and unknown top-level fields were rejected. An exact schema-2 physical identity passed intake only. Even with a synthetic all-true review, the runner returned exit 3 with `blocked/profile_unqualified`, wrote only `admitted` and `terminal` journal records, emitted no `spawn_intent` or `server_started`, retained null `worker_exit`, and left the task fixture unchanged.

The retained fail-closed journal SHA-256 is `a6b2e5f65f743609657f26f07128cff296cae680e8d374343b88940af44016a0`; the unchanged task SHA-256 is `b35366b508eea199c12142a8a4a8d13a083426c35c4b9ebaf9f0ccf168eeab3a`.

## Coverage and integrity assessment

Coverage used the literal package `src` directory as its production denominator. LLVM-reported paths were normalized with `System.IO.Path.GetFullPath` before membership testing, so lexical paths such as `src/../tests/...` resolve outside production. Eight LLVM-reported production files contributed 1,602 executable lines; `src/lib.rs` is the ninth declared source file and has zero executable lines. No first-party executable production file was excluded. Test fixtures and support code were excluded only after normalized-path classification. Branch coverage was **NOT_RUN**.

The test-integrity review found no mock decorator, alias/re-export wrapper, proc-macro test double, skipped/ignored case, constant/vacuous assertion, swallowed failure credited as success, duplicate pass inflation, fabricated success output, or production coverage suppression. `tests/support/mod.rs` uses `allow(dead_code)` only because each integration-test binary consumes a subset of shared fixture APIs. The deterministic Rust peer is an external process with asserted requests, OS handles, exits, journal bytes, sentinels, deadlines, and process-tree state; it is evidence for offline protocol/process behavior and is not credited as native Codex behavior.

## Findings and disposition

- Confirmed product defects: 0.
- Resolved QA harness errors: 1 (`QA-HARNESS-01`), with the failed and passing streams both retained.
- Open prerequisite/evidence gaps: 4 (`QA-GAP-01` through `QA-GAP-04`).
- Source repair: none.
- Full native-readiness required-case rate: 5/12 = 41.666666666666664%, below the 95% floor.
- Full native-readiness acceptance: INCOMPLETE; no PASS is claimed.
- Framework acceptance/release/deployment authorization: NOT_EVALUATED and not granted by this QA run.

## Evidence index

- `test-plan.md`: pre-execution scope, denominator, source inventory, and stop conditions.
- `candidate-binding.json`: initial literal-root and frozen-manifest binding.
- `environment.json`: host and tool versions.
- `test-results.json`: structured counts and NI accounting.
- `coverage.json`: raw LLVM coverage stream.
- `coverage-assessment.json`: normalized denominator and per-file counts.
- `integrity.json`: mock/gaming and boundary review.
- `source-readback.json`: final 36/36 unchanged candidate readback.
- `findings.json`: gaps and resolved harness classification.
- `receipts/`: durable combined command streams.
- `artifact-manifest.json`: hashes and sizes for the final evidence set.
