# SKILL-003: devforge-design

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: no callable implementation is supplied by this design package.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Make the selected requirements reviewable as user journeys, screen states, and local mockups before committing to implementation behavior. |
| Direct request | Use DevForgeAI to design mockups for this MVP. |
| Indirect request | Show how a customer would complete signup, including errors and empty states. |
| Expected result | design-spec plus a standardized handoff. |
| Required context | Relevant accepted requirements, existing UI conventions, target device constraints, and prior user feedback. |
| Plugin capability | Skill and local files. Existing browser tools may help; generated imagery and MCP UI are optional, not MVP requirements. |
| State/action boundary | Use a declared local design directory. A mockup demonstrates intended experience; it does not establish backend functionality, accessibility conformance, or production readiness. |
| MVP support decision | Conditional for UI or interaction changes. Pure backend stories can record why design is not applicable. |
| Does not activate for | A technical uncertainty that needs execution belongs to prototype; a production patch belongs to develop. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| product-brief | Required | The requirement IDs and user goals being designed. |
| architecture-contract | Optional | Existing UI stack and design constraints; do not invent a replacement. |
| design-spec | Optional | Current flows and accepted interaction decisions. |
| prototype-report or change-request | Conditional | Observed feedback or the requested revision. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Frame | Choose the user task, affected requirements, and existing design constraints. | Design scope and missing decisions are explicit. |
| 2. Model | Describe journeys, states, validation, loading, empty, error, and keyboard behavior where relevant. | The flow covers the meaningful success and failure paths. |
| 3. Render | Create browser-viewable mockups with local HTML/CSS or the approved existing UI tooling; give exact preview instructions. | Actual mockup files exist and can be inspected, or an execution limitation is recorded. |
| 4. Iterate | Incorporate user feedback as traceable revisions and identify unresolved questions for a prototype. | The accepted design revision and its remaining uncertainties are identifiable. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| design-spec | UX | Flows and screen-state decisions, linked mockup assets, requirement coverage, and feedback disposition. | [design-spec.md](../templates/devforge-design/design-spec.md) |


Consumer coverage: design-spec -> prototype; architect; plan; review; change.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Ask for mockups of an accepted workflow. | Creates assets and a design record linked to requirement IDs. |
| Indirect activation | Ask what happens when a signup form fails. | Includes a concrete error state and recovery path. |
| Missing tooling | Browser preview is unavailable. | Supplies files and truthful manual preview steps; does not claim visual inspection. |
| Scope preservation | An established project has an approved UI stack. | Uses its conventions or records an explicit proposal. |
| Out of scope | Ask for a database index with no UI impact. | Does not manufacture a UI design task. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

## Rework, stopping, and recovery

Rework: Revise mockups for feedback. Product-scope conflicts return to define-product via change; uncertain behavior becomes a bounded prototype.

Stop the affected continuation when: Missing requirements that materially change a flow prevent declaring that flow ready. Unavailable visual tooling does not become a successful visual check.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-design to satisfy SKILL-003.
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

You are here: Design and iterate the user experience. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
