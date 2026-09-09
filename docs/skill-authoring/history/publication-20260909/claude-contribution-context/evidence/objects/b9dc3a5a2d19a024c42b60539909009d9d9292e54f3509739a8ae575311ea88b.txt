# SKILL-005: devforge-architect

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: no callable implementation is supplied by this design package.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Record the architecture, dependency versions, source layout, interface responsibilities, and test policy that govern a delivery slice. |
| Direct request | Use DevForgeAI to establish this project's architecture and stack contract. |
| Indirect request | How should we structure this SaaS so later sessions do not introduce incompatible libraries? |
| Expected result | architecture-contract plus a standardized handoff. |
| Required context | Accepted product scope, relevant designs and experiments, the real repository if it exists, and verified documentation for selected versions. |
| Plugin capability | Skill, repository inspection, and available primary-source research. DevForge owns executable policy and stack/test adapters; the current POC's synthetic dependency check is not a NuGet/npm adapter. |
| State/action boundary | Author a proposed contract and record actual user decisions. The skill cannot make an external DevForge policy effective or replace an existing stack by editing prose. |
| MVP support decision | Required before governed production development; existing projects begin with an evidence-backed inventory rather than a replacement architecture. |
| Does not activate for | A new library release alone is not authorization to upgrade; route the proposal through change. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| product-brief | Required | Functional and nonfunctional requirements for this slice. |
| design-spec and prototype-report | Conditional | Relevant interaction contracts and feasibility findings. |
| Repository and package manifests | Required when present | Observed dependencies, versions, layout, interfaces, tests, and operating constraints. |
| Primary technical sources | Required for selected API claims | Version, URL or supplied reference, verification date, and applicable limitations. |
| architecture-contract or change-request | Conditional | Existing accepted rules and the bounded amendment. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Inventory | Inspect current scope, code, manifests, and constraints; distinguish observed state from desired state. | Existing decisions and evidence gaps are listed. |
| 2. Resolve | Compare consequential alternatives and check version-specific APIs; use a prototype for unresolved execution risk. | Each architectural choice has a reason and evidence or an explicit open question. |
| 3. Specify | Assign rule and decision IDs; define dependencies, file ownership, interfaces, data boundaries, test commands, and required capabilities. | The contract is precise enough for a story author and a validator adapter. |
| 4. Adopt and hand off | Record accepted choices and provide their exact revision to the external policy owner. | No claim of mechanical enforcement is made without a supported adapter and observed gate evidence. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| architecture-contract | ARCH | Versioned decisions, approved stack, source tree, interface rules, security/operating requirements, test policy, and expertise needs. | [architecture-contract.md](../templates/devforge-architect/architecture-contract.md) |


Consumer coverage: architecture-contract -> plan; project-expert-creator; evaluate-expert; develop; review; change.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Ask to define a project's architecture. | Produces a contract mapped to product requirements. |
| Indirect activation | Ask how to prevent stack drift. | Defines dependency and layout rules with separate enforcement requirements. |
| Existing stack | The repository uses Dapper and the user has retained it. | Preserves that decision; Entity Framework appears only as an explicitly requested proposal. |
| Version uncertainty | A familiar API example does not match the pinned version. | Verifies it or records uncertainty rather than silently changing versions. |
| Out of scope | Ask for an isolated copy edit. | Does not impose a new architecture process. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

## Rework, stopping, and recovery

Rework: Prototype unresolved choices. Changes to accepted contracts produce a change request, revised contract, and affected-consumer review; they do not overwrite prior accepted evidence.

Stop the affected continuation when: Conflicting adopted rules or unsupported enforcement adapters block the applicable production readiness claim. A useful draft can still be completed.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-architect to satisfy SKILL-005.
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

You are here: Establish the project contract. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
