---
id: DFF-00
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-18
---

# DevForgeAI Adaptive Spec-Driven Engineering Framework

Scannable entry: [README.md](../../../README.md). Start with [foundation](foundation.md), then [core workflows](core-workflows.md) and [project context/policy](project-context-and-policy.md). This set defines one connected framework of guidance, project experts and executable guardrails. It retains the 2026-09-15 baseline with the 2026-09-17 discovery/setup refinements below; it is not a complete runtime specification or acceptance record.

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

### Discovery workflow selection, 2026-09-17

The earlier documentation request specified [phase 1: brainstorm (DFF-WF-01)](workflows/phase-1-brainstorm-spec.md). No numbered phase 0 existed in this collection before that revision. [Setup/activation](installation-and-integrations.md#setup-intake-and-proposed-activation-workflow) remains a separate prerequisite where applicable, not a required product-discovery phase. The user's selected route is **brainstorm -> prd-create -> prd-review**, followed by work planning and stories when those are needed. [Core workflows](core-workflows.md#discovery-route-and-workflow-names) defines the proposed consumers and optional entry points.

The phase 1 documentation delivered a bounded authoring specification, a discovery-brief contract and 20 future assessment scenarios; it did not itself author or install the skill. Existing dev/qa/story-create contracts remain unchanged. [The decision disposition](roadmap-and-decisions.md#discovery-workflow-disposition-2026-09-17) separates that scope from unresolved bootstrap/worktree and runtime work. [Before identities and preserved document snapshots](../../plan/framework-discovery-planning/20260918T014059438Z/inputs-before.json) retain the input state for that revision.

### Phase 2 PRD authoring specification, 2026-09-17

[Phase 2: prd-create (DFF-WF-02)](workflows/phase-2-prd-create-spec.md) specifies how selected discovery or equivalent requirements become a traceable, revisioned PRD for independent review. It defines 20 requirements, 26 future independent assessment cases and a [copyable skill-builder request](workflows/phase-2-prd-create-spec.md#9-copyable-skill-builder-request). That documentation task delivered the specification, not the skill package or its later evaluation.

The retained [brainstorm assessment](../../plan/skill-validations/brainstorm/20260918T021707Z/validation-report.md) and [no-change handoff](../../plan/skill-validations/brainstorm/20260918T021707Z/handoff.json) remain candidate-specific upstream evidence. Phase 2 preserves that producer and accepts equivalent adequate inputs without requiring its execution. Work planning and stories consume sufficiently reviewed scope later. [The phase 2 disposition](roadmap-and-decisions.md#prd-authoring-disposition-2026-09-17) records that delivery's bounded decisions and remaining work.

### Phase 3 PRD review specification, 2026-09-18

[Phase 3: prd-review (DFF-WF-03)](workflows/phase-3-prd-review-spec.md) now defines independent assessment and retest of an identified PRD against original requirements and project policy. It specifies 20 requirements, 32 future mandatory evaluation cases, a review report contract and a [copyable skill-builder request](workflows/phase-3-prd-review-spec.md#9-remaining-scope-and-copyable-skill-builder-request). This is specification delivery; prd-review has not been authored or evaluated by this task.

The upstream [prd-create retest report](../../plan/skill-validations/prd-create/20260918T121331Z/validation-report.md) records 31/31 required Windows/PowerShell cases passing, with its [source-drift finding resolved](../../plan/skill-validations/prd-create/20260918T121331Z/finding-retest.json) for that candidate. These retained results do not qualify prd-review or imply installation/framework acceptance. [The phase 3 disposition](roadmap-and-decisions.md#prd-review-disposition-2026-09-18) records source identity, scoped results, independence and retest boundaries. Next selectable skill authoring is prd-review; sufficient reviewed scope subsequently goes to DFF-03 work planning, whose full skill contract remains separate.

### Separately selected runtime work

The earlier bounded contract is [DFF-WORKER-FEAS-01 v1.0.0](runtime/codex-worker-feasibility-v1.md). Its [scoped coding handoff](../../plan/framework-worker-coding-handoff.md) and [verification](../../plan/framework-worker-contract/20260915T151300Z/verification.md) are retained historical inputs, not instructions to resume that stream merely by opening this index. Inspect the actually selected current candidate and handoff before runtime work. New documentation revisions do not update old sealed manifests or transfer acceptance to new inputs.

The earlier framework execution MVP direction remains in [MVP scope](mvp/scope.md), [acceptance scenarios](mvp/acceptance.md), [runtime architecture](runtime/architecture.md), [evaluation protocol](evaluation/benchmark-protocol.md) and the [next-session handoff](../../plan/framework-mvp-next-session.md). These documents select a bounded direction; they do not make the runtime implementation-ready. The capability map above remains the owner of shared definitions. The continued discussion is retained in [enhancement notes, sections 9–12](../../plan/devforgeai-adaptive-framework-enhancement-notes.md#9-continued-discussion-dedicated-terminal-versus-a-rust-engine).

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
