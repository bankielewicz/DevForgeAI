---
id: DFF-02
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# Core workflows and artifact flow

## Purpose and ownership

This document connects framework capabilities through their inputs and outputs. It is a planning baseline, not an executable workflow definition or evidence that any transition is enforced. The [index](index.md) records the documentation set; [foundation](foundation.md) owns the framework boundary and [Rust guardrails](guardrails-and-rust-runtime.md) owns proposed enforcement. This document owns the relationship between discovery, specification, implementation, assessment, and delivery.

The framework guides the user's selected work. It does not require every project to begin with business analysis, execute a universal waterfall, or activate every available specialist. A well-specified defect can enter implementation after its dependencies are checked. An uncertain product idea can remain in discovery. A documentation request does not require fabricated code tests. Explicit user interruption ends active execution without establishing completion.

## Inputs, outputs, and dependencies

Inputs are the current request, selected project and work items, applicable [project policy](project-context-and-policy.md), existing specifications and decisions, current candidate identity, and relevant prior evidence. Referenced documents supply context without automatically selecting their deliverables. Missing facts are investigated; missing product decisions remain explicit questions.

The principal artifact flow is:

| Capability | Consumes | Produces and next consumer |
| --- | --- | --- |
| Discovery and business analysis | Problem, stakeholders, current behavior, constraints | Agreed outcomes, uncertainties, and requirements for design or further discovery |
| Architecture and design | Requirements, project context, integration constraints | Selected boundaries, interfaces, decisions, and acceptance implications for work planning |
| Work planning | Selected requirements and shared contracts | Bounded work items, dependencies, and acceptance mappings for implementation or assessment |
| Development | Selected work, current source, applicable policy | Candidate changes and executed verification evidence for independent QA |
| Independent QA | Selected requirements, candidate, preserved evidence | Assessment, demonstrated findings, gaps, and repair packet for development or delivery review |
| Delivery and follow-up | Qualified candidate, required approvals, selected effects | Authorized delivery result or explicit unresolved obligations; observations can initiate new selected work |

These are capabilities, not mandatory phases. A consumer needs the relevant artifact properties, not proof that a specifically named skill authored the artifact. [Work items](work-items-and-dependencies.md) owns decomposition; [quality and delivery](quality-and-delivery.md) owns outcome distinctions. Operational deployment remains a separate authorized effect.

## Confirmed decisions and proposed behavior

Skills supply reusable task guidance. Project expertise supplies grounded domain or technical context. Subagents provide optional execution contexts. None of these identities grants acceptance authority. [Skills and project expertise](skills-and-project-expertise.md) owns their composition. One agent may complete a coherent behavioral slice through the applicable development checks; separate agents are justified by independent review or genuinely separable work, not merely by naming Red, Green, Refactor, and QA.

The proposed framework retains the selected objective and its obligations across handoffs and sessions. A follow-up such as “test Linux coverage” adds or clarifies verification work unless the user changes the objective; it does not silently discard an unresolved repair. The eventual runtime must distinguish a stopped agent turn from a completed work item. This baseline does not define that runtime's state schema or continuation algorithm.

Review can be adversarial without repeatedly rebuilding the same context. A reviewer receives the governing requirements, candidate identity, relevant contracts, and evidence needed to challenge the implementation. The implementer's explanation is contextual evidence, not the review oracle. Agent count, context isolation, and retry policy remain execution choices to specify; no token-saving claim is made without measurement.

## Concrete success and failure scenarios

The shared fictional example is **OrderDesk**, with a requested cancellation-rule change: permit cancellation before dispatch and deny it after dispatch. This example is planning material, not an authorization to build a product.

1. Business analysis establishes what “dispatch” means and how competing cancellation and dispatch requests should behave. An unanswered race-condition question prevents claiming the affected behavior is implementation-ready; unrelated confirmed requirements can still be developed when separately selected.
2. Architecture identifies the existing order state owner and transaction boundary. It does not create a second state store simply because a new expert agent is available. A contract change is recorded before dependent implementation relies on it.
3. Development translates the selected rule into meaningful tests, retains the expected failure, implements the change, and performs applicable regression and QA checks. This repository's mandatory TDD rules remain applicable to its programming work.
4. Independent QA challenges boundary timing, invalid transitions, repeated requests, and the evidence's candidate identity. A confirmed defect returns a bounded repair obligation. The developer's report cannot close the independent finding.
5. A satisfied functional test does not authorize production deployment. A required unavailable platform remains a gap; a user pause leaves the selected work unfinished rather than accepted.

The integrated walkthrough will later bind the exact fixture, contracts, and artifacts. This document does not resolve OrderDesk's storage, API, or delivery design.

## Reusable assets and compatibility

The current [dev skill](../../../src/agents/skills/dev/SKILL.md) already accepts selected multi-document contracts and owns implementation, tests, refactoring, integration, and developer QA. The current [qa skill](../../../src/agents/skills/qa/SKILL.md) owns independent product assessment and repair handoff. Skill-package authoring and validation remain separate capabilities; they are not prerequisites for ordinary application development.

Historical workflow summaries under `src/claude/skills/` provide domain examples, not mandatory phase counts or verified enforcement interfaces. Existing specifications and retained evidence under `docs/plan/` remain unchanged. No operational skill, hook, or configuration is installed or modified by this baseline.

## Open questions and next bounded expansion

- **DFF-02-Q1:** Which minimal artifact properties allow each supported entry point to proceed, and which unresolved properties block only dependent work?
- **DFF-02-Q2:** How will explicit changes of objective be distinguished and recorded from additional verification requests without treating model interpretation as protected authority?
- **DFF-02-Q3:** Which review responsibilities need protected actor separation, and which need only an independent evidence-based assessment?

Next, expand the OrderDesk walkthrough through one selected change and one failed QA retest, naming each artifact producer, consumer, blocking condition, and user decision. Reconcile its dependencies with [roadmap and decisions](roadmap-and-decisions.md) before specifying runtime transitions.
