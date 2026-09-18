# Worker startup diagnostics and logging design

## Scope and conclusion

This is a read-only source audit and an implementation proposal. It does not
change the frozen candidate, launch policy, installed Codex configuration, or
prior evidence, and it does not run native Codex.

The completed attempt does **not** establish that the DevForgeAI Rust probe
failed. The probe successfully created the pinned Codex process, queried its
held Job Object, observed one process with zero active processes, and reported a
blocked preflight. The child exit code was 1. The evidence therefore localizes
the unresolved condition to the pinned Codex app-server becoming inactive before
`initialize`; it does not explain why. [S1]

The source does establish an observability gap in the probe. Child stderr is
piped and hashed, but its events are consumed and journaled only inside the RPC
receive loop. The process guard runs before the first request is sent. When that
guard rejects, cleanup does not drain the queued stream events. [S2] [S3] [S4]
The empty outer `stderr.bin` consequently says nothing about child stderr. This
gap can hide an argument/configuration error, a host/runtime startup failure, or
another child diagnostic. Fixing it would materially improve the next
investigation, but it cannot retroactively classify the completed attempt.

The probe currently has no configurable logging levels and no logging/tracing
dependency. It has an append-only, synchronized evidence journal, closed
diagnostic projections, JSON errors on the probe's own stderr, and bounded child
stream handling. Those are useful mechanisms, but they are not a general
logging facility. [S5] [S6] [S7] [S8]

## Current behavior

### Durable evidence journal

`journal.jsonl` is the authoritative run state record. Each accepted record is
serialized, appended, and `sync_all` is called before the sequence advances.
The allowed record kinds are closed and a terminal record seals the journal.
[S5] This evidence must remain mandatory because it supports cleanup and outcome
assessment. A logging setting must never suppress, weaken, redirect, or make
best-effort any required journal record.

The existing preflight diagnostics are also intentionally closed: they contain
process counts, RPC stage/checkpoint, source-review state, and config-validation
categories without raw config, paths, command lines, credentials, identifiers,
or arbitrary server text. [S7] These are safe evidence projections rather than
verbose logs.

### Child output and the startup blind spot

The worker gets three dedicated inherited pipes. Two detached reader threads
read stdout and stderr and send messages into one synchronous channel of capacity
32. A shared 8 MiB counter caps combined stdout/stderr; stdout lines are capped
at 1 MiB. Stderr is represented per read block only as byte count and SHA-256.
[S2]

There are four material limitations:

1. `Incoming::Stderr` becomes a journal record only in `Session::receive`.
   The first process guard runs before `send_until` and before `receive`. [S3]
2. The early-rejection cleanup closes stdin and waits; it does not consume the
   incoming channel. The reader threads are detached and are not joined. [S4]
3. Stderr has no explicit end-of-stream message. The code therefore cannot prove
   that all child stderr was drained before writing `process_exit`. [S2]
4. Blocking sends to the 32-entry channel can stop a reader. If no consumer is
   active and a child writes enough output, the pipe may fill and make the child
   block. The 8 MiB limit cannot prevent that if the reader itself is blocked on
   the full channel. [S2]

The run captures the worker exit code only after cleanup invokes `stop`, whose
implementation calls `TerminateJobObject(..., 1)` unconditionally. [S4] [S9]
For this completed attempt, the held Job Object already reported `total=1,
active=0` before the stop request. The sole assigned process had therefore
terminated before cleanup. `TerminateJobObject` targets processes currently
associated with the job, so it cannot explain that earlier inactive snapshot
and would not ordinarily replace the exit code of a process that had already
terminated. The retained exit code 1 should be treated as the child's observed
code, while still not treating that code as a cause. The record schema's lack of
an explicit `observed_before_stop` disposition remains a generic ambiguity for
other paths where a worker could still be live when cleanup begins. Pre-stop
sampling fixes that broader attribution problem; it is not a theory that cleanup
manufactured exit code 1 in this run.

### Existing configuration surface

The request and nested profile use `deny_unknown_fields`; neither contains a
logging or diagnostics setting. [S10] Native arguments come from a digest-bound,
compiled launch policy and callers cannot append flags. [S11] That policy starts
`app-server --listen stdio:// --strict-config` and supplies fixed `-c` overrides;
it has no diagnostic-log option. [S12]

The main CLI only emits a single `{"error": reason}` object for its own terminal
errors and streams journal events to stdout. It constructs fixed `Options`; no
environment variable, CLI flag, or file selects a log level. [S8]

The separate `devforgeai-index` application should not be used as proof of probe
logging. Its daemon writes a small request/response metadata log, rotates at
10 MiB through five archives, and exposes its path through diagnostics. It has no
level selector. Its launcher also discards detached daemon stdout/stderr. [S13]
[S14] A shared logging component could be considered later, but the worker probe
needs the startup fix within its own process-ownership and evidence contracts.

## Proposed design

### Separate evidence from diagnostic logging

Implement two explicit sinks:

* `EvidenceJournal` retains the current mandatory append/sync semantics and
  closed records used for run outcome, process ownership, cleanup, and inspection.
  It is always enabled.
* `DiagnosticSink` writes a separate `diagnostics.jsonl` in the fresh run
  directory. It is observational, bounded, never read by admission or dispatch,
  and never changes a guard result. Its level may be `off`, `minimal`, `verbose`,
  or `debug`.

The word `off` means **no supplemental diagnostic file**. It does not disable
the evidence journal or the minimum process-exit and stream-summary fields needed
to interpret a terminal result. This distinction must be stated in CLI help and
the schema rather than letting `off` imply that authoritative evidence disappears.

### Bound configuration

Use an explicit, run-local, digest-bound file rather than an installed or ambient
configuration file. A future request-schema revision should add required
`diagnostics_ref` and `diagnostics_sha256` fields. The referenced file should be
read with the existing bounded, literal-path intake rules and copied into the run
directory before spawn.

```json
{
  "schema_version": 1,
  "level": "minimal",
  "redaction_policy": "closed-v1"
}
```

The Rust type must use `deny_unknown_fields`; accepted levels and the redaction
policy are closed enums. Size limits are compiled constants associated with each
level, not caller-controlled numbers. A missing file, digest mismatch, unknown
field/value, reparse path, or oversized file fails admission before spawn. The
selected level and configuration digest belong in `inputs.json`; the config
contents and local path do not belong in ordinary stdout.

### Level behavior

| Level | Supplemental records | Content rules |
| --- | --- | --- |
| `off` | None | Mandatory journal still records spawn/guard/exit, stream totals and hashes, truncation/reader errors, and cleanup state. |
| `minimal` | Process lifecycle and stream summaries | Spawn-return time, PID observation, guard time, natural exit observed before stop, exit code, stdout/stderr byte counts and full-stream hashes, EOF/reader/overflow status. |
| `verbose` | Minimal plus phase transitions | Fixed policy ID/digest, argument count and argument-vector digest, source-review phase, RPC method from a closed enum, queue high-water mark, pipe close timing, and cleanup disposition. No argument values or protocol payloads. |
| `debug` | Verbose plus bounded event detail | Per-stream chunk lengths/hashes, UTF-8 validity, line counts/lengths, redaction/classifier version and closed startup-error categories. No raw or redacted-free child text, raw config, protocol bodies, paths, environment values, tokens, account identifiers, prompts, or model output. |

There should be no ordinary `raw` level. Redaction based only on token patterns
cannot guarantee that arbitrary child output is free of secrets. If a later
investigation truly requires raw stderr, it needs a distinct, explicitly
authorized forensic design with access controls and retention rules; selecting
`debug` must not silently create that exposure.

### Stream ownership and bounded draining

Replace detached readers with owned stream pumps and explicit completion:

1. `OwnedProcess` owns both reader join handles and a stream coordinator.
2. Each pump continuously reads its pipe, updates its own total byte count and
   incremental SHA-256, and emits a final `StreamClosed` summary. It never waits
   for a journal write.
3. The coordinator consumes pump messages from spawn until teardown. Protocol
   stdout lines go to a separately bounded protocol queue. Diagnostic detail may
   be dropped after its compiled budget, while aggregate count/hash processing
   continues. A dropped-detail counter is retained.
4. If protocol stdout exceeds its line/total/queue limit, the coordinator marks
   `output_limit`, closes input, and requests bounded teardown. It must not let a
   full message queue block the pipe pump indefinitely.
5. When the Job Object reports `active=0`, the runner captures the process exit
   code immediately, then drains until both stream EOF markers and reader joins
   complete or the existing teardown deadline expires.
6. Only after recording `natural_exit_observed=true|false`, pre-stop exit code,
   both stream summaries, and drain completeness may cleanup terminate the job.
   A later post-stop exit observation is a separate field.

The mandatory journal should gain a closed `startup_exit` or extended
`process_exit` record containing only:

```json
{
  "observed_before_stop": true,
  "pre_stop_exit_code": 1,
  "post_stop_exit_code": 1,
  "stdout": {"bytes": 0, "sha256": "...", "eof": true},
  "stderr": {"bytes": 123, "sha256": "...", "eof": true},
  "drain_complete": true,
  "reader_error": null,
  "detail_dropped": 0
}
```

The record must be written before the terminal record and must remain present at
every log level. Supplemental logger failure must be reflected as
`diagnostics_incomplete` in mandatory evidence and must not bypass cleanup. A
mandatory journal failure retains the existing `evidence_write_failed` behavior.

### Safe startup classification

Hashes prove identity but cannot explain a message. Add a versioned, closed Rust
classifier that examines bounded child stderr in memory and emits only a safe
category such as `argument_rejected`, `strict_config_rejected`,
`configuration_parse_failed`, `authentication_prerequisite`, `runtime_load_failed`,
or `unclassified`. Each rule must match a narrowly defined byte pattern and have
negative tests. The output records the classifier version and matched category,
never the matching bytes. Unknown output remains `unclassified`; it must not be
guessed from exit code 1. A closed classifier may therefore leave the startup
cause unresolved. Logging levels cannot recover the text discarded by the
completed run, and a future level selection alone does not guarantee an answer.
Retaining arbitrary raw stderr would be a distinct evidence contract and privacy
decision requiring explicit scope, authorization, access controls, limits, and
retention rules.

This classifier is evidence for diagnosis only. It cannot qualify a profile,
relax the fixed argument vector, authorize work, or establish framework
acceptance.

## Minimum change that addresses this attempt

The first implementation slice should avoid a general logging framework and
close the specific attribution gap:

1. own and join both child readers;
2. send EOF for both stdout and stderr;
3. on a failed process guard, capture `exit_code` before stop and drain both
   streams to their EOF/limit within the current teardown bound;
4. retain byte counts, full-stream hashes, drain status, reader error, and
   pre-stop/post-stop exit disposition in the mandatory journal;
5. add a closed classifier for known Codex startup failures; and
6. ensure pipe draining cannot block behind diagnostic persistence.

That slice would show whether the next identical failure has child stderr, prove
whether it was fully drained, distinguish a natural early exit from probe
termination, and often assign a safe cause category. It still may return
`unclassified`, which is more honest than turning exit code 1 into a cause.

The level-controlled `DiagnosticSink` can follow once this required lifecycle
evidence is correct. Adding `tracing` or another facade before fixing ownership
would produce more probe-side messages while leaving the child startup blind
spot intact.

## TDD and acceptance cases

Implementation is subject to the repository's red, green, refactor, QA workflow.
The focused red suite should include real child processes and independent
content/absence oracles:

1. A peer writes one stderr message and exits 1 before the first guard. Assert
   pre-stop exit 1, stderr EOF, nonzero byte count, exact full-stream hash, and
   the expected closed classifier category.
2. A peer exits 1 without output. Assert zero-byte SHA-256, both EOF markers, and
   `unclassified`; do not infer a crash cause.
3. A peer writes more than 32 chunks before protocol receive. Assert bounded
   completion without pipe/channel deadlock and an accurate total/hash or an
   explicit `output_limit` with cleanup verified.
4. A peer writes invalid UTF-8 and a final unterminated stdout line. Assert byte
   accounting remains exact and protocol classification remains unchanged.
5. Capture a naturally exited child, then call cleanup. Assert pre-stop and
   post-stop observations are distinct and natural exit is not relabeled as a
   probe termination.
6. Force reader failure, queue saturation, diagnostics-file failure, and
   mandatory journal failure independently. Assert each has its specified
   outcome and cleanup still runs.
7. Run every level. Assert `off` creates no supplemental file while mandatory
   evidence stays complete; increasing levels adds only the documented fields.
8. Seed stderr, paths, config values, bearer strings, API-key shaped canaries,
   account identifiers, prompts, and arbitrary server text. Assert none appear
   in journal, diagnostics, stdout, stderr, or terminal data at any level.
9. Reject unknown schema fields, unknown levels/policies, digest drift,
   nonliteral/reparse config paths, and oversized diagnostic configuration before
   process creation.
10. Exercise ordinary successful preflight/dispatch peers. Assert stream pumps
    do not reorder protocol lines, change deadlines, alter the `1/1` guard, or
    add an authority input.
11. Verify exact byte and event budgets at their boundary and one byte/event
    above; retries must not erase overflow evidence.
12. Preserve inspection compatibility or version it explicitly. Inspection must
    reject missing mandatory exit summaries and tolerate absence of the
    supplemental file only when the bound level is `off`.

After focused tests, run formatting, Clippy, all required regression and negative
cases, line coverage with the declared full first-party denominator, and Windows
Job Object/process tests. Native Codex behavior remains a separately authorized
attempt after independent QA of changed bytes.

## Staged delivery

1. **Lifecycle capture:** implement owned pumps, EOF/join, pre-stop exit capture,
   bounded drain, and the mandatory stream summary. This directly addresses the
   riddle and should be reviewed as a behavior change.
2. **Diagnostic configuration:** add the digest-bound schema and separate sink,
   the four levels, strict budgets, and privacy tests.
3. **Closed classification:** add only evidenced Codex startup patterns with
   independently written negative fixtures; unknowns remain unknown.
4. **Independent QA:** assess all changed package bytes and required metrics.
5. **Native diagnostic selection:** only after QA passes, prepare a new bounded
   attempt for separate authorization. A pass or cause classification still does
   not issue framework acceptance.

## Numbered source citations

1. **[S1]** `docs/plan/framework-worker-native-diagnostics/20260916T202125Z/diagnostic-report.md:3-33` — observed blocked result, child exit 1, empty outer stderr limitation, and unresolved cause.
2. **[S2]** `devforgeai/experiments/codex-worker-probe/src/process_windows.rs:141-191,195-302` — pipe readers, byte/line caps, stderr hashing, synchronous channel, detached readers, and process creation.
3. **[S3]** `devforgeai/experiments/codex-worker-probe/src/protocol.rs:141-204,249-272,288-307` — stderr consumption occurs in receive; process guard precedes send/receive.
4. **[S4]** `devforgeai/experiments/codex-worker-probe/src/protocol.rs:767-803` and `devforgeai/experiments/codex-worker-probe/src/runner.rs:182-220` — rejection cleanup, wait/stop, and exit journaling without incoming drain.
5. **[S5]** `devforgeai/experiments/codex-worker-probe/src/journal.rs:11-23,44-62,86-162` — closed journal kinds, create-new files, synchronization, sequence, and terminal seal.
6. **[S6]** `devforgeai/experiments/codex-worker-probe/Cargo.toml:1-27` — dependencies contain no logging or tracing framework.
7. **[S7]** `devforgeai/experiments/codex-worker-probe/README.md:13-17,40-46` — preflight scope, closed/privacy-limited diagnostics, fixed vector, journal authority, and exit semantics.
8. **[S8]** `devforgeai/experiments/codex-worker-probe/src/main.rs:26-45,82-103` — probe stderr JSON, fixed options, journal stdout, and no level selection.
9. **[S9]** `devforgeai/experiments/codex-worker-probe/src/process_windows.rs:399-443` — process counts, exit-code observation, unconditional job termination, and stopped wait.
10. **[S10]** `devforgeai/experiments/codex-worker-probe/src/request.rs:15-46` — strict request/profile shape with no diagnostics configuration.
11. **[S11]** `devforgeai/experiments/codex-worker-probe/src/launch_policy.rs:48-82` — strict compiled policy binding and returned fixed argument vector.
12. **[S12]** `devforgeai/experiments/codex-worker-probe/src/restrictive-launch-policy.json:1-121` — actual native app-server arguments and strict configuration overrides.
13. **[S13]** `devforgeai/src/service.rs:114-136,260-267` — separate index request log, rotation, and diagnostics metadata.
14. **[S14]** `devforgeai/src/cli.rs:544-623` — separate index daemon launcher and discarded child stdout/stderr.
