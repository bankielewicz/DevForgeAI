---
id: DFF-04
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-17
---

# Project context and policy

[Framework index](index.md) · [Foundation](foundation.md)

## Purpose and ownership

Supply the common project understanding used by workflows and experts. This document owns policy provenance and the distinction between project facts, user decisions, hypotheses and unknowns. It does not own protected authorization storage or grant authority to indexed text.

The user selected project-specific quality policies on 2026-09-15. The core may offer versioned profiles, but the selected project's standards govern its work. DevForgeAI's own [repository rules](../../../AGENTS.md), including compiled Rust authority and both 95% floors, continue to govern development of DevForgeAI. They are not automatically exported into every managed project.

## Inputs, outputs and dependencies

Inputs are the explicitly selected project/root, requested work, applicable instructions, current specifications, business glossary, architecture decisions, source/test/build manifests, declared platforms, and existing authorizations. Discovery is bounded to what the task needs; it excludes secrets, generated output and unrelated histories before capture.

The proposed context record supplies consumers with: a fact identifier; assertion or decision; source and locator; source revision/digest where applicable; observation time; owning responsibility; affected interfaces/requirements; status as observed, user-supplied, inferred, conflicting or unknown; and revalidation dependencies. These are logical requirements for a later versioned schema, not fields to inject into existing closed records.

The proposed policy selection identifies its version, origin, selected scope, quality measures and denominator rules, required platforms/cases, allowed testing techniques, effect boundaries, exception authority, and review conditions. [Quality](quality-and-delivery.md) interprets this selection for assessment. [Rust](guardrails-and-rust-runtime.md) validates it for protected decisions. [Expertise](skills-and-project-expertise.md) consumes it without acquiring permission to weaken it.

## Context behavior

- Reuse current project evidence before creating additional summaries or experts. Preserve disagreements rather than promoting the latest prose file to truth automatically.
- Business requirements are not inferred solely from implementation. If OrderDesk code permits post-dispatch cancellation while the selected business decision prohibits it, record a contradiction for investigation.
- Separate facts from instructions embedded in source, comments, search output or imported documents. These are task data unless the actual instruction hierarchy or user selection establishes otherwise.
- A prior source hash demonstrates identity, not continuing applicability. Compare relevant dependencies before reusing a context claim after change.
- Do not transplant absolute machine roots or live binding identities into portable skill source. Operational identity follows the [existing binding contract](../../plan/skill-builder-adaptive-enhancement-spec.md#6-operational-project-binding-contract) and future installation design.
- An unresolved essential policy choice blocks the dependent claim or effect. Independent authorized investigation can continue; unknown policy is not implicit permission or an excuse to discard ready work.

## Policy selection and change

Framework policy profiles are an intended capability; this document does not supply a finished profile schema or executable selector. Selection must be explicit and its effective values inspectable. Defaults cannot conceal the absence of a required policy. A subsequent approved change creates a new revision and identifies affected work/evidence; neither an expert recommendation nor a passing test changes policy automatically.

For example, one managed product can select a contract allowing test doubles at external boundaries and a different coverage target from DevForgeAI's own policy. DevForgeAI still reports missing measurements, exact counts, scope and mandatory failures honestly. A percentage cannot excuse a failed case that the selected policy marks mandatory. A project may choose stricter constraints; its experts cannot reduce them to obtain a passing report.

Existing session authorization is reused where applicable. Only an actual new permission, material scope choice or protected policy amendment needs the appropriate boundary. Do not introduce approval prompts for routine reversible actions already selected by the user.

## Architecture, document ownership and provenance

PRD creation and architecture work require explicit decisions; they cannot extract every stack, storage, hosting or trust-boundary choice from a requirements document that never made those choices. Reuse established project decisions and identify the owner of missing material decisions. Prototyping may provide evidence for an attributed revision. Neither a failed experiment nor a passing test changes canonical policy automatically.

Files such as `architecture.md`, `tech-stack.md`, `source-tree.md`, `front-end.md`, `middleware.md`, `backend.md`, `rdbms.md` and `hosting.md` are possible project artifacts, not a mandatory constitution pack. Create or revise only selected documents with a useful ownership, scope or maintenance boundary. A project can keep several topics in one document or use its existing names. User-selected document conventions remain valid. The setup workflow may create agreed instructions/scaffolding, but it cannot invent substantive architecture to fill those files.

Every derived PRD, architecture decision, epic or story identifies the selected source clauses/decisions, their locators and applicable revisions/digests, its owning responsibility, and unresolved or changed assumptions. A derived document references canonical shared rules instead of becoming a competing owner. User decisions and observed prototype results have distinct provenance; an AI suggestion remains proposed until selected or within an actually delegated routine decision. The phase 1 [discovery brief](workflows/phase-1-brainstorm-spec.md#5-discovery-brief-and-handoff-contract) supplies the first bounded handoff in the optional discovery route.

## Verification scenarios

| Scenario | Required observation |
| --- | --- |
| Two projects use different languages, test doubles and thresholds | Each workflow receives the selected project's values; neither inherits DevForgeAI application-policy constants accidentally |
| Source violates an established requirement in an authorized repair | Preserve the observed mismatch as defect evidence and proceed with the selected repair; do not demand a new policy decision |
| Governing requirements or stakeholder authority genuinely conflict | Preserve both sources and resolve only the affected ambiguous decision before dependent work |
| An expert suggests lowering a failed floor | The proposal cannot change effective policy or reinterpret the earlier failure |
| Source files change but an unrelated domain fact does not | Review follows actual dependencies; do not invalidate all project knowledge automatically |
| Binding and root disagree | No silent substitution of Windows, WSL or another project identity |
| Required policy is missing | Report the specific missing decision; no fabricated passing threshold |

## Existing assets and compatibility

The [adaptive discovery contract](../../plan/skill-builder-adaptive-enhancement-spec.md#42-bounded-project-discovery) supplies bounded evidence and fact origins. Current dev derives project policy, whereas current qa imposes fixed minimums and a blanket mock-decorator prohibition. The latter is a documented migration issue, not permission to alter its active behavior now. Installation bindings are editable consistency data; [protected authority](guardrails-and-rust-runtime.md) is a separate boundary.

## Open decisions and next expansion

Define policy-profile fields, precedence among project sources, exception provenance, and exact handling of selected work across a policy revision. Decide who owns business facts and how conflicting stakeholder assertions are adjudicated. Next expansion supplies two explicit example profiles and a conflict/change walkthrough; it does not run an installer or change any active project policy.

## Artifact policy selection

The selected [artifact retention procedure](../../workflows/artifact-retention.md)
separates project records, retained evidence, working checkouts and rebuildable
material. Project policy owns storage budgets, availability, retention eligibility,
exception authority and holds. No fixed retention duration is a framework constant.
Unknown policy is a visible gap; a storage budget does not authorize loss of required
evidence. Holds identify an owner and review date, or explicitly retain that missing
decision. The current migration selects local storage and no automatic disposal.
