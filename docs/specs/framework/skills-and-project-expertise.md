---
id: DFF-05
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-17
---

# Skills and project expertise

## Purpose and ownership

DevForgeAI combines reusable engineering workflows with expertise grounded in the selected project's requirements, architecture and operating conventions. A project should receive the responsibilities it needs, not a predetermined collection of personas. This document plans how those responsibilities are selected, specialized and maintained. It does not implement a router, installer or agent supervisor.

The [foundation](foundation.md) owns framework purpose and boundaries. [Project context and policy](project-context-and-policy.md) owns project facts, applicable instructions and selected quality policy. This capability owns skill responsibilities, specialization lineage and expert artifact contracts. [Subagents and context](subagents-and-context.md) owns delegation and context transfer; a skill responsibility does not imply a dedicated worker. [Quality and delivery](quality-and-delivery.md) owns assessment and completion distinctions. The [document index](index.md) identifies the complete planning baseline.

## Reusable contract and agreed boundaries

Preserve the existing adaptive roles:

| Role | Responsibility | Required boundary |
| --- | --- | --- |
| `core` | Reusable lifecycle guidance that discovers applicable project conventions. | Do not invent a language, layout, architecture or development style. |
| `project_variant` | A separately named specialization of one selected core. | Preserve upstream bytes and account for every parent requirement. |
| `expertise` | A distinct product responsibility supported by domain evidence. | State ownership, exclusions, activation and exchanges with other responsibilities. |

These meanings come from the [builder adaptive contract, sections 2 and 5](../../plan/skill-builder-adaptive-enhancement-spec.md). Its role is a skill responsibility, not a native agent profile, privileged identity or permanently running worker. It rejects redundant roles and does not require a fixed phase or worker count. Language/layout portability does not establish tested support for every environment.

Retain an existing skill when it already satisfies the need. Create a variant when selected project conventions require a real specialization. Create expertise when there is a distinct, evidenced responsibility that the existing set does not cover. Adding references to an existing responsibility can be preferable to another package. Semantic overlap needs review; different names alone do not prove different responsibilities.

A managed project uses its selected quality policy. DevForgeAI's own implementation remains subject to this repository's Rust and 95% requirements; those requirements are not silently imposed on every managed product. Policy resolution remains owned by the context and quality documents.

## Inputs, outputs and dependencies

Selection consumes an explicitly identified project, applicable policy, requested lifecycle outcomes, bounded project evidence, existing selected packages and their exact identities, and any selected parent cores. Evidence distinguishes observed facts, user-supplied requirements and unknowns. Missing evidence is not proof that a capability or convention is absent.

The output is a concrete proposal: retain/create/revise decisions, distinct responsibilities and exclusions, requirement and fact references, prerequisites, required capabilities, activation and near-miss cases, and producer-consumer contracts. Each handoff identifies its artifact, required content, consumer and behavior when absent or invalid. Current `propose`, `author_set` and `review_updates` records remain governed by the existing closed schemas; this document does not add fields to them.

Selected authoring produces development packages and manual validation requests. Variant lineage binds exact parent bytes and maps every parent requirement as retained, modified or removed with its reason. A changed parent digest identifies changed input, not automatically a defective variant. Missing parent history must remain an explicit gap.

Operational installation, binding and upstream core modification remain separate effects. Existing adaptive source stays free of concrete project UUIDs, installation roots and copied bindings. Its operational consistency check does not become protected authority. Ordinary skills are not retroactively required to carry adaptive metadata. The [current builder](../../../src/agents/skills/skill-builder/SKILL.md) and [validator](../../../src/agents/skills/skill-validator/SKILL.md) retain their separate authoring and assessment ownership.

### Core responsibility and first-version packaging

Enhancing reusable dev behavior, authoring a justified project variant, and combining both through separately selected changes are valid design directions. A core's architectural responsibility does not automatically change its present package contract. DEV-025 preserves standalone dev; imposing `binding_required` on it is not an activation repair. Improvements need the applicable specification revision, authoring and independent assessment rather than inheritance of a prior PASS from different bytes.

The [phase 1 brainstorm contract](workflows/phase-1-brainstorm-spec.md) specifies a reusable discovery responsibility with ordinary standalone packaging for its first version. It does not emit an adaptive descriptor with unsupported fields or values. Current binding-required packages continue to require their existing checks. An adaptive wrapper, project specialization or setup bootstrap is separate work under the applicable versioned contract; this decision does not globally close AMB-12 or implement project setup.

## Proposed framework extensions

The framework may expose these responsibilities through direct skill invocation or bounded delegation according to task need and host capability. Native agent configuration, automatic routing and expert scheduling require separate host contracts; they are not established by a role descriptor.

Expert maintenance should use the evidence-based review in [expert health and realignment](expert-health-and-realignment.md). Current update review is primarily defined for variants and selected parent/project changes. Extending it to expertise needs a versioned evidence-baseline contract. Existing selected-set graphs are acyclic; a development feedback loop must not be smuggled into them as a dependency cycle.

## Observable scenarios

**Shared fictional example:** OrderDesk permits cancellation before dispatch and denies it after dispatch; racing cancellation and dispatch must not yield contradictory states. These are walkthrough inputs, not actual project requirements. Business analysis confirms the boundary; architecture owns the race contract; development implements against that evidence; QA checks counterexamples. These are collaborating responsibilities, not four mandatory agents. Each receives the same identified rule revision and relevant artifacts rather than reconstructing the rule from conversation memory.

Success means the proposal retains adequate existing coverage, identifies any justified specialization and makes the cancellation contract available to its consumers. A storage expert does not silently decide customer eligibility; an authorization expert does not invent dispatch state semantics. Conflicting dispatch definitions produce a precise unresolved question for affected work while independent work continues.

A variant that omits the parent core's required failure handling without a supported disposition fails lineage review. A consumer receiving an old cancellation contract must identify the mismatch rather than report integration success. A new expert whose only distinction is its title has no demonstrated need. Qualification requires actual applicable behavior and handoff evidence under the [validator adaptive contract](../../plan/skill-validator-adaptive-enhancement-spec.md), not a complete-looking proposal.

## Unresolved decisions and bounded next expansion

Before implementation, decide: which initial lifecycle responsibilities are selected; who owns authoritative domain statements when sources conflict; when specialization warrants a package rather than a reference; how expertise baselines differ from variant lineage; and whether an uninstalled advisory mode is needed alongside current adaptive binding requirements.

The next expansion should specify one selected core, one justified specialization or expert, and one real artifact exchange using synthetic inputs. Define its contracts and success/failure cases before deciding further package count. Record the resulting decisions in [roadmap and decisions](roadmap-and-decisions.md). Broader catalogs, automatic spawning and operational setup remain follow-up proposals, not implied deliverables.
