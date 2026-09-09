# SKILL-012: devforge-change

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: no callable implementation is supplied by this design package.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Turn feedback, defects, dependency updates, or changed decisions into a bounded change proposal with the affected artifact revisions and the correct return path. |
| Direct request | Use DevForgeAI to assess this change and identify what must be updated. |
| Indirect request | A new library version or customer request changes our assumptions; what does that invalidate? |
| Expected result | change-request plus a standardized handoff. |
| Required context | A concrete change trigger, current relevant artifacts, dependency/provenance links, and existing decision authority. |
| Plugin capability | Skill and read-only provenance inspection; DevForge owns mechanical freshness checks and state transitions. The MVP uses manual invocation, not scheduled self-updating experts. |
| State/action boundary | Discovery of a newer version does not approve an upgrade. Impact assessment cannot silently rewrite accepted artifacts, erase evidence, or mark refreshed expertise evaluated. |
| MVP support decision | Required for changes affecting adopted intent or governing context; small implementation fixes inside unchanged criteria return directly to develop. |
| Does not activate for | Routine work already covered by an accepted story does not need a new change process. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| Change trigger or feedback | Required | Observed defect, user request, release feedback, or verified external update. |
| Affected current artifacts | Required | Exact relevant idea/product/design/architecture/story/expert/candidate identities. |
| release-record, review-report, or expert-evaluation-report | Conditional | The evidence motivating the change. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Capture | Identify the trigger, evidence, current behavior, and requested outcome. | The request is attributable and distinguishes a defect from new scope. |
| 2. Trace impact | Walk declared upstream/downstream references and check affected semantics; include installed skill copies and active runs. | Direct and transitive dependents are listed with uncertain coverage disclosed. |
| 3. Decide | Separate an in-scope repair from a governing amendment; record existing authorization or the missing decision. | The proposal has a clear disposition without inventing approval. |
| 4. Route and verify | Hand accepted changes to the owning skill, then track refreshed artifacts, reevaluation, and supersession. | Affected work remains stale or blocked until the required new evidence exists. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| change-request | CHG | Before/after intent, rationale, impact graph, acceptance state, refresh/retest plan, and owning next workflow. | [change-request.md](../templates/devforge-change/change-request.md) |


Consumer coverage: change-request -> brainstorm; define-product; design; prototype; architect; plan; project-expert-creator; develop; review.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Request impact analysis for an architecture amendment. | Identifies governing records and dependent stories, experts, and runs. |
| Indirect activation | Mention a new package release. | Verifies relevant facts and proposes an upgrade without silently applying it. |
| Unchanged semantics | Fix a typo outside governed behavior. | Keeps the response proportionate and avoids forcing unrelated reevaluation. |
| Transitive drift | An API revision affects an expert used by a story. | Marks the chain for review and records installed-copy refresh and reevaluation. |
| Out of scope | Ask to implement an unchanged ready story. | Routes to develop without reopening adopted decisions. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

## Rework, stopping, and recovery

Rework: Declined changes are retained with rationale. Accepted changes create new revisions through the owning skills; unaffected work can continue under its existing valid context.

Stop the affected continuation when: Unknown impact or missing authority blocks applying the affected amendment, not documenting the proposal. A missing provenance edge must be reported as incomplete analysis.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-change to satisfy SKILL-012.
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

You are here: Assess changes and refresh their dependents. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
