# Codex worker feasibility probe

Isolated Windows Rust experiment implementing [DFF-WORKER-FEAS-01 v1.0.0](../../../docs/specs/framework/runtime/codex-worker-feasibility-v1.md). This package supplies offline observations; it issues no framework acceptance and does not close framework work. Native Codex/Pro trials require a separate explicit selection and reviewed profile. No native trial has been executed in this implementation task.

## Build and exercise offline

From this directory, using native Windows Rust 1.97.1 or later and the existing offline Cargo cache:

```powershell
cargo test --locked --offline --all-targets
cargo fmt --all -- --check
cargo clippy --locked --offline --all-targets -- -D warnings
```

The process tests use real Windows Job Objects, a hidden-console Ctrl+C driver, abrupt harness exit, and a peer descendant holding pipes. WF-16 includes the production 120-second watchdog; allow approximately 130 seconds for that test. No dependency installation is performed. The own `[workspace]` and Cargo.lock do not modify the index workspace.

## Terminal interface

```text
devforgeai-codex-worker-probe.exe run --request <absolute-json-path>
devforgeai-codex-worker-probe.exe inspect --run-dir <absolute-path> --after <u64> --limit <1..100>
```

The request schema, fixture bytes and profile requirements are defined in the linked contract. Only the test-built `protocol-peer.exe` beside the selected build is admitted as a peer. Peer arguments are always `--fixture-root <absolute-path>`. A native request must identify the captured Codex executable and a digest-bound operator review; the argument vector is fixed to the selected stdio adapter. No shell command input exists.

Keep harness stdin open until completion. Exact `{"op":"cancel"}` plus LF, EOF and Ctrl+C request cancellation. Invalid control input fails the run. `scenario=cancel` latches cancellation immediately after the turn ID is recorded. Library test options can shorten deadlines or inject evidence/cleanup observations; the production CLI always uses fixed limits.

The append-only `journal.jsonl` is the state record. Records are synchronized before emission or their related dispatch effect. Inspection is read-only and never spawns, resumes, repairs or kills a historical PID. Existing run directories are rejected. Preserve the referenced fixture, worker binary and profile artifacts for complete inspection. A stopped tree does not establish file/network isolation.

Exit codes: 0 completed with exact result, unchanged fixture, verified stopped tree and observed zero worker exit; 2 invalid request/path/identity; 3 unavailable prerequisite/profile; 4 worker/protocol/output/evidence failure; 5 cancellation; 6 deadline; 7 cleanup uncertain. Sound inspection exits 0 independently of the recorded historical outcome.

## Evidence and fixture ownership

Frozen fixture copies in `tests/fixtures` originate from the selected specification and captured schema-command receipt. Expected results are compiled into the verifier and external peer, and never copied into the worker fixture or prompt. The peer validates outgoing protocol fields independently of runtime predicates. Additional numbered peer subfixtures in the tests cover typed events, RPC errors, pagination and invalid data; they do not inflate the 20-case denominator.

Developer execution evidence is retained under [the implementation run](../../../docs/plan/framework-worker-implementation/20260915T1544548240203Z/context.md). Final metrics, limitations and independent retest selection are in that run's delivery report when present. A passing peer does not qualify native Codex, supported production dispatch, protected authority or the full MVP.
