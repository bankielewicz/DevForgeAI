# SKILL-007: devforge-project-expert-creator

Status: Codex promotion candidate, revision 3, 2026-09-08. Manual invocation, handoffs and commands; operational and behavioral status remain evidence-dependent.
Current implementation: providers/codex/plugins/devforgeai/skills/devforge-project-expert-creator. Claude scope is unchanged.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Author a focused expert capability from a concrete project need, approved decisions, and verified references, producing a candidate that can be evaluated in the target terminal. |
| Direct request | Use DevForgeAI to create the persistence expert this project needs. |
| Indirect request | Our next story needs someone who knows this codebase's data access rules and pinned APIs. |
| Expected result | expert-spec; expert-package; native skill instructions plus a standardized handoff. |
| Required context | A concrete goal or story, the current expertise map, applicable architecture rules, the selected runtime, and approved reference sources. |
| Plugin capability | Skill plus an available native creator and local package tools. Creator invocation is an authoring aid, not an independent verdict. DevForge handles structural binding and installation. |
| State/action boundary | Generate guidance and supporting resources inside the declared expert directory. Do not change external policy, evaluator expectations, or permissions to make the candidate pass. |
| MVP support decision | Required when a real capability gap exists; reuse suitable current expertise and refresh only when changes or observed failures justify it. |
| Does not activate for | An organizational role label alone does not justify a new skill. A small task may need a bounded context packet instead. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| architecture-contract | Required for production expertise | Applicable rules, versions, source layout, and required capability. |
| story or concrete project goal | At least one required | The work that needs this expertise and its acceptance intent. |
| Current expertise map and expert package | Optional | Existing capabilities, measured failures, and prior revisions. |
| Primary technical references | Required for factual API guidance | Version-specific sources with verification evidence. |
| change-request or expert-evaluation-report | Conditional | Accepted change or observed failure motivating a refresh. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

All five named phases and required actions below are Enforced; these preserve the former builder's accepted identities. SKILL-007's older four-phase draft is superseded for Codex by this explicit mapping.

| Phase | Required work | Exit condition |
| --- | --- | --- |
| Intake | Recover project goal, accepted constraints, source/version identities, provider and write fence. | Actual authority and missing inputs recorded. |
| Selection | Search existing expertise and source/install mapping. | Justified reuse, bounded enhancement or creation, with collision handling. |
| Design | Focused Q&A; preserve decisions/API versions; populate skill-design-spec and classifications. | Grounded specification, requirements and proposed cases recorded before authoring. |
| Authoring | Create/enhance only the canonical candidate and its necessary resources. | Useful authoring and change record; no target tests, binding or installation by creator. |
| PreparedTransfer | Save candidate/XSPEC/XPKG identities and an actionable evaluator handoff. | Prepared handoff with actual limitations and next user invocation; no receiver execution claim. |

Legacy four-phase mapping: Identify the gap -> Intake/Selection; Specify -> Design; Author -> Authoring; Bind for evaluation -> PreparedTransfer plus separately owned operator binding/installation. This does not turn binding into creator work.

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| expert-spec | XSPEC | Capability scope, activation boundary, authoritative inputs, and behavioral expectations written before authoring. | [expert-spec.md](../templates/devforge-project-expert-creator/expert-spec.md) |
| expert-package | XPKG | Frozen candidate file manifest, native skill path, source pins, and intended runtime targets; later observations belong to EVREPORT. | [expert-package.md](../templates/devforge-project-expert-creator/expert-package.md) |
| native skill instructions | NATIVE | SKILL.md and necessary references; provenance is held in the expert-package sidecar. | [expert-skill.md](../templates/devforge-project-expert-creator/expert-skill.md) |

The native SKILL.md template follows the provider skill format rather than the general artifact envelope. Its exact files and provenance are carried by the expert-package sidecar; later installation and evaluation observations are carried by EVREPORT. Templates remain under docs until intentionally used for skill authoring.

Consumer coverage: expert-spec -> project-expert-creator; evaluate-expert; review; expert-package -> evaluate-expert; develop; review; change; native skill instructions -> evaluate-expert; develop.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Request an expert for a specified persistence story. | Produces a capability specification and native candidate with project references. |
| Indirect activation | Describe a concrete expertise gap. | Checks reuse before creating another skill. |
| Stack conflict | The candidate proposes an unapproved ORM. | Preserves the contract and reports the conflict. |
| Refresh | Change one accepted API version. | Updates affected guidance and invalidates affected prior evaluation; retains history. |
| Out of scope | Ask for a full team of experts without tasks. | Identifies actual capability needs instead of generating an org chart. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

The created package includes source-grounded version-specific knowledge, declared refresh conditions, and reproducible tests. Create optional folders only when justified. The native creator receives the assigned provider path; it must not use a shared default source. Description optimization uses distinct authored/held-out queries, while output-quality comparisons retain the appropriate no-skill or old-skill baseline.

## Rework, stopping, and recovery

Rework: Use evaluator findings to make bounded revisions. Governing-rule defects return through change. Every changed candidate receives a new package identity and relevant reevaluation.

Stop the affected continuation when: Missing approval for a consequential rule, unverifiable required API behavior, or a conflicting write fence prevents declaring the candidate ready for evaluation or production as applicable.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-project-expert-creator to satisfy SKILL-007.
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

You are here: Create or refresh project expertise. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.

## F01–F08 manual promotion contract

The Codex packages replace skill-builder/skill-validator as discoverable workflows. Their managed v1 protocol IDs and old receipts remain unchanged; no new-name managed adapter is admitted. The creator authors, the evaluator evaluates read-only, and the user initiates each receiving skill and relevant command. Automatic orchestration and G8 funded-launch repair remain deferred; original cases and failed evidence are preserved.

Use the creator's skill-design-spec.md as the detailed XSPEC source; XPKG is its exact candidate/provenance map. EVPLAN and EVREPORT bind the evaluator's detailed plan/results/decision rather than demanding duplicated reports. Preserve both producer handoffs and the bounded repair specification.

The accepted Routine/Full policy applies to manual mode. Routine requires an accepted baseline and scope, immediate/cumulative impact, compatibility and independent reviewed coverage. First qualification and consequential control/transfer changes require Full, including real user-mediated receiving evidence; merely saying validate or install does not require Full. Every phase/task retains its classification and a result or explicit conditional disposition.

Mechanical checks and semantic review are separate. Existing expert prepare/bind/status/check and the evaluator's helpers enforce only their implemented predicates, not universal phase completion. Missing enforcement blocks its dependent claim/action; reporting remains possible. The package manual-operation reference documents exact commands, owners, outputs and gaps.

Retain existing-environment, create-Git-worktrees and static-only choices. Preparation is not native readiness. Observe source/history/output boundaries and authentication before native execution. No credential changes or old execution-window renewal is implied.


An owner-approved local unqualified baseline may be installed after the separate [bounded local acceptance set](../skill-authoring-contract.md#owner-approved-local-unqualified-baseline) passes. This is not first/Full qualification: preserve unexecuted qualification cases as NOT_RUN and all historical failures. Required workflow classifications and ownership boundaries are unchanged.
