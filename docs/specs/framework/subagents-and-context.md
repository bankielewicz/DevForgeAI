---
id: DFF-06
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# Subagents and execution context

[Framework index](index.md) · [Expertise](skills-and-project-expertise.md)

## Purpose and ownership

Define optional specialist execution and editable host profiles. A skill supplies guidance, project expertise supplies grounded knowledge, and an agent executes a selected task. A specialist is useful when independent scrutiny or parallel work justifies its context and coordination cost. This baseline does not mandate an agent per phase or create operational agent files.

Inputs are selected work, requirement/policy references, relevant source/evidence, expertise resources, host capabilities and effective configuration. Outputs are candidate changes, observations, counterexamples, decisions needing resolution and a bounded handoff. [Work dependencies](work-items-and-dependencies.md) govern order; [Rust](guardrails-and-rust-runtime.md) owns protected transitions. A role name or separate conversation is not a protected reviewer identity.

## Proposed role catalog

All profiles are constrained by the [Codex/Pro baseline](foundation.md#codex-and-chatgpt-pro-operating-boundary). No model identifier here grants access or requires API billing. Use only models/efforts actually supported by the selected subscription and host; do not route work to another provider or paid endpoint as a silent fallback. Agent-count limits and continuation budgets must fit observable host/account limits. Missing quota telemetry is a gap, not an unlimited allowance.

| Suggested role name | Responsibility | Required handoff content |
| --- | --- | --- |
| coordinator | Maintain selected scope and reconcile dependent work | Outstanding obligations, decisions, current candidate and next work |
| red_test_builder | Develop a focused reproduction for the selected behavior | Test bytes, baseline identity, actual failure and setup distinction |
| green_implementer | Implement the selected contract | Candidate changes and test results against identified assertions |
| refactor_reviewer | Assess/improve structure where justified | Rationale, actual changes or no-change finding, affected checks |
| qa_adversary | Challenge requirements and failure assumptions independently | Counterexamples, observed defects, coverage/gaps and retained oracles |
| project_expert | Supply a selected distinct domain responsibility | Attributed facts, limitations, affected interfaces and unresolved conflicts |

Names above are proposed project profiles, not built-in agents or installed capabilities. A story owner may perform red/green/refactor and regression work in one context. A test for integration behavior need not be a unit test. QA remains adversarial in its expectations, not merely a second agent agreeing with development.

## Codex attribute catalog and applicability

The [official custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) describes standalone TOML profiles under .codex/agents for a project or ~/.codex/agents for personal use. Each profile requires name, description and developer_instructions. Other supported session settings may be layered onto it. This does not mean every global setting takes effect per role on every backend.

The observed local CLI was 0.154.0. No activation trial was performed. The [captured structural schema](references/codex-config-schema-20260915.json) contains all 98 root properties and 171 definitions returned by the live official configuration endpoint on 2026-09-15, including nested keys, types, enums, defaults where declared, references and restrictions. Prose descriptions/examples were removed; fields named description were retained. This is a complete structural inventory of that response, not a version-pinned assertion about the installed binary or per-agent applicability. The three standalone identity fields above are separately described by the custom-agent guide; the general schema alone is not a complete standalone-profile validator.

| Attribute / family | Type and values | Default / customization boundary |
| --- | --- | --- |
| name | Required agent name string | Explicit profile identity; this framework's proposed profiles use distinct nonempty descriptive names |
| description | Required string | Explains when to choose this role; not a routing guarantee |
| developer_instructions | Required string in standalone profile | Role guidance; does not enforce file ownership or gates |
| model | Optional model identifier string | Omission inherits the resolved choice; availability must be checked for the host/account |
| model_reasoning_effort | Optional model-dependent string | Omission uses resolution/inheritance rules; inspect supported model values rather than assume one universal enum |
| model_reasoning_summary | Optional auto, concise, detailed or none in the reference | Presentation setting; not evidence of reasoning quality |
| model_verbosity | Optional low, medium or high where supported | Omission uses the selected model/preset behavior |
| sandbox_mode | Optional read-only, workspace-write or danger-full-access in the reference | Inherited/live parent restrictions and managed policy still matter; no framework recommendation to broaden access |
| approval_policy | Optional on-request, never or supported granular object | Controls host approval behavior, not framework permission or acceptance |
| mcp_servers | Optional keyed server configurations | Per-server transport, enablement, tools, timeouts and environment fields are in the structural schema; secret values are not placed in these documents |
| skills.config | Optional array of skill path/enablement overrides | Only supported selected skill overrides; this does not install a skill |
| Other supported session keys | Full types and nested constraints in the captured schema | Consult the official reference and validate applicability; absence of a schema default does not imply false, zero or unlimited |

The effort documentation and schemas evolve: the custom-agent guide discusses low/medium/high/xhigh/max/ultra while other reference material includes minimal or narrower sets. The captured ReasoningEffort schema accepts a nonempty string. Neither source establishes that every model accepts every value. The host/model compatibility check must reject unsupported combinations; do not silently substitute another model or effort. [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)

Global agent settings are separate from each role's instructions:

| Key | Type / constraint | Meaning and qualification note |
| --- | --- | --- |
| agents.enabled | Boolean; documented default true | Enable multi-agent tools; backend feature selection can affect precedence |
| agents.max_concurrent_threads_per_session | Integer >=1 in captured schema | Cap open spawned threads; omission uses backend default, not an assumed unlimited value |
| agents.max_threads | Documented legacy alias | Compatibility setting; do not emit both aliases with conflicting values |
| agents.default_subagent_model | String | Default spawn model when not otherwise selected |
| agents.default_subagent_reasoning_effort | Model-dependent string | Default spawn effort |
| agents.interrupt_message | Boolean; documented default true | Whether an interruption message enters agent context |
| agents.max_depth | Integer in captured schema | Backend-specific V1 nesting control; not a universally effective V2 limit |
| agents.<role>.config_file | Path string | Alternate declared-role layer, resolved relative to declaring configuration |
| agents.<role>.description | String | Declared-role guidance; distinct from omission of required standalone profile description |
| agents.<role>.nickname_candidates | Array of strings in captured schema | Role nickname candidates; backend/version applicability still needs a trial |

Native configuration does not supply framework fields such as phase predicates, requirement ownership, required platforms, story dependencies, protected approval or a run continuation budget. Those belong to the approved workflow/policy contract, not invented keys in a Codex TOML file.

## Editable example and resolution rules

The following is documentation, not an installed profile. Commented model/effort lines are edit locations, not a recommended model choice:

```toml
name = "red_test_builder"
description = "Create a focused reproduction for a selected requirement."
# model = "MODEL_ID_SUPPORTED_BY_YOUR_HOST"
# model_reasoning_effort = "high"
developer_instructions = """
Use the selected requirement and project testing conventions.
Create and execute a focused reproduction.
Report the baseline, test bytes, actual failure and setup limitations.
Return observations for external validation.
"""
```

For each proposed role, substitute its name, description and concrete responsibility from the table; model/effort can be chosen independently. Omitted settings inherit. The guide describes model/effort resolution from explicit spawn values, global agent defaults and parent settings, followed by file overrides. A file changing only the model may preserve an already resolved effort. Parent live sandbox/approval overrides and managed policy can supersede file defaults. Record effective settings rather than infer them from a file alone.

## Context, change and verification

Give an adversarial reviewer the requirements, current candidate, independent oracles and relevant counterevidence. Fresh context is an option to evaluate, not proof of independence or a mandate to hide relevant history. Preserve a story's ownership across handoffs; avoid four context transfers merely because TDD has named phases.

Capture host/version, profile bytes, selected model/effort, effective permissions, task inputs and observable usage. Unavailable token/cost telemetry remains unavailable. Changing the model creates a new invocation configuration; it does not erase a valid native test of unchanged source/tests/tools. Agent-behavior evaluation about the old configuration cannot be relabeled as evidence for the new one.

Required scenarios include incompatible model/effort rejection, conflicting live/file permission settings, a QA agent identifying an OrderDesk race missed by the implementer, a role declining an unrelated responsibility, and a handoff preserving a known failure. Measure useful outcomes and overhead before selecting more agents; no percentage savings is asserted.

## Open decisions and next expansion

Pin the first supported host/backend/config schema and run native profile-resolution trials; decide allowed model overrides, context selection, task isolation and usage reporting. Specify test-revision invalidation narrowly before adopting automatic repeated cycles. Next expansion compares one story owner plus adversarial review with optional specialist delegation on the same bounded task, preserving outcomes and actual usage. No operational profiles or permissions are changed by this baseline.
