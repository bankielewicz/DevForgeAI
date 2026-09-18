# DevForgeAI index application

Development implementation of [the index-service specification](../docs/plan/devforgeai-index-service-mvp-spec.md). Read the [current evidence](../docs/plan/index-service-implementation/20260914T0727264112301Z/context.md) before treating this as a qualified release. This application observes source; it has no framework acceptance or mutation-broker authority.

## Build and tests

Rust 1.93 or newer and a native C compiler are required for the bundled Tree-sitter grammars and SQLite. Cargo.lock pins the complete dependency graph. From this directory:

```text
cargo build --locked --release
cargo test --locked --all-targets
cargo fmt --all -- --check
cargo clippy --locked --all-targets -- -D warnings
```

On Linux, the CLI and daemon are the supported binaries; tray commands return `UNSUPPORTED_PLATFORM`. The Windows tray uses Win32 controls and notification-area APIs without a browser/webview. Windows ownership tests require a token permitted to create protected DACLs on their own temporary directories. A sandbox denial is an unperformed native check.

## Terminal usage

Keep `devforgeai` and `devforgeai-indexd` in the same directory. Windows also needs adjacent `devforgeai-tray.exe`. Installation and startup changes are separate explicit actions.

PowerShell examples, after building:

```powershell
.\target\release\devforgeai.exe daemon start --json
.\target\release\devforgeai.exe project add --root 'C:\Projects\Example' --name 'Example' --json
.\target\release\devforgeai.exe project list --json
.\target\release\devforgeai.exe index status --project '<returned-project-id>' --json
.\target\release\devforgeai.exe index reindex --project '<returned-project-id>' --wait --json
.\target\release\devforgeai.exe daemon pause --json
.\target\release\devforgeai.exe daemon resume --json
.\target\release\devforgeai.exe daemon stop --json
```

POSIX examples:

```sh
./target/release/devforgeai daemon start --json
./target/release/devforgeai project add --root '/home/example/project' --name 'Example' --json
./target/release/devforgeai index rescan --project '<returned-project-id>' --wait --json
./target/release/devforgeai daemon stop --json
```

`daemon run` stays foreground and handles termination signals. Start preserves paused mode. Pause retains published generations; Resume reconciles dirty projects. `job status --job ID` returns exit 0 even when its data reports a failed job. `index rescan/reindex --wait` returns exit 11 for failed/cancelled/interrupted completion. A wait timeout does not cancel its job. `project remove --project ID --yes` deletes only the registration and application cache.

`project update --project ID --config-file settings.json` accepts typed configuration: `exclusions`, `text_extensions`, `text_names`, `default_exclusions`, `max_file_bytes`. The size limit ranges from 1 KiB to 50 MiB. Configuration is stored in the application state directory, never in the indexed root. Sensitive/VCS/application-state exclusions remain mandatory. Hidden folders are governed by the same explicit rules as other folders.

## Data, recovery and limits

Windows defaults to `%LOCALAPPDATA%\DevForgeAI\Index`; Linux to `$XDG_STATE_HOME/devforgeai/index` or `~/.local/state/devforgeai/index`. `DEVFORGEAI_INDEX_DATA` is an explicit absolute development/test override, inherited by test daemon children; unset it for normal operation. Native roots must belong to their selected environment. No network listener is created. Never point application state at a source tree.

Captured bytes, SHA-256, byte lengths, original source ranges and adapter/query versions are retained in SQLite generations. Byte offsets include UTF-8 BOMs. Tree-sitter syntax errors produce partial results; syntactic calls/imports do not establish resolved references or compiler validity. The companion query CLI is a separately selected extension and is not supplied here.

Two persistent parser workers use rendezvous queues with serial source admission. Only one captured file (maximum 50 MiB) is admitted at a time; this favors a clear memory bound over pipeline throughput. Parser work has a cooperative two-second budget. Full reindex stages replacements while the prior generation remains published. The current and preceding generations are retained; staging failure leaves the published pointer intact.

Registrations are stored separately from the cache for recovery. A corrupt database leaves status/diagnostics available. `index rebuild --project ID --yes --affected-projects ID1,ID2` prints the current affected-project preview to stderr and rejects a mismatched confirmation. It quarantines the corrupt cache under the application data directory. Reindex does not perform recovery. Backups, quarantine and prior run evidence are not silently deleted.

JSON stdout contains one envelope. IPC uses a four-byte big-endian length prefix: requests <=1 MiB, responses <=8 MiB. The internal WSL bridge uses one unframed JSON document. Timeouts are 100–120000 ms (default 10000); mutation timeout outcomes may be uncertain. Retry the same request ID and unchanged payload only when intentionally reconciling an uncertain outcome. See [request schema](schemas/request-v1.json), [response schema](schemas/response-v1.json) and [examples](schemas/examples.json).

## Windows tray and WSL

`devforgeai tray` launches/focuses the native management window and tray. Select an environment and project, then submit an operation. The status panel shows acknowledgment, jobs, generations and coverage; an accepted job is not a completed job. Closing the window hides it. Exit tray leaves daemons running. Stop and exit names the selected environment and requires confirmed stop or an explicit close-after-timeout choice.

Register a WSL identity from Windows with `environment add-wsl --alias ALIAS --distribution NAME --user USER --cli /absolute/linux/devforgeai`. The Linux binaries must already exist; registration installs and launches nothing. `--environment ALIAS` routes through an argument-vector `wsl.exe --distribution ... --user ... --exec ...` invocation. Polling inventories running distributions before invoking Linux and rechecks immediately beforehand. The unavoidable check/invocation race remains; polling may affect WSL idleness. Explicit Start may launch a stopped registered distribution; Stop never terminates WSL.

Startup defaults are off. Inspect with `tray settings show --json`. An explicit `tray settings set --launch-at-sign-in true --start-local-daemon false --json` changes the current user's tray startup entry. Enabling local-daemon startup never starts WSL. These operations change Windows startup configuration; they are not run by builds/tests as installation steps.

The [systemd unit example](packaging/devforgeai-index.service) uses foreground hosting and `Restart=on-failure`. Install it only if you intentionally choose systemd supervision and place binaries at the shown user path. Do not combine systemd and detached-start supervisors. Explicit daemon Stop exits successfully and should not restart under this policy. WSL shutdown ends the daemon; no linger or WSL configuration changes are made.
