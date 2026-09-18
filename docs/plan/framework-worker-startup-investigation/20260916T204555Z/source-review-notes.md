# Coordinator source review and reconciliation

Scope: independent synthesis of five delegated investigations plus read-only coordinator checks. No native Codex process was launched. The frozen candidate and historical evidence are inputs, not editable work products. This is diagnosis and a proposed change, not a new full QA or acceptance campaign.

## Verified local facts

- The selected native index SHA256 is `1a22ca36d2fe92f86b7ebded1c6345db0d969ee39e600d5d79502fed1d708750`; all 67 entries match. The selected QA index SHA256 is `552912696c5260091a8cb2305b13d1f1987e53630b610dd66afec55f84d132d9`.
- [preservation-readback.json](preservation-readback.json) verifies 6004 file bindings: 58 original candidate files, 58 snapshot files, 67 native artifacts and 5821 prior QA artifacts. It does not claim a recursive snapshot of all user/system state.
- The native journal's successful job query records total=1/active=0 before stop_requested. The child was already inactive; the parent Rust probe continued and returned its documented blocked result.
- `process_windows.rs:141-191` starts separate readers, caps bytes, discards stderr content after hashing each read block, queues metadata, and emits an end marker only for stdout. `protocol.rs:193-196` persists stderr metadata only inside receive. `protocol.rs:288-300` invokes the process guard before the send/receive path. `protocol.rs:767-803` has no incoming drain on the no-thread/no-turn interruption path.
- `main.rs:31-103`, strict request fields, Options and Cargo.toml provide no configurable logging levels for this probe. The separate index application's rudimentary request log is not a probe logging system.

## Primary external cross-checks

Current official [App Server documentation](https://learn.chatgpt.com/docs/app-server) requires initialization before other protocol requests. It supports the distinction between opening a process and having a ready protocol connection. Current [configuration documentation](https://learn.chatgpt.com/docs/config-file/config-reference) documents a log directory and TUI logging; it does not establish a worker-probe logging setting or prove version 0.154.0 behavior. No current example was run.

The official [OpenAI source tag rust-v0.154.0, app-server/lib.rs](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/app-server/src/lib.rs) was inspected independently at the relevant regions: configuration/auth bootstrap (approximately 456-526), state initialization (586-594), and tracing setup (629-658). The source supports strict configuration and state-access failures as plausible pre-protocol causes, and exposes RUST_LOG/LOG_FORMAT controls after earlier bootstrap work. It also handles Windows detached-console signal registration. These facts do not establish the native failure's cause or prove that the retained standalone executable is a reproducible build of the public tag.

The tagged [rollout state database source](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/rollout/src/state_db.rs) has try_init (approximately 55-119) opening the state runtime and waiting for startup backfill. The call path is not bypassed merely by a features.sqlite=false override. Its startup warning path can write stderr before a tracing subscriber exists. This supports retaining child stderr at the process boundary even when the child's configurable logger has not started.

Microsoft's [job accounting contract](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information) distinguishes lifetime and active membership. [TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject) targets processes currently associated with the job. The current run's earlier zero-active observation therefore rules out later probe cleanup as the cause of that inactivity. Exit code 1 remains a status, not a diagnosis; external termination or a handled child error remains possible.

## Additional observations and their limits

[windows-event-observation.json](windows-event-observation.json) records a read-only Application log query for event IDs 1000/1001 from 20:27:55 through 20:28:25 UTC. Windows returned NoMatchingEventsFound. This is a bounded negative observation, not proof that there was no crash or host intervention; other event channels were not queried.

[log-directory-metadata.json](log-directory-metadata.json) records that the conventional `C:\Users\bryan\.codex\log` path was not present to the read-only metadata check. No log contents, live installed configuration, SQLite database or credentials were read. The actual pinned app-server log destination was not independently established; absence of this conventional directory does not establish absence of logging elsewhere.

## Reconciled conclusions

1. The ~103 ms between server_started and the failed guard is an observation interval containing source verification and journal work. It is not an exact child lifetime. The older run's similar interval does not prove the same underlying predicate because its diagnostics were less specific.
2. Authentication/configuration RPCs and model work were not reached. Bootstrap authentication/configuration and state initialization inside the child remain possible causes before any RPC.
3. Exit sampling before teardown is a worthwhile future improvement. This does not mean the current run's exit code was fabricated by cleanup: the sole worker was already inactive.
4. The stderr visibility limitation is concrete. The current frozen diagnostic contract deliberately preserves closed data and adds no configuration input. The new investigation does not retroactively claim an unproven violation of that contract or reverse the bounded offline QA PASS. It proposes a stronger startup observability requirement.
5. Default/debug logging must not silently retain arbitrary raw child text, environment values or configuration values. A closed classifier can remain unclassified; a verbosity toggle alone cannot guarantee a root cause. An explicitly selected forensic-capture design would be a separate contract decision if ordinary classified evidence remains insufficient.
6. The first implementation should improve bounded stream ownership, pre-cleanup status and startup classification. Optional severity/verbosity routing is the second concern. The 1/1 guard and fixed launch policy remain unchanged; no speculative config relaxation or native retry occurred.

Detailed proposals and independently authored hypotheses remain in the four review reports. The coordinator report is the reconciled recommendation. The synthetic reproduction report states its actual executed evidence and limits separately.
