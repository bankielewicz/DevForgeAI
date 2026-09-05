# SKILL-006: devforge-plan

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: no callable implementation is supplied by this design package.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Break adopted scope into dependency-ordered epics and bounded stories with traceable acceptance criteria and the expertise each story needs. |
| Direct request | Use DevForgeAI to turn this product brief into epics and stories. |
| Indirect request | What should we implement first, and what does done mean for each change? |
| Expected result | epic; story plus a standardized handoff. |
| Required context | Adopted requirements and architecture, relevant accepted design, experiment dispositions, and existing backlog items. |
| Plugin capability | Skill and local templates; deterministic graph and provenance checks belong to DevForge. The MVP does not require a sprint scheduler or issue tracker integration. |
| State/action boundary | Planning may propose missing behavior but cannot silently add requirements, broaden permissions, or rewrite the stack. Sprint grouping is optional. |
| MVP support decision | Required for a delivery slice; revises affected stories without regenerating an entire backlog. |
| Does not activate for | A request to execute a ready story belongs to develop; clarification of product value belongs to define-product. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| product-brief | Required | Selected requirement IDs and delivery non-goals. |
| architecture-contract | Required for production stories | Applicable rule IDs, test policy, source roots, and capability requirements. |
| design-spec or prototype-report | Conditional | Relevant flows, states, observations, and hardening disposition. |
| Existing epics/stories and change-request | Conditional | Dependencies, completed work, and the accepted amendment. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Select | Identify the delivery outcome and exact accepted source revisions. | Scope and non-goals are traceable. |
| 2. Partition | Create outcome-oriented epics and small, independently checkable stories. | Each story has a useful outcome and explicit dependencies. |
| 3. Specify | Write behavioral acceptance criteria, negative cases, write scope, test policy, and expertise needs; include only relevant context excerpts. | A developer can identify what to change, how to verify it, and what not to infer. |
| 4. Check readiness | Check coverage, cycles, unresolved decisions, source freshness, and capability gaps. | Separate ready stories from blocked stories without pretending a missing expert exists. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| epic | EPIC | Outcome, requirement coverage, ordered story membership, and explicit deferred scope. | [epic.md](../templates/devforge-plan/epic.md) |
| story | STORY | Observable acceptance cases, relevant rule references, bounded scope, dependencies, and required expert capabilities. | [story.md](../templates/devforge-plan/story.md) |


Consumer coverage: epic -> plan; review; release; change; story -> project-expert-creator; evaluate-expert; develop; review; release; change.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Ask for epics and stories from adopted scope. | Produces linked epic and story documents. |
| Indirect activation | Ask what to implement next. | Uses dependencies and readiness rather than inventing a sprint requirement. |
| Missing behavior | A requirement leaves authorization behavior undefined. | Marks the dependent acceptance criterion unresolved and routes clarification. |
| Traceability | Provide one unsupported acceptance criterion. | Identifies it as a new proposal, not an inherited requirement. |
| Out of scope | Ask to brainstorm alternatives without selected scope. | Routes to brainstorm or define-product. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

## Rework, stopping, and recovery

Rework: Story defects return here. Product or architecture contradictions route through change to their owner. Revisions preserve prior acceptance criteria and invalidate affected downstream evidence.

Stop the affected continuation when: A story cannot be implementation-ready with unresolved acceptance behavior, stale governing inputs, dependency cycles, or required missing expertise.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-plan to satisfy SKILL-006.
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

You are here: Derive epics and implementable stories. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
