---
id: DFF-00
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# DevForgeAI Adaptive Spec-Driven Engineering Framework

Start with [foundation](foundation.md), then [core workflows](core-workflows.md) and [project context/policy](project-context-and-policy.md). This set defines one connected framework of guidance, project experts and executable guardrails. It is the persisted baseline from the 2026-09-15 planning session, not a complete runtime specification or acceptance record.

The base must be feasible within supported Codex and an individual ChatGPT Pro subscription. [Operating constraints](foundation.md#codex-and-chatgpt-pro-operating-boundary) exclude hidden paid-API, Enterprise, undocumented-host or unlimited-agent assumptions. [Ambiguities](roadmap-and-decisions.md#ambiguity-register) identify unresolved capabilities and exactly what is blocked. The framework capability baselines remain not ready. One bounded [nonproduction worker feasibility contract](runtime/codex-worker-feasibility-v1.md) is specified for offline harness implementation; its native profile and production integration remain unqualified.

## Capability map and dependencies

Dependencies below are specification/implementation prerequisites, not permission to execute another workflow or a runtime waterfall. Feedback references may connect consumers back to owners without making an authoring dependency cycle.

| ID / document | Contract owner | Main prerequisites | Current state |
| --- | --- | --- | --- |
| [DFF-01 Foundation](foundation.md) | Purpose, terminology, components, Codex/Pro boundary | User decisions | Discussed; planning baseline |
| [DFF-02 Core workflows](core-workflows.md) | Lifecycle responsibilities and artifact handoffs | DFF-01, project policy | Discussed; planning baseline |
| [DFF-03 Work items](work-items-and-dependencies.md) | Selected scope, epics/stories, decomposition and dependencies | DFF-01/02/04 | Discussed; planning baseline |
| [DFF-04 Project context/policy](project-context-and-policy.md) | Facts, standards, sources and permitted effects | DFF-01 | Discussed; planning baseline |
| [DFF-05 Skills and expertise](skills-and-project-expertise.md) | Core/variant/expertise composition and lineage | DFF-02/04 | Discussed; existing contracts to reconcile |
| [DFF-06 Subagents/context](subagents-and-context.md) | Optional roles, editable attributes and handoffs | DFF-03/04/05; host capability | Discussed; native profile trials absent |
| [DFF-07 Rust guardrails](guardrails-and-rust-runtime.md) | Protected validation, state and receipts | DFF-03/04/08; host boundary | Design only; concrete workflow/protection gaps |
| [DFF-08 Quality/delivery](quality-and-delivery.md) | Evidence, independent QA, repair and release separation | DFF-03/04 | Discussed; policy migration required |
| [DFF-09 Expert health](expert-health-and-realignment.md) | Drift evidence and bounded realignment | DFF-04/05/08 | Proposed extension; baseline schema unresolved |
| [DFF-10 Knowledge/continuity](knowledge-and-continuity.md) | Retrieval, decisions, checkpoints and resume | DFF-03/04; optional index | Discussed; continuity schema unresolved |
| [DFF-11 Installation/integrations](installation-and-integrations.md) | Owned distribution/activation and host adapters | DFF-04/05/06/07/08 | Design only; no installer delivered |
| [DFF-12 Roadmap/decisions](roadmap-and-decisions.md) | Iterations, ambiguities, migrations and next work | This capability map | Active planning record |

## How to continue in a new session

The first bounded contract has now been finalized: [DFF-WORKER-FEAS-01 v1.0.0](runtime/codex-worker-feasibility-v1.md). Use its [scoped coding handoff](../../plan/framework-worker-coding-handoff.md) for a separately selected implementation request. [Verification](../../plan/framework-worker-contract/20260915T151300Z/verification.md) records current discovery and document identities. The original planning handoff and reasoning remain retained.

The approved next increment is the framework execution MVP candidate. Read [MVP scope](mvp/scope.md), [acceptance scenarios](mvp/acceptance.md), [runtime architecture](runtime/architecture.md) and [evaluation protocol](evaluation/benchmark-protocol.md), then follow the [next-session handoff](../../plan/framework-mvp-next-session.md). These documents select a bounded direction; they do not make the runtime implementation-ready. The capability map above remains the owner of shared definitions. The continued discussion is retained in [enhancement notes, sections 9–12](../../plan/devforgeai-adaptive-framework-enhancement-notes.md#9-continued-discussion-dedicated-terminal-versus-a-rust-engine).

1. Read this index, foundation and the roadmap's next-session task.
2. Select the bounded iteration and read its owned documents plus governing dependency contracts. A reference supplies context; it does not select its implementation.
3. Inspect current bytes, tools and policy before expanding a capability. Preserve confirmed decisions and label any proposed change explicitly.
4. Resolve or record the exact affected ambiguity. Do not guess an interface, support level, subscription feature or approval mechanism.
5. Update owned documents, the decision register and next task after authorized work. Preserve the prior reasoning in [enhancement notes](../../plan/devforgeai-adaptive-framework-enhancement-notes.md).

## Status vocabulary

- **Discussed / planning baseline:** an identified direction with concrete boundaries and open questions; not a runnable promise.
- **Specified:** the selected capability has complete inputs, outputs, failure behavior, dependencies and testable acceptance cases.
- **Implemented:** identified source/build supplies the behavior; evidence must name the candidate and checks.
- **Qualified:** selected native scenarios, integrity conditions and policy thresholds were actually demonstrated for the identified scope.

These are documentation status descriptions. Protected acceptance requires its actual authority. Package existence, Python output, a complete-looking document or a checked story box cannot promote runtime status.

## Existing evidence and companion contracts

Current development packages include [dev](../../../src/agents/skills/dev/SKILL.md), [qa](../../../src/agents/skills/qa/SKILL.md), [skill-builder](../../../src/agents/skills/skill-builder/SKILL.md) and [skill-validator](../../../src/agents/skills/skill-validator/SKILL.md). Their existence and retained evaluation evidence do not qualify this complete framework.

Reuse the [adaptive builder](../../plan/skill-builder-adaptive-enhancement-spec.md), [adaptive validator](../../plan/skill-validator-adaptive-enhancement-spec.md), [Rust authority design](../../plan/devforgeai-codex-rust-enforcement-design.md), [index service](../../plan/devforgeai-index-service-mvp-spec.md) and [query contract](../../plan/devforgeai-index-query-cli-spec.md) with explicit compatibility review. Historical Claude workflows may inform responsibility discovery but their phase counts, shell gates and claimed enforcement are not inherited implementation authority.

The [configuration structural reference](references/codex-config-schema-20260915.json) accompanies DFF-06. It is upstream schema evidence with limitations, not an installed profile. The [original foundation verification](../../plan/framework-foundation/20260915T111940Z/verification.md) is historical evidence for the earlier document bytes. [Current MVP planning verification](../../plan/framework-mvp-planning/20260915T145455Z/verification.md) records this continuation's document identities, links, preservation and review. Neither record reports product TDD or framework acceptance.
