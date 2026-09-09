# SKILL-011: devforge-release

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: no callable implementation is supplied by this design package.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Turn a reviewed candidate into a reviewable PR or release package, carrying its provenance into any authorized publication and accurately recording what occurred. |
| Direct request | Use DevForgeAI to prepare the PR and release record for this candidate. |
| Indirect request | Package this accepted change for delivery, including recovery and verification. |
| Expected result | release-record plus a standardized handoff. |
| Required context | Exact reviewed candidate, its evidence, target branch/environment, release requirements, and the user's existing authority for any external action. |
| Plugin capability | Skill and local Git/file tools; optional authorized GitHub tooling. External DevForge verification remains separate. No new publishing service or autonomous deployment agent is required. |
| State/action boundary | PR drafting, PR creation, merge, deployment, and release acceptance are separate actions. Execute external actions only within existing authorization; ask only when the required authority is missing. |
| MVP support decision | MVP guarantees preparation and local verification when its inputs are available. Authorized PR creation is conditional on existing Git tooling/authentication; automatic production deployment is deferred. |
| Does not activate for | A failed readiness review returns to its owning workflow. Creating a release record does not establish that deployment happened. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| review-report | Required | Candidate identity, readiness recommendation, and remaining limitations. |
| development-record, story, and epic | Required as relevant | Change scope, verification evidence, and delivered outcomes. |
| architecture-contract | Required as relevant | Migration, recovery, monitoring, and release requirements. |
| Git/CI/environment observations and action authorization | Conditional | Actual targets, current checks, credentials available to the human-operated workflow, and permitted actions. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Recheck | Confirm the candidate still matches the reviewed evidence and that target information is current. | No stale review is promoted to a different candidate. |
| 2. Prepare | Draft PR title/body, release notes, applicable migration/recovery steps, and verification criteria. | A concrete local delivery package exists before any missing publication approval is requested. |
| 3. Execute authorized actions | Use available approved tooling for the explicitly authorized action; otherwise leave the package as a draft. | Each external action has an observed outcome or a clear not-run reason. |
| 4. Record | Read back created references and distinguish local acceptance, PR state, merge, deployment, and verification. | The record states exactly what happened and what remains. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| release-record | REL | Draft PR material, exact candidate mapping, planned actions, actual PR/release references, and recovery/verification evidence. | [release-record.md](../templates/devforge-release/release-record.md) |


Consumer coverage: release-record -> change; review.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Ask to prepare a PR. | Produces a draft tied to the reviewed candidate. |
| Indirect activation | Ask to package accepted work for delivery. | Includes applicable recovery and validation steps. |
| No publication authority | Only drafting was requested. | Completes a reviewable draft and does not post or merge it. |
| Missing CI observation | Hosted CI is unavailable. | Records NOT_RUN or COULD_NOT_RUN, not hosted GREEN. |
| Out of scope | Ask to fix a failing requirement. | Routes to develop or change. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

## Rework, stopping, and recovery

Rework: Candidate changes return to develop/review with new evidence. Release-plan corrections can be revised locally; operational failure becomes a change request or the project's existing incident process.

Stop the affected continuation when: Identity mismatch or unmet required readiness prevents promotion. Missing external access blocks only the dependent action, not preparation of reviewable materials.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-release to satisfy SKILL-011.
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

You are here: Prepare and record delivery. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
