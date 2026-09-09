# SKILL-010: devforge-review

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: a draft instruction file exists in the POC; this expanded contract and its terminal behavior are not yet validated.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Assess the exact candidate against its story, upstream decisions, test evidence, and relevant quality requirements, returning actionable findings and a scoped readiness recommendation. |
| Direct request | Use DevForgeAI to review this candidate against its story. |
| Indirect request | Is this change ready, and what evidence supports that conclusion? |
| Expected result | review-report plus a standardized handoff. |
| Required context | Exact candidate identity, acceptance criteria, governing rules, test receipts, and the relevant design and expert evaluation records. |
| Plugin capability | Skill, read-only repository tools, and independent DevForge verification. Security, performance, accessibility, and operations checks are selected by applicable requirements and risk, not a universal checklist. |
| State/action boundary | Review is read-only by default. The reviewer assesses meaning independently of author summaries and cannot redefine requirements or policy to make the candidate acceptable. |
| MVP support decision | Required for delivery readiness; expert behavioral evaluation moves to evaluate-expert, while review may inspect that report as evidence. |
| Does not activate for | Creating or repairing a candidate belongs to develop. Measuring a generated expert as a capability belongs to evaluate-expert. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| development-record and exact candidate | Required | Raw files, manifest, test receipts, and unresolved limitations. |
| story and architecture-contract | Required | Acceptance IDs and applicable governing rules. |
| design-spec and expert-evaluation-report | Conditional | Relevant experience expectations and required capability evidence. |
| Prior review-report | Optional | Findings requiring verification on the new candidate. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Establish scope | Confirm candidate and governing identities and the requested independence conditions. | The reviewer knows what is being evaluated and can meet the review conditions. |
| 2. Inspect | Read raw changes and relevant upstream facts; verify requirement traceability and applicable quality risks. | Claims are supported or flagged with concrete evidence. |
| 3. Validate | Independently rerun the appropriate checks and compare receipts to the candidate. | Actual results and unavailable checks are distinguished. |
| 4. Route | Report readiness and send candidate defects to develop, story defects to plan, and governing changes through change. | Every blocking finding has a responsible workflow and precise recheck condition. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| review-report | QA | Requirement coverage, observed checks, findings, correct remediation ownership, and readiness for the exact candidate. | [review-report.md](../templates/devforge-review/review-report.md) |


Consumer coverage: review-report -> develop; release; change.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Request review of an exact candidate. | Produces a scoped report with evidence and findings. |
| Indirect activation | Ask whether the change is ready. | Checks actual acceptance criteria, not only green test output. |
| Weak test | All tests pass but a stated failure case is absent. | Identifies the coverage or behavioral defect. |
| Wrong revision | Evidence belongs to a different candidate. | Rejects the readiness claim until evidence matches. |
| Out of scope | Ask to generate project expertise. | Routes to the expert creator. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

## Rework, stopping, and recovery

Rework: Re-review changed candidates and affected findings. Preserve prior reports; a previous PASS is not carried to a new candidate without the applicable verification.

Stop the affected continuation when: Missing candidate identity, stale governing inputs, unavailable required checks, or unmet independence conditions prevent the corresponding readiness claim.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-review to satisfy SKILL-010.
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

You are here: Review correctness and readiness. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
