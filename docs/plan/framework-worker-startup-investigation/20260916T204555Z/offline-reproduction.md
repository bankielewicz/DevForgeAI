# Offline reproduction: startup stderr observability

## Result

**OBSERVED.** The frozen Rust probe has a startup observability blind spot that exactly matches the shape of the blocked native preflight, but this result does not identify why the native Codex worker exited.

The unchanged process reader did receive the synthetic child's stderr. It immediately reduced the raw 38-byte block to a byte count and SHA256. When the child had already exited, the pre-send process guard observed total 1, active 0 and returned before the protocol receive loop could journal that queued metadata. A live 1/1 control reached the receive loop and journaled the same metadata.

The evidence therefore disproves this inference: an empty outer CLI stderr file or absent stderr journal event does **not** prove the worker emitted no stderr. It does not show that the Rust CLI caused the exit. In this reproduction the Rust guard correctly detected an already exited child and blocked the RPC.

## Executed cases

| Case | Runtime observation | Result |
|---|---|---|
| SR-01 early exit | Synthetic child wrote fixed stderr and exited 23. Held Job Object reported 1 total, 0 active. `Session::preflight` returned `profile_unqualified`; journal recorded `unexpected_process_count` and `process_guard_rejected`, with no stderr event. The undrained receiver contained `bytes: 38`, SHA256 `d3cf90ebd82863af99e57c32156dd7b3a6645c3877eccde5e26aa19e12f01fca`, plus stdout end. | OBSERVED |
| SR-02 receive control | The same child stayed active at 1/1, emitted the same stderr bytes, accepted initialize and returned the fixed local result. The receive loop journaled the same 38-byte SHA256 with `content: omitted`; before-send and after-receive guards remained 1/1. | OBSERVED |

Both cases ended with `tree_stopped: true`, active count 0, and null thread/turn identifiers. Only `synthetic-peer.exe` was passed to `OwnedProcess::spawn`. Native Codex was not launched.

## Source explanation

The compiler dependency file binds the executable to the frozen `process_windows.rs`, `protocol.rs`, and companion modules. In the selected source:

1. `process_windows.rs:141-191` reads child output. For stderr, lines 158-163 construct only `Incoming::Stderr { bytes, sha256 }`; raw bytes are discarded at that boundary.
2. `protocol.rs:249-272` emits process accounting and returns `profile_unqualified` unless the held Job Object reports exactly 1/1.
3. `protocol.rs:288-303` calls that guard before sending initialize.
4. `protocol.rs:141-204` journals stderr metadata only while the protocol receive loop is running.

The early return in step 3 prevents step 4. The metadata still existed in the receiver and was read by the harness after preflight returned, establishing ordering rather than a reader failure.

## Repair direction

Add a bounded startup-diagnostic drain when a pre-send process guard fails. It should collect already queued stderr metadata, stdout end state, and the child exit code before returning the existing blocked result. Keep the 1/1 predicate and RPC prohibition unchanged.

A stronger design decouples process telemetry from the protocol receive loop: the process reader should publish bounded lifecycle telemetry to a journal sink that remains active from spawn through teardown. This avoids losing early stderr metadata at any guard boundary.

Logging levels can help operators, but a level switch alone will not close this gap because the event is currently stranded before the logger's receive path. Separate mandatory evidence from optional diagnostics:

- mandatory lifecycle evidence: spawn, total/active counts, exit code, stderr byte count and digest, teardown result;
- minimal: mandatory evidence only;
- verbose: RPC stage/checkpoint timings and queue state, without payload content;
- debug: explicitly selected bounded and sanitized stderr excerpts plus internal state, written only to a fresh protected evidence directory.

An operator-facing `off` setting may suppress console logs, but it should not suppress the mandatory evidence needed to explain a blocked framework decision. Configuration should be schema-validated, default to minimal, reject unknown levels, and record the effective level in the run evidence. Raw stderr can contain sensitive data, so full unbounded content should not be a logging mode.

## Integrity and limits

- Candidate manifest SHA256: `419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540`.
- Every one of the 58 candidate files matched that manifest before and after each Cargo command.
- Commands ran on native Windows from the harness directory with cached Cargo, `--locked --offline`, and a fresh target root.
- Attempt 01 built successfully. Attempt 02 is retained as a request-adapter setup failure. Attempt 03 is retained as an incomplete oracle failure after SR-01 exposed the companion RPC diagnostic. Attempt 04 passed both declared cases. Neither failed attempt is counted as product evidence.
- The wrapper has a different Cargo manifest directory and exposes one adjacent call to the unchanged private initialize RPC for the control. It does not test public path-sensitive admission, repeat native execution, determine the actual native child's exit cause, repeat full QA, or establish framework acceptance.

Evidence: [test plan](offline-repro/test-plan.md), [integrity review](offline-repro/integrity-review.md), [runtime summary](offline-repro/runtime/04-run/summary.json), [successful receipt](offline-repro/attempts/04-run/receipt.json), and [artifact index](offline-repro/artifact-index.json).

Framework acceptance remains **NOT_EVALUATED**.
