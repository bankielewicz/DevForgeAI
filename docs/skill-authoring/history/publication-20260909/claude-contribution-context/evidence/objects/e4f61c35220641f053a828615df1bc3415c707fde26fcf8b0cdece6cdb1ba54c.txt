# SKILL-004: devforge-prototype

Status: DRAFT MVP specification, revision 2, refreshed 2026-09-05 UTC. This document defines required behavior; it is not an installed skill or a passing evaluation.
Current implementation: no callable implementation is supplied by this design package.

## User goal and use-case inventory

| Field | Contract |
| --- | --- |
| User goal | Run a bounded experiment that informs product, design, or architecture decisions, with a recorded result and explicit disposition of prototype code. |
| Direct request | Use DevForgeAI to prototype the risky part before we commit. |
| Indirect request | Can this approach support the interaction or performance we need? |
| Expected result | experiment-plan; prototype-report plus a standardized handoff. |
| Required context | A concrete uncertainty, relevant product/design/architecture drafts or accepted constraints, and the permitted experiment workspace. |
| Plugin capability | Skill with approved local runtime tools. No model API service is required; optional external systems require existing authorization and availability. |
| State/action boundary | Prototype work stays inside a declared experiment fence. It cannot silently become production code or override an accepted architecture decision. |
| MVP support decision | Conditional when an experiment could change a decision. Skip when the uncertainty can be resolved reliably by inspection or existing evidence. |
| Does not activate for | A fully specified production behavior with no open feasibility question belongs to develop. |

## Shared authoring requirements

Use the [skill authoring contract](../skill-authoring-contract.md) for provider source ownership, runtime packaging, scripts, reproducible eval fixtures, and separate A/B/C results. The original instructions, if present, need alignment with this revision; existence is not evidence of conformance. Core framework skills and generated experts use the same evaluation process.

## Inputs and provenance

| Input | Requirement | Consume only |
| --- | --- | --- |
| product-brief, design-spec, or architecture-contract | At least one relevant source | Identify the uncertain requirement or decision and whether its source is draft or accepted. |
| Experiment constraints | Required | Permitted paths, tools, time/resource bound, and observable success/failure measures. |
| prototype-report | Optional | Earlier experiment and what this iteration changes. |

Use the [artifact contract](../artifact-contract.md) for exact revisions, hashes, stable section IDs, decisions, and source evidence. A proposed source can support exploration, but cannot become an accepted production constraint by being copied downstream. For an established project, reuse valid current artifacts rather than replaying every earlier phase.

Use the [execution contract](../execution-contract.md): every writing session has an owner and fence; concurrent writers use distinct worktrees and branches from recorded commits. A shared worktree is not a concurrency mechanism. The [session template](../templates/shared/session-record.md) records the authority-selected assignment.

## Workflow and phase exits

| Phase | Work | Exit condition |
| --- | --- | --- |
| 1. Specify | Write the hypothesis, experiment cases, observation method, and bounded effort. | A plan exists before its measurements or result are known. |
| 2. Build | Implement only enough inside the experiment fence to test the hypothesis. | Prototype files and reproduction steps are identified. |
| 3. Observe | Run the planned checks; preserve outputs and environment details. | Each measurement is observed, failed, or explicitly unavailable. |
| 4. Decide | Compare evidence to the planned threshold and recommend a disposition and upstream revision. | Consumers can distinguish observation from recommendation; promotion requires separate hardening work. |

These phases describe the skill's workflow, not new CLI subcommands. The user can invoke the skill in an ordinary subscribed terminal once it is installed and discovered. Only documented, implemented DevForge commands may be named as executable gates. On interruption, preserve the current phase and evidence; resume by checking their identities and the session assignment again.

## Outputs and standardized templates

| Artifact | ID prefix | Required content | Template |
| --- | --- | --- | --- |
| experiment-plan | XPLAN | Hypothesis, measurement method, constraints, and stop conditions recorded before execution. | [experiment-plan.md](../templates/devforge-prototype/experiment-plan.md) |
| prototype-report | XREPORT | Observed results, exact prototype identity, limitations, and discard/reference/hardening disposition. | [prototype-report.md](../templates/devforge-prototype/prototype-report.md) |


Consumer coverage: experiment-plan -> prototype; review; prototype-report -> define-product; design; architect; plan; change.
The labeled artifact edges in the [roster diagram](../roster.md) summarize these flows; the input table above defines conditional paths.

Every result includes a [handoff](../templates/shared/handoff.md) with output identities, observed checks, unresolved decisions, next owner, and one copyable task prompt. Follow an existing authorized continuation; do not interpret a handoff recommendation as authority for unrelated external actions.

## Validation and behavioral acceptance

| Case | Representative request or condition | Required observation |
| --- | --- | --- |
| Direct activation | Ask to test a feasibility risk. | Creates a plan, prototype, and result tied to the original uncertainty. |
| Indirect activation | Ask whether a latency target is realistic. | Defines a measurement before claiming a result. |
| Unavailable runtime | The experiment cannot execute. | Records COULD_NOT_RUN and makes no performance claim. |
| Failed hypothesis | Measurements miss the stated threshold. | Preserves the failure and recommends a revision rather than moving the threshold. |
| Out of scope | Ask to add a fully specified production endpoint. | Routes to develop. |

Additional common cases:
- A concurrent writer claims this session's worktree or branch: stop dependent writes and report the ownership collision without deleting or resetting anyone's work.
- A relevant upstream revision, installed skill, base commit, or candidate changes: mark the applicable prior evidence stale and route a new check or run.
- A template placeholder remains in a required result field: the result stays a draft and cannot be presented as ready.
- A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS.

Acceptance requires real outputs from representative requests in each terminal for which support is claimed. Record the terminal version, actual discovery/activation, skill revision, source revisions, execution assignment, and evidence location. These cases are authoring acceptance requirements; they have not been executed by writing this specification.

## Rework, stopping, and recovery

Rework: A new hypothesis or changed threshold requires a new plan revision. Findings return to the owning product/design/architecture skill; production adoption becomes a planned story.

Stop the affected continuation when: Stop at the experiment's resource bound or when it needs authority beyond the declared fence; preserve partial observations.

Preserve accepted versions and observed failures. Do not force-unlock, overwrite another session's result, change external gates, or automatically retry indefinitely. If the worktree or active run changes, re-establish the appropriate baseline and evidence before resuming. Report missing observations precisely.

## Native creator authoring prompt

Use the available native skill creator with the following task; the placeholder values are supplied at authoring time:

```text
Assignment: Use the operator-supplied worktree, provider, write fence, and base.
Read skill-authoring-contract.md at the selected revision.
Goal: Create or improve devforge-prototype to satisfy SKILL-004.
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

You are here: Test a consequential uncertainty. Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit. A document's accepted status and an external gate's passing result are separate facts.
