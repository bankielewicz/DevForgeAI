# Pinned 0.154.0 launch compatibility review

## Conclusion

The process that exited with code 1 was the pinned Codex 0.154.0
`codex.exe` child. The DevForgeAI Rust probe remained healthy, observed the child
as inactive, applied its unchanged `total=1, active=1` guard, and then returned
its own documented blocked exit code 3. This evidence does not identify which
Codex startup operation returned the child exit code.

The retained launch vector is structurally compatible with the pinned CLI. No
specific Windows quoting defect, TOML quoting defect, disabled feature dependency,
`DETACHED_PROCESS` incompatibility, or closed stdin explains the exit. The two
strongest unresolved candidates are:

1. a strict configuration or bootstrap configuration rejection; and
2. an immediate user-home runtime-state initialization failure, including access
   to the Codex SQLite state.

The current evidence cannot rank those two reliably because the probe redirected
the child's stderr into its own pipe, converted each read block to only a byte
count and SHA-256, and reached the process-count guard before draining that pipe.
The outer probe's empty `native-001/stderr.bin` is therefore not the child's
stderr. A deterministic error message may have been queued and discarded during
teardown.

This is a startup observability gap in the Rust probe. It is not evidence that the
Rust probe caused the Codex exit, nor evidence of a Codex product defect.

## Evidence boundary

This review was read-only. It did not launch Codex, execute the probe, inspect the
live installed profile or credentials, modify the candidate, or alter retained
evidence. It used the frozen native diagnostic, retained 0.154.0 discovery
records, candidate source, and the official OpenAI `rust-v0.154.0` source tag.
Current documentation was not treated as proof of pinned behavior.

Important local bindings:

| Artifact | SHA-256 |
| --- | --- |
| `src/restrictive-launch-policy.json` | `1dbc48c4a3627f7c5fc7a996935ec507426e4cd90adac058eb81100ac9b526b5` |
| `src/process_windows.rs` | `11aefb84b0cc867e94887e5c93c4a2ae20a6577e38e9aca08f6da11823332f4d` |
| `src/runner.rs` | `6b5a11f9c22446efbea7541ad882e4cb7f637f2e82115240d5a7e50b4bf834cf` |
| `src/protocol.rs` | `9a1768d044e237e8d6070e1c5c94569c2801af89d671d2fea6da0fb6f5a50b6e` |
| Retained 0.154.0 app-server help | `95d290035d274e91e6f85b9af63e9a3fd2cf70a2295d9eedbfc23a2ee82d4383` |
| Retained 0.154.0 feature baseline | `10e096f2fdf3dd3546065097bb3eadccb1336d91160586fb4a5b0a6eeb577ec9` |
| Native journal | `2c7918e7601a67f9fe6e5511f295653a0e411060082ef23a16cbf5e47217f2d3` |
| Native attempt receipt | `6e6ae8d21e9855948e642327e9b467ce99db4d973ad9d3a317bf64178e4e0f06` |

The pinned executable remains the 298,169,136-byte file with SHA-256
`be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde`.

## What the one attempt proves

The journal records `spawn_intent`, then `server_started`, then the first
preflight guard observation with `total_processes=1` and `active_processes=0`.
No initialize message was sent. The held process handle subsequently returned
exit code 1. The probe recorded and verified cleanup and exited 3.

`server_started` means `CreateProcessW` returned successfully and the probe held
the process and Job Object handles. It is not an app-server readiness event. The
child could have failed immediately after process creation.

The roughly four seconds between `spawn_intent` and `server_started` do not show
that Codex ran for four seconds. `runner.rs` performs its final executable/source
check after recording `spawn_intent` and immediately before calling
`OwnedProcess::spawn`; hashing the 298 MB binary occurs in that interval. Only
about 103 ms elapsed between `server_started` and the failed guard, and that
interval includes the post-spawn source-review work. The child therefore failed
very early. That timing favors parsing/bootstrap/access failures over a bounded
protocol timeout, but it does not prove a specific cause.

## Launch-vector assessment

### Windows quoting and TOML values

`process_windows.rs` builds one Windows command line because `CreateProcessW`
requires it. Its `quote` routine wraps every argument and implements the standard
backslash-before-quote and trailing-backslash doubling rules. It supplies the
executable separately as `lpApplicationName` and also quotes it as `argv[0]`.
There are no NUL-containing arguments.

The inner quotes in values such as `model_provider="openai"` and quoted dotted
keys such as `plugins."documents@openai-primary-runtime".enabled=false` remain
literal characters inside the reconstructed argument. That is the form expected
by the CLI's TOML parser. Earlier retained 0.154.0 probes reached typed config
validation for the string/enum forms and for dynamic app, MCP and plugin keys.
Those facts make a Windows/TOML quote-loss defect unlikely.

This source review is stronger than the existing tests for command-line quoting:
the package asserts the fixed logical vector, but has no direct child-argv
round-trip test containing the policy's embedded quotes. Adding that offline test
would close a test gap, although it is not the leading explanation for this exit.

### Command and option placement

The vector begins:

```text
app-server --listen stdio:// --strict-config -c <value> ...
```

Pinned local help explicitly accepts `-c`, `--strict-config`, and
`--listen stdio://` as app-server options. It states that each `-c` value is
parsed as TOML and that strict mode rejects configuration fields unrecognized by
that Codex version. The command and option placement are therefore supported by
the selected executable.

Earlier discovery never ran the exact final 116-element app-server vector.
Fourteen original feature disables were exercised through `features list`; the
later 21 feature names came from the exact pinned feature registry, but their
combined app-server startup was first exercised by the blocked attempt. Static
tests prove vector bytes and admission, not native parsing of the whole vector.

### Disabled features

All 35 disabled names occur in the retained 0.154.0 feature list. The official
tagged feature implementation applies false values directly and normalizes only
the `code_mode_only -> code_mode` dependency. The local app-server uses the local
code-mode provider, so disabling `code_mode_host` does not hit the tagged source's
remote-host requirement. The removed `tui_app_server` flag remains enabled and is
documented in source as a compatibility no-op.

`features.sqlite=false` is not a way to make app-server startup stateless. In the
pinned app-server source, SQLite state initialization is unconditional and occurs
before the stderr tracing subscriber is installed. The feature flag controls
other rollout persistence behavior; disabling it does not bypass app-server state
database initialization. No reviewed feature dependency establishes that one of
the false switches must terminate app-server.

This lowers the disabled-feature-dependency hypothesis. It does not fully
qualify every runtime effect of the policy.

### `DETACHED_PROCESS` and stdio

The Rust launcher creates inheritable stdin/stdout/stderr pipes, removes
inheritance from the parent ends, restricts inherited handles to the three child
ends, sets `STARTF_USESTDHANDLES`, atomically assigns the process to the Job
Object, and retains the parent stdin writer. The diagnostic supervisor also held
the probe's own stdin open. No EOF was deliberately sent to the Codex child
before the failed guard.

The pinned app-server source explicitly handles Windows operation without a
console: if registering a Ctrl+C listener fails for a detached daemon, it keeps
the local control path active. Stdio is an explicit supported transport. These
facts make `DETACHED_PROCESS` or missing console inheritance unlikely to explain
an immediate exit.

## Leading unresolved causes

### 1. Strict or bootstrap configuration rejection

This is a strong candidate because it fits an exit within the first observed
100 ms. In pinned source, app-server parses all CLI overrides, loads configuration
through a strict `ConfigManager`, validates auth configuration, and returns an
error when strict configuration loading fails. The earlier local research noted
that no non-session command could validate strict mode with the exact policy:
`features list` rejects `--strict-config` as unsupported for that subcommand.

Possible members of this class include an invalid combined override, a config
field accepted by another surface but rejected by app-server strict loading, or
an unrecognized field in an inherited configuration layer. The investigation did
not read the current live configuration content, so none is established.

### 2. Codex-home runtime state access or initialization

This is also credible. Pinned app-server source initializes SQLite state before
starting its stderr tracing subscriber and returns exit failure if initialization
fails. Retained commands using the same executable repeatedly warned that access
was denied while cleaning/creating `C:\Users\bryan\.codex\tmp\arg0` aliases,
although those commands continued. The native host snapshot also contained ten
preexisting Codex processes. Those facts show concurrent Codex use and at least
one user-home access problem; they do not show a database lock, corrupt database,
or failed state write.

The very short observed lifetime makes a long database lock timeout less likely,
while an immediate access denial remains possible. Read-only inspection of the
retained evidence cannot distinguish it from configuration rejection.

## Why the startup diagnostic disappeared

The child stderr is not connected to `native-001/stderr.bin`. It is connected to
an internal pipe owned by `OwnedProcess`. The reader thread turns each block into
`Incoming::Stderr { bytes, sha256 }`, omitting content. `Session::receive` is the
only code that journals those events. Preflight calls `process_guard` before its
first send or receive, so an already-dead child causes `profile_unqualified`
before the queued stderr events are consumed. Teardown then drops them.

Consequently:

- empty outer stderr says only that the Rust probe did not write to its own
  stderr;
- the journal's lack of a stderr event does not prove the child wrote no stderr;
- increasing Codex verbosity alone cannot help while the probe discards queued
  startup diagnostics.

## Concrete repair and next diagnostic design

The smallest useful repair is in the Rust probe's process/protocol boundary:

1. When the first process guard sees `total=1, active=0`, read the process exit
   code and perform a short, bounded drain of already-queued stdout/stderr before
   teardown.
2. Retain a bounded startup-error artifact. For ordinary evidence, store byte
   count, full-stream SHA-256, UTF-8 validity, and a closed redacted error class.
   For an explicitly authorized diagnostic mode, store bounded raw stderr in a
   restricted evidence file after reviewing its potential to contain local paths
   or configuration data.
3. Distinguish `child_exited_before_initialize` from
   `unexpected_process_count`; keep the process-count predicate unchanged.
4. Hash the complete stderr stream, rather than separate read chunks whose
   boundaries are scheduler-dependent.
5. Add Windows argv round-trip coverage using a purpose-built test child with
   the policy's embedded quote/backslash shapes.

For Codex 0.154.0, the tagged app-server already supports `RUST_LOG` for module
filters and `LOG_FORMAT=json` for structured stderr. Those are environment
controls, not the requested probe configuration file, and they take effect only
after configuration and SQLite initialization. Fatal early errors should still
be returned by the CLI, so retaining stderr is the primary fix. A later closed
diagnostic policy could set `LOG_FORMAT=json` and one reviewed `RUST_LOG` value;
it should not accept arbitrary caller environment injection.

If the Rust probe gains configurable logging, use a closed enum such as
`off|minimal|verbose|debug`, fixed sinks beneath the fresh evidence root, bounded
rotation/size, structured event schemas, and secret/path redaction. Mandatory
admission, child exit, cleanup, and decision records should remain present at
every level. `minimal` should include a sanitized early-startup failure. `debug`
may add raw child diagnostic custody only when explicitly selected. This would
make future failures explainable, but it cannot reconstruct the lost stderr from
the consumed attempt.

After that repair has its own TDD and independent QA, one separately authorized
diagnostic can use the same pinned executable, vector, fixture, and 1/1 process
predicate. The decisive outcome should be the retained child startup error, not
a relaxed guard or a retry of the current evidence.

## Official pinned-source references

- [OpenAI Codex `rust-v0.154.0` source tree](https://github.com/openai/codex/tree/rust-v0.154.0/codex-rs)
- [Pinned app-server startup, state initialization, and logging source](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/app-server/src/lib.rs)
- [Pinned feature registry and dependency normalization](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/features/src/lib.rs)

These primary references support source-path compatibility findings. They do not
substitute for the missing runtime stderr or establish the actual exit cause.
