# PASS for the approved source-identity amendment; INCOMPLETE native qualification

The bounded Rust junction amendment is implemented and independently QA-qualified. Installed-source collection now succeeds. A subsequent no-work preflight created the real pinned Codex process and then denied the effective profile with `profile_unqualified`; it verified process-tree cleanup and an unchanged fixture. Neither WN-01 nor WN-02 ran. Framework acceptance is **NOT_EVALUATED** and is not established.

## Candidate, contract, platform and scope

- Candidate: `C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`, 56 frozen files; manifest SHA256 `3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c`. No Git metadata is present.
- Contracts: `docs/specs/framework/runtime/codex-worker-feasibility-v1.md`, `codex-worker-native-readiness-v1.md`, `codex-worker-preflight-v1.md`, and the approved `codex-worker-source-identity-v1.md`. All four remain unchanged from independent QA.
- Approved scope: one exact reviewed Chrome plugin-cache directory junction; compiled source inventory/review and final identity checks; developer qualification; independent Windows offline QA; installed-source collection and the previously selected native prerequisites. No authority implementation/provisioning is included.
- Platform: native Windows x64 on the selected C: checkout, Windows 10.0.26200, PowerShell 7.6.6; Rust/Cargo 1.97.1, LLVM 22.1.6, rustfmt 1.9.0-stable, Clippy 0.1.97, cargo-llvm-cov 0.8.4. No optional package features. Linux and native tray behavior are outside this experiment's selected scope.
- Actual continuation executable: QA `target-original/debug/devforgeai-codex-worker-probe.exe`, SHA256 `b63a0dfb0a48adfc5977a75d145fa766345a9d948e99b3a5bbdf5d5ce74079b2`. Pinned Codex is physical 0.154.0, SHA256 `be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde`.

See the [developer delivery](../../framework-worker-source-identity/20260916T021843Z-dev/delivery.md) and [independent QA report](../../framework-worker-source-identity-qa/20260916T021843Z-retest/qa-report.md) for exact changes, requirements matrix, environment/tool discovery, Red/Green evidence, commands and exclusions.

## Results and denominators

| Declared Windows offline measure | Result |
| --- | --- |
| Independent required traceability groups | 42/42, 100% |
| Unique original all-target Rust tests | 123/123, 100%; 37 unit and 86 integration; zero failed/ignored |
| Required unit subset | 37/37, 100% |
| Executed first-party lines | 3,191/3,339 = 95.5675351901767% |
| First-party source denominator | All 12 `src/*.rs` files; no first-party exclusion; lib declarations contribute 0 executable lines |
| Build / rustfmt / Clippy | PASS; locked/offline build and warnings denied |
| Documentation tests | Command PASS, zero tests discovered |
| Branch coverage | NOT_RUN |
| Native trial scope | 0/2 passing, 0%; both BLOCKED/NOT_RUN, zero trial attempts |

The 42 groups overlap in traceability and are not 42 additional executable tests. Developer 30/30 groups are another overlapping view. Retries, repeated collections, preflight attempts and inspector calls do not enlarge the required-case denominator or erase earlier outcomes. These offline metrics are also the overall metrics for the selected Windows offline QA scope; they are not a whole-framework or full native-readiness percentage.

Independent negative controls, real-junction fixtures and the deliberately bypassed final-check mutant passed their intended sensitivity checks. No test-result manipulation or product defect was established in the selected offline scope. QA's excluded attempt13 lacked original helper bytes; attempt35 was a retained oracle/seam error with a separately recovered helper. The QA report explains these limitations. Original failures remain preserved.

## Native continuation: retained observations

### Source collection and changed inputs

The approved exception is still only `chrome/latest` to `chrome/26.908.70816` with directory-junction tag `0xA0000003`. No installed plugin/cache file was edited. Fresh inventories contain 137 entries: 36 physical file bindings, 56 directory indices and 45 absences; one reviewed junction is metadata only, never traversed as a second source.

Collection001 passed, then AGENTS.md changed externally to add advisor instructions. Collection002 preserved a fresh binding. The original inventory remains historical. Final source readback shows the worker and four specifications unchanged, with AGENTS.md the sole changed file among the ten originally selected input records.

The host's approved advisor-retry command added 816 bytes to `C:\Users\bryan\.codex\rules\default.rules` after collection002. [The drift record](preflight-source-drift.json) verifies that the original 104,808 bytes remain an exact prefix and the added suffix refers to the approved advisor retry. The agent did not edit this rule file. This host side effect is retained explicitly rather than claiming all operational inputs stayed unchanged.

### Preflight 1: stale rules, no Codex launch

[Receipt](preflight-001/receipt.json): native worker-harness exit3, 8.047 seconds supervised duration, no timeout. Only `admitted` and `terminal(profile_unqualified)` were emitted. No spawn intent or server-start event exists; worker exit is null. The current-rule diagnostic collection identified the sole persistent inventory change above. Rust correctly rejected stale source evidence before a Codex launch.

### Preflight 2: current rules, real process, profile denied

A single documented follow-up used a fresh fixture/run ID, complete current inventory and all-false review findings. This refreshed externally changed evidence; it did not alter the Rust policy, installed configuration or first attempt. Preflight is separate from the one-shot model trials under the companion contract. No further automatic preflight attempt is selected.

[Receipt](current-rules-preflight/preflight-001/receipt.json): native worker-harness exit3, 15.766 seconds supervised duration, no timeout. The seven [journal events](current-rules-preflight/preflight-001/stdout.bin) show admission, native identity recheck, spawn intent, real Codex `server_started`, `stop_requested(profile_unqualified)`, process exit, and blocked terminal. Terminal fields include `tree_stopped:true`, `fixture_unchanged:true`, null thread/turn/usage, and `oracle:not_evaluated`.

Both preflight subprocesses received a child-only environment omitting exactly `ANTHROPIC_API_KEY`. The parent environment and saved credentials were not modified; no credential value was retained. All other variables and every Rust guard remained active. Both reviews retain all four findings false. See [the recorded assessment](advisor-assessment.md) for authorization reasoning and limits. The inherited-environment rejection is static analysis only, not an executed third case.

The PowerShell tool surfaced exit1 for the supervisors' nonzero completion; their retained receipts preserve the actual worker-harness exit3. Codex's observed worker exit1 is distinct again: it follows stop_requested and may be the harness's explicit Job Object termination code. It does not establish that Codex independently crashed.

Compiled `inspect` returned exit0 for both durable blocked journals, with zero truncated tail. This validates historical journal structure only. Post-run compiled source collection is byte-identical to the fresh preflight inventory (SHA256 `4915790cb3e2ca093777e97e132d471362bd2583ff539674b98f8f85fa702046`); no persistent source drift was observed across that launch. This does not exclude transient drift or read errors.

## Findings and gaps, ordered by effect

### G-NATIVE-01 — effective profile remains unqualified; precise predicate unavailable

**Classification:** native prerequisite/diagnostic gap, not a confirmed product defect. **Requirement:** preflight companion, fixed inspection and failure preservation; source-identity companion continuation boundary.

**Expected:** complete the bounded effective-config/features/hooks/plugins/apps/MCP/account/model checks and verified cleanup before reporting `preflight_checked`. **Actual:** the current-rule attempt spawned Codex, returned `profile_unqualified` before any passing config-stage observation, and verified cleanup. The raw harness streams contain no RPC error, stderr event, config observation or granular denial code. No authentication, Pro/model availability, hook/plugin/app/MCP inactivity, permission isolation or rate-limit conclusion can be drawn.

The source bounds the possible region to post-spawn `verify_preflight_review` (`runner.rs:168`), Job Object accounting during initialize/config RPCs (`protocol.rs:217-235`, `process_windows.rs:401-403`), or effective config validation before its event (`protocol.rs:318-323`, `273-285`). The accounting predicate requires exactly one total and one active process: an early worker exit or extra/transient process could fail it. Neither happened conclusively from this evidence. Later inspection stages would require the missing config observation first.

**Impact:** WN-01/WN-02 remain blocked. Preserve this actual launch as evidence; do not rerun it or relax policy to infer a pass. **Reproduction:** the exact selected command, input bytes, environment-name policy, executable hashes and original outcomes are in the linked receipts; the run IDs are single-use and must not be replayed.

**Focused next handoff:** [native-diagnostic-handoff.md](native-diagnostic-handoff.md). A new development selection should add sanitized closed denial-stage observations, independently QA the changed bytes, then select one fresh no-work diagnostic launch. Do not expose raw configuration/credentials, change guard predicates, manufacture true findings, or treat the added diagnostics as qualification.

### G-ADVISOR-01 — no usable Claude review

The optional [advisor skill](../../../../.agents/skills/advisor/SKILL.md) was invoked in read-only subscription mode. Attempt001 ended with ConnectionRefused. The approved final attempt reached its $1 cap without producing reviewer Markdown. Both exited1; response validity is NOT_EVALUATED and there is no verdict or recommendation. The CLI reported $1.015353 cost despite its $1 configured cap; this is retained CLI accounting, not a verified bill. Both permitted attempts are consumed. No third attempt, budget increase, auth-mode change or advisor repair was performed.

See [advisor assessment](advisor-assessment.md) and [immutable request/attempts](../../advisor-runs/20260916T034812Z-8d3c2a/). The independent product QA PASS does not rely on Claude.

## Final readback, custody and handoff

[Final readback](final-readback.json) verifies 56 candidate files, four worker specifications, the QA report/index, selected binary, twelve captured stream receipts, both fixture tasks and journals. No stream hash/size mismatch was found. The fresh source inventory remained identical after the real Codex process. No owned worker remains per compiled cleanup; neither supervisor timed out or required outer containment. Python helpers retain evidence and issue no framework authority.

- Developer evidence seal: 18,999 entries, SHA256 `c8d537420e79156f5b147789e35948b7577e587bce5b837a9564d21e96b3de9e`, zero readback errors.
- Independent QA index: 312 entries, SHA256 `cbb0f150f80282a3e3490fd4ec150c1645ab71cad026b07cfb6888b77f93eb5c`.
- Independent QA report: SHA256 `b2e8304c07a89a7c155669e1d0a9e9b93c8f5a0ac966b567fca1fee461b7f2d0`.
- This continuation's final artifact manifest covers its reports/receipts, the two exact owned trial roots, and both advisor intake/run roots. It does not rewrite the already sealed development or QA evidence.

The approved source-identity amendment is complete. Native qualification is INCOMPLETE with 0/2 trials run. Authority implementation/provisioning remains outside this amendment, and no applicable qualified compiled-Rust acceptance authority issued a decision. Framework acceptance remains **NOT_EVALUATED**.
