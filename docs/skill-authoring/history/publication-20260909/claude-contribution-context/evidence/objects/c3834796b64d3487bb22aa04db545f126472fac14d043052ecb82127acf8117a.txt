# SKILL-009: devforge-develop

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: a draft instruction file exists in the POC; this expanded contract and its terminal behavior are not yet validated.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Produce a bounded candidate satisfying a ready story while preserving its approved architecture and obtaining the applicable test-first evidence. |
| Direct request | Use DevForgeAI to implement STORY-001. |
| Indirect request | Build this approved behavior and show the failing test before the implementation passes. |
| Expected result | development-record plus a standardized handoff. |
| Required context | Ready story, relevant accepted contract, required evaluated expertise, exact baseline, external policy/run paths, and available test adapter. |
| Plugin capability | Skill plus the external DevForge CLI and a supported runtime adapter. Human-operated gate transitions are sufficient for MVP; automatic hooks or a background broker are not prerequisites. |
| State/action boundary | The worker edits only its declared candidate fence. DevForge controls external gate evidence. Test or governing-context changes require the applicable new run; no gate weakening is an implementation fix. |
| MVP support decision | Required for production changes. Non-code work follows the applicable accepted verification policy rather than inventing a failing test. |
| Does not activate for | Unresolved product behavior belongs upstream; disposable feasibility work belongs to prototype. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| story | Required | Acceptance cases, dependencies, scope, and readiness. |
| architecture-contract | Required | Applicable rules and supported test/stack adapters. |
| expert-package and expert-evaluation-report | Required for each declared expert capability | Exact installed revision and relevant successful evaluation scope. |
| Baseline and external run context | Required | Candidate identity, policy identity, state location, write fence, and runner identity. |
| review-report | Conditional | Inside-scope findings to remediate. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Prepare | Verify story readiness, source pins, expert identity, baseline, scope, and runner availability. | The authority owner initializes a valid run before governed edits. |
| 2. Establish RED | Write discriminating tests for new behavior and have the authority runner observe the intended assertion failure. | A valid RED receipt exists; errors or skipped/empty suites do not qualify. |
| 3. Establish GREEN | Implement within scope while preserving the recorded RED tests; run the applicable checks. | GREEN evidence refers to the exact candidate and unchanged required tests. |
| 4. Hand off | Map acceptance cases to tests and preserve the candidate and receipts for review. | The reviewer receives raw evidence and exact identities rather than a success claim. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| development-record | DEV | Candidate manifest, acceptance-to-test mapping, actual gate receipts, change summary, and unresolved limits. | [development-record.md](../templates/devforge-develop/development-record.md) |


Consumer coverage: development-record -> review; release; change.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Request a ready story. | Produces a bounded patch and traceable development record. |
| Indirect activation | Ask to implement approved behavior with TDD. | Obtains observed RED before the GREEN implementation snapshot. |
| Gate bypass | Attempt production-first work or change recorded RED tests. | The supported external gate rejects the transition; the skill reports the failure. |
| Stack drift | Introduce a prohibited dependency. | Reports and remedies the violation within scope; does not edit external policy. |
| Out of scope | Ask to choose a new product direction. | Routes upstream instead of inventing acceptance criteria. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

## Rework, stopping, and recovery

Rework: Fix implementation defects under the same governing scope when evidence remains valid. Test changes, stale inputs, or semantic changes route to a new run or change as appropriate.

Stop the affected continuation when: A failed or unavailable required gate blocks the dependent transition. Partial work and errors remain visible; unsupported adapters cannot be labeled enforced.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-develop to satisfy SKILL-009.
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

You are here: Implement one governed story. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
