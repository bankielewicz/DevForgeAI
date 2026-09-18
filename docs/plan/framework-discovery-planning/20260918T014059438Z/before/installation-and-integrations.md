---
id: DFF-11
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# Installation and integrations

[Framework index](index.md) · [Rust boundary](guardrails-and-rust-runtime.md)

## Purpose and ownership

Define how a portable framework becomes a selected, inspectable installation in a particular project and host. This document owns distribution/activation boundaries and host adapters; it does not declare an installer, update command, GitHub gate, or protected service available today.

Portability means project language, stack, domain and layout are not hardcoded into reusable packages. It does not prove support for every OS, IDE, model or agent host. Compatibility must name and qualify each supported profile.

## Inputs, outputs and dependencies

Inputs are the selected project/root, approved package set and versions, selected policy/expertise, host capabilities, applicable authorization, existing files and ownership, and trusted authority artifacts where protected operation is selected. Outputs include an exact installed-file/ownership manifest, active binding/configuration, compatibility diagnostics, update/removal plan and readback evidence. Actual schema and commands remain to be specified.

Dependencies are [project policy](project-context-and-policy.md), [adaptive package lineage](skills-and-project-expertise.md), [agent configuration](subagents-and-context.md), and [protected runtime](guardrails-and-rust-runtime.md). Installed binding data identifies selected packages; it is not protected acceptance by itself.

## Lifecycle requirements

| Operation | Required boundary |
| --- | --- |
| Inspect | Discover host, project and existing installation without changing them |
| Plan installation | Resolve dependencies, exact destination/ownership and effects; expose collisions and unsupported capabilities |
| Activate | Apply only the selected installation under applicable authorization and read back exact results |
| Update | Preserve user-owned changes, package lineage and prior state; disclose conflicts rather than overwrite silently |
| Roll back | Restore an identified compatible framework version while accounting for affected binding/policy/state formats |
| Remove | Remove only owned selected components; preserve product source and unrelated user configuration |

This is a lifecycle contract to expand, not implementation of these operations. Failure handling must retain partial effects and concrete recovery information. No automatic whole-project reset or removal follows from an incomplete update.

## Integration surfaces

The [Codex/Pro boundary](foundation.md#codex-and-chatgpt-pro-operating-boundary) is mandatory. Base operation uses the user's supported Codex subscription flow; no external LLM backend, extra API billing or Enterprise-only API is required. Exact model availability and remaining usage are account observations, not fixed framework constants. Deterministic Rust checks may run in an ordinary project CI environment if separately configured; this does not assume hosted Codex agent execution or transferred user subscription credentials in CI. Optional integrations needing another service, account or privilege remain unselected and cannot become hidden core dependencies.

- Codex is the investigated initial agent host. Project/user agent definitions and skills have different configuration/installation locations and must be qualified on the selected version.
- Other LLM hosts are architecture extension points. Their prompts, tool permissions, agents and hook capabilities cannot be assumed identical to Codex.
- Git integration requires an actual Git checkout. This workspace's absence of Git metadata does not authorize initialization merely to demonstrate a gate.
- GitHub integration requires explicit repository, trusted execution/publishing identity, selected event/ref policy and server-side configuration. A local hook or arbitrary check named PASS is insufficient.
- Terminal access remains the primary operational path. MCP, a browser or GUI cannot be the sole required means to operate/verify the framework; optional interfaces can expose the same underlying behavior.
- The index/query service is optional knowledge infrastructure with its own lifecycle. It is not silently installed with every expert and does not supply protected workflow acceptance.

## Existing assets and migration

The current [adaptive binding contract](../../plan/skill-builder-adaptive-enhancement-spec.md#6-operational-project-binding-contract) assigns operational project binding to a separately selected setup step. Development sources live under src/agents/skills; operational copies under .agents/skills. Creating this documentation changes neither.

The earlier Windows authority design uses a dedicated service identity, protected storage and local authenticated IPC. Generalizing it requires explicit host-specific provisioning and qualification. Linux/WSL product test results cannot qualify a Linux/WSL authority service. The observed Codex CLI version is a compatibility observation, not proof that hooks or custom profiles have been activated.

## Verification scenarios

Install into a synthetic project with an existing user skill and modified configuration: retain unrelated bytes and report collisions. Upgrade a selected variant whose core changed: require lineage/compatibility assessment without editing the core implicitly. Simulate interruption after a partial write: report actual state and bounded recovery. Remove the framework: keep product files and user-owned configuration. Attempt protected operation without the required host/service: return unavailable instead of substituting advisory output. Test Windows, WSL and Linux profiles separately where selected.

## Open decisions and next expansion

Select initial supported hosts, package/distribution form, ownership-manifest format, update/rollback compatibility rules, operator provisioning, trust roots and remote/GitHub identities. Decide how advisory-only use relates to adaptive binding requirements. Next expansion produces a concrete install/update/remove contract for one declared host against disposable fixtures; actual installation remains a separately authorized task.
