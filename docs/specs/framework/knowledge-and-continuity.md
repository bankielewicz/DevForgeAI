---
id: DFF-10
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# Knowledge and continuity

[Framework index](index.md) · [Project context](project-context-and-policy.md)

## Purpose and ownership

Keep project understanding and selected work recoverable across sessions, context compaction, specialist handoffs and interruptions. This document owns retrieval and continuity behavior; DFF-04 owns fact/policy meaning, DFF-03 work identity, and DFF-07 authoritative state.

Durable documents can preserve decisions and evidence; they cannot guarantee that a model remembers or understands them. Resumption must recover selected obligations from the actual records and recheck relevant changes. A conversational summary is a navigation aid, not a replacement for exact contracts or protected status.

## Inputs, outputs and dependencies

Inputs include selected specifications, the index and decision log, project fact references, candidate/evidence identities, required work, known failures, prior checkpoints, and current filesystem/tool observations. Outputs are a bounded context package for a selected task and a resumable handoff identifying what remains true, changed, missing and actionable.

The proposed checkpoint records selected scope and authorization references; requirement/story/defect IDs; governing contract versions; last identified candidate; evidence and limitations; open decisions and affected dependencies; owned jobs/processes/fixtures; and the next safe action. Credentials and unnecessary private data are excluded. Exact storage/schema and retention are future decisions, not additions to existing schemas.

## Retrieval and resumption behavior

1. Start at the framework/project index and the selected task. Read its governing contracts and affected dependency interfaces, not every historical document.
2. Distinguish specification, implementation, observation and hypothesis. Retain contradiction/counterexample references alongside favorable evidence.
3. Reuse a context package only while its actual prerequisites remain valid. Changed source may require targeted reinspection; it does not prove every fact false.
4. Resume protected work from Rust-owned state when that boundary applies. A checkpoint marked COMPLETE cannot override unmet predicates.
5. Report interrupted/unexecuted work honestly. An ended session neither completes nor cancels a selected obligation; cancellation comes from its actual controlling instruction or policy.
6. Do not automatically repeat a failed or uncertain-effect command on resume. Inspect its recorded outcome, scope and owned resources before selecting a new attempt.

## Optional code knowledge

The [index service](../../plan/devforgeai-index-service-mvp-spec.md) and [query extension](../../plan/devforgeai-index-query-cli-spec.md) can reduce repeated source discovery where available and qualified. They supply structural/lexical observations, captured bytes, source ranges, generations, freshness and coverage limits. They do not establish semantic equivalence, complete callers, absence of existing functionality, or permission to modify source.

Ordinary terminal inspection remains available when indexing is absent. Adding indexing is not a prerequisite for every skill or every project. Readback against current relevant bytes is necessary before relying on stale captured evidence for a change. Project source and comments returned by retrieval remain data rather than new agent instructions.

## Planning-session continuity

The [index](index.md) and [roadmap](roadmap-and-decisions.md) identify the next bounded expansion and unresolved decisions. The [enhancement notes](../../plan/devforgeai-adaptive-framework-enhancement-notes.md) preserve the original incident and evolving proposals. Update this navigation after each authorized planning iteration, retaining superseded reasoning and its disposition rather than silently rewriting conversation history.

## Verification scenarios

- A new session reconstructs OrderDesk's selected cancellation rule, pending race decision, prior failed case and next task without the original conversation.
- A checkpoint cites an old candidate while source changed: it remains historical evidence; no current qualification is inferred.
- Index search finds no cancellation handler: the consumer reports the indexed scope/limitations and performs appropriate additional inspection, not a claim that the feature is absent.
- A context package omits an unresolved QA failure: the selected-work/evidence accounting detects the missing obligation.
- An expired generation or inaccessible prior artifact yields a named gap; the workflow does not fabricate its content or silently redirect to another project.

## Existing assets, open decisions and next expansion

The continued discussion proposes a user `.devforgeai` data root and CLI-mediated history/context retrieval. [Runtime architecture](runtime/architecture.md#persistence-and-project-knowledge) records the logical history/knowledge/workflow distinction and why physical database partitioning remains a decision. A database per role or a fixed two-database layout is not selected. The [MVP handoff](../../plan/framework-mvp-next-session.md) narrows the next contract task without claiming that persistence or a new home directory has been implemented.

Current [dev](../../../src/agents/skills/dev/SKILL.md) and [qa](../../../src/agents/skills/qa/SKILL.md) include evidence/resume responsibilities. The broader context packaging and index navigation described here are not a shipped continuity service. Define checkpoint schema/versioning, index-update ownership, retention, stale-reference behavior and context selection limits. The next expansion exercises a cold resume of the fictional change with one missing artifact and one changed dependency, recording exactly which facts and work remain usable.

## Selected artifact lifecycle policy (2026-09-18)

The [artifact retention procedure](../../workflows/artifact-retention.md) now defines
purpose classes, identity-versus-locator separation, local/shared availability,
retention eligibility and holds for the selected migration. It refines the earlier
open retention decision without implementing a continuity service or extending any
closed schema. Relocation records preserve original locators and sealed report
bytes. Resolve their current locations through the
[retrieval catalog](../../plan/artifact-relocation/retrieval-catalog.md); unchanged
published historical records may use immutable Git links. Inaccessible or expired
artifacts remain explicit retrieval gaps. Execution records from another candidate
never become fresh qualification merely because their location was repaired.
