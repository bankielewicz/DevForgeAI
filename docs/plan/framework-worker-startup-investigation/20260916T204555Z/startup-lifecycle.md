# Rust launcher and worker startup lifecycle investigation

## Scope and disposition

This is a read-only source and retained-evidence investigation of the frozen
`codex-worker-probe` candidate and the single native preflight attempt. It did
not launch Codex, run the frozen executable, change product source, read profile
contents, install anything, or modify prior evidence.

The supplied bindings were rechecked before analysis:

- candidate manifest SHA256:
  `419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540`;
- native evidence index SHA256:
  `1a22ca36d2fe92f86b7ebded1c6345db0d969ee39e600d5d79502fed1d708750`.

**Finding:** the Rust CLI successfully created the pinned Codex process. That
process exited with status 1 before the first `initialize` request and before
the Rust CLI requested cleanup. The retained evidence does not identify why it
exited. The Rust CLI did not demonstrably terminate the live worker early, but
its fixed launch vector and Windows launch context remain possible triggers.
The CLI also has a confirmed observability limitation: it can read child startup
stderr, but an exit discovered by the pre-send process guard bypasses the only
code that records that stderr metadata. This limitation likely hid the most useful
diagnostic evidence.

This establishes a new launcher diagnostic requirement for resolving this
failure class. No reviewed frozen-contract clause required that early-startup
stderr metadata be retained, so this review does not label the limitation a
frozen-contract violation. It is not the cause of the child exit and does not
establish a Codex product defect.

## What the attempt proves

1. Admission, native identity verification and `spawn_intent` completed. The
   next event recorded PID 66880, so `CreateProcessW` returned successfully.
   The journal then recorded `total_processes=1` and `active_processes=0` at
   `initialize / before_send`, followed by `process_guard_rejected` and only
   then `stop_requested` [E1].
2. The guard obtains both counts from one
   `JobObjectBasicAccountingInformation` query [S6]. Microsoft defines
   `TotalProcesses` as all processes associated over the job lifetime,
   including terminated ones, and `ActiveProcesses` as processes currently
   associated [W1]. The observation therefore means that the one associated
   process had terminated before the guard query. Microsoft documents
   `TerminateJobObject` as terminating processes *currently* associated with
   the job [W2]. Because the active count was already zero, the later cleanup
   call did not manufacture this attempt's status 1. Status 1 is the worker's
   pre-cleanup exit status, although it does not say whether the cause was
   argument/config rejection, a runtime error, or another startup failure.
3. `initialize` was not sent. The preflight sets its guard and starts with
   `initialize`; `rpc_inner` runs `process_guard` before assigning an RPC ID or
   writing to stdin [S4]. This rules out failures caused by protocol RPCs,
   including the planned configuration, account, model and rate-limit queries,
   as well as thread/turn or provider work. It does **not** rule out work the
   pinned process performs during bootstrap before RPC readiness. Companion
   pinned-source review found strict configuration loading, authentication
   configuration validation and SQLite state initialization in that startup
   path [C1]. Any of those could fail before `initialize` is received.
4. The outer supervisor held the Rust CLI's stdin pipe open until the CLI
   exited and did not time out or invoke containment [E2]. Independently, the
   Rust launcher retained the worker stdin writer: the writer thread owns the
   parent pipe end and the sender remains in `OwnedProcess` until interruption
   [S2]. There is no evidence of parent-induced stdin EOF before the guard.
5. The Rust launcher assigned the process atomically to a Job Object, inherited
   only three newly created standard-stream handles, set the resolved checkout
   root as cwd, inherited the Rust CLI environment, and used
   `EXTENDED_STARTUPINFO_PRESENT | DETACHED_PROCESS` [S2]. The job's only limit
   is kill-on-close [S2]. These are real launch conditions, but the attempt did
   not isolate any of them as causal.

## Confirmed observability limitation

`process_windows::reader` drains child stderr on its own thread, but converts
each block into only `{bytes, sha256}` and queues it as `Incoming::Stderr`
[S1]. This is privacy-preserving and adequate once a receive loop is active.
The only consumer that turns those messages into journal records is
`Session::receive` [S3].

The failed path never enters that receive loop. `process_guard` detects 1/0 and
returns `profile_unqualified`; `rpc_inner` exits before sending or receiving
[S4]. Because no thread or turn exists, `Session::interrupt` closes stdin and
waits without draining the incoming queue [S5]. Thus the absence of a stderr
event in the journal does **not** mean the child emitted no stderr. The empty
`native-001/stderr.bin` is the Rust CLI's own stderr, since the child stderr was
redirected to the Rust process's internal pipe [E2, S2].

The existing stderr test covers a peer response that reaches `receive`; it does
not cover stderr emitted by a child that exits before the first RPC guard
[T1]. Covering that path is a proposed new diagnostic requirement; it is not
presented as a violation of the frozen contract.

The launcher also samples `exit_code()` only after cleanup in the general
runner path [S7]. The 1/0 guard observation makes the current attempt's status 1
attributable to a prior worker exit, as explained above. Capturing the exit code
at the guard would still remove temporal ambiguity and improve every startup
failure record.

## Could the Rust CLI have caused the exit?

The answer has two parts.

### What is ruled out

- The later `stop_requested` and `TerminateJobObject` cleanup did not cause this
  worker to become inactive; inactivity was observed first [E1].
- The outer Python timeout/containment did not run [E2].
- The Rust CLI did not send malformed protocol data; it sent no protocol data
  at all [S4].
- A simple spawn failure is ruled out. A PID was returned and the Job Object
  counted one lifetime process [E1].

### Plausible parent-supplied triggers, in priority order

1. **Strict configuration or bootstrap state initialization: plausible,
   unproven.**
   The compiled policy invokes `app-server --listen stdio:// --strict-config`
   and then supplies 56 configuration overrides [S8]. The package tests prove
   the policy bytes and `-c` pairing [T2]; they do not execute the pinned
   parser or prove that the installed config plus every override is accepted.
   Current upstream app-server source describes `--strict-config` as failing on
   unknown configuration fields [U1]. A public Windows report documents an
   app-server exit before binding when strict validation encountered an
   app-managed unknown field [U2]. Companion pinned-source review also identifies
   authentication configuration validation and unconditional SQLite state
   initialization before RPC readiness [C1]. These facts make configuration,
   authentication bootstrap, and state initialization credible cause classes;
   none is demonstrated for this attempt, and current evidence cannot rank them
   reliably.

2. **Launch context compatibility: plausible, no supporting failure evidence.**
   `DETACHED_PROCESS`, atomic Job Object membership, the fixture cwd, inherited
   environment and a restricted handle list differ from an ordinary terminal
   invocation [S2]. Microsoft confirms that `DETACHED_PROCESS` removes the
   parent's console for a console process [W3], while `STARTF_USESTDHANDLES`
   supplies the redirected streams. A startup dependency on a console, cwd, or
   spawning a helper under the inherited job could fail. No attempted child is
   visible in job lifetime accounting, and no Windows API call failed, so this
   remains a lower-priority hypothesis.

3. **Argument reconstruction: low-priority hypothesis, still unqualified at
   the OS boundary.** The quoting function follows the usual Windows escaping
   pattern: it quotes every argument and doubles backslashes before quotes and
   the closing quote [S1]. `CreateProcessW` also receives the executable through
   `lpApplicationName`, avoiding executable-path ambiguity [S2]. The fixed
   paths and arguments are representable as Unicode. However, no test makes a
   child echo its parsed argv after passing through this exact private quoting
   implementation. Policy-vector tests alone do not prove the child's parsed
   vector [T2].

4. **Premature stdin close: evidence weighs against it.** The worker's stdin
   pipe remains owned and open until the failed session is interrupted [S2,
   S5]. This should be tested directly with a blocking synthetic child, but it
   is not a good explanation of this attempt on present evidence.

## Repair and test proposal

Apply red-green-refactor-QA to the Rust launcher before another native Codex
attempt.

### 1. Reproduce the visibility failure offline

Add a synthetic child mode that writes a known stderr sentinel, exits with code
1 before reading stdin, and never writes stdout. Launch it through the real
`OwnedProcess` and exercise the pre-send guard. The initial test should fail
because the journal lacks startup stderr metadata. Its assertions should prove:

- job accounting is 1/0 before cleanup;
- the natural exit code is 1 when captured at that boundary;
- stderr byte count and SHA256 are retained;
- raw sentinel content is absent from normal evidence;
- no request was written and no thread/turn exists.

This reproduces the evidence loss without Codex, credentials, installed
configuration or network access.

### 2. Capture a bounded startup snapshot before teardown

Add one nonblocking `OwnedProcess` operation used whenever a guard sees an
inactive worker. It should capture, in this order:

1. one Job Object accounting result;
2. process signaled state and `GetExitCodeProcess` result;
3. queued stdout EOF/error state;
4. all currently queued stderr metadata, aggregated as total bytes, chunk count
   and a streaming digest;
5. Windows errors as numeric codes if any query fails.

Emit one structured `worker_startup_failed` journal event before
`stop_requested`. Keep the original process predicate at 1/1. Do not treat
diagnostics as acceptance or weaken strict configuration.

The current chunk-by-chunk SHA256 is not a digest of the entire stderr stream.
For stable comparison, maintain a streaming digest in the reader and report
both aggregate bytes and the final digest when the stderr pipe reaches EOF.
Bound the drain by bytes and time so a noisy child cannot delay cleanup.

### 3. Qualify the parent launch mechanics offline

Use small compiled test helpers under the same `CreateProcessW` path:

- an argv echo helper to assert the exact parsed policy vector, including
  embedded quotes and trailing backslashes;
- a stdin-liveness helper that remains active with no input, proving the guard
  observes 1/1 until the sender is explicitly dropped;
- a stderr-before-exit helper for the failure above;
- a descendant helper to confirm intended Job Object inheritance and record
  both lifetime and active counts.

These tests should use the actual private launcher, standard handles and
creation flags. A `std::process::Command` substitute would not qualify this
boundary.

### 4. Make logging modes useful without weakening evidence

Separate mandatory audit records from configurable diagnostic detail:

| Mode | Startup information |
| --- | --- |
| `off` | No supplemental diagnostic sink. Preserve every existing mandatory admission, source, spawn, worker, stop, process-exit, terminal and cleanup evidence record unchanged. |
| `minimal` | Add stage, timing, process counts, natural exit code, stderr bytes and aggregate digest. Recommended default. |
| `verbose` | Add policy ID/digest, cwd digest, inherited environment variable names after denylisting, pipe/handle setup results and bounded state transitions. |
| `debug` | Add bounded structured detail such as stream chunk lengths/digests, UTF-8 validity, queue state and closed startup-error categories. Exclude raw child text, arbitrary argv values, config, protocol bodies, paths, environment values and credentials. |

The level should come from a closed Rust-owned configuration enum, be recorded
in the journal, reject unknown values, and never suppress mandatory evidence.
Redaction must occur before durable verbose/debug output. Logging would have
materially helped this investigation because minimal mode would at least bind
the natural exit status and stderr digest, while a closed classifier could retain
a safe startup-error category. Hash-only logging cannot identify the error text
by itself. If bounded raw stderr is ever required, it must use a separate,
explicitly selected forensic-capture contract with its own authorization, access
controls, content limits and retention rules; selecting ordinary `debug` must
not enable it.

### 5. Run the next native diagnostic only after offline qualification

With the repaired launcher, the first separately authorized native attempt
should retain the same executable, fixed argv, cwd, environment rules, Job
Object, 1/1 predicate and no-work preflight. If the new startup event records a
config/parser error, repair or migrate the exact incompatible configuration or
policy key and keep `--strict-config`; do not disable strict validation as the
first response. If stderr is absent, use separately authorized one-factor
trials to compare launch contexts in this order: fixture cwd, detached-console
flag, then Job Object context. Each trial must retain its own evidence and must
not send thread/turn work.

One instrumented attempt may reveal the cause. A no-stderr result will require
multiple controlled trials to distinguish launch-context factors; it should not
be called resolved after a single unchanged retry.

## Evidence and source citations

- **[E1]** [Native journal](../../framework-worker-trials/20260916T202125Z-diagnostic/run/journal.jsonl),
  sequences 3-8; [observed result](../../framework-worker-native-diagnostics/20260916T202125Z/observed-result.json).
- **[E2]** [Native receipt](../../framework-worker-native-diagnostics/20260916T202125Z/native-001/receipt.json)
  and [supervisor](../../framework-worker-native-diagnostics/20260916T202125Z/diagnostic.py), lines 25-103.
- **[S1]** [`process_windows.rs`](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs),
  lines 121-190.
- **[S2]** [`process_windows.rs`](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs),
  lines 195-302.
- **[S3]** [`protocol.rs`](../../../../devforgeai/experiments/codex-worker-probe/src/protocol.rs),
  lines 141-204.
- **[S4]** [`protocol.rs`](../../../../devforgeai/experiments/codex-worker-probe/src/protocol.rs),
  lines 249-307.
- **[S5]** [`protocol.rs`](../../../../devforgeai/experiments/codex-worker-probe/src/protocol.rs),
  lines 767-803.
- **[S6]** [`process_windows.rs`](../../../../devforgeai/experiments/codex-worker-probe/src/process_windows.rs),
  lines 386-408.
- **[S7]** [`runner.rs`](../../../../devforgeai/experiments/codex-worker-probe/src/runner.rs),
  lines 148-217.
- **[S8]** [`restrictive-launch-policy.json`](../../../../devforgeai/experiments/codex-worker-probe/src/restrictive-launch-policy.json),
  lines 1-122.
- **[T1]** [`protocol_edges.rs`](../../../../devforgeai/experiments/codex-worker-probe/tests/protocol_edges.rs),
  lines 165-190.
- **[T2]** [`launch_policy.rs`](../../../../devforgeai/experiments/codex-worker-probe/tests/launch_policy.rs),
  lines 43-208.
- **[C1]** [Companion pinned launch-compatibility review](launch-compatibility.md),
  lines 152-171.
- **[W1]** Microsoft,
  [JOBOBJECT_BASIC_ACCOUNTING_INFORMATION](https://learn.microsoft.com/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information).
- **[W2]** Microsoft,
  [TerminateJobObject](https://learn.microsoft.com/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject).
- **[W3]** Microsoft,
  [Process Creation Flags](https://learn.microsoft.com/windows/win32/procthread/process-creation-flags).
- **[U1]** OpenAI Codex source,
  [app-server main.rs](https://github.com/openai/codex/blob/main/codex-rs/app-server/src/main.rs).
- **[U2]** OpenAI Codex issue,
  [strict-config rejects an app-managed project field on Windows](https://github.com/openai/codex/issues/33181).

## Current classification

- Worker early exit: **CONFIRMED**, status 1 before initialize.
- Rust cleanup caused early exit: **RULED OUT for this attempt**.
- Rust fixed vector or launch context triggered the worker exit: **PLAUSIBLE,
  UNPROVEN**.
- Strict-config/config compatibility: **PLAUSIBLE, UNPROVEN**.
- Bootstrap authentication configuration or SQLite state initialization:
  **PLAUSIBLE, UNPROVEN**.
- Early-startup stderr evidence loss in the Rust CLI: **CONFIRMED observability
  limitation and proposed new diagnostic requirement; no frozen-contract
  violation established**.
- Codex product defect: **NOT ESTABLISHED**.
- Framework acceptance: **NOT_EVALUATED**.
