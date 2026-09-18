---
id: DFF-03
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# Work items and dependencies

## Purpose and ownership

This document owns proposed epic/story decomposition, shared-contract ownership, and dependency accounting. It does not convert document names or model-authored checkboxes into authoritative completion. See the [index](index.md), [foundation](foundation.md), and [core workflows](core-workflows.md) for the wider framework.

An epic describes a coherent capability and its shared contract. A story describes a bounded, independently assessable outcome within that capability. An implementation task is a local step within a story. A test case verifies behavior; it is not automatically a story. These distinctions prevent a specification from becoming hundreds of files merely because it has many requirements, functions, platforms, or test phases.

## Inputs, outputs, and dependencies

Inputs are selected requirements and acceptance criteria, existing behavior, canonical shared contracts, [project policy](project-context-and-policy.md), authorized scope, and known integration constraints. The output is a proposed work set with requirement ownership, acceptance mappings, dependency reasons, and unresolved decisions. Selection of that proposal for implementation is separate from authoring it.

Each proposed story records its observable outcome, in-scope and out-of-scope behavior, governing references, prerequisites, verification obligations, and expected deliverables. Each dependency states what the consumer actually needs: a contract decision, delivered interface, qualified artifact, or evidence. Reading another specification does not select its entire implementation.

Every normative clause has one canonical owner. Stories reference shared clauses rather than copy and edit competing versions. A requirement spanning stories is mapped at a sufficiently specific clause level to avoid marking the entire requirement complete after one partial implementation. Shared acceptance scenarios remain visible at epic level.

## Confirmed decisions and proposed decomposition

The decomposition method is **quasi-deterministic**: stable inputs and rules constrain the result, while semantic boundaries still require review. It does not promise identical story counts from every model.

1. Inventory explicit outcomes, requirements, acceptance scenarios, and existing shared contracts using their stable source identities. Record missing decisions before creating dependent stories.
2. Seed groups from independently observable outcomes. Coalesce criteria that exercise the same state transition or must change together to preserve an interface or invariant. Do not seed a group for each source paragraph.
3. Assign each clause one owner and attach references to cross-cutting constraints. Record concrete producer/consumer dependencies; detect cycles and missing prerequisites.
4. Propose a split only when both resulting groups have independently assessable outcomes and the split gives a real dependency, delivery, or bounded-verification advantage. A temporary implementation stub is not independent completion.
5. Propose a merge when groups cannot be assessed separately without the same unfinished behavior, or when their separation merely duplicates contracts and setup. Preserve a genuinely reusable prerequisite rather than merging it into every consumer.
6. Record the specific split/merge reason, acceptance coverage, and remaining integration obligations. An adversarial review challenges the grouping before the selected work set is treated as ready.

There is no universal story-count cap or minimum. Do not split solely by CLI flag, source file, platform, TDD phase, agent role, requirement row, or document length. A platform may justify a separate story when it introduces an independently deliverable capability with its own behavior; a second execution of the same acceptance case does not.

Future Rust checks can reject duplicate identities, missing required fields, unresolved references, dependency cycles, or incomplete mappings once their schemas and policies exist. Rust cannot infer from graph structure alone that an outcome is useful or that a split is sensible. Semantic review must cite the concrete coupling or independence; neither a model score nor structural success establishes readiness by itself. No time or token reduction is claimed without comparative execution evidence.

## Concrete examples and failure scenarios

The [query specification](../../plan/devforgeai-index-query-cli-spec.md) suggests a six-group illustration: query foundation/coverage; structural navigation/inspection; lexical discovery/ranking; candidate calls; freshness/lifecycle resilience; integrated terminal delivery. The [Rust authority design](../../plan/devforgeai-codex-rust-enforcement-design.md) admits an eight-group illustration: control/evidence contracts; protected Windows host for the earlier bounded proposal; durable run state; workflow transitions; immutable candidates; restricted evaluation; evidence validation/receipts; client/hooks. Native protection and recovery remain integrated qualification obligations. These are discussion examples, not required counts, selected story files, or approved implementation order. Actual source and dependency inspection can justify merging or splitting them.

For fictional OrderDesk, “permit cancellation before dispatch; deny it afterward” is one candidate outcome. Separate Red, Green, Windows, Linux, handler, and database story files would add administration without establishing separate outcomes. A genuinely independent notification contract could justify another story, but only after its requirement and dependency are selected. The cancellation/dispatch race remains a shared acceptance obligation, not an omitted edge case.

A successful work set maps all selected clauses, explains each dependency, preserves canonical policy, and retains epic-wide verification. A failed decomposition copies contradictory cancellation rules into different stories, creates a circular prerequisite, hides an unexecuted platform under a completed story, or claims the epic complete from a subset. These are review findings even if all files parse correctly.

## Reusable assets and compatibility

The current [dev skill](../../../src/agents/skills/dev/SKILL.md) already calls for dependency-ordered behavioral slices; [qa](../../../src/agents/skills/qa/SKILL.md) accepts selected stories and sprint scopes. Existing specifications remain governing inputs until explicitly revised. A canonical specification plus referenced story files is valid; physical fragmentation is not required.

[Skills and project expertise](skills-and-project-expertise.md) supplies optional reasoning support. Specialist profiles do not dictate work-item boundaries. [Quality and delivery](quality-and-delivery.md) owns evidence and outcome distinctions, while [Rust guardrails](guardrails-and-rust-runtime.md) owns eventual protected transitions. Historical planning documents are preserved rather than rewritten as accepted story baselines.

## Open questions and next bounded expansion

- **DFF-03-Q1:** What minimal persisted work-item schema expresses clause ownership, dependency kinds, selection, and proposed versus approved revisions?
- **DFF-03-Q2:** Which measurable workload limits justify further splitting, and how are limits selected without using an arbitrary global story quota?
- **DFF-03-Q3:** Who resolves disputed semantic grouping, and what evidence makes a changed grouping ready without silently changing scope?

Next, apply these rules manually to one selected specification and the small OrderDesk example, retaining the initial grouping and every justified adjustment. Record unresolved schema and review decisions in [roadmap and decisions](roadmap-and-decisions.md) before building a decomposition validator or generating implementation story files.
