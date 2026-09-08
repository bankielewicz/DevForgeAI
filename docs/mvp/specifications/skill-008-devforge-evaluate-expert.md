# SKILL-008: devforge-evaluate-expert

Status: Codex promotion candidate, revision 3, 2026-09-08. Manual invocation, handoffs and commands; operational and behavioral status remain evidence-dependent.
Current implementation: providers/codex/plugins/devforgeai/skills/devforge-evaluate-expert. Claude scope is unchanged.

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

All phases P1–P6 and tasks T01–T12 remain Enforced. These replace the older four-phase draft table for Codex while preserving original validator IDs.

| Phase | Tasks | Exit record |
|---|---|---|
| P1 Intake and baseline | T01 identify target, provider, authority, specification and write fence; T02 freeze candidate/specification/cases/rubric/baseline | Frozen input identities; bounded workspace allocation when selected; complete experiment plan before native execution, or explicit missing-input causes |
| P2 Deterministic checks | T03 inspect structure, references, source/installed resource identity and documented script syntax | Raw structural results; semantic behavior remains unevaluated |
| P3 AI review | T04 independently inspect prompt engineering and framework compliance against the rubric | Per-criterion findings with source evidence and reviewer identity |
| P4 Behavioral tests | T05 establish isolated runtime/fixtures; T06 installed resources (C); T07 candidate/baseline output quality (B); T08 discovery/activation (A) | Separate case outcomes, run manifests, artifacts and transcripts |
| P5 Verdict | T09 adjudicate evidence, applicability, findings, incomplete coverage and freshness | Deterministic decision receipt plus evidence-based disposition |
| P6 Builder handoff | T10 write verification results; T11 write bounded repair/enhancement specification and rerun plan; T12 deliver custody/handoff | Saved results, repair specification, and handoff with exact identities |


Legacy mapping: Plan -> P1; Establish runtime -> P4/T05; Exercise -> P4/T06–T08; Assess -> P2/P3/P5, with explicit P6 reporting and repair handoff.

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
resources, reproducible eval cases/fixtures and a prepared handoff. A separate
evaluation owner supplies actual A/B/C observations.
Record the real installation mode and candidate/baseline identities.
Do not claim implicit activation from a run explicitly supplied SKILL.md.
Boundaries: Preserve user scope and existing approval. Keep DevForge authority
external, respect the assigned worktree, and report unavailable checks truthfully.
```

The native creator may improve wording and packaging without changing this specification's accepted meaning. Move lengthy conditional procedures into references, keep the trigger description precise, and use scripts only for real deterministic operations. During plugin authoring, copy needed templates into the package and use package-relative references; installed skills must not depend on this repository's docs path being present.

## Completion handoff

You are here: Measure expert skill behavior. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.

## F01–F08 manual promotion contract

The Codex packages replace skill-builder/skill-validator as discoverable workflows. Their managed v1 protocol IDs and old receipts remain unchanged; no new-name managed adapter is admitted. The creator authors, the evaluator evaluates read-only, and the user initiates each receiving skill and relevant command. Automatic orchestration and G8 funded-launch repair remain deferred; original cases and failed evidence are preserved.

Use the creator's skill-design-spec.md as the detailed XSPEC source; XPKG is its exact candidate/provenance map. EVPLAN and EVREPORT bind the evaluator's detailed plan/results/decision rather than demanding duplicated reports. Preserve both producer handoffs and the bounded repair specification.

The accepted Routine/Full policy applies to manual mode. Routine requires an accepted baseline and scope, immediate/cumulative impact, compatibility and independent reviewed coverage. First qualification and consequential control/transfer changes require Full, including real user-mediated receiving evidence; merely saying validate or install does not require Full. Every phase/task retains its classification and a result or explicit conditional disposition.

Mechanical checks and semantic review are separate. Existing expert prepare/bind/status/check and the evaluator's helpers enforce only their implemented predicates, not universal phase completion. Missing enforcement blocks its dependent claim/action; reporting remains possible. The package manual-operation reference documents exact commands, owners, outputs and gaps.

Retain existing-environment, create-Git-worktrees and static-only choices. Preparation is not native readiness. Observe source/history/output boundaries and authentication before native execution. No credential changes or old execution-window renewal is implied.


An owner-approved local unqualified baseline may be installed after the separate [bounded local acceptance set](../skill-authoring-contract.md#owner-approved-local-unqualified-baseline) passes. This is not first/Full qualification: preserve unexecuted qualification cases as NOT_RUN and all historical failures. Required workflow classifications and ownership boundaries are unchanged.
