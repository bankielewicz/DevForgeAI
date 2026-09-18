# Manual app-server: quoted CLI override keys

The user reported native exit 1 with `invalid transport` at `mcp_servers."node_repl"` after the independent `history.notify` correction. The saved launch vector contains `mcp_servers."node_repl".enabled=false`, with literal quotes in the argument. This is a launch-policy defect exposed after the preceding user-configuration error was removed.

The pinned [CLI override parser](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/utils/cli/src/config_override.rs) parses the right-hand value as TOML but retains the dotted key text. The [override layer builder](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/config/src/overrides.rs) splits keys on dots and inserts each segment literally. Consequently, the quotes create a separate server name rather than referring to the existing `node_repl` entry. The new entry has only `enabled=false`. The [MCP configuration conversion](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/config/src/mcp_types.rs) requires a command or URL before considering the enabled flag and emits the reported error when neither exists.

The user's existing `node_repl` entry has a stdio command. It was not removed, disabled globally, or rewritten. Its environment values and executable command were not copied into these artifacts.

## Correction implemented

`C:\Projects\DevForgeAI\Start-CodexAppServerDiagnostic.ps1` now derives a manual argument vector from the unchanged, digest-verified frozen policy. It removes only the embedded name quotes from the 15 matching `mcp_servers`, `plugins` and `apps` override keys. Quoting in values, all other arguments, the 116-token count, strict-config, read-only mode and approval policy remain unchanged. The helper refuses to launch if the expected correction count changes and identifies the correction in console and CheckOnly output.

For example, `mcp_servers."node_repl".enabled=false` becomes `mcp_servers.node_repl.enabled=false`. The same defect affected the second MCP server and thirteen plugin/app overrides. The correction targets their intended names instead of introducing quoted duplicate names.

The old helper is retained as [original-console-helper.ps1](original-console-helper.ps1). The frozen Rust candidate, its snapshot and historical evidence were not edited. The Rust policy still needs a separately selected candidate repair and independent QA; this manual helper change does not qualify it or establish framework acceptance. The earlier compatibility review did not establish this defect and should not be read as proof of correct CLI key interpretation.

## Executed checks and limits

- [Red result](red-result.json): the original helper's actual CheckOnly output created two transport-less MCP entries under the published dotted-key semantics. The expected key-set assertion failed before editing the helper.
- [Verification](verification.json): corrected argument preparation passed in native PowerShell 7 and through Windows PowerShell 5.1 delegation. Independent synthetic fixture assertions checked exact server/plugin/app names, all disable flags, intact string values and the preserved launch restrictions. All 58 files in both the candidate and frozen snapshot matched their retained manifest.
- [Current-config replay](current-config-replay.json): an in-memory application of the corrected arguments retains the existing MCP names and transport fields and disables the intended servers. Only non-secret transport-presence metadata was retained.
- No native Codex process was launched in this investigation. The replay follows the reviewed parsing semantics but is not execution of the complete Codex loader. Native startup remains to be retested by the user.

This finding concerns the saved CLI override format, not a failure of the configured node runtime or MCP server to start. The reported process exits during configuration conversion, before MCP initialization.
