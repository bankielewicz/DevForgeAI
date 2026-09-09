# SKILL-001: devforge-brainstorm

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: a draft instruction file exists in the POC; this expanded contract and its terminal behavior are not yet validated.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Turn an undeveloped idea or competing ideas into a durable record the user can refine without losing alternatives or inventing commitments. |
| Direct request | Use DevForgeAI to brainstorm my idea for an application. |
| Indirect request | I have three ideas and cannot decide what problem is worth solving. |
| Expected result | idea-ledger plus a standardized handoff. |
| Required context | The user's own statements; an existing idea ledger when one exists. No PRD, architecture, or chosen stack is required. |
| Plugin capability | Instruction-based skill with local Markdown templates. Research is optional when a factual claim requires verification; no MCP server is required. |
| State/action boundary | Local discussion and artifact authoring. Attribute statements to user, AI proposal, or cited evidence; only the user's actual adoption changes a proposal into a decision. |
| MVP support decision | Required for an undeveloped idea; reuse an existing ledger for later discussion. |
| Does not activate for | A bounded implementation request with an accepted story should use develop; a change to an accepted decision should use change. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| User statements | Required | The user's actual words or a faithful attributed summary; retain uncertainty. |
| idea-ledger | Optional | Existing alternatives, decision records, and unresolved questions. |
| change-request | Optional | Accepted direction to revisit a specific idea; proposed requests remain proposals. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Brainstorm-specific clarifications

Preserve a user's explicit early technology decision or preference with its actual scope and attribution; the skill must not choose a stack on the user's behalf. A later architecture phase does not invalidate recording an actual early constraint.

A missing session record permits execution_ref: null with the gap in missing_inputs; it does not establish single-writer ownership. Before artifact writes, verify the task's actual assignment and collision state. Preserve earlier accepted bytes when revising a ledger. Hash completed output artifacts for the handoff; never embed a handoff's own complete-byte hash inside itself.

The migrated pilot has draft develop, review, and expert-creator siblings; define-product and change are absent. A negative brainstorm activation test is independently observable. A suggested missing continuation must be reported as a capability gap rather than a fictional invocation.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Recover | Read the relevant ledger and latest user steering. | Identify the ideas and decisions already recorded. |
| 2. Explore | Clarify people, problem, alternatives, and desired outcome. Continue useful discussion while nonblocking questions remain. | Each candidate idea has a recognizable problem and open questions. |
| 3. Record | Assign idea IDs, preserve attribution, connect split or merged ideas, and separate proposed from adopted decisions. | No AI suggestion is silently recorded as a user decision. |
| 4. Focus | Identify a small discovery step or experiment and the capability it needs. | The user has a reviewable ledger and a concrete continuation. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| idea-ledger | IDEAS | Idea entries, evidence, assumptions, adoption records, and one next experiment or discovery question. | [idea-ledger.md](../templates/devforge-brainstorm/idea-ledger.md) |


Consumer coverage: idea-ledger -> define-product; change.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Ask to brainstorm an app idea. | Produces a ledger with attributed ideas and unresolved questions. |
| Indirect activation | Describe three competing problems without naming the skill. | Explores and records alternatives without prematurely selecting a stack. |
| Missing input | Say only 'I want to build something'. | Asks a useful initial question and does not fabricate a target user. |
| Provenance | Give two ideas, then merge them. | The resulting idea retains links to both origins. |
| Out of scope | Supply a ready story and ask for its implementation. | Routes to develop without forcing a new brainstorming exercise. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

The paired adoption cases, B6 source mismatch, B7 operator-authored ownership fixture, and installed-resource checks are defined in the shared authoring contract. Resolve the script against the installed skill path and outputs against the consuming project. Report placeholder/hash checks as structural observations, with semantic quality judged separately.

## Rework, stopping, and recovery

Rework: Revise the draft ledger as discussion proceeds. Preserve adopted revisions and record later changes as new revisions; unresolved product choices go to define-product.

Stop the affected continuation when: Only decisions needed for the next dependent activity stop that activity. Brainstorming itself can continue with explicitly recorded uncertainty.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-brainstorm to satisfy SKILL-001.
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

You are here: Explore and preserve ideas. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
