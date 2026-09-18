# Bounded native diagnostic report

**Diagnostic task completed; native preflight BLOCKED, exit 3.** Exactly one native
attempt ran, with no retry or thread/turn dispatch. The observed failure is
`process_accounting / initialize / before_send / unexpected_process_count`:
the held Job Object query returned **total=1, active=0**, while the unchanged
predicate requires **total=1, active=1**. Framework acceptance remains
**NOT_EVALUATED**. This is no WN-01/WN-02 credit and no native model trial.

## Observed result and classification

The selected original-package Rust CLI created one pinned Codex app-server.
Its mandatory source recheck completed far enough to enter the first initialize
guard. Journal sequence 5 records the successful accounting query with zero active
processes; sequence 6 records `rpc / initialize / process_guard_rejected`.
Sequence 7 requests a stop for `profile_unqualified`. The terminal at sequence 9
reports `outcome:blocked`, `worker_exit_code:1`, `tree_stopped:true`,
`fixture_unchanged:true`, null thread/turn/usage and `oracle:not_evaluated`.

The process was already inactive at the query, before the recorded stop request.
This is not a `query_failed` observation, an extra-process observation, or an
effective-configuration rejection. The recorded exit code 1 does not establish
a crash or its cause. The CLI's stderr file is empty; this does not establish
that the child generated no startup diagnostic, because no approved child
startup cause was retained before the guard rejected.

**Supported classification:** the native startup/liveness prerequisite is
BLOCKED; its underlying cause is UNRESOLVED. The guard rejected according to its
unchanged predicate. No product defect or specific host/profile configuration
failure is established. The available evidence cannot distinguish an unmet
host/profile startup prerequisite, launch/runtime compatibility, or an unobserved
harness interaction. The remaining attribution gap is why this pinned app-server
became inactive before initialize.

`initialize` was not sent: the frozen
[protocol implementation](../../../../devforgeai/experiments/codex-worker-probe/src/protocol.rs)
queries the guard at lines 288-292 before sending at lines 296-300, and its
preflight starts with initialize at lines 386-390. Config inspection, requirements,
features, hooks, plugins, apps, MCP, account, model and rate-limit checks were
therefore **NOT_RUN**. Selected `gpt-6-astra`/`high` availability and Pro
authentication remain unqualified.

Primary evidence: [observed result](observed-result.json),
[native receipt](native-001/receipt.json),
[native stdout](native-001/stdout.bin),
[durable journal](../../framework-worker-trials/20260916T202125Z-diagnostic/run/journal.jsonl),
and [compiled inspection](inspect-001/stdout.bin). The stdout and journal are
identical 2,418-byte files, SHA256
`2c7918e7601a67f9fe6e5511f295653a0e411060082ef23a16cbf5e47217f2d3`.
The inspector returned exit 0, state `blocked`, nine records and no truncated tail;
that exit verifies inspection, not preflight success.

## Exact selection and bindings

Workspace: `C:\Projects\DevForgeAI`. Original package:
`C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe`.
No Git metadata is present. The user-selected
[QA handoff](../../framework-worker-diagnostics-qa/20260916T191731Z/native-diagnostic-handoff.md)
and its artifact-index were verified before work and after execution. The index
SHA256 equals the supplied value:
`552912696c5260091a8cb2305b13d1f1987e53630b610dd66afec55f84d132d9`.

The frozen 58-file candidate manifest is
`C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics\20260916T181820Z-dev\candidate-v2-manifest.json`,
SHA256 `419c98b437a44ce479554170bda36b40f4b8a05b3f2307361680d44fab039540`.
The selected executable is
`C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics-qa\20260916T191731Z\target\debug\devforgeai-codex-worker-probe.exe`,
2,307,584 bytes, SHA256
`0ab81c4c0e6c1a23227cc5c6343c810ae62e37d92dd356b39d8101a34c4d9623`.
No rebuild, source edit, QA wrapper or peer substitution occurred.

The executed request uses the following fresh bindings. Full absolute paths and
sizes are retained in [prelaunch input-bindings.json](inputs-002-prelaunch/input-bindings.json).

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| [Fixture task.json](../../framework-worker-trials/20260916T202125Z-diagnostic/fixture/task.json) | 307 | `b35366b508eea199c12142a8a4a8d13a083426c35c4b9ebaf9f0ccf168eeab3a` |
| [Executed request](inputs-002-prelaunch/request.json) | 1269 | `83852362ed1213fe58a11f647e5ae91ce42fb49e732f111faaca958added6d40` |
| [All-false review v2](inputs-002-prelaunch/review.unqualified.json) | 9096 | `d8693161d6beeca8c50b9faee371bbdb960d79ae720cadaef91570f547ce5125` |
| [Compiled inventory v2](sources-002-prelaunch/stdout.bin) | 30686 | `f98ed9c6e8146082055dc065a4145571c15c9310f21318e53819a6dc37103352` |
| Fixed restrictive launch policy | 3194 | `1dbc48c4a3627f7c5fc7a996935ec507426e4cd90adac058eb81100ac9b526b5` |
| Pinned native Codex executable | 298169136 | `be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde` |

Worker literal path:
`C:\Users\bryan\.codex\packages\standalone\releases\0.154.0-x86_64-pc-windows-msvc\bin\codex.exe`.
Adapter is `codex-0.154.0-stdio`; launch policy is
`codex-0.154.0-readonly-no-external-tools-v2`. Rust supplied the compiled argv.
The physical executable and source/executable junction identities were checked
through unchanged Rust. All four review findings remain false in the prepared
versions and the runtime snapshot.

The runtime's normalized request snapshot has SHA256
`28c04ef9e24f01917f50a281933691190b9f38980c80751f01b9f8669dd4c933`.
Readback verified it equals the executed request after the implementation's
standard Windows extended-path normalization; the distinct input digest was
not confused with this snapshot digest. Its stored review and task are exact
copies of the selected bytes.

## Host, invocation and receipts

Native Windows x64, Windows NT `10.0.26200`, C: NTFS. Shell:
`C:\Program Files\PowerShell\7\pwsh.exe`, PowerShell 7.6.6. Evidence supervisor:
`C:\Program Files\Python310\python.exe`, Python 3.10.11. All commands used cwd
`C:\Projects\DevForgeAI`; no WSL or other checkout was used. Exact environment
and observed process inventories are in [environment.json](environment.json),
[host before](host-processes-before.json) and [host after](host-processes-after.json).

The approved invocation was:

```powershell
python -B -X utf8 docs/plan/framework-worker-native-diagnostics/20260916T202125Z/diagnostic.py launch
```

After refreshing and binding sources in that host context, the supervisor invoked
exactly once:

```text
C:\Projects\DevForgeAI\docs\plan\framework-worker-diagnostics-qa\20260916T191731Z\target\debug\devforgeai-codex-worker-probe.exe preflight --request C:\Projects\DevForgeAI\docs\plan\framework-worker-native-diagnostics\20260916T202125Z\inputs-002-prelaunch\request.json
```

The [supervisor](diagnostic.py) is 11,661 bytes, SHA256
`f3f01f661e22d8f11a10d07ebbe140921072ef54b237883c250ed4b267ca03e6`.
It held stdin open without input and used an exclusive invocation latch and
attempt directory. It preserved the 120-second dispatch, 10-second RPC and
5+5-second cleanup limits. The outer bound was 145 seconds.

Native start: `2026-09-16T20:28:02.089194+00:00`; receipt end:
`2026-09-16T20:28:17.681254+00:00`. Measured process duration: **15.563 seconds**.
No timeout, spawn error or outer containment occurred. The recorded Rust CLI
exit is **3**. The surrounding PowerShell tool reported command exit 1 for that
nonzero external command; the subprocess receipt retains the actual CLI code.
The terminal journal elapsed time is 7.993 seconds and starts after admission;
it is a different interval from the supervisor measurement.

| Operation | Exit | Seconds | Receipt |
| --- | ---: | ---: | --- |
| Initial compiled source observation | 0 | 0.094 | [sources-001](sources-001/receipt.json) |
| Compiled source refresh after host approval | 0 | 0.094 | [sources-002-prelaunch](sources-002-prelaunch/receipt.json) |
| Sole native no-work preflight | 3 | 15.563 | [native-001](native-001/receipt.json) |
| Final compiled source observation | 0 | 0.094 | [sources-003-after](sources-003-after/receipt.json) |
| Compiled terminal inspection | 0 | 0.016 | [inspect-001](inspect-001/receipt.json) |

Only the native preflight launched Codex. Source collection and inspection
invoke the compiled probe's read-only operations. The initial Python preparation
encountered an extended-path spelling assertion after successful collection;
the original helper and failure explanation are preserved in
[preparation-observation.md](preparation-observation.md). This was a preparation
helper error, not a native attempt, product failure or valid TDD red result.
Binding resumed from the same successful inventory without repeating its collection.

The parent environment stayed unchanged. Only `ANTHROPIC_API_KEY` was omitted
from a child-environment copy, with its name recorded and no value logged.
No other credential/provider variable matched the unchanged preflight guard.
There was no alternate CODEX_HOME, login, credential-file read/copy, installation,
policy relaxation, true finding or operational edit.

## Permission refresh, cleanup and preservation

Host approval saved the concrete command prefix. Between initial preparation
and the approved prelaunch observation, the only changed inventory entry was
`C:\Users\bryan\.codex\rules\default.rules`: 106,309 to 106,469 bytes, with hashes
retained in [source-refresh-readback.json](source-refresh-readback.json). The
initial inventory/review/request remain preserved. A fresh inventory and new
immutable all-false review/request were bound after this host-permission change,
before native launch. See [permission-refresh.json](permission-refresh.json).
No agent command edited installed rules or configuration.

Prelaunch and post-launch inventory bytes are identical: 137 entries, 36 physical
file bindings and the same reviewed junction identity. This verifies the selected
control-source scope; it does not inspect credential contents or all unrelated
Codex runtime bookkeeping. No installed-state changes were performed as part of
the diagnostic beyond the host's separately recorded approval-rule update.

The worker PID observation was 66880; supervisor-owned probe PID was 69468.
Unchanged Rust reported stopped-tree verification using held handles. The later
host snapshot independently found neither PID and no probe process; all ten
preexisting observed Codex PIDs were still present. Those PID observations are
supplemental and were not used to authorize killing a historical process.
The outer recorder did not invoke taskkill. The fixture still contains exactly
the original `task.json` bytes.

[Preservation readback](preservation-readback.json) rechecked all 5,821 indexed QA
artifacts, 24 QA-bound inputs, 58 current candidate files, 58 frozen snapshot files,
91 prior native-evidence files and both fresh input versions. Every checked size
and SHA256 matched. The frozen candidate, previous attempt and offline QA result
remain unchanged. No regression/coverage campaign was rerun or claimed here.

## Remaining decision

The consumed one-attempt selection is complete. There is no remaining retry
authorization. Further work would need a separately selected investigation of
the early startup exit, preserving the exact fixed vector and current predicate.
The concrete unresolved question is: **why did the pinned app-server become
inactive before initialize?** Any additional runtime diagnostic, repair, contract
change or installed-state change requires its own selection. No allowlist or
process-count relaxation follows from this result.

The report, input bindings, receipts, journal and readback are bound by the new
[artifact-index.json](artifact-index.json). They are evidence, not a protected
acceptance decision. **Framework acceptance: NOT_EVALUATED.**
