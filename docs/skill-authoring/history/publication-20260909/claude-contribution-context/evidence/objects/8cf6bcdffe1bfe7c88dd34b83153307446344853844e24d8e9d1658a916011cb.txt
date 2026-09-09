# SKILL-008: devforge-evaluate-expert

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: no callable implementation is supplied by this design package.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Determine whether an exact installed expert skill activates appropriately and improves representative project work while respecting its constraints. |
| Direct request | Use DevForgeAI to evaluate this generated expert skill. |
| Indirect request | Does this expert actually help, or does its SKILL.md just look convincing? |
| Expected result | expert-evaluation-plan; expert-evaluation-report plus a standardized handoff. |
| Required context | The expert specification, exact candidate package, relevant raw project inputs, terminal availability, and a permitted isolated evaluation workspace. |
| Plugin capability | Native subscribed terminal runs, optionally bounded subagents when available and authorized. A manual separate-session evaluation is valid; no model API harness is required. |
| State/action boundary | Evaluation authors expectations from the task and accepted rules. It must not change the candidate or governing expectations to obtain a pass, or describe a shared contaminated session as independent. |
| MVP support decision | Required before a generated expert is treated as evaluated; record results separately for Codex and Claude when claiming support for both. |
| Does not activate for | Final acceptance of an application patch belongs to review. Frontmatter-only validation cannot substitute for this skill. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| expert-spec | Required | Capability expectations and the facts that ground them. |
| expert-package | Required | Exact source and installed candidate identities. |
| story, architecture-contract, and relevant raw evidence | Required as applicable | The same underlying task facts for candidate and baseline runs. |
| Prior evaluation report | Optional | Regression cases and previous revision identity. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Plan | Define representative direct, indirect, missing-input, negative, and out-of-scope cases from the specification; retain held-out cases where useful. | Expectations and evaluation scope are recorded before runs. |
| 2. Establish runtime | Check the actual target terminal, installed skill discovery, permissions, and session isolation. | The runtime and discovery check are observed or explicitly unavailable. |
| 3. Exercise | Run equivalent tasks with the candidate and an appropriate baseline, with equal underlying project facts and separate outputs. | Actual artifacts, case outcomes, and environment limitations are preserved. |
| 4. Assess | Judge outputs against expectations; distinguish triggering, task quality, constraint compliance, and resource cost. | The report supports a scoped recommendation, failure, or unavailable result without claiming certification. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| expert-evaluation-plan | EVPLAN | Predefined test requests, expected behaviors, baseline treatment, runtime, and outcome thresholds. | [expert-evaluation-plan.md](../templates/devforge-evaluate-expert/expert-evaluation-plan.md) |
| expert-evaluation-report | EVREPORT | Observed discovery, activation, outputs, case results, limitations, and recommendation for the exact installed revision. | [expert-evaluation-report.md](../templates/devforge-evaluate-expert/expert-evaluation-report.md) |


Consumer coverage: expert-evaluation-plan -> evaluate-expert; review; expert-evaluation-report -> project-expert-creator; develop; review; change.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Request evaluation of a candidate. | Produces a plan and evidence-bound report. |
| Indirect activation | Ask whether a generated skill improves work. | Includes a relevant baseline comparison. |
| Unavailable terminal | Native startup or authentication cannot complete. | Reports COULD_NOT_RUN; file existence is not skill discovery. |
| Weak grader | The result includes expected headings but violates the stack. | Fails behavioral compliance despite formatting. |
| Out of scope | Ask for source-code QA without an expert-evaluation task. | Routes to review. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

Report A (native discovery/activation), B (output quality), and C (installed resource resolution) independently. Explicit invocation, direct domain requests, and implicit activation are distinct observations. A no-skill baseline must not discover the candidate from another installation. Keep fixture, case, source, installed, and baseline identities in each run manifest. Inspect a creator harness before relying on its subscription mode or consultation detector. Framework-skill bootstrap evaluation uses the common authoring report; this skill's XSPEC/XPKG workflow remains the project-expert specialization.

## Rework, stopping, and recovery

Rework: Failed behavior returns to the creator with cases and evidence. Changed candidates need new evaluation identity; tests whose expectations change require a recorded rationale and version.

Stop the affected continuation when: Unavailable runtime, missing raw inputs, or an independence requirement that cannot be met blocks the corresponding claim. Do not substitute an author's self-report.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-evaluate-expert to satisfy SKILL-008.
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

You are here: Measure expert skill behavior. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
