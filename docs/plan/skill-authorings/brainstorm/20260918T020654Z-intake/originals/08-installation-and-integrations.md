---
id: DFF-11
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-17
---

# Installation and integrations

[Framework index](index.md) · [Rust boundary](guardrails-and-rust-runtime.md)

## Purpose and ownership

Define how a portable framework becomes a selected, inspectable installation in a particular project and host. This document owns distribution/activation boundaries and host adapters; it does not declare an installer, update command, GitHub gate, or protected service available today.

Portability means project language, stack, domain and layout are not hardcoded into reusable packages. It does not prove support for every OS, IDE, model or agent host. Compatibility must name and qualify each supported profile.

## Inputs, outputs and dependencies

Inputs are the selected project/root, approved package set and versions, selected policy/expertise, host capabilities, applicable authorization, existing files and ownership, and trusted authority artifacts where protected operation is selected. Outputs include an exact installed-file/ownership manifest, active binding/configuration, compatibility diagnostics, update/removal plan and readback evidence. The existing project-binding-v1 schema remains authoritative; installation commands and the broader ownership/recovery contracts remain to be specified.

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

## Setup intake and proposed activation workflow

`project-setup-and-activation` is a proposed workflow owner, not an installed skill or a numbered phase 0. Project/setup intake identifies the selected root, host, existing Git/tree/instructions/packages, intended identity and authorized effects. Product/work intake and discovery questions remain with DFF-02/03/04; a single conversation can gather these inputs without duplicating answers. Empty projects and existing projects both qualify for inspection. Product discovery is not a prerequisite for registering an already selected complete package.

The proposed bounded flow is **inspect -> identify missing setup -> present concrete changes -> apply authorized changes -> verify/read back -> hand off**. Reuse existing authorization and an already valid setup; do not mint a new identity or rewrite a binding merely because the workflow runs again. Package/role selection consumes actual descriptors and the DFF-05 selection, rather than automatically activating every installed skill.

An initial implementation can register selected already-installed packages. Optional Git initialization, directories and project instructions require their actual selected effects; they are not implied by registration or an empty root. Existing artifacts must be inspected for compatibility and ownership, not blindly overwritten or blindly treated as satisfactory. Unresolved architecture does not justify a fabricated constitution pack. A later installer/updater adds its own dependency, collision, partial-write and recovery behavior under AMB-13.

Preserve the existing binding rules: exact installed bytes, complete descriptors, one active implementation per core responsibility, stable project identity for the same product, revision increments for actual binding updates, and explicit relocation/recheck. Handoff reports actual changed/unchanged files, binding observation and available or blocked selected capabilities. A matching binding establishes applicability, not product readiness or protected acceptance. It does not automatically invoke brainstorming or another skill.

## Setup bootstrap and worktree compatibility

A setup entry point must operate before a binding exists. Giving it the same unconditional binding prerequisite as story-create would create a circular dependency. A standalone setup entry point or an explicitly versioned bootstrap contract must define its pre-binding effects; no existing adaptive schema is modified by this planning statement. The first [brainstorm specification](workflows/phase-1-brainstorm-spec.md) selects ordinary standalone packaging for that separate discovery capability, without bypassing any current binding-required package.

The current binding records one resolved absolute `project_root`, and consumers check that root and the loaded package location. Multiple worktrees therefore need an explicit project-versus-checkout identity and package/binding placement design. Copying a binding to another root or trusting a shared UUID does not satisfy the current check. Before claiming parallel adaptive execution, specify per-checkout availability, relocation versus concurrent checkout behavior, concurrent updates and preservation/recovery tests. AMB-20 records this gap; it is not resolved by Git worktree creation alone.

The conversational skill can explain choices and collect the selected effects. Deterministic framework setup operations and any authority remain compiled Rust under AGENTS.md. Existing Python binding checks remain observations; do not turn them into a replacement mutation broker or protected authorization service. No concrete setup executable or command is selected here.

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
