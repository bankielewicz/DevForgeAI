---
id: DEVFORGEAI-INDEX-SERVICE-001
specification_version: "1.0"
status: proposed
recorded: "2026-09-13"
implementation_status: not_started
---

# DevForgeAI Indexing Daemon and Windows Tray MVP Specification

## 1. Purpose, delivery boundary, and decisions

Build a portable, per-user Rust daemon that indexes explicitly registered projects using Tree-sitter and full-text retrieval. Provide a Windows notification-area (system tray) application with a compact management window. Users can start, pause, resume, and stop indexing; register projects; inspect status; and request rescans or full reindexes. A native daemon runs in Windows, standalone Linux, or a WSL distribution.

This document specifies the application MVP. The companion [CLI query specification](devforgeai-index-query-cli-spec.md) extends the same application with code retrieval. Authoring these specifications does not build, install, or qualify their described software. A subsequent implementation request must select the applicable specification. All executable names and examples below are proposed interfaces.

MUST and MUST NOT are normative. SHOULD is a recommendation whose implementation deviation must be recorded. Requirements apply to the application being built, not to the documentation-authoring session.

### 1.1 Selected product decisions

| Decision | Required MVP behavior |
| --- | --- |
| Hosting | Per-user background daemon; no administrator installation or Windows Service Control Manager registration. |
| Windows UI | Separate tray application plus a compact project/status window. |
| WSL management | Windows tray manages explicitly registered WSL distribution/user pairs. |
| Linux UI | Native CLI; no Linux tray required. |
| Structural languages | Rust, Python, JavaScript/JSX, TypeScript/TSX. |
| Search | Structural and lexical/full-text retrieval; no embedding model or external inference dependency. |
| Authority | Index observations only; no framework phase, mutation-broker, or acceptance authority. |
| Network | No network listener, cloud synchronization, telemetry, or source upload. |

### 1.2 Why a daemon instead of a Windows Service

Windows Services do not directly display interactive UI. A tray controller must be a separate user-session application even when a Windows Service is used. The selected user-session daemon supports the current requirement with less installation complexity. Service Control Manager hosting can be added later for operation after sign-out or under a separate identity; it is outside this MVP. See [Microsoft: Interactive Services](https://learn.microsoft.com/en-us/windows/win32/services/interactive-services).

Linux can run the same daemon in the foreground, detached, or through an optional systemd user unit. WSL lifecycle remains controlled by WSL: shutdown ends the daemon, and systemd services do not themselves keep the distribution alive. Do not promise continuous operation when WSL is stopped. See [Microsoft: systemd in WSL](https://learn.microsoft.com/en-us/windows/wsl/systemd).

### 1.3 Existing workspace and authority boundaries

At specification authoring, the inspected `devforgeai/` directory was empty and no Cargo manifest was found in the inspected source tree. This is a new application foundation, not evidence that a runnable DevForgeAI CLI already exists. Reinspect the target before implementation and integrate any concurrent work without replacement.

The [compiled-Rust enforcement design](devforgeai-codex-rust-enforcement-design.md) describes a different protected authority service. Its proposed `devforgeai-control` interface and trust boundary remain distinct. This indexer runs under the developer's identity; an index hash is provenance, not protection against that identity. No query result establishes framework acceptance. Do not inspect or copy legacy implementations prohibited by that design.

Do not change installed `.agents/skills`, `.claude`, Codex configuration, existing evidence, or project source bytes as part of daemon operation. Runtime project registrations are separate from existing adaptive-framework binding identities.

### 1.4 Mandatory engineering policy

Apply [repository guidance](../../AGENTS.md): red -> green -> refactor -> QA for implementation, executed-line coverage >=95% for first-party framework code, and required-case pass rate >=95%, independently per required platform. Retain counts, denominator/exclusions, commands, tool versions, and raw reports. Skipped, blocked, errored, and unexecuted required cases are not passes; do not round below-threshold values up. A failed mandatory acceptance scenario or authority/security invariant cannot be waived by either numeric floor. These requirements are not a claim that a compiled quality gate already exists.

All framework behavior and terminal/native adapters are implemented in Rust. Codex skill packages may use Python resources and must bind a Python JSONL runner and deterministic graders as required evaluation build artifacts when those skills are built. This MVP creates no skill package and requires no Python runtime for normal daemon/CLI operation; it must not remove or weaken that mandatory skill-build requirement. Python evidence never becomes framework authority.

Every management operation must be invocable and testable from Codex CLI terminal without GUI/MCP dependencies. The tray is the required human UI deliverable, while terminal equivalents provide automation and verification. Native visual QA is additionally required for the tray and is not implied by terminal checks. Specifications must remain concrete and testable, with implemented versus specified status explicit.

## 2. Architecture and implementation units

**DS-001 — Components.** Establish the application Rust workspace under `devforgeai/`, with these logical units:

| Unit | Responsibility |
| --- | --- |
| `devforgeai` binary | Lifecycle/project CLI; later extended by the companion specification. |
| `devforgeai-indexd` binary | Headless scheduler, project registry, scanner, extraction, database, local IPC. |
| `devforgeai-tray` binary | Windows GUI process; menus, compact management window, tray icon, environment selection. |
| Protocol library | Versioned request/response types, operation definitions, errors, limits. |
| Client library | IPC client, deadline handling, environment dispatch, WSL relay. |
| Index library | Language adapters, source snapshots, extraction, coverage, SQLite storage. |
| Platform library | User directories, locks, Windows pipes/process startup, Unix sockets, watcher adapters. |

Keep scheduling and index semantics in shared compiled Rust. The tray and CLI use the same client library and never open SQLite directly. Tree-sitter's native runtime is an allowed parser dependency; no Python runtime is required for this application. Package all grammars and extraction queries with the build. Pin dependencies and retain grammar licenses and query versions. Use a Windows-native tray/window implementation; do not require a browser server or webview runtime.

**DS-002 — Local data flow.** Source files flow through enumeration, exclusion/encoding checks, immutable byte capture, parsing/extraction, and transactional generation publication. IPC operations read published generations or submit management jobs. The daemon owns the only database writer. Tree-sitter supplies syntax trees; project discovery, persistence, comment association, scheduling, and search are DevForgeAI responsibilities.

**DS-003 — Required platforms.** Qualify Windows 11 x64, Ubuntu 24.04 x64, and Ubuntu 24.04 under WSL2. Release separate native Windows and Linux binaries. ARM64, WSL1, macOS, network shares, and cross-filesystem indexing are deferred. Lack of a test host is reported as NOT_RUN, never as a platform pass.

## 3. Environment identity, IPC, and WSL

**DS-004 — Isolation and ownership.** Run one daemon per OS user and environment. Windows uses the current user SID; Linux uses the current UID. A WSL environment is an explicitly registered distribution and Linux username. Assign an opaque environment identity on first initialization. No identity embeds a project-specific constant in source. Every database and runtime endpoint belongs to one environment.

- Windows: a named pipe whose name includes the user identity discriminator; restrict the DACL to the intended user and required OS administration principals, reject remote pipe clients, and check the connecting identity.
- Linux: a Unix-domain socket under a mode-0700 user runtime directory, socket mode 0600, with peer-UID verification. If `XDG_RUNTIME_DIR` is unavailable, use an owned mode-0700 application runtime directory under the user's state directory.
- Obtain an exclusive user/environment lock before creating endpoints. A stale PID alone is insufficient evidence for process termination. Use the lock and an authenticated handshake to distinguish running, stale, and conflicting instances.
- Do not expose TCP or accept arbitrary remote endpoints in v1. No shared cross-environment database.

**DS-005 — WSL bridge.** A Windows environment registration stores an alias, exact WSL distribution name, exact Linux username, and absolute Linux CLI executable path. Use argument-vector process creation and `wsl.exe --distribution ... --user ... --exec ...`; do not interpolate requests into a shell command. Send one protocol request on stdin to the Linux CLI's internal `bridge request` operation and receive one response on stdout. The Linux CLI connects to its local daemon, or performs the explicit bootstrap operation when requested. The internal bridge is not an MCP server.

The bridge accepts only this protocol's known operations and validates all input exactly like a local client. It does not expose arbitrary command execution or source writes. `bridge request` has a bounded input size, no prompts, and no startup-banner output. The selected Linux user owns all roots and data accessed by that request.

**DS-006 — No implicit WSL wake.** Before background status polling, inspect the distribution's running state using WSL inventory. A stopped distribution is displayed as unavailable/stopped without invoking a Linux executable. Recheck immediately before a scheduled bridge invocation; acknowledge the unavoidable check/invocation race in diagnostics. Never deliberately wake it through polling. Only explicit Start may intentionally launch a stopped registered distribution. Running-distribution probes may affect WSL idle behavior; do not promise that polling is lifecycle-neutral.

Stop closes only `devforgeai-indexd`; never call `wsl --shutdown`, terminate a distribution, or change its boot settings. Keep only one polling request in flight per environment. Poll while the management window is open every 5 seconds and otherwise every 30 seconds; suspend WSL executable probes for known-stopped distributions. Failed probes use a 30-second backoff.

**DS-007 — Paths and roots.** All project paths are interpreted by their owning daemon. Windows roots are local Windows paths; WSL roots are native distribution paths. Reject UNC/network roots on Windows and `/mnt/<drive>` Windows mounts in WSL for this qualified MVP. Linux local disk mounts remain eligible. Do not translate a root and silently redirect it to another environment. Linux and Windows checkouts are separate projects, even if their file contents match.

Canonicalize roots with OS filesystem semantics. Reject duplicate or overlapping roots within an environment to avoid ambiguous project ownership. Do not assume Windows paths are universally case-insensitive; use native identity/case behavior. Roots can lack Git metadata. Never follow a directory symlink, junction, or reparse point during traversal. Reject path escape when opening files and exclude linked regular files whose resolved target is outside the root. Non-UTF-8 path names are skipped with a coverage reason in v1.

## 4. Lifecycle and jobs

**DS-008 — States.** Track daemon state separately from indexing state and coverage:

| Dimension | Values |
| --- | --- |
| Client-observed daemon | stopped, starting, running, stopping, unavailable, failed |
| Daemon indexing mode | active, pausing, paused |
| Project activity | queued, scanning, indexing, idle, failed |
| Project coverage | complete, partial, unknown |
| Job outcome | queued, running, succeeded, failed, cancelled, interrupted |

An idle daemon can have incomplete or stale data. Status MUST show these separately. `complete` means all eligible files from the last completed reconciliation were accounted for successfully; it does not mean every project file was structurally parsed. Show structural/text/skipped/error counts separately.

**DS-009 — Start and run.** `daemon run` stays in the foreground and responds to normal termination signals. `daemon start` launches the daemon detached and without a visible console on Windows, then waits for a handshake, up to 10 seconds by default. A matching running daemon returns success with `already_running=true`. Existing paused mode is preserved; Start is not Resume. A new environment defaults to active. Persist paused mode across restart. Concurrent starts result in one owner and consistent responses.

**DS-010 — Pause and resume.** Pause is global to the selected daemon. Stop scheduling new parse/scan work immediately, bring the in-flight file operation to a safe boundary, and report `paused` only after index writers are quiescent. Do not suspend OS threads or block query IPC. Watcher events collapse into bounded dirty-project markers while paused. Resume clears paused mode and schedules a full eligible-file reconciliation for dirty or unverified projects before claiming caught-up status. An already-paused/resumed request is idempotent.

**DS-011 — Stop.** Stop accepts the request, enters stopping, cancels pending work, rolls back unpublished transactions, and closes the endpoint after flushing committed metadata. The CLI normally waits up to 10 seconds for confirmed endpoint/process shutdown. Timeout returns an explicit error; it does not force-kill the process or mean shutdown was cancelled. Published generations survive. Gracefully cancelled jobs become cancelled; jobs left active after a crash become interrupted at startup. A stopped target returns success with `already_stopped=true`.

**DS-012 — Job semantics.** Rescan, reindex, and reconciliation barriers return opaque job IDs immediately. One indexing job runs per project; explicit conflicting reindex/rescan requests return `JOB_CONFLICT` with the existing job ID. Background changes are coalesced behind active jobs. Job cancellation is cooperative and idempotent for cancelled jobs; cancellation after success returns the terminal result without changing it. Retain terminal job records for 7 days. `job status` returns not-found once a record expires.

Rescan enumerates eligible files and reuses unchanged records verified by content hash. Full reindex reparses all eligible files using the installed adapters and replaces the published generation atomically. Full reindex never deletes source or removes the currently queryable generation before replacement succeeds. A file-level extraction error can publish a partial generation; a job-level storage/scan failure cannot publish an incomplete transaction.

## 5. Registration, scanning, and extraction

**DS-013 — Projects and configuration.** Register roots explicitly. The daemon assigns an opaque project ID unrelated to adaptive-framework project bindings. Store display name, canonical root, effective exclusions, text extensions, file-size limit, and timestamps. Changes are made through typed project-update operations; the application does not write configuration into indexed roots.

Removing a project cancels its jobs, unregisters it, and deletes its cached index and snapshots. It never deletes source files. A removal response reports only application-cache deletion. UI removal requires a concrete dialog naming the project and cache effect; CLI removal requires `--yes` for noninteractive automation. Unregistering an environment alias does not stop its daemon or delete its projects.

**DS-014 — Eligible files.** Apply defaults before scanning:

- Respect repository `.gitignore` and `.git/info/exclude`, plus explicit root-relative project exclusion globs. Do not depend on a user's global Git ignore file. Include eligible untracked files.
- Always exclude VCS internals, the application's own data directories, and `.agents/devforgeai/` operational binding/state data. These exclusions cannot be overridden in v1.
- Default dependency/build exclusions: `node_modules/`, `target/`, `dist/`, `build/`, `.venv/`, `venv/`, `__pycache__/`, `.next/`, and `coverage/`; project configuration may override these defaults explicitly.
- Default sensitive-file exclusions: `.env` and `.env.*`, private-key extensions `.key` and `.p12`/`.pfx`, and conventional `id_rsa`, `id_ed25519`, and `credentials` files. These are precautions, not a guarantee of secret detection. Explicitly excluded source is reported as excluded, never as indexed.
- Default maximum file size is 5 MiB. Allow a per-project limit from 1 KiB through 50 MiB. Record oversized files as skipped.
- Support UTF-8 and UTF-8 BOM text. Binary and unsupported encodings, including UTF-16 in v1, receive named skip reasons; do not silently transcode byte coordinates.

Default text extensions are `.md`, `.mdx`, `.txt`, `.json`, `.jsonc`, `.yaml`, `.yml`, `.toml`, `.ini`, `.cfg`, `.xml`, `.csv`, `.sql`, `.sh`, `.ps1`, `.cs`, `.html`, and `.css`, in addition to structural-language extensions. Extensionless and additional files require explicit text-extension/name configuration. Hidden directories are not universally excluded: effective rules decide their eligibility.

**DS-015 — Structural extraction.** Provide fixtures and query adapters for Rust (`.rs`), Python (`.py`, `.pyi`), JavaScript (`.js`, `.jsx`, `.mjs`, `.cjs`), and TypeScript (`.ts`, `.tsx`, `.mts`, `.cts`). Extract supported named functions/methods, classes/types/traits/interfaces, modules, signatures, containing declarations, import syntax, and syntactic calls. Represent anonymous functions as structural outline nodes without claiming stable named-symbol identity.

Capture leading documentation comments/docstrings and internal comments separately. Language-specific rules must avoid attaching a file header or unrelated neighboring comment to a declaration. Python docstrings are string expressions, not comment tokens. Keep comment association kind and original source ranges. Preserve code and comment bytes without generating natural-language summaries.

Tree-sitter `ERROR` and `MISSING` regions produce partial extraction status. Retain useful unaffected captures with parse status, but never claim compiler validity. Imports and call names are syntactic observations; type resolution, macro expansion, dynamic dispatch, cross-file reference completeness, and semantic equivalence are not provided.

**DS-016 — Change handling.** Debounce filesystem changes for 500 ms per project. Bound pending event memory by collapsing overflow into a dirty-project marker. Reconcile every 5 minutes while active, and after restart, watcher failure/overflow, resume, or configuration changes. Reconciliation checks content hashes, not just modification times. Events during reconciliation schedule a follow-up; do not clear newer dirty markers accidentally.

Handle atomic saves, deletes, renames, changing permissions, and unavailable roots. A rename can be represented as deletion plus addition; do not infer cross-generation symbol identity. Capture immutable source bytes and hash the captured bytes before parsing. If a file changes during capture or is unstable, retry capture up to two times, then report it as unstable and leave the project dirty. Never combine a hash from one read with syntax from another. No scan claims an atomic snapshot of a changing filesystem.

**DS-017 — Resource bounds.** Default to two parse workers and one project scan coordinator. Per-file parsing has a cooperative 2-second budget; timeout marks that file partial and permits other work. Backpressure must bound captured-but-uncommitted source bytes to 64 MiB, excluding the currently processed file and parser allocations. Cancellation and shutdown are checked between files and in supported parser cancellation callbacks. Never load every project's source into RAM simultaneously.

## 6. Storage, generations, and diagnostics

**DS-018 — Storage.** Use SQLite with FTS5 and a single daemon writer. Store Windows data under `%LOCALAPPDATA%\DevForgeAI\Index`; Linux uses `$XDG_STATE_HOME/devforgeai/index` or `~/.local/state/devforgeai/index`. Runtime data and endpoint directories are private to the user. Use local filesystem storage, never a database in an indexed root or shared Windows/WSL mount. Back up metadata before a schema migration and refuse newer unsupported schemas; no automatic destructive downgrade.

**DS-019 — Generations.** Each project has immutable logical generations backed by content-addressed captured bytes. Publish a batch through one database transaction. Retain the current and immediately previous published generation, with garbage collection deferred while an in-flight request holds a read transaction. No long-lived pagination lease pins generations: a later page may receive `SNAPSHOT_EXPIRED`. Full reindex stages a new generation while existing queries read the old one. Retain source snapshots only for retained generations. Old build/parser/query versions remain attached to old results.

Generation identity identifies captured records, not an atomic whole-filesystem view. Each record includes the source SHA-256, byte length, source range, language/adapter version, and extraction status. Structural queries must not operate on a mixture of generation identifiers. A failed publication leaves the prior pointer unchanged.

**DS-020 — Coverage and freshness.** Status includes last successful reconciliation time, current generation, requested/active jobs, dirty state, eligible count, indexed text count, structurally indexed count, excluded count, skipped count, and failed/partial file count. Classify root availability, parser capability gaps, watcher failures, and storage failures explicitly. Reconciliation completing with file-level gaps is not complete coverage. Freshness is `observed_current`, `dirty`, or `unknown`; it always includes an observation timestamp and coverage qualifier.

**DS-021 — Diagnostics.** Rotate logs at 10 MiB, retaining five files. Log operation IDs, durations, counts, and diagnostic codes; do not log source contents or query strings by default. Root paths may appear in local diagnostics. Provide a diagnostics view and `daemon diagnostics` command. Corrupt storage produces a degraded service accepting status/diagnostics and explicit rebuild operations. Rebuild quarantines the corrupt database under the application data directory before creating a replacement; do not silently discard it. Preserve separately stored project registrations for recovery. Never follow a user-supplied arbitrary deletion path.

## 7. Shared protocol and lifecycle CLI contract

**DS-022 — Protocol.** Use UTF-8 JSON request/response messages framed by a four-byte unsigned big-endian payload length on named pipes and Unix sockets. Limit requests to 1 MiB and responses to 8 MiB. One request/response per connection in v1. The WSL bridge uses exactly one unframed JSON document on stdin and one on stdout, with identical limits and types.

Request fields: `protocol_version` (integer major, initially 1), `request_id` (UUID), `operation` (registered string), `timeout_ms` (positive bounded integer), and `params` (operation-specific object). The client routes the environment before IPC; the server verifies any supplied project ID belongs to itself. Unknown operations and parameters are rejected; missing required values are errors. There is no generic shell or SQL execution operation.

Response fields: `protocol_version`, `request_id`, `service_version`, `environment_id`, `ok`, `data`, and `error`. `error` is null on success and otherwise contains `code`, `message`, and structured `details`; `data` is null on error. Client-side errors retain this envelope with null service/environment identity when unknown. Negotiation failure returns `PROTOCOL_INCOMPATIBLE` before executing the operation. Additional response fields within major version 1 may be ignored by clients.

Default request timeout is 10 seconds, configurable from 100 ms to 120 seconds. The service enforces its received budget locally, and the client enforces an end-to-end budget including bridging. A mutation timeout can have an uncertain outcome; do not blindly retry. Retain management request IDs and outcomes for 24 hours, returning the same result for an identical retry and `REQUEST_ID_CONFLICT` for changed payloads. Desired-state start/stop/pause/resume operations are independently idempotent. Read-only polling retries stay within the caller's budget.

**DS-023 — Management operations and commands.** Expose these commands with `--json`, `--environment <alias>` (default `local`), and `--timeout-ms` where applicable. Commands referring to a project require `--project <id>` except add/list. No implicit project inference is required in v1.

| Command | Behavior / operation |
| --- | --- |
| `devforgeai daemon start` | Local bootstrap or explicit WSL bootstrap, then handshake; not an IPC request to a stopped process. |
| `devforgeai daemon run` | Foreground host entry point; cannot target a remote environment. |
| `devforgeai daemon status` | `daemon.status`; synthesize stopped/unavailable when no endpoint can answer. |
| `devforgeai daemon pause` / `resume` / `stop` | `daemon.pause`, `daemon.resume`, `daemon.stop`. |
| `devforgeai daemon diagnostics` | `daemon.diagnostics`; bounded output without source contents. |
| `devforgeai environment add-wsl --alias <alias> --distribution <name> --user <name> --cli <absolute-path>` | Save a Windows-side environment registration; no implicit installation or launch. |
| `devforgeai environment list` / `remove --alias <alias>` | Manage client-side aliases; `local` cannot be removed. |
| `devforgeai project add --root <absolute-path> --name <name>` | `project.add`; registers and queues initial indexing if active. |
| `devforgeai project list` | `project.list`. |
| `devforgeai project update --project <id> --config-file <json-path>` | `project.update`; typed exclusion/text/size settings, followed by reconciliation. |
| `devforgeai project remove --project <id> --yes` | `project.remove`; cache-only deletion and unregistration. |
| `devforgeai index status --project <id>` | `index.status`. |
| `devforgeai index rescan` / `reindex --project <id>` | `index.rescan`, `index.reindex`; returns job ID. |
| `devforgeai index rebuild --project <id> --yes` | Explicit recovery after corrupt storage; serialized environment recovery may affect all projects sharing the database and must list them before confirmation. |
| `devforgeai job status` / `cancel --job <id>` | `job.status`, `job.cancel`. |
| `devforgeai tray` | Launch or focus the local Windows tray application; Windows only. |

The rebuild command's CLI preflight prints the affected-project preview; noninteractive use requires `--yes` plus `--affected-projects <comma-separated-ids>` matching the current preview. The GUI presents that same list. Normal reindex has no corruption-recovery side effects.

`--wait` on rescan/reindex observes its job until terminal outcome; default is immediate job-ID return. Waiting times out without cancelling the job. On paused daemons, explicit rescan/reindex is queued and identified as waiting for resume; no hidden resume. Protocol implementation must include operation schemas and representative request/response examples as build artifacts.

The command shorthand in the table applies flags to both alternatives: for example, both `index rescan --project <id>` and `index reindex --project <id>` require a project. `daemon diagnostics` and `daemon status` do not require a project. Internal operations additionally register `index.rebuild`, `index.reconcile` (the query freshness barrier), and `daemon.handshake`; they use the same typed registry and do not create a second service protocol.

**DS-024 — Shared output/exit semantics.** JSON mode writes exactly one JSON envelope to stdout, including failures. Human-readable diagnostics use stderr; stdout is reserved for the requested result. No prompts in JSON mode. Windows and POSIX shells must both be supported without shell-specific parsing assumptions.

| Exit | Category / example codes |
| --- | --- |
| 0 | Successful response, including no matches, already-stopped state, or an accepted queued job. |
| 2 | Invalid input: `INVALID_ARGUMENT`, `INVALID_ROOT`, `UNSUPPORTED_PLATFORM`, `PATH_OUTSIDE_PROJECT`. |
| 3 | Unavailable target: `SERVICE_UNAVAILABLE`, `ENVIRONMENT_STOPPED`, `WSL_CLI_MISSING`. |
| 4 | `PROTOCOL_INCOMPATIBLE`. |
| 5 | Index not fit for the requested freshness: `INDEX_NOT_READY`, `INDEX_INCOMPLETE`, `INDEX_PAUSED`, `SNAPSHOT_EXPIRED`, `STALE_SYMBOL`. |
| 6 | Missing identity: `PROJECT_NOT_FOUND`, `SYMBOL_NOT_FOUND`, `JOB_NOT_FOUND`, `ENVIRONMENT_NOT_FOUND`. |
| 7 | `TIMEOUT`. |
| 8 | Internal/storage failure: `INTERNAL_ERROR`, `STORAGE_CORRUPT`. |
| 9 | Conflict: `JOB_CONFLICT`, `REQUEST_ID_CONFLICT`, `INSTANCE_CONFLICT`, `ROOT_OVERLAP`. |
| 10 | `ACCESS_DENIED`. |
| 11 | Waited job ended unsuccessfully: `JOB_FAILED`, `JOB_CANCELLED`, `JOB_INTERRUPTED`. |

A `job status` response successfully reporting a failed job is exit 0; `--wait` requesting successful completion maps its unsuccessful terminal result to exit 11. This distinction must be documented in help and tested. `daemon status` reports a known stopped local daemon as exit 0; a query against that daemon returns exit 3.

## 8. Windows tray and management window

**DS-025 — UI.** Show one tray icon per interactive user session, with text/tooltips distinguishing disconnected, active, paused, and error states without relying on color alone. Prevent duplicate tray instances. The compact window provides environment selection, project rows, state/progress, last reconciliation, current generation, coverage counters, active job, and actionable error details. Project registration supports a Windows folder picker and explicit Linux path entry for WSL; do not use a Windows picker to imply Linux path validation.

Menus expose Start, Pause indexing, Resume indexing, Stop, Open status, and exit actions. Project controls expose Rescan, Full reindex, Cancel job, Edit exclusions, and Remove. Disable inapplicable controls with an explanatory status. Long work stays asynchronous; no IPC wait on the UI thread. Display success only after the relevant acknowledgment, with queued/running work distinguished from completed work. Repeated clicks cannot enqueue duplicates accidentally.

**DS-026 — Startup and exit.** Windows sign-in startup is opt-in and off by default. Enabling it creates a per-user startup entry for the tray only, without elevation. A separate visible setting controls starting the local daemon with the tray, also off by default. Never auto-start stopped WSL distributions. Exit tray leaves all daemons running. Stop daemon and exit applies only to the explicitly selected environment, shows that target in its label/dialog, and exits only after confirmed stop or an explicit choice to close the UI after a timeout. No global stop of unrelated environments.

Ship an optional Linux systemd user-unit example using `daemon run`, `Restart=on-failure`, and normal user ownership. Explicit Stop must exit successfully so this policy does not restart it. Documentation distinguishes systemd-managed startup from detached startup and prevents simultaneous supervisors. Installing/enabling the unit is a separate user action; do not edit WSL configuration or enable linger automatically.

Expose Windows tray preferences through `devforgeai tray settings show` and `devforgeai tray settings set --launch-at-sign-in <true|false> --start-local-daemon <true|false>`, with JSON/noninteractive support. These are local Windows user-settings operations, independent of daemon availability. This keeps startup configuration accessible from the terminal. `devforgeai tray` without subcommands retains its launch/focus behavior. Configuration changes require an explicit invocation and never start WSL.

## 9. Acceptance matrix

Each scenario requires retained exact commands/actions, expected result, observed result, and platform. Use synthetic fixtures and temporary roots. Native GUI evidence includes screenshots and observed actions; compilation alone is not UI qualification.

| Scenario | Requirements | Required result |
| --- | --- | --- |
| DS-A01: two simultaneous Starts | DS-004, DS-009 | One daemon; both clients get an accurate result; no database/endpoint collision. |
| DS-A02: pause during scanning, edit files, resume | DS-008, DS-010, DS-016 | Writers quiesce; old data remains queryable; resume reconciles edits before caught-up status. |
| DS-A03: Stop and tray exit | DS-011, DS-026 | Stop preserves published data; tray exit alone leaves the daemon; timeout never silently force-kills. |
| DS-A04: crash during publication/reindex | DS-012, DS-018, DS-019 | Prior generation remains intact; unfinished job becomes interrupted; restart reconciles. |
| DS-A05: multi-environment Windows tray | DS-003, DS-005, DS-025 | Local and registered WSL projects route correctly; paths/databases never cross environments. |
| DS-A06: stopped WSL and explicit start/stop | DS-005, DS-006 | Polling does not intentionally launch it; Start can launch it; Stop leaves WSL and unrelated processes running. |
| DS-A07: unauthorized peer and invalid protocol | DS-004, DS-022 | Access or version rejected before operation execution. |
| DS-A08: root boundaries and removal | DS-007, DS-013, DS-014 | Reject overlap/escape; skip symlink/junction traversal; removal changes only app cache/registration. |
| DS-A09: exclusions and encodings | DS-014, DS-020 | Git/user rules, sensitive defaults, untracked files, binary, UTF-16, and oversized cases have exact accounting. |
| DS-A10: language adapter fixtures | DS-015 | All required languages, JSX/TSX, docstrings, nested declarations, comments, ERROR/MISSING cases match expected captures. |
| DS-A11: edits, renames, deletes, overflow | DS-016 | Published data converges after reconciliation; no orphan deleted symbols or lost dirty markers. |
| DS-A12: atomic reindex with active readers | DS-012, DS-019 | Readers see one committed generation; failed/cancelled rebuild preserves prior pointer. |
| DS-A13: resource cancellation and UI response | DS-017, DS-025 | Oversized/slow files bounded; progress stays interactive; no blocking IPC on UI thread. |
| DS-A14: schema/corruption recovery | DS-018, DS-021, DS-023 | Newer schema refused; corrupt bytes quarantined only after explicit scoped rebuild; registrations recoverable. |
| DS-A15: protocol, output, and retry | DS-022, DS-024 | JSON validates; stdout clean; timeout ambiguity retained; repeated request ID cannot double-apply mutations. |
| DS-A16: startup and systemd hosts | DS-003, DS-009, DS-026 | Defaults cause no startup installation; explicit opt-in works; user unit stop does not restart normally. |
| DS-A17: source immutability | DS-001, DS-013, DS-023 | Source manifests before/after management and indexing are byte-identical, except fixture edits made by the test harness. |
| DS-A18: benchmark | DS-017, DS-020 | Record cold/warm indexing, query concurrency, memory, CPU and idle activity on fixed fixtures; no unmeasured performance claim. |
| DS-A19: engineering policy | Section 1.4, DS-026 | Retained red/green/refactor/QA evidence; measured coverage and pass rate each >=95%; CLI-only management/startup settings tested; mandatory failures remain unresolved rather than waived. |

The benchmark fixture must be reproducible from a fixed seed: 10,000 files, 100 MiB total UTF-8 source/text, balanced across supported structural languages and text, with a documented 100-file edit batch. Report hardware, build mode, grammar versions, and three measured repetitions. Treat figures as a baseline, not a promised production SLO. Correctness, response/resource bounds specified above, and native-platform results are separate acceptance dimensions.

## 10. Build sequence, delivery, and deferred scope

Implement in order: shared protocol and local daemon host; source/index engine; lifecycle/project CLI; WSL bridge and Windows tray; then the companion query extension. Specification 1's bridge and core client are prerequisites for WSL tray control; query features are not prerequisites for lifecycle controls.

Deliver source, locked dependencies, bundled grammar/query manifests, protocol schemas/examples, synthetic fixtures, automated checks, native binaries, startup/unit examples, and user documentation. Retain run evidence under a distinct `docs/plan/` run directory. Report static checks, automated runtime tests, Windows native tray qualification, WSL qualification, Linux qualification, and installation separately. Do not claim protected Rust-framework acceptance from this MVP.

Deferred: Windows Service host, administrator installer, cross-user sharing, Linux tray, automatic upgrades, ARM64, remote hosts, MCP, embedding models, semantic search, resolved call graphs, compiler analysis, arbitrary user Tree-sitter queries, source rewriting, Git hooks, skill changes, and workflow enforcement. A future protected authority service must independently verify any index evidence it consumes.

## 11. Sources and interpretation

Official sources consulted on 2026-09-13:

- [Tree-sitter introduction](https://tree-sitter.github.io/tree-sitter/): incremental concrete syntax trees; not a ready-made project index.
- [Tree-sitter code navigation](https://tree-sitter.github.io/tree-sitter/4-code-navigation.html): tags, definitions/references, and documentation captures.
- [Microsoft interactive services](https://learn.microsoft.com/en-us/windows/win32/services/interactive-services): separate interactive UI and service IPC.
- [Microsoft WSL commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands): distribution inventory and explicit distribution/user invocation.
- [Microsoft systemd in WSL](https://learn.microsoft.com/en-us/windows/wsl/systemd): optional hosting and WSL lifetime limits.

All product defaults, component names, protocol contracts, and acceptance criteria in this specification are DevForgeAI design decisions. No listed external library provides framework acceptance authority.
