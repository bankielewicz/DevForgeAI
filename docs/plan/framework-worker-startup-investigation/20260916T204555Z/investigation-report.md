# Blocked worker preflight investigation

Five delegated investigations and two executed synthetic cases establish a startup observability gap in the Rust worker probe. They do **not** establish why the retained native Codex worker exited. The proposed solution is to make startup evidence independent of protocol receive, then add configuration-controlled diagnostic levels. No production repair or native retry occurred.

## Which process exited, and what preflight means

The DevForgeAI Rust probe is the parent supervisor. It launched the pinned Codex 0.154.0 executable as an app-server child. Preflight checks that the worker is alive and can satisfy the required protocol/configuration prerequisites before any thread or turn can run.

The retained attempt stopped at the first of those checks:

| Observation | Meaning |
| --- | --- |
| `server_started`, elapsed 7,877 ms | Windows returned a process handle. This event does not establish app-server readiness. |
| Job Object total 1, active 0, elapsed 7,980 ms | One process had been assigned; none remained active before `initialize` was sent. |
| `unexpected_process_count`, then `process_guard_rejected` | The required 1/1 predicate failed. The probe correctly withheld the RPC. |
| Stop requested at 7,984 ms; child exit status 1 subsequently recorded | The worker had already terminated before cleanup. The exit status does not identify its cause. |
| Parent probe exit 3 | The Rust supervisor completed its blocked-result path; the evidence does not show a parent crash. |

Thus, the Codex child exited. There is no established launch defect in the Rust probe, and its later cleanup cannot explain the already-zero active count. There is, however, a confirmed limitation in how the probe retains startup diagnostics. This distinction prevents mistaking an instrumentation repair for a proven fix to the worker's exit.

The 103 ms between process creation being journaled and the guard is an observation interval, not an exact child lifetime. A similar older attempt used the same worker and policy but a different probe binary; its less detailed evidence cannot prove the same internal failure predicate. [Native reconstruction](native-evidence.md).

## Why the existing evidence cannot identify the cause

The child writes stderr into an internal pipe owned by the Rust probe. The probe's reader immediately reduces each block to a byte count and SHA256; it discards the message text. Only the protocol receive loop persists those metadata events. The process guard runs before the first send/receive, and its failure path does not drain the queued events.

There are therefore two separate losses: raw diagnostic text is deliberately omitted, and even its metadata can be stranded when startup fails early. The empty outer `stderr.bin` belongs to the parent probe and cannot establish that the child emitted nothing. The completed process's lost pipe/queue contents cannot now be recovered from the retained artifacts.

The frozen contract already limited diagnostics to closed fields. This investigation identifies a need for stronger startup observability; it does not claim an unproven violation of that contract or revoke the prior offline QA result.

## Executed independent reproduction

The offline agent compiled a wrapper around unchanged candidate modules and used a purpose-built local peer. Both cases ran on native Windows from this fresh C: evidence directory, using Cargo with `--locked --offline`. Native Codex was not executed.

| Case | Runtime evidence |
| --- | --- |
| SR-01: early exit | The peer wrote 38 known stderr bytes and exited 23. The job reported 1/0; preflight returned `profile_unqualified`; no stderr event reached the journal. The harness then recovered the expected byte count/hash from the still-queued receiver. |
| SR-02: live control | The same peer stayed at 1/1, wrote the same bytes, accepted initialize, and returned a fixed response. The normal receive path journaled the expected stderr metadata. |

Both cases finished with active count 0, verified cleanup, and no thread/turn. They demonstrate the ordering gap without relying on a mock reader or fabricated result. They do not explain the earlier native worker exit or qualify public path-sensitive admission: the wrapper has a different manifest directory and exposes one adjacent private RPC call for the control.

Four commands are retained: successful build, request-adapter setup failure, an incomplete harness oracle that omitted the companion RPC diagnostic, and the corrected run observing both cases. The first two unsuccessful executions remain visible and receive no product-failure or acceptance credit. No new full-suite pass rate or coverage was claimed. [Report](offline-reproduction.md), [runtime observations](offline-repro/runtime/04-run/summary.json), [command receipt](offline-repro/attempts/04-run/receipt.json), [sealed reproduction index](offline-repro/artifact-index.json).

## Plausible native causes

The launch review found no specific unsupported option placement, Windows/TOML quoting error, disabled-feature dependency, detached-console incompatibility, or premature stdin close. This reduces those explanations without qualifying the exact real-child launch.

The leading unresolved explanations are a strict/bootstrap configuration rejection or a failure opening/initializing Codex runtime state. Bootstrap authentication/configuration can fail before protocol requests; the absence of RPC activity does not exclude those causes. Shared launch context, host intervention, and other child failures remain possible. The retained exit status alone cannot rank them conclusively.

The official [0.154.0 app-server source](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/app-server/src/lib.rs) supports `RUST_LOG` and `LOG_FORMAT=json`, but initializes its logger after configuration and state setup. This makes process-boundary capture necessary for early failures. The public tag is source evidence, not proof that the retained executable is a reproducible build of that tag.

A bounded Windows Application log query for IDs 1000/1001 found no matching events. The conventional Codex log directory was absent to a metadata check. Neither observation excludes other logs, a handled error, or host intervention. Installed configuration contents, credentials and live databases were not inspected. [Source review and limitations](source-review-notes.md), [launch compatibility review](launch-compatibility.md).

## Current logging and the proposed configuration

The worker probe currently has a synchronized JSONL evidence journal and fixed diagnostic events. It has no configuration-file selector for off/minimal/verbose/debug. The separate index application's request log also has no such selector and does not supply logging to this worker probe.

The proposed design keeps mandatory evidence always enabled and adds a separate optional diagnostic sink:

| Proposed level | Supplemental output |
| --- | --- |
| `off` | No supplemental log file; all existing mandatory evidence and required new startup summaries remain present. |
| `minimal` | Lifecycle, exit disposition, stream totals/digests, EOF, reader errors and cleanup. |
| `verbose` | Minimal plus phase/RPC timing, policy and argv digests, and queue state. |
| `debug` | Verbose plus bounded stream/internal detail and a versioned, closed startup-error category. |

A future, explicitly bound configuration file could contain:

```json
{"schema_version":1,"level":"minimal","redaction_policy":"closed-v1"}
```

This is a proposed interface, not an implemented option. The request would bind the file by digest; Rust would reject unknown fields/levels, altered digests, invalid paths and excessive size before spawn. The sink would write structured records beneath the fresh run directory with fixed budgets. New levels/categories could be added through an explicit schema revision with compatibility tests. No logging option would change the process guard or an acceptance decision.

Ordinary debug output should not contain arbitrary child text, credentials, configuration values or protocol payloads. A narrowly tested classifier may identify known startup failures while emitting only a closed category. Unknown text must remain `unclassified`. If that is insufficient, bounded raw forensic capture requires a separately selected evidence/privacy contract; it is not automatically enabled by `debug`.

This reconciles the agents' alternatives: some individual reports discuss sanitized excerpts or opt-in raw capture. The recommendation here and in the dedicated logging design keeps arbitrary text out of every ordinary logging level. Likewise, an exit observed before cleanup must not be labeled proof of a spontaneous or internally caused exit; external termination remains possible. [Detailed logging design and twelve proposed acceptance cases](logging-design.md).

## Concrete repair sequence

1. **Capture startup independently of receive.** Give the process owner both reader handles and explicit stdout/stderr EOF states. Continue bounded stream accounting from spawn through teardown. On a guard failure, sample child status before stop, then drain/join within the existing cleanup bound. Persist complete-stream totals/digests, EOF/errors, dropped-detail counts and drain completeness before the terminal record. Keep the failed 1/1 predicate and RPC prohibition unchanged.
2. **Prevent diagnostic backpressure.** A full diagnostic channel or slow log file must not strand pipe readers. Keep protocol and diagnostic queues separately bounded, preserve existing output-limit behavior, and record incomplete capture explicitly. Optional log failure must not prevent cleanup; mandatory journal failure retains its existing failure semantics.
3. **Add versioned classification and configuration.** Match only evidenced startup patterns with negative controls. Add the four-level file and separate structured sink. Keep raw capture outside ordinary levels. Do not change the launch vector, installed configuration or state database speculatively.
4. **Execute red, green, refactor and independent QA against changed bytes.** First demonstrate missing startup evidence with a failing test, then implement and rerun meaningful Windows process/Job Object, output-limit, logging-level, privacy, persistence-failure and regression cases. Include argv round trips, no-output exits, invalid UTF-8, more than 32 chunks before receive, and distinct pre/post-cleanup status. Require the repository's coverage/pass-rate floors independently, and no unresolved required case, including `query_failed`. The frozen package's prior PASS does not qualify a changed candidate.
5. **Prepare one new native diagnostic only after independent QA passes.** That attempt needs separate authorization and should retain the pinned child/vector and process predicate, with no thread/turn or automatic retry. A retained cause category should determine any subsequent targeted launch/configuration repair. An unchanged successful launch would instead leave the previous cause unresolved and suggest host-state or timing sensitivity.

These are proposed changes. The exact new record/request schemas, classifier patterns, version compatibility and fixed capture budgets must be finalized as a contract amendment before production implementation. Logging will make the next failure more diagnosable; it cannot guarantee an explanation for arbitrary failures or recover this attempt's discarded text.

## Custody and status

The five workstreams were native evidence reconstruction, [startup lifecycle](startup-lifecycle.md), launch compatibility, logging design and offline reproduction. Their original reports remain available alongside this reconciled assessment.

[Preservation readback](preservation-readback.json) verified 6,004 file bindings: 58 candidate files, 58 frozen snapshot files, 67 native artifacts and 5,821 prior QA artifacts. The native index still has the supplied SHA256 `1a22ca36d2fe92f86b7ebded1c6345db0d969ee39e600d5d79502fed1d708750`. The reproduction has its own sealed 60-artifact index; the final coordinator seal independently checks it and its selected executables. Build intermediates are excluded from the coordinator index and are not acceptance inputs.

| Assessment | Status |
| --- | --- |
| Startup stderr observability gap | OBSERVED in two synthetic cases and source review |
| Exact native worker exit cause | UNRESOLVED |
| Production repair | NOT_IMPLEMENTED |
| Native attempts during this investigation | 0 |
| Original native preflight | BLOCKED; unchanged |
| Full QA of proposed changes | NOT_RUN |
| Framework acceptance | NOT_EVALUATED |

The final artifact index and readback receipt bind this investigation. No installed skill, native configuration, credential, startup setting, frozen source or prior evidence was changed.
