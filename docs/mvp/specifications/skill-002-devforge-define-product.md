# SKILL-002: devforge-define-product

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: no callable implementation is supplied by this design package.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Turn selected ideas and evidence into a bounded MVP or later release scope with measurable outcomes, requirements, and explicit non-goals. |
| Direct request | Use DevForgeAI to define the MVP from these ideas. |
| Indirect request | What is the smallest version worth shipping, and how would we know it helped? |
| Expected result | product-brief plus a standardized handoff. |
| Required context | Selected idea IDs, known users and constraints, evidence the user already has, and existing product requirements for an established project. |
| Plugin capability | Skill plus available read-only research tools. No new backend or API account is a prerequisite; unavailable evidence must remain visible. |
| State/action boundary | Research and local planning within the user's scope. Do not contact customers, spend money, or turn illustrative technology choices into approved architecture. |
| MVP support decision | Required when defining or changing a release scope; includes proportionate discovery and feasibility research. |
| Does not activate for | A request only to restyle an accepted screen belongs to design; approved implementation details belong to architect or develop. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| idea-ledger | Required for a new product | Selected idea IDs and relevant adoption records. |
| product-brief | Required for an existing product | Current accepted goals, requirements, outcomes, and non-goals. |
| Evidence and constraints | As available | Source URLs or supplied files, dates, limitations, budget or operating constraints if supplied. |
| change-request | Conditional | The scoped amendment being considered; preserve its acceptance state. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Select | Identify the product problem and delivery slice, using existing accepted scope where available. | Scope origin and current decision state are known. |
| 2. Investigate | Examine supplied evidence and research only consequential unknowns. Record source dates and distinguish inference. | Important claims have evidence or are labeled assumptions. |
| 3. Define | Write goals, users, success measures, functional requirements, nonfunctional requirements, and non-goals. | Each requirement has a stable ID and observable outcome. |
| 4. Review scope | Expose tradeoffs and unresolved decisions; record adoption already supplied by the user. | Dependent design and planning can identify the exact adopted requirements. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| product-brief | PROD | Requirements and measurable acceptance intent traced to ideas or cited constraints. | [product-brief.md](../templates/devforge-define-product/product-brief.md) |


Consumer coverage: product-brief -> design; prototype; architect; plan; review; change.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Ask for an MVP from two selected ideas. | Produces a bounded scope with explicit non-goals. |
| Indirect activation | Ask what to ship first. | Prioritizes outcomes and records the assumptions driving the choice. |
| Missing evidence | Ask for a market-size claim without sources. | Researches if available or marks the claim unverified; no invented statistics. |
| Traceability | Include one requirement unsupported by any idea or constraint. | Marks its origin as a proposal and requests the relevant decision. |
| Out of scope | Ask to deploy an already accepted build. | Routes to release rather than generating another product brief. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

## Rework, stopping, and recovery

Rework: Revise a draft when discovery changes understanding. Route changes to adopted product behavior through change, then issue a new brief revision.

Stop the affected continuation when: Missing target users or conflicting scope decisions block acceptance of dependent requirements, not unrelated evidence gathering.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-define-product to satisfy SKILL-002.
Context: Read this specification, its named templates, and only the relevant
sections of the shared artifact and execution contracts.
Output: A focused skill in the assigned provider source, its needed runtime
resources, reproducible eval cases/fixtures, and separate A/B/C observations.
Record the real installation mode and candidate/baseline identities.
Do not claim implicit activation from a run explicitly supplied SKILL.md.
Boundaries: Preserve user scope and existing approval. Keep DevForge authority
external, respect the assigned worktree, and report unavailable checks truthfully.
```

The native creator may improve wording and packaging without changing this specification's accepted meaning. Move lengthy conditional procedures into references, keep the trigger description precise, and use scripts only for real deterministic operations. During plugin authoring, copy needed templates into the package and use package-relative references; installed skills must not depend on this repository's docs path being present.

## Completion handoff

You are here: Define a useful delivery scope. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
