# Native early-exit evidence audit

## Scope and result

This is a read-only reconstruction of the retained native attempts and the frozen
Rust source. It launches no Codex worker or Rust probe, changes no candidate or
prior evidence, and makes no framework acceptance decision.

The strongest supported conclusion is that the pinned Codex child terminated
before the first `initialize` request. The Rust probe process remained alive,
classified the preflight as blocked, cleaned up, and exited 3. The retained
evidence does not establish why the Codex child terminated. It therefore does not
establish a Codex product defect or a Rust probe defect.

The behavior recurred in two separately retained native preflights with the same
pinned Codex SHA256 and the same compiled launch-policy SHA256. The earlier Rust
probe binary and the later diagnostic Rust probe binary had different hashes.
Both attempts reached `profile_unqualified` about 103 to 105 ms after the
`server_started` event and ultimately recorded Codex status 1. Only the latest
attempt proves that the child was already inactive at that point, because the
older build did not retain process counts. This repeated external symptom makes
a one-time race less likely. It does not distinguish the fixed child/argv/config
path, shared Windows launch mechanics, stable profile state, or a repeatable
external intervention.

## Timeline reconstructed from primary evidence

The latest journal has one JSON record per line in
[`journal.jsonl`](../../framework-worker-trials/20260916T202125Z-diagnostic/run/journal.jsonl):

| Journal sequence | Elapsed | Observation | Meaning |
| ---: | ---: | --- | --- |
| 1 | 0 ms | request admitted | The Rust CLI admitted the request and created its journal. |
| 2 | 3,912 ms | pinned native identity rechecked | The selected Codex executable still matched SHA256 `be96...dfde`. |
| 3 | 3,914 ms | spawn intent | The fixed adapter and child identity were selected. |
| 4 | 7,877 ms | `server_started`, PID 66880 | `CreateProcessW` returned a process handle. The source records this event without first querying liveness ([runner.rs:148-160](../../../../devforgeai/experiments/codex-worker-probe/src/runner.rs)). |
| 5 | 7,980 ms | total 1, active 0 | One process had been assigned to the held Job Object and none remained active. The query succeeded. |
| 6 | 7,981 ms | initialize guard rejected | The guard mapped the failed `1/1` predicate to `profile_unqualified`. |
| 7 | 7,984 ms | stop requested | Cleanup was requested after the zero-active observation. |
| 8 | 7,991 ms | stopped, child status 1 | Cleanup verified the tree stopped and then read the process status. |
| 9 | 7,993 ms | terminal blocked | No thread, turn, usage, or oracle result exists. |

The 103 ms from `server_started` to the count observation is an observation
interval, not a measured child lifetime. It includes post-spawn source review and
journal work. The retained evidence locates termination after process creation
returned and no later than the count query; it does not locate the exact instant
inside that interval.

The first RPC path runs the Job Object guard before writing `initialize`
([protocol.rs:249-271](../../../../devforgeai/experiments/codex-worker-probe/src/protocol.rs),
[protocol.rs:288-303](../../../../devforgeai/experiments/codex-worker-probe/src/protocol.rs)).
The latest [observed result](../../framework-worker-native-diagnostics/20260916T202125Z/observed-result.json)
therefore correctly reports `initialize_sent:false`.

The earlier current-rules preflight independently shows the same shape in
[`journal.jsonl`](../../framework-worker-trials/20260916T120406Z-current-rules-preflight/run/journal.jsonl):
spawn intent at 4,031 ms, `server_started` at 8,079 ms, stop requested at
8,184 ms, and child status 1 at 8,191 ms. That older implementation lacked the
new count diagnostic. Its outcome is consistent with the same startup/liveness
branch, but the older evidence alone cannot distinguish that branch from another
post-spawn `profile_unqualified` source. The older Rust executable SHA256 was
`b63a0dfb...74079b2`; the current one is `0ab81c4c...d9623`. Both requests bind
the same worker SHA256 `be96b992...cbdfde` and launch-policy SHA256
`1dbc48c4...26b5`.

## What `total=1, active=0` proves

The values come from one successful
`JobObjectBasicAccountingInformation` query
([process_windows.rs:386-408](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs)).
They establish all of the following for that held Job Object at the query instant:

- one process had been assigned since the job was created;
- no assigned process remained active;
- the result was a count mismatch rather than a Job Object query failure; and
- no assigned descendant had been counted, because the cumulative total stayed
  at one.

They do not establish the child application's reason for exit. They also do not
inventory unrelated host processes or prove that no process could escape through
an independently permitted breakaway mechanism. No breakaway permission appears
in this Rust job setup; its only configured limit is kill-on-job-close
([process_windows.rs:203-211](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs)).

The status 1 is best described as the sole child's pre-cleanup termination
status. The process was already inactive before sequence 7. The later
`TerminateJobObject(..., 1)` call cannot explain the earlier zero-active state
([process_windows.rs:423-428](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs)).
Because the implementation reads the status only after cleanup, it should still
record a separate `pre_cleanup_exit_code` in a future diagnostic. Status 1 by
itself does not distinguish a handled configuration/argument error, another
application failure, or an external termination that also supplied status 1.

## Observability gap in the current Rust probe

The Rust probe creates dedicated stdout and stderr pipes and starts reader
threads ([process_windows.rs:195-200](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs),
[process_windows.rs:270-300](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs)).
Child stderr becomes an in-memory `Incoming::Stderr {bytes, sha256}` message
([process_windows.rs:141-167](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs)).
It reaches the durable journal only while the protocol receive loop drains that
channel ([protocol.rs:141-203](../../../../devforgeai/experiments/codex-worker-probe/src/protocol.rs)).

Here the pre-send guard failed before the receive loop ran. With no thread and
turn, `interrupt()` closes stdin and waits; it does not drain pending output
([protocol.rs:767-772](../../../../devforgeai/experiments/codex-worker-probe/src/protocol.rs)).
The empty `native-001/stderr.bin` is the outer Rust CLI's stderr. It does not show
that the Codex child emitted zero startup bytes. The child may have produced an
argument or configuration diagnostic that remained queued and was discarded.
Even on the normal receive path, the journal deliberately retains only each
chunk's length and digest, with `content:"omitted"`; those fields establish that
output existed but cannot explain its meaning.

The current probe has an append-only JSON evidence journal and fixed diagnostic
events. A scoped search of its `src/`, tests, and applicable runtime contracts
found no probe configuration for off, minimal, verbose, or debug logging. The
compiled child launch record likewise has no logging argument; it contains the
app-server command, strict configuration, policy overrides, sandbox mode, and
approval policy
([restrictive-launch-policy.json:1-123](../../../../devforgeai/experiments/codex-worker-probe/src/restrictive-launch-policy.json)).
The probe therefore does not currently provide the configurable logging levels
described in the investigation question.

Mandatory authority/audit events should remain independent of any future
verbosity setting. A setting that says `off` may suppress optional diagnostics;
it must not suppress admission, policy decisions, cleanup evidence, or terminal
records.

## Ranked hypotheses and falsification tests

### 1. Pinned child rejected the fixed argv or effective startup configuration

**Rank: co-leading.** Two attempts, hours apart, used different Rust probe binaries
but the same pinned Codex bytes and policy digest, then ended with the same status
and similar post-spawn observation intervals. The fixed argv begins with
`app-server --listen stdio:// --strict-config` and contains many `-c` overrides.
A handled parse/configuration failure is compatible with status 1. No child
diagnostic was retained, so the evidence cannot rank this above the shared launch
mechanics or a repeatable external intervention.

**Falsification test:** in a separately authorized attempt using exactly the same
worker, argv, cwd, environment rule, Job Object, and stdin lifetime, capture the
pre-cleanup exit status plus a bounded child-stderr record before teardown. A
retained diagnostic that names a rejected option or configuration field confirms
the category. An alive `1/1` snapshot followed by a successful initialize rejects
it. Changing flags one at a time before observing the unchanged vector would
destroy comparability and is not the first test.

### 2. Shared Windows launch mechanics are incompatible with this real child

**Rank: co-leading.** Both Rust binaries share `CreateProcessW`, inherited pipe
handles, `DETACHED_PROCESS`, a Job Object supplied at creation, a fixture cwd,
and an unchanged environment copy
([process_windows.rs:237-267](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs)).
The offline peer tests exercise those mechanics with a synthetic executable;
they do not prove that the pinned app-server accepts this exact native setup.

**Falsification test:** first retain spawn-return, immediate liveness, post-source-
review liveness, pre-cleanup status, and child-output evidence from the unchanged
launch. If the child reports no argv/config issue, compare one launch-mechanic
variable at a time only under a new explicit selection. Keep the current attempt
as the fixed baseline. A successful unchanged launch after instrumentation would
instead identify timing or host-state sensitivity.

### 3. Stable installed profile state causes a startup rejection before RPC

**Rank: plausible.** The child inherited the normal Codex home and the
policy requested ChatGPT login. Static source identity passed in both attempts,
but effective config, account, model, and rate limits were never queried. The
default rules file changed after host approval before the latest attempt, while
the outcome stayed the same. That makes that single rule-file revision an
unlikely sole cause; another stable profile prerequisite could still matter.

**Falsification test:** use only bounded, non-secret identity and existence
observations before launch, then rely on the child's retained startup category.
Do not inspect credential contents or mutate installed state. If the child stays
alive, the existing read-only preflight can qualify effective config and account
state through its defined RPCs.

### 4. Host protection or an unhandled native fault terminated the child

**Rank: plausible but less directly evidenced.** Process creation succeeded and the observed status is 1 rather
than a typical unhandled Windows exception code. A read-only query of Application
Error and Windows Error Reporting IDs 1000/1001 from 20:27:55 through 20:28:25 UTC
found no matching event
([windows-event-observation.json](windows-event-observation.json)). Event absence
does not exclude a clean error exit, an unlogged fault, or another protection
system.

**Falsification test:** bind read-only Code Integrity, Defender, and relevant
Application event observations for the exact PID/image/timestamp window. Any
matching enforcement event would outrank inference from status 1. Empty event
sets remain supplemental and cannot prove that host protection was absent.

### 5. Probe cleanup caused the original child exit

**Rank: contradicted for this attempt.** The successful Job Object query recorded
zero active processes before stop was requested. Cleanup can account for status 1
when it terminates a live child, but that generic behavior does not explain this
timeline. A pre-cleanup status observation should make this distinction explicit
in future evidence.

## Minimal safe additional evidence

No further causal content can be recovered from the retained process pipes: the
process is gone and the pending child-output queue was never persisted. Existing
artifacts support the timeline and recurrence only. The smallest useful Rust
diagnostic change is:

1. Record one `spawn_returned` event immediately after `CreateProcessW` with PID,
   monotonic elapsed time, one Job Object count pair, and nullable exit status.
2. Record the same fields immediately after the post-spawn source review and at
   guard failure, before closing stdin or calling `TerminateJobObject`.
3. On a pre-send failure, drain the already captured channel for a short fixed
   bound. Always retain stream byte count, chunk count, total digest, truncation
   state, and EOF state.
4. Add an explicitly selected diagnostic mode that may retain a small bounded
   startup-stderr artifact. Apply deterministic secret/path redaction before a
   report consumes it; seal the original in a restricted fresh evidence location
   with its digest. Metadata-only mode remains the default. The report must state
   when content was unavailable or redaction prevented attribution.
5. Record the compiled launch-policy digest, exact argv digest, cwd identity,
   creation flags, environment-name delta, and child executable digest. Do not
   log credential values, arbitrary environment values, or configuration-file
   contents.
6. Keep the required `total==1 && active==1` predicate unchanged. Diagnostic
   detail must never convert a denial into admission or authorize work.

Implement this through development TDD and fresh independent QA before another
native attempt. The next native attempt needs a separate authorization and should
reuse the exact pinned vector once, with no thread/turn and no automatic retry.

## Interpretation corrections

- `server_started` means process creation returned successfully. It is not a
  readiness or liveness observation in the current source.
- `native-001/stderr.bin` is the Rust CLI's stderr. It is not the child app-server
  stderr stream.
- Child status 1 is a real pre-cleanup termination status under this timeline,
  but it supplies no cause category.
- The latest count diagnostic localizes the latest result to startup/liveness.
  The similar older result is supporting recurrence evidence; it does not prove
  that older attempt used the same internal branch.
- The frozen candidate's offline QA pass remains applicable to its tested scope.
  Native readiness remains blocked, and framework acceptance remains
  `NOT_EVALUATED`.
