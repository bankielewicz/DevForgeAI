# PARTIAL — native executable identity delivered

The executable-identity and schema-v2 intake increment is implemented and independently tested. The full native-readiness plan remains **INCOMPLETE**: 5/12 required NI criteria are satisfied, **41.6666666667%**, below the 95% floor. No full-readiness PASS or framework acceptance is claimed.

## Delivered candidate

`C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`

36-file candidate manifest SHA-256: `73ecd4a115b34f824e3e9eef3083866d89c5715cf0053919f9456ee8a4bbb7a8`. Final readbacks matched all 36 files. No Git metadata exists. Candidate bytes are retained in `candidate-snapshot/`; `changes.json` identifies four modified and four added files, with no removed files.

Rust now verifies the exact selected physical Codex executable, its digest, and both pinned directory-junction types and targets. It rejects alternate paths, changed targets, symlink substitutions, extra reparses and repeated mappings. Other path restrictions remain intact.

Schema-v2 native intake requires both policy identity fields and rejects schema-v2 peers, incomplete/null/unknown fields and injected arguments. Legacy v1 behavior remains unchanged. **All v2 reviews remain unqualified**, so even a synthetic all-true review returns `profile_unqualified` without spawning Codex. No restrictive policy argv is enabled.

## Verification

Required platform: native Windows x86_64, this C: NTFS checkout; PowerShell7.6.6 and Rust/Cargo1.97.1. No Linux or tray qualification is selected.

| Check | Developer | Independent QA |
| --- | --- | --- |
| Frozen project test functions | 62/62, 100% | 62/62, 100% |
| Original WF parent cases | 20/20, all required subfixtures | 20/20, all required subfixtures |
| Additional independent compiled cases | separate QA responsibility | 7/7, 100% |
| Executed first-party lines | 1543/1602, 96.3171036205% | 1542/1602, 96.2546816479% |
| Formatting and Clippy | PASS | PASS |
| Branch coverage | NOT_RUN | NOT_RUN |

All eight executable production source files are included; `lib.rs` contains only module declarations. No uncovered production source was excluded. Developer documentation-test execution succeeded with zero doctests present, and does not add passing cases. All builds/tests used the existing offline dependencies and lockfile.

Independent QA found **no confirmed product defect** in the executed scope. It retained one QA-only path-spelling oracle error and the corrected attempt. Development separately retained its original valid intake red result, repeated-junction rejection red result, and mklink fixture setup failures. None of these attempts was erased or used to inflate the required-case denominator.

Independent QA has an evidence-retention limitation: some command receipts are partial terminal transcriptions or summaries, rather than complete raw stdout/stderr. The raw LLVM coverage JSON is retained and supports its measured coverage. Missing console/native-exit/timing metadata must stay explicitly unretained; the gap does not become invented evidence. The independent report records this limitation. Developer commands retain separate raw stdout/stderr and structured command/source/exit/duration receipts.

## Remaining requirements

- **NI-T05:** synthetic repeated verification catches drift, but the actual native admission-to-pre-spawn branch is unexecuted because the profile gate remains closed.
- **NI-T07–T10:** the restrictive policy and effective profile remain unqualified. Pinned local probes establish parsing/feature state, but do not prove inactive hooks, plugins, MCP servers or apps in a running app-server. The original proposal lacks thirteen additional feature disables.
- **NI-T11/T12 (WN-01/WN-02):** already conditionally selected by the user, but prerequisite-blocked and NOT_RUN. No native completion or cancellation result is claimed.
- **Acceptance authority:** deferred under the selected native-first plan; no provisioning or protected decision occurred. Framework acceptance is **NOT_EVALUATED and not established**.

The ready identity/offline NI group is 5/6 complete (83.3333333333%) when NI-T05 is counted in full; the full selected readiness denominator remains 5/12. The passing test-function and line-coverage rates do not waive either gap.

## Evidence and continuation

- [Detailed development handoff](handoff.md): requirement matrix, retained attempts, exact next dependency and selected native limits.
- [Independent QA report](../../framework-worker-native-qa/20260915T2132038923673Z/qa-report.md): scope-qualified INCOMPLETE verdict, results, gaps and source readback.
- [Profile compatibility research](profile-research/compatibility.md): 17 bounded non-session probe receipts and pinned protocol-schema references.
- [Revised policy proposal](restrictive-launch-policy.next-proposed.json): adds the thirteen missing feature disables, with a new policy ID; remains PROPOSED_NOT_RUNTIME_QUALIFIED_DO_NOT_LAUNCH.
- `candidate-manifest.json`, `metrics.json`, `coverage.json`, `post-execution-source-readback.json`, `evidence-manifest.json`, and `compiled-and-raw-coverage-manifest.json` bind source, measurements and retained artifacts.

Next work is a bounded, typed pre-thread qualification contract and compiled preflight, followed by implementation/independent QA of the qualified policy and review-v2 binding. Then execute the already selected WN-01/WN-02 once each using `gpt-6-astra`/`high`, with the selected limits and no automatic retry or substitution. The policy proposal, Python inventories and this delivery report grant no execution or acceptance authority.
