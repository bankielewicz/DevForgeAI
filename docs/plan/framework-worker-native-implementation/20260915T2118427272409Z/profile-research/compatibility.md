# Codex 0.154.0 restrictive-profile compatibility review

Status: **BLOCKED for schema-2 native launch**. This review supports a fail-closed implementation of NI-01 and schema-2 intake. It does not qualify NI-07..12. One `codex app-server --help` discovery invocation ran; it exited after printing help. No app-server transport/session was opened, and no thread, turn, integration-inventory, or model RPC was invoked. The probes did not instrument process or network side effects beyond the captured CLI process, so runtime profile effects remain unverified.

## Bound inputs

- Installed executable: `C:\Users\bryan\.codex\packages\standalone\releases\0.154.0-x86_64-pc-windows-msvc\bin\codex.exe`
- Observed version: `codex-cli 0.154.0`
- Executable SHA-256: `be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde`
- Proposed-policy SHA-256: `5744b73169784ef8bba9f87a46ab611828aa14fb4da8d5441354e715b9bd4d0e`
- User-config SHA-256 after the probes: `b438f4fbd9ed78c2fb1878b3f75a61a921eebe8180eac4f786d3d1db8ab32d13`, matching the earlier sanitized profile review.
- A retained read-only inventory found the same user-config bytes and no user, repository-root, or `%ProgramData%\OpenAI\Codex` hook/config/requirements files at the inspected paths. It does not prove the absence of every possible layer or integration source.

The CLI emitted warnings that its arg0 helper could not clean or create temporary aliases under `C:\Users\bryan\.codex\tmp\arg0`; all inspected commands nevertheless completed or failed with their reported exit code. No configuration write command was invoked.

## What 0.154.0 proves locally

The installed binary's help confirms `-c key=value` and `--strict-config` exist. A type-rejection probe through `codex -c <case> features list` distinguished recognized settings from an unknown control:

| Setting family | Deliberately invalid value | Result |
| --- | --- | --- |
| `model_provider` | integer | exit 1, error at `model_provider` |
| `forced_login_method` | unknown enum | exit 1, error at `forced_login_method` |
| `web_search` | unknown enum | exit 1, error at `web_search` |
| `features.memories` | string | exit 1, error in `features` |
| `features.hooks` | string | exit 1, error in `features` |
| `apps._default.enabled` | string | exit 1, error at that field |
| `apps.<id>.enabled` | string | exit 1, error under `apps` |
| `mcp_servers.<id>.enabled` | string | exit 1, error at that field |
| `plugins.<id>.enabled` | string | exit 1, error at that field |
| `definitely_unknown_qa_key` control | string | exit 0 |

This establishes version-specific recognition and typed parsing for the nine known setting forms exercised. Dynamic app, MCP, and plugin identifiers were sampled; it does not prove the operational effect of every configured identifier.

The current effective feature list reported these effect-capable features as enabled: `apps`, `browser_use`, `browser_use_external`, `browser_use_full_cdp_access`, `computer_use`, `hooks`, `image_generation`, `in_app_browser`, `memories`, `multi_agent`, `plugins`, `shell_tool`, `tool_suggest`, and `view_image`.

A non-session probe supplied `features.<name>=false` for all fourteen names and `features list` reported all fourteen as false. That proves the pinned binary parses the feature switches and computes a disabled feature state. It does not prove that a future app-server has no active integrations, hooks, child processes, or connected apps.

## Blocking findings

1. The proposed policy omits `features.hooks=false`. Official OpenAI documentation says hooks are enabled by default, hook sources are additive across layers, and plugin hooks load alongside other sources. A higher-priority empty hooks table cannot remove lower-layer hooks. The exact proposed policy therefore cannot support `no_external_tool_or_hook_effects`.
2. The proposed policy disables named plugins and one named app but leaves thirteen other effect-capable feature families enabled, including `hooks`, `plugins`, `apps`, browser/computer-use, image-generation, multi-agent, shell, tool-suggestion, and view-image. The installed profile currently reports all fourteen observed effect-capable features, including the proposal's existing `memories` setting, as enabled without overrides. A closed trial policy should disable the thirteen additional families and retain exact per-integration entries as defense in depth.
3. There is no non-session CLI command that both applies the policy and performs strict configuration validation. `codex --strict-config ... features list` exits 1 with ``--strict-config` is not supported for `codex features``. Help and typed-parser probes cannot establish runtime disablement.
4. The installed help describes `--strict-config`, but no compatible non-session command in this run proved its unknown-field behavior. Strict parsing would still not prove that recognized integrations are inactive, that an admin/workspace requirement has not pinned them on, or that the configured Windows sandbox is operational.
5. Current official documentation describes the product family, but this run did not obtain a complete version-tagged source checkout. The installed-binary probes and retained 0.154.0-generated schemas are the version-specific evidence. They do not close the runtime-effect gap.

## Required policy correction

Keep the existing exact MCP, plugin, app, provider, authentication, web-search, and memory arguments, then add exact `false` overrides for:

`features.hooks`, `features.plugins`, `features.apps`, `features.browser_use`, `features.browser_use_external`, `features.browser_use_full_cdp_access`, `features.computer_use`, `features.image_generation`, `features.in_app_browser`, `features.multi_agent`, `features.shell_tool`, `features.tool_suggest`, and `features.view_image`.

The policy digest and ID must change after this correction. Do not silently reuse the proposed digest. If a managed requirement rejects or overrides one of these settings, readiness fails.

## Proposed pre-thread qualification sequence

Status: **PROPOSED_UNEXECUTED**. No existing standalone command provides the required proof. If independently implemented and tested, a compiled worker could perform one bounded, contained app-server preflight before allowing `thread/start`:

1. Reverify executable identity and corrected policy digest, then spawn the physical executable with the exact shell-free argv and `--strict-config` under the existing Job Object.
2. Complete only the app-server `initialize`/`initialized` handshake. Do not create or resume a thread.
3. Read `config/read` with `includeLayers=true`, `configRequirements/read`, and `experimentalFeature/list`; require the effective corrected feature switches to be false and reject conflicting/pinned requirements or unaccounted layers.
4. Inspect `plugin/list`, `app/installed`, and `mcpServerStatus/list` with bounded pagination. In the retained 0.154.0 schema, plugin summaries expose `enabled` and `installed`; `app/installed` exposes effective `enabled` and model-tool `callable`; MCP status exposes tools/resources/templates and optional runtime status. Require the closed-state values defined by the qualification contract. These endpoints are observations, so process and protocol-notification oracles remain necessary.
5. Use `model/list` only after the integration checks pass; require exact `gpt-6-astra` and `high` support. Treat authentication, availability, or model-list denial as a prerequisite failure.
6. Stop the contained app-server and verify the entire process tree stopped. Bind raw protocol records, effective configuration, layer/source identities, environment-name inventory, process observations, executable/policy hashes, and timestamps into a fresh review artifact.

`app/list` also exists in the retained schema, but it returns experimental catalog metadata; it is not a substitute for the committed effective runtime state returned by `app/installed`. Because these protocol observations do not independently prove process or network inactivity, unknown, incomplete, paginated-but-unfinished, malformed, or unsupported responses must leave the profile unqualified. Only after this preflight passes may the separate WN-01/WN-02 process start; do not reuse the preflight process as a trial process.

## Primary references

- [OpenAI configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic)
- [OpenAI configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [OpenAI hooks behavior and disable switch](https://learn.chatgpt.com/docs/hooks)
- [OpenAI app-server protocol](https://learn.chatgpt.com/docs/app-server)
- [OpenAI Codex `rust-v0.154.0` source tag](https://github.com/openai/codex/tree/rust-v0.154.0/codex-rs)

Relevant current documentation facts used here: CLI overrides have highest ordinary precedence; `mcp_servers.<id>.enabled`, `plugins.<plugin>.enabled`, `apps._default.enabled`, and `apps.<id>.enabled` are defined; hooks are additive and use `features.hooks=false` as the canonical disable. The retained 0.154.0 schema, rather than current documentation alone, verifies the RPC names and response fields used in the proposed sequence. See `source-receipts.json` and the raw subprocess evidence under `01-version` through `17-config-layer-readback`.
