---
id: DFF-WORKER-NATIVE-01
version: 0.1.0
status: proposed-amendment
implementation_readiness: identity-slice-specified-profile-slice-needs-version-verification
native_trial_readiness: blocked
updated: 2026-09-15
---

# Bounded native worker readiness amendment

[Base worker contract](codex-worker-feasibility-v1.md) · [Authority design](../../../plan/devforgeai-codex-rust-enforcement-design.md) · [Discovery](../../../plan/framework-native-readiness/20260915T1937559109498Z/launcher-identity.json)

## Selection and scope

The user selected preparation of executable-identity admission, effective-profile review, two concrete native trial requests, and a bounded authority contract. This document specifies the next worker changes; it does not claim they are implemented or qualify a native execution. The base v1.0.0 contract and its retained QA evidence remain unchanged. Its synthetic fixture, wire schema, one-turn/no-retry limits, error sanitization and verified Job Object cleanup remain mandatory.

Implementation destination is the existing isolated `devforgeai/experiments/codex-worker-probe` package. No index workspace, installed Codex configuration, skill installation, credential store or startup setting is changed by this amendment. Independent QA must assess changed candidate bytes; the prior F-01/F-02 closure remains about its original manifest.

## NI-01: Exact executable identity

Observed on 2026-09-15:

- Captured launcher: `C:\Users\bryan\AppData\Local\Programs\OpenAI\Codex\bin\codex.exe`.
- Its `bin` directory is a junction to `C:\Users\bryan\.codex\packages\standalone\current\bin`.
- `current` is a junction to `C:\Users\bryan\.codex\packages\standalone\releases\0.154.0-x86_64-pc-windows-msvc`.
- Physical executable: `C:\Users\bryan\.codex\packages\standalone\releases\0.154.0-x86_64-pc-windows-msvc\bin\codex.exe`.
- Alias and physical SHA-256: `be96b992178b1e467c225800da0d65f2c86d5eba1ef0b14632f65db381cbdfde`; size 298169136 bytes; fresh `--version` returns `codex-cli 0.154.0`.

Retain `tests/fixtures/schema-command.json` unchanged as historical capture. Add a separate versioned, compiled-in `native-executable-identity.json` with closed fields `schema_version=1`, `adapter="codex-0.154.0-stdio"`, `captured_alias`, `physical_executable`, `executable_sha256`, and `junctions` (ordered entries with `path` and `target`). The values above are the selected identity, not a runtime caller-controlled allowlist. Bind the record into candidate/build manifests.

Rust admission must:

1. Validate the supplied physical executable through the existing strict non-reparse resolver. Never launch the alias. Match the pinned physical path and digest; ordinary relative/parent/UNC/device paths are not newly admitted.
2. Inspect only the exact two compiled-in junction locations, require directory-junction reparse type, and require each target to match the pinned mapping after standard Windows extended-path-prefix normalization. Reject additional/changed reparse components, symlink substitutions, missing targets, loops and another executable. Do not introduce an unrestricted `canonicalize` exception for arbitrary request paths.
3. Resolve the captured alias through that inspected mapping and verify that it reaches the same physical executable. Recheck physical digest and mapping immediately before spawn. Drift is `invalid_worker` (exit 2 before spawn); do not search PATH or refresh the identity automatically.
4. Keep strict reparse rejection for every fixture, run directory, review record and profile-source path. The narrow launcher observation exception grants no filesystem mutation permission.

The mapping is intentionally machine-specific for this feasibility unit. Updates require new discovery, identity selection, schema compatibility review and QA. A same-user adversary replacing executable bytes between checks and process creation is not a protected boundary of this prototype; this amendment must not claim otherwise. The authority contract supplies a different trust boundary.

## NI-02: Versioned restrictive launch policy

The current effective profile cannot be approved: two MCP servers are configured without `enabled=false`, twelve plugins are enabled, and cached plugin hook definitions exist. Static inspection cannot establish their active runtime state or safely approve a no-external-effects finding. A prompt saying not to use tools is not enforcement.

Proposed replacement for the base sections 4–6 prohibition on configuration overrides: allow **one compiled-in, digest-bound native-only restrictive launch policy**, selected through the reviewed policy ID. It may only disable effect-capable integrations and select already-reviewed authentication/provider/sandbox settings. No arbitrary caller-supplied command/config map, environment expansion, script or executable arguments.

The concrete proposed argv array is retained in the readiness evidence as `restrictive-launch-policy.proposed.json`. It uses the discovered executable with `app-server --listen stdio:// --strict-config`; each override is its own `-c` and TOML argument. It sets `model_provider="openai"`, `forced_login_method="chatgpt"`, `web_search="disabled"`, `features.memories=false`; disables each observed MCP server and plugin by exact quoted key; disables default and explicitly configured app entries. It does not change model selection, permissions or instructions beyond the contract's explicit per-thread/per-turn read-only/never settings. No alternative CODEX_HOME, login, credential injection, hook-trust bypass, provider fallback, approval bypass or sandbox weakening.

This argv is **proposed, not qualified against 0.154.0**. The CLI help verifies override syntax and strict-config availability; current online documentation does not prove that every key works in the pinned executable. Before implementing this policy, verify each selected key against version-matched configuration definitions and its actual effective behavior. If a key is unsupported, fail readiness and amend the selected policy explicitly. Never ignore unknown keys or silently select another version. Hooks from non-plugin layers are additive: a higher-priority empty hooks table is not a reliable disabling policy. Any applicable managed/user/project hook not demonstrably inactive blocks this profile.

Select request schema version 2 for restrictive native launches: all v1 request fields remain required and unchanged, while `profile` additionally requires `launch_policy_id` and `launch_policy_sha256`. Review schema version 2 adds the same two required fields to the v1 review. Both are closed schemas and both values must equal the compiled-in policy identity. Version-1 native records cannot authorize the new argv. Peer requests remain schema version 1 with null profile; reject schema2 peers. Keep legacy v1 native admission behavior unchanged for historical compatibility, without treating it as qualification for the new policy. Tests must distinguish legacy and restrictive native variants explicitly.

## NI-03: Honest profile review

Record source paths and SHA-256, explicit absences, configured model/effort, effective provider and authentication mode, active MCP/plugin/app/hook state, inherited environment variable **names** relevant to credential risk, and Windows sandbox mode. Do not copy credential files, token values, account identifiers or raw config containing arbitrary environment/header values. The review must cover the exact fixture cwd and launch policy, including ancestor instructions/config, user defaults, system/managed sources and plugin inputs. A source inventory hash alone cannot prove completeness.

Current static observations are in `profile-review.md` under the readiness root. Configured model `gpt-6-astra` and effort `high` are proposed for the two trials; actual account entitlement and availability require observed protocol preflight and user selection. `windows.sandbox="unelevated"` is a configured mode, not demonstrated filesystem/network isolation. An installed executable/help response does not prove that mode is operational. The narrower no-tool fixture never qualifies arbitrary shell/network workloads.

Every required review boolean must be supported. Unknown stays unqualified; never write all true to make admission pass. Bound a fresh review to each fixture root, launch-policy digest and source manifest. A changed source, new hook/plugin/config layer, altered environment policy or changed executable invalidates the affected review. Inherited API credential/provider variables fail before spawn as in the base contract.

## NI-04: Native trial selection and evidence

Two draft request bundles are prepared at `docs/plan/framework-native-readiness/20260915T1937559109498Z/trials/`. Exact disposable layout selected for future launch:

- `docs/plan/framework-worker-trials/20260915T1937559109498Z-WN-01/fixture/task.json` and sibling `run/`.
- `docs/plan/framework-worker-trials/20260915T1937559109498Z-WN-02/fixture/task.json` and sibling `run/`.

Do not create a `run/` directory in preparation. The fixture bytes, prompt and oracle are the existing base contract's bytes. Draft request files are closed v1 shapes bound to explicitly **unqualified** review records. They are not launch authorization and are not substitutes for the future versioned NI-02 record. Rebuild request/review bytes under the finalized policy schema after admission repair/profile qualification; preserve drafts.

Select `gpt-6-astra`/`high` only after user confirmation and protocol model-list validation; no substitutions. WN-01 complete and WN-02 immediate post-turn-ID cancel each permit one server/thread/turn and zero harness retries. Dispatch 120 seconds, per-RPC10 seconds capped by remaining time, grace5 seconds, teardown5 seconds; process supervisor safety bound145 seconds including evidence finalization. A supervisor timeout retains an errored attempt and triggers owned-process containment; it never counts as a product deadline pass.

WN-01 requires exactly the expected final JSON, no tool/delegation event, unchanged fixture and verified stopped tree. WN-02 requires an observed interrupted turn plus stopped tree; exit5 or interrupt acknowledgement alone is insufficient. Completion racing cancellation is INCONCLUSIVE, not a pass or automatic retry. Auth/model/profile denial is a prerequisite outcome, not proof of defective Codex. Keep both native cases in the denominator; no native success is demonstrated until execution.

## Required development/QA cases

| ID | Independent expected behavior |
| --- | --- |
| NI-T01 | Pinned two-junction mapping admits exact physical path/digest without launching the alias. |
| NI-T02 | Changed junction target or reparse type rejects before spawn; same bytes at another target do not bypass identity. |
| NI-T03 | Executable digest mismatch, missing physical file and unsupported adapter reject; no PATH fallback. |
| NI-T04 | Fixture/run/review/profile reparse paths still reject, including a path through either approved launcher junction. |
| NI-T05 | Alias-target or physical-byte drift between initial admission and pre-spawn check rejects; old evidence unchanged. |
| NI-T06 | Peer admission and original WF-01..20/all subfixtures plus F-01/F-02 regressions remain valid. |
| NI-T07 | Restrictive argv is exact, shell-free and native-only; any supplied config/argv injection rejects. |
| NI-T08 | Old/unknown/mismatched review-policy version/digest and incomplete source inventory block native readiness. |
| NI-T09 | Every disabled integration is proven inactive before thread/turn; unsupported key, managed override or active hook blocks. |
| NI-T10 | Missing/changed profile, API credentials, unavailable Pro/model/effort or unexpected sandbox response prevents turn/start. |
| NI-T11 | WN-01 with qualified exact profile meets content/no-tool/immutability/process criteria. |
| NI-T12 | WN-02 proves interruption/tree cleanup or honestly retains race/denial/failure; no replay. |

NI-T01..06 are a ready bounded offline development slice. NI-T07..10 depend on versioned launch-policy/schema finalization; NI-T11..12 additionally depend on qualified profile and concrete trial selection. No synthetic peer result may pass a native case. Apply >=95% executed-line coverage over all first-party executable source and >=95% required-case pass rate per selected platform; no failed mandatory or security case is waived. Declare denominators before each selected campaign; do not combine unselected native cases into an offline pass claim.

## Sources and maturity

Fresh 0.154.0 app-server help still labels the command experimental. Current [app-server documentation](https://learn.chatgpt.com/docs/app-server) states that the command/transport are not supported for production workloads. Native success would establish only this nonproduction fixture profile.

[Configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic), [configuration fields](https://learn.chatgpt.com/docs/config-file/config-reference), [additive hook discovery](https://learn.chatgpt.com/docs/hooks), and [Windows sandbox modes](https://learn.chatgpt.com/docs/windows/windows-sandbox) informed the review. Documentation was read on 2026-09-15; pinned-version verification remains explicit.
