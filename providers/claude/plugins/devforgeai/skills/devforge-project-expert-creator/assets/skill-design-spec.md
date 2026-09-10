# Skill design specification

Copy this template to the project's artifact location and fill it there; never fill it in place inside the skill package. Remove an optional section that does not apply. Preserve the identities of the governing template and of any accepted specification you are working from.

This is a DevForgeAI authoring document. It carries the design, the framework authority and source mapping, an optional evaluator-repair intake, and the change record. It does not certify a skill, and completing it establishes nothing about behaviour.

## 1. Identity and purpose

**Skill name:**
`[short-name-using-lowercase-and-hyphens]`

**Purpose:**
[The task this skill helps complete, and why project-specific guidance changes the result.]

**Description for discovery:**
[What it does and the conditions that should select it. Claude uses this text to decide automatic invocation, so state the precise triggers and the nearest work that should route elsewhere.]

**Intended users or role — optional:**
[Who uses this workflow.]

## 2. Scope and activation

**Use this skill when:**
[The requests and situations it should handle.]

**Outside its scope:**
[Closely related tasks it should not handle, and where they belong. Name these where confusion is likely.]

**Example activating requests:**

- "[Typical request.]"
- "[Another relevant request.]"

**Near-miss requests that must not activate it:**

- "[Request that looks similar and belongs elsewhere.]"

**How it should be invoked:**
[Automatically when relevant and explicitly by name - the default - or explicitly only.]

## 3. Inputs and expected results

**Required inputs:**
[Information, files or access necessary to perform the task.]

**Optional inputs:**
[Additional context that would improve the result.]

**When information is missing:**
[What may be inferred, what default applies, and what requires a question. Distinguish proceeding with a gap recorded from stopping.]

**Expected deliverable:**
[The finished result.]

**Output format and destination:**
[Structure, file type, naming and destination, where relevant. An externally selected destination governs; a project default applies only when nothing was selected.]

**Completion criteria:**

- [Observable condition that defines a successful result.]
- [Another meaningful condition.]

## 4. Workflow

Describe the essential process as named workflows, phases and tasks. Add or remove rows as needed and leave implementation choices open where several approaches are acceptable.

For each genuinely new, unclassified item, ask the user whether it is optional or whether its completion is required before its dependent action. Record the answer, its applicability and any permitted skip. Reuse answers already given; an explicit answer for a named group covers its named members, and an enforced parent does not automatically classify its children.

| ID | Level and parent | Action | Decision or expected result | Optional or required? | Enforcement route |
|---|---|---|---|---|---|
| W1 | Workflow; no parent | [Overall workflow.] | [Finished result.] | [User's choice.] | [Route ID or not applicable.] |
| P1 | Phase; parent W1 | [Phase action.] | [Phase result.] | [User's choice.] | [Route ID or not applicable.] |
| T1 | Task; parent P1 | [Task action.] | [Task result.] | [User's choice.] | [Route ID or not applicable.] |

**Applies when:**
[For each conditional item, the trigger and the conditions under which it may be skipped.]

**Dependencies and completion evidence:**
[For each required item: the action that must wait, what would demonstrate completion, who or what produces that evidence, and when it becomes stale.]

**Conditional paths — optional:**
[When situation X occurs, follow approach Y.]

**When to stop or seek clarification — optional:**
[Concrete conditions that prevent meaningful or authorised progress.]

## 5. Task-specific rules

**Required standards or conventions:**
[Domain rules, formats, calculations, terminology or project conventions.]

**Preferences:**
[Preferred approaches that still allow reasonable alternatives. Keep these distinct from requirements.]

**Actions requiring explicit authorisation — when applicable:**
[Consequential actions whose authorisation must exist before execution.]

**Known pitfalls — optional:**
[Demonstrated problems and how to recognise them. Avoid speculative restrictions.]

## 6. Tools and supporting resources — optional

**Target environment:**
[Claude Code, the relevant operating system or WSL, repository, or other relevant environment.]

**Required tools or integrations:**
[Each dependency and its purpose.]

**Access requirements:**
[Needed access, described without credentials or secrets.]

**Supporting materials:**

| Resource | Purpose | When it is needed |
|---|---|---|
| [Reference document.] | [Rules or domain knowledge.] | [Relevant task or condition.] |
| [Template or asset.] | [Basis for a generated output.] | [Relevant deliverable.] |
| [Script.] | [Repeated deterministic operation.] | [Relevant workflow step.] |

**Unavailable dependency behaviour:**
[An acceptable fallback, a request for missing access, or the specific limitation to report.]

**Enforcement route for required items — requirement only:**

Every item the user marks as required gets an entry here. One entry may cover several items when their conditions stay distinguishable. Record the requirement separately from whether enforcing it is feasible - these are different facts and merging them is how an unmet requirement quietly disappears.

Repeat for each entry:

- **Route ID and covered items:** [Identifier and the workflow, phase or task IDs.]
- **Requirement and protected action:** [The precise condition, and the action that must wait for it.]
- **Observable evidence:** [What could actually be inspected. Distinguish proof of completion from a self-reported marker.]
- **State and freshness:** [Where the evidence lives, who writes it, how it ties to this run and specification revision, and what invalidates it.]
- **Intended allow or refuse behaviour:** [The exact conditions for permitting the protected action or refusing it. A warning is advisory, not a refusal.]
- **Missing evidence and errors:** [Intended behaviour for missing or stale evidence, timeouts and unavailable dependencies.]
- **Recovery and user message:** [What remains incomplete, the action that resolves it, and a bounded stopping condition when progress is impossible.]
- **Owner:** Integration owner. The check itself is compiled into the DevForge CLI and invoked by whatever wiring that owner selects; this document records the requirement, not an implementation.
- **Feasibility:** [Unknown until the integration owner confirms it, or their recorded answer.]
- **Status:** Requirement recorded. No gate is implemented, activated or executed by this skill.

Where a requirement cannot be met in the target environment, record "Enforcement requested; not confirmed available" and propose a feasible alternative for discussion. Do not silently downgrade a required item into advisory prose, and do not write phase narration, self-issued PASS labels or a simulated command sequence into the skill as a substitute. For a subjective requirement, discuss a concrete evidence or human-decision condition and record its limits.

## 7. Acceptance cases — capture only

Record realistic cases and observable expected behaviour for a later evaluation. Write them before the candidate, so the expectations are independent of whatever gets authored. This skill does not run validators, tests, sample tasks or evaluations against the generated skill. That prohibition does not stop you authoring a skill whose own requested purpose is evaluation.

| Case | Example request or input | Expected behaviour |
|---|---|---|
| Typical task | [Example.] | [Expected result.] |
| Missing information | [Example.] | [Clarify, or apply a stated default.] |
| Outside scope | [Example.] | [Route elsewhere rather than applying this skill.] |
| Important variation — optional | [Example.] | [Correct alternative behaviour.] |

**Example of a good deliverable — optional:**
[An example, or a link to a representative file.]

## 8. Placement and maintenance — optional

**Availability:**
[This project / personal use across projects / bundled in a named plugin.]

**Installation location:**
[Recorded in section 10. An installed copy is never an alternative source.]

**Maintainer:**
[Person or team responsible for updates.]

**Reasons to revisit:**
[Changes to tools, versions, standards or workflow, and demonstrated failures.]

## 9. Authoring decision and progress

**Current status:**
[Draft / needs input / authored / reuse recommended.]

**Working specification and target paths:**
[This document's location, and the intended existing source or new skill directory.]

**Search scope and limitations:**
[Locations actually searched, relevant locations that were unavailable, and the limits of the comparison.]

**Related skills:**

| Candidate and source | Relevant overlap | Gap or meaningful distinction | Recommendation |
|---|---|---|---|
| [Existing skill and path.] | [Shared purpose or behaviour.] | [Missing behaviour or different scope.] | [Reuse / enhance / separate workflow.] |

**Selected approach and rationale:**
[Reuse / enhance / create, justified against the searched inventory.]

**Enhancement details — when applicable:**
[The selected durable source, the intended changes, and the existing behaviour to preserve.]

**Requirements, defaults and open decisions:**

| Item | Requirement or decision | Basis | Status |
|---|---|---|---|
| [Item ID or topic.] | [Requirement or proposed default.] | [User statement / supplied source / proposed assumption.] | [Settled / proposed / awaiting answer.] |

**Authored or changed files:**
[Paths and the purpose of each, filled in after authoring.]

**Material unresolved dependencies or enforcement gaps:**
[Recorded explicitly. Do not describe a recorded requirement as active enforcement.]

**Validation status:**
Not performed.

**Enforcement status:**
[Requirements recorded; no gate implemented by this skill. / Not applicable.]

## 10. Framework authority and source identity

Record observed identities, not guessed values. Preserve the selected governing bytes when a newer conflicting source appears. Use `unknown` or `null` with a reason and the affected work where information is missing. Hashing identifies bytes; it does not validate behaviour.

**Framework and provider:**
[Framework checkout or distributed package identity; Claude Code client and version; the consuming project.]

**Assignment and authority:**
[Actual authoring scope, selected provider and skill, owner or assignment reference, user authorisation, and the integration owner for shared changes. Do not fabricate an assignment ID.]

**Roster role:**
[The accepted roster role, or a separately scoped authoring utility. Authoring a utility does not amend the roster or certify a framework capability.]

**Selected source records:**

| Record | Governing source or preserved location | Revision or artifact ID | SHA-256 | Selection authority and purpose | Gaps or conflicts |
|---|---|---|---|---|---|
| Framework context | [Path.] | [Identity.] | [Hash or unknown with reason.] | [Source of accepted scope.] | [Gap or none.] |
| Skill-authoring contract | [Path.] | [Selected revision.] | [Hash.] | [Authoring, provider and packaging boundary.] | [Gap or none.] |
| Applicable artifact and execution contracts | [Paths.] | [Selected revisions.] | [Hashes.] | [Requirements that apply.] | [Gap or none.] |
| Governing design specification | [Preserved path.] | [Accepted revision or ID.] | [Hash.] | [User or owner selection.] | [Gap or none.] |
| Template used for this document | [Governing or package asset path.] | [Revision or preserved identity.] | [Hash.] | [Selected source and transformation.] | [Gap or none.] |

**Canonical source and generated runtime mapping:**

| Purpose | Selected path and provider | Identity or manifest reference | Ownership and refresh responsibility |
|---|---|---|---|
| Canonical framework source | [For Claude: the selected checkout's `providers/claude/plugins/devforgeai/skills/<name>`.] | [Before and after manifest, as applicable.] | [Assigned author or source owner.] |
| Project-specific source — when applicable | [Explicitly assigned durable source.] | [Manifest reference.] | [Owner.] |
| Installed project copy | [Consuming project's `.claude/skills/<name>`, or the explicitly selected mapping.] | [Installed manifest, or not generated.] | [Integration owner; generated from the canonical source.] |
| Plugin export — when applicable | [Assigned export destination and provider.] | [Export manifest, or not generated.] | [Integration owner.] |
| Working specification | [Project artifact location.] | [Specification identity.] | [Authoring owner.] |

A provider source folder alone is not a discovered installation. Installed copies and exports are generated artifacts, never alternative canonical sources. Package resources resolve from the loaded `SKILL.md` directory; project output paths resolve separately.

**Package derivations:**

| Source path and exact revision or preserved bytes | Source SHA-256 | Package-relative destination | Destination SHA-256 | Transformation | Refresh condition and owner |
|---|---|---|---|---|---|
| [Shared contract, template or reference.] | [Hash.] | [Resource path.] | [Hash.] | [Exact copy / bounded adaptation, explained.] | [Selected source change and responsible owner.] |

[Keep this metadata in the package's maintenance record where that is more appropriate. No record contains its own digest.]

**Authority, contract, installation or provider gaps:**
[Missing source bytes, unsupported runtime behaviour, unresolved ownership, required integration work, or conflicting selected revisions. Identify the affected work and continue the independent authorised authoring.]

**Preserved boundaries:**
[Named sibling gates, shared contracts, the accepted roster, and unrelated provider or skill behaviour that this assignment must not alter. A contract defect goes to its owner.]

**Authoring and release status:**
[Authored candidate / design only / reuse recommended. Evaluation and adoption are separate; a source or package identity establishes no activation, quality or release readiness.]

## 11. Evaluator repair intake — when applicable

Use a supplied frozen evaluator handoff without restarting settled Q&A. Retain the report bytes and existing requirement IDs. The evaluator evaluates; this skill changes the selected canonical source.

**Input records:**

| Record | Artifact type and identity | Retained path | SHA-256 | Purpose or intake gap |
|---|---|---|---|---|
| Evaluation report | [`devforge.artifact/v1`; skill-evaluation-report; SEVAL identity.] | [Path.] | [Hash.] | [Actual outcomes and limits.] |
| Repair specification | [Identity.] | [Path.] | [Hash.] | [Authorised changes.] |
| Handoff | [Selected envelope and identity.] | [Path.] | [Hash.] | [Assigned authoring scope and input references.] |
| Frozen target source manifest | [Candidate identity.] | [Path.] | [Hash.] | [Complete package-relative file-to-hash map.] |
| Frozen accepted specification | [Revision or identity.] | [Path.] | [Hash.] | [Governing requirements.] |
| Plan, cases and rubric | [Selected identities.] | [Paths.] | [Hashes.] | [Preselected expectations and evidence.] |
| Previous iteration — when applicable | [Identity.] | [Paths.] | [Hashes.] | [Retained history; no silent replacement.] |

**Current target versus frozen target:**
[Matching identities, or the observed drift with affected paths and requirements, the ownership reconciliation, the retained baselines, and the new candidate chosen for edits. Do not apply stale findings blindly.]

**Finding and requested-change intake:**

| Finding ID | Severity | Change ID and type | Requirement or workflow IDs | Expected behaviour and observed evidence | Proposed authoring scope | Status or missing evidence |
|---|---|---|---|---|---|---|
| [F-###.] | [BLOCKER / MAJOR / MINOR / ADVISORY.] | [CHG-###; required repair / authorised enhancement / unapproved proposal / bounded investigation.] | [Stable IDs.] | [Evidence locator and report reference.] | [Bounded source correction or investigation.] | [Accepted scope / proposed / blocked / needs evidence.] |

**Settled answers retained:**
[Accepted decisions, requirement IDs and classification answers that continue to apply.]

**New decisions — only if material:**
[Genuinely new unclassified items or scope conflicts needing Q&A.]

**Evaluation prerequisites:**
[Missing activation or loading observations, installed-resource checks, unavailable runtime, or other unobserved conditions. These do not alone establish a target defect or authorise an unsupported edit.]

**Specification amendments — only if authorised:**
[Accepted changes, their source, the preserved former identity, the new revision, and the affected requirement IDs. Do not weaken a fixed expectation to convert an old failure into a pass.]

**Repair constraints:**
[No target or helper execution, compilation, tests, validators, evaluations or activation by this skill. Preserve prior reports and route shared contract defects to their owner.]

## 12. Change record

Complete this after authoring or enhancement. It is an authoring record, not a completion receipt and not a validation result. Never record the containing document's own digest.

**Identity and authoring scope:**
[Record ID and date; actual owner or assignment reference; provider, target skill, permitted paths, and the requested create, enhance or reuse action.]

**Input references:**
[Selected handoff, report, specification, contract and template paths, identities and hashes, or not applicable. Preserve the frozen source manifest reference and any drift reconciliation.]

**Change mapping:**

| Finding IDs — if any | Change ID | Change type | Requirement IDs preserved or changed | Disposition | Old path and SHA-256 | New path and SHA-256 | Summary or reason |
|---|---|---|---|---|---|---|---|
| [F-### or not applicable.] | [CHG-###.] | [Required repair / authorised enhancement / unapproved proposal / bounded investigation.] | [IDs.] | [applied / deferred / declined.] | [Path and hash; absent for a new file.] | [Path and hash; absent for a removed file.] | [Bounded result or reason.] |

**New canonical source manifest:**
[Complete package-relative file-to-hash map, the candidate identity, and a separate retained manifest path and hash. No manifest includes its own digest. Record missing values and their reasons explicitly.]

**Resulting specification identity:**
[This specification's stable ID, revision and path, with prior-revision references retained.]

**Preserved behaviour and requirements:**
[Requirements and unrelated behaviour retained, including settled classifications and invocation policy.]

**Derivations and generated-copy work remaining:**
[Package derivation changes; canonical-to-installed and export mapping; the integration owner action required.]

**Deferred proposals, gaps and evaluation prerequisites:**
[Remaining items with reasons and owners.]

**Finding status — when applicable:**
Source changes recorded; reevaluation required.

**Validation status:**
Not performed.

**Enforcement status:**
[Requirements recorded; no gate implemented by this skill. / Not applicable.]

**Next handoff:**
[Populate the package's `assets/handoff.md` with the allocated next owner and the prerequisites. Distinguish a prepared document from an actual receiving invocation. Route adapter gaps to integration. No evaluation is launched, and old results do not transfer to changed bytes.]

## Evaluation coverage proposed

Record the accepted baseline, capability and environment scope, the current candidate, any prior accepted baseline, the impact of this change, the coverage you propose, and the evidence that is missing. Reuse accepted choices rather than reopening them.

This skill proposes evaluation coverage. A separate evaluator and an independent reviewer assess it, and the words "validate" or "install" appearing in a request do not by themselves select a level of evidence. The accepted Routine/Full manual-mode policy governs the promoted Codex packages and is `NOT_APPLICABLE` to this Claude package until an owner selects an equivalent for it.

For downstream consumers, map this design into the expert specification through exact references and stable sections, and use the expert package record for candidate and provenance identities. Preserve the authoring-only status, the recorded classifications, the bounded change dispositions, and the actual next user invocation. No source edit closes an earlier evaluation finding.
