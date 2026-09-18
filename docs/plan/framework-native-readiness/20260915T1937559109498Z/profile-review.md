# Effective-profile review — BLOCKED for native execution

This is a sanitized static readiness review of the exact installed environment, not a qualified operator approval or a completed native test.

## Observed facts

| Area | Observation | Meaning |
| --- | --- | --- |
| Executable | Physical Codex0.154.0; alias and physical SHA-256 `be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde` | Identity is known; current Rust admission still rejects the captured junction path. |
| Model/effort defaults | `gpt-6-astra` / `high` | Suitable concrete proposal from this user's configuration; native availability and trial selection not observed. |
| User config | `C:\Users\bryan\.codex\config.toml`, initial SHA-256 `b438f4fbd9ed78c2fb1878b3f75a61a921eebe8180eac4f786d3d1db8ab32d13` | Hash binds these observations; any later drift requires review. |
| User instructions | `.codex/AGENTS.md` is empty; repository AGENTS.md applies | Repository requirements remain active. No trial-local instruction/config files were installed. |
| MCP | `node_repl` command server and `openaiDeveloperDocs` URL server configured without disablement | Cannot assert absence of external-tool effects for current profile. No server was activated by this review. |
| Plugins | Twelve enabled names, thirteen cached version candidates | Effective runtime versions not observed. Cache presence is not an activation receipt. |
| Hooks | Five cached version candidates declare hooks: computer-use, unified-computer-use, browser, chrome and chrome/latest | Some may represent duplicate cache versions. This is not a claim five hooks actually ran. Hook trust/effective activation remains unknown. |
| User/project hook files | No hooks.json or inline hooks in inspected user/root layers | This does not rule out plugin/cloud/managed hooks. Higher-priority configuration does not erase additive lower-layer hooks. |
| Apps/search/memory | One explicitly configured app; cached web search; memories enabled | Proposed restrictive launch disables these capabilities for the trial only. |
| Windows sandbox | Configured `unelevated` | No native isolation trial performed. Configuration is not proof of effective read-only/network enforcement. |
| API credentials | No selected API-key/provider env names present in the discovery process | Account state remains unobserved; no credential store read, login/refresh or model request. |
| Rules | default.rules103876 bytes,291 allow-prefix entries | Existing executable approval rules do not establish MCP/hook isolation; unchanged. |
| Host identity | Evaluated process token was non-administrative | Does not establish a separate trusted reviewer identity or provision authority protection. |

Source manifest: profile-source-inventory.json. Extension cache source identities: extension-observations.json. Full user config, environment values and credential stores are not copied. Source absence observations cover documented local candidate locations and the selected ancestry; active cloud/managed state and effective plugin resolution remain unresolved. The all-true native review required by the worker contract cannot honestly be issued from these observations.

## Review disposition by required boolean

- `native_read_only_available`: UNPROVEN. Configured Windows mode and future protocol response need actual effective verification.
- `no_external_tool_or_hook_effects`: NOT SATISFIED by current static profile. Enabled integrations/cached hook definitions prevent qualification.
- `codex_managed_chatgpt`: UNPROVEN. Requires Codex-owned account/read preflight without credential extraction; planType must be pro.
- `no_custom_provider`: No explicit custom provider observed in user configuration; effective provider remains UNPROVEN until complete source/protocol review.

The two `profile-review.unqualified.json` files encode every unresolved required finding as false because the current schema has no unknown value and must fail closed. Their reviewer attribution explicitly identifies static preparation. They must not be edited in place into an approval; retain them and issue fresh qualified review records only after the prerequisites are proven.

## Concrete next change

The proposed [native-readiness amendment](../../../specs/framework/runtime/codex-worker-native-readiness-v1.md) adds strict physical executable identity and a versioned restrictive invocation policy. Its exact20 TOML overrides are in restrictive-launch-policy.proposed.json. These disable selected integrations without editing user or operational files. Base-contract override prohibition must be explicitly amended; pinned0.154.0 key semantics and effective disablement must be verified. An unknown/managed integration that cannot be disabled blocks the trial rather than being waived.

Current official references: [configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic), [MCP/app controls](https://learn.chatgpt.com/docs/config-file/config-reference), [additive hook discovery](https://learn.chatgpt.com/docs/hooks), [Windows modes](https://learn.chatgpt.com/docs/windows/windows-sandbox). These support the review method; local execution determines the selected version's behavior.

## Boundaries preserved

No real Codex turn, app-server session, account/model query, hook activation, profile write, installation, startup mutation or protected acceptance occurred. The only Codex executions were bounded physical-binary `--version`, `--help` and `app-server --help`, with receipts/output retained. Help discovery cannot pass either WN case.
