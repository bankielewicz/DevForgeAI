# Profile preflight integration development evidence

Scope: real Windows child-process integration tests for the compiled Rust `Session::preflight` path. The test peer performs no Codex launch, configuration mutation, thread creation, or turn creation.

## TDD and diagnostic attempts

| Attempt | Result | Interpretation |
| --- | --- | --- |
| `01-red` | Cargo 101 | Valid RED: the otherwise-compilable focused test required the absent `Session::preflight` API. |
| `02-green` | Cargo 101 | Setup failure: `src/profile_sources.rs` was temporarily absent while its owner was editing it. No product conclusion. |
| `03-green` | Cargo 101; candidate changed during command | Mixed candidate and early process rejection. Preserved, not qualification evidence. |
| `04-accounting-diagnostic` | 0/8 | Stable diagnostic showed the job grew from one to two live processes before any RPC. Negative-case targeted-RPC assertions prevented vacuous passes. |
| `05-job-images` | 0/1 | Identified the second contained process as `C:\Windows\System32\conhost.exe`; raw PID/image evidence is in stderr. |
| `06-detached-green` | 0/1 | DETACHED_PROCESS removed `conhost.exe`; a peer-only path-spelling mismatch then caused `worker_exited`. No product conclusion. |
| `07-fixture-corrected` | 1/1 | Exact positive trace passed after the peer consumed the request's verbatim resolved checkout path. |
| `08-optional-cursor-red` | 0/1 | Valid RED: schema-valid omitted final `nextCursor` produced `protocol_error`. |
| `09-profile-green` | 8/8 | Final focused candidate passed all 23 explicit scenarios/subfixtures. |
| `10-final-policy-green` | 8/8 | The same 23 scenarios passed after the contract and compiled policy expanded the independent disabled-feature denominator from 14 to 35 names. |
| `11-rate-limit-red` | Cargo 101 | Setup failure: the new test omitted the `json!` macro import. No product conclusion. |
| `12-rate-limit-red` | 0/1 | Valid RED: a successful response with missing `usedPercent` returned success without the required `not_measured` event. |
| `13-rate-limit-green` | 1/1 | Missing and nonnumeric measurements emitted exactly one typed `not_measured` event; a reported 100 percent limit blocked preflight. |
| `14-profile-green` | 9/9 | Final focused candidate passed all 26 explicit scenarios/subfixtures. |

All attempts retain exact argv, cwd, native exit code, duration, raw stdout/stderr, candidate manifest, tool hash, fixture root, and source-stability observation in their `receipt.json` and sibling files.

## Final focused coverage

The nine Rust test functions contain 26 counted scenarios: one positive exact trace; two config/requirements negatives; four feature negatives; two optional-cursor positives; seven hook/plugin/app/MCP negatives; four RPC/deadline/cancellation/notification cases; two privacy projection cases; one transient-descendant case; and three rate-limit measurement cases.

The final candidate passed 9/9 functions and 26/26 scenarios. Each rejection asserts that its targeted RPC was reached. Every process is stopped and observed with zero active processes. The positive trace contains only initialization, inventory, account/model and rate-limit reads; it contains no `thread/*` or `turn/*` method. The final peer uses an independent literal 35-name feature list derived from the selected contract; it does not import the production constant. Rate-limit observations never retain account data: unavailable measurements produce only `{"rate_limits":"not_measured"}`, and a reported exhausted limit rejects before any thread or turn.

Before attempt 10, one setup invocation ran from the package directory and could not locate the workspace-relative `record.py`; Cargo did not start. Its exact conversational tool response is retained in `pre-final-policy-setup-failure-tool-response.json`. The native exit code, native command duration, stdout/stderr separation, raw bytes, and raw line endings were not retained by that tool wrapper. It is an evidence-retention limitation, not a product result; attempt 10 is the first executed final-policy test command and has complete retained streams and receipt metadata. This development run therefore cannot claim complete raw-stream retention for every attempt. Fresh qualification QA must establish complete final-candidate command evidence independently.

This focused result is development evidence. It is not independent QA or protected framework acceptance.
