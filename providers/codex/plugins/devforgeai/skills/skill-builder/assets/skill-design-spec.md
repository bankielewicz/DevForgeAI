# Skill Design Specification

Fill in the placeholders below. Optional sections can be removed when they do not apply. Preserve the selected governing template and accepted specification identities. This DevForgeAI authoring document includes framework authority, canonical/runtime mapping, optional validator remediation intake, and a builder change receipt; it does not certify a skill.

## 1. Identity and purpose

**Skill name:**  
`[short-name-using-lowercase-and-hyphens]`

**Purpose:**  
[Describe the task this skill helps complete and why specialized guidance is useful.]

**Description for skill discovery:**  
[Briefly state what the skill does and when it should be used. This helps Codex select it.]

**Intended users or role — optional:**  
[Who uses this workflow?]

## 2. Scope and activation

**Use this skill when:**  
[Describe the requests or situations it should handle.]

**Outside its scope:**  
[Identify closely related tasks it should not handle, if confusion is likely.]

**Example activating requests:**

- "[Typical user request]"
- "[Another relevant request]"

**How it should be invoked:**  
[Automatically when relevant and explicitly by name—the default—or explicitly only.]

## 3. Inputs and expected results

**Required inputs:**  
[List the information, files, or access necessary to perform the task.]

**Optional inputs:**  
[List additional context that would improve the result.]

**When information is missing:**  
[Explain what may be inferred, what defaults apply, and what requires clarification.]

**Expected deliverable:**  
[Describe the finished result.]

**Output format and destination:**  
[Specify the structure, file type, naming, or destination when relevant.]

**Completion criteria:**

- [Observable condition that defines a successful result.]
- [Another meaningful condition.]

## 4. Workflow

Describe the essential process as named workflows, phases, and tasks. Add or remove rows as needed; leave implementation choices open where multiple approaches are acceptable.

During the design conversation, ask the user for each unclassified item: "Should [item] be optional, or should its completion be enforced before [dependent action]?" Ask small groups of related questions and record the answers. Reuse answers already supplied; do not repeatedly request the same decision. Preserve explicit named group answers through remediation and ask again only for genuinely new unclassified items or a material conflict.

Record a classification for each item. An enforced parent does not automatically make every child enforced. Apply a shared classification only when the user explicitly applies it to the named group, and record any exceptions.

| ID | Level and parent | Action | Decision or expected result | Optional or enforced? | Hook proposal |
|---|---|---|---|---|---|
| W1 | Workflow; no parent | [Overall workflow.] | [Finished result.] | [User's choice.] | [Proposal ID or not applicable.] |
| P1 | Phase; parent W1 | [Phase action.] | [Phase result.] | [User's choice.] | [Proposal ID or not applicable.] |
| T1 | Task; parent P1 | [Task action.] | [Task result.] | [User's choice.] | [Proposal ID or not applicable.] |
| T2 | Task; parent P1 | [Task action.] | [Task result.] | [User's choice.] | [Proposal ID or not applicable.] |

**Applies when:**  
[For each conditional item, identify the trigger and when the item may be skipped.]

**Dependencies and completion evidence:**  
[For each enforced item, identify the action that must wait, what demonstrates completion, who or what produces that evidence, and when it becomes stale.]

**Conditional paths — optional:**  
[When situation X occurs, follow approach Y.]

**When to stop or seek clarification — optional:**  
[Specify concrete conditions that prevent meaningful or authorized progress.]

## 5. Task-specific rules

**Required standards or conventions:**  
[Domain rules, formatting requirements, calculations, terminology, or project conventions.]

**Preferences:**  
[Preferred approaches that allow reasonable alternatives.]

**Actions requiring explicit authorization — when applicable:**  
[Identify consequential actions whose authorization must be established before execution.]

**Known pitfalls — optional:**  
[Include demonstrated problems and how to recognize them. Avoid speculative restrictions.]

## 6. Tools and supporting resources — optional

**Target environment:**  
[Codex CLI, desktop app, WSL, Windows, repository, or other relevant environment.]

**Required tools or integrations:**  
[Name each dependency and explain its purpose.]

**Access requirements:**  
[Describe needed access without including credentials or secrets.]

**Supporting materials:**

| Resource | Purpose | When it is needed |
|---|---|---|
| [Reference document] | [Rules or domain knowledge.] | [Relevant task or condition.] |
| [Template or asset] | [Basis for generated output.] | [Relevant deliverable.] |
| [Script] | [Repeated operation requiring reliable execution.] | [Relevant workflow step.] |

**Unavailable dependency behavior:**  
[Use an acceptable fallback, request missing access, or explain the specific limitation.]

**Hook proposals for enforced items — design only:**

Propose a hook design for every item the user marks enforced. One hook may cover several items when their conditions can be kept distinct; map every enforced item to its proposal. Record the requested requirement separately from the feasibility of enforcing it.

Repeat the following fields for each proposal:

- **Proposal ID and covered items:** [Hook ID and workflow, phase, or task IDs.]
- **Requirement and protected action:** [The precise condition and the action that must wait.]
- **Target runtime and scope:** [Codex surface/version, project or plugin, and how the hook identifies the relevant skill run without affecting unrelated work.]
- **Event and matcher:** [An event supported by the target runtime and the tools/actions it covers. Do not invent a workflow-phase event.]
- **Observable condition:** [Evidence the hook can inspect; distinguish proof of completion from a self-reported marker.]
- **State and dependencies:** [Where evidence lives, who writes it, how it is tied to the current run and specification revision, and when it is invalidated.]
- **Allow/block behavior:** [Exact conditions for allowing the protected action or blocking it. A warning is advisory.]
- **Missing evidence and errors:** [Desired behavior for missing or stale evidence, timeouts, unavailable dependencies, and hook errors; describe any difference from the runtime's actual behavior.]
- **Recovery and user message:** [Explain what remains incomplete and the action that resolves it, with a bounded stopping condition when progress is impossible.]
- **Exceptions — if explicitly permitted:** [Who may authorize an exception and how it is recorded. Do not assume an override is allowed.]
- **Configuration and activation requirements:** [Proposed hook configuration location, handler dependencies, and any required review/trust. A hook script placed in a skill folder alone does not activate enforcement.]
- **Feasibility and coverage gaps:** [Supported / partial / unsupported / unknown, with evidence from the target runtime's documentation and any uncovered tool paths.]
- **Proposal status:** [Design only; not installed, activated, executed, or validated.]

For unsupported or uncertain cases, record "Enforcement requested; [unsupported or unconfirmed] in the target environment" and propose a feasible alternative for discussion. Do not silently downgrade an enforced requirement to an instruction. For subjective requirements, discuss a concrete approval or evidence condition and document its limits.

Use the [official Codex hook documentation](https://learn.chatgpt.com/docs/hooks) when choosing events and handlers. Hook support and coverage depend on the target runtime. Design checks here describe proposed future behavior; the builder does not execute them.

## 7. Validation examples — capture only

Record realistic cases and observable expected behavior for future validation. The builder does not run validators, tests, sample tasks, or evaluations against the generated skill or proposed hooks. This does not prohibit authoring a skill whose own requested purpose involves validation.

| Case | Example request or input | Expected behavior |
|---|---|---|
| Typical task | [Example.] | [Expected result.] |
| Missing information | [Example.] | [Clarify or apply a stated default.] |
| Outside scope | [Example.] | [Avoid applying this skill.] |
| Important variation — optional | [Example.] | [Correct alternative behavior.] |

**Example of a good deliverable — optional:**  
[Paste an example or link to a representative file.]

## 8. Placement and maintenance — optional

**Availability:**  
[This project / personal use across projects / bundled in a named plugin.]

**Installation location:**  
[Record the canonical source and generated installation/export mapping in section 10; do not treat an installed copy as an alternative source.]

**Maintainer:**  
[Person or team responsible for updates.]

**Reasons to revisit the skill:**  
[Changes to tools, standards, workflow, or demonstrated failures.]

## 9. Authoring decision and progress

**Current status:**  
[Draft / needs input / authored / reuse recommended.]

**Working specification and target paths:**  
[This document's location and the intended existing source or new skill directory.]

**Search scope and limitations:**  
[Locations actually searched, relevant unavailable locations, and any limits on the comparison.]

**Related skills:**

| Candidate and source | Relevant overlap | Gap or meaningful distinction | Recommendation |
|---|---|---|---|
| [Existing skill and path.] | [Shared purpose or behavior.] | [Missing behavior or different scope.] | [Reuse / enhance / separate workflow.] |

**Selected approach and rationale:**  
[Reuse / enhance / create. Explain why this is appropriate based on the searched inventory.]

**Enhancement details — when applicable:**  
[Selected durable source, intended changes, and existing behavior to preserve.]

**Requirements, defaults, and open decisions:**

| Item | Requirement or decision | Basis | Status |
|---|---|---|---|
| [Item ID or topic.] | [Requirement or proposed default.] | [User statement / supplied source / proposed assumption.] | [Settled / proposed / awaiting answer.] |

**Authored or changed files:**  
[Paths and the purpose of each file, populated after authoring.]

**Material unresolved dependencies or enforcement gaps:**  
[Record gaps explicitly. Do not describe proposed hooks as active enforcement.]

**Validation status:**  
Not performed.

**Hook status:**  
[Design only / not applicable.]

## 10. Framework authority and source identity

Record observed identities, not guessed values. Preserve the selected governing bytes when a newer conflicting source appears. Use unknown/null with a reason and the impacted work when information is missing. Hashing identifies bytes; it does not validate their behavior.

**Framework and provider:**  
[Framework checkout or distributed package identity; Codex target runtime/client/version; consuming project.]

**Assignment and authority:**  
[Actual authoring scope, selected provider/skill, owner or assignment reference, user authorization, and integration owner for shared changes. Do not fabricate an assignment ID.]

**Utility or accepted roster role:**  
[Existing accepted role or separately scoped authoring utility. Authoring a utility does not amend the 12-skill roster or certify a framework capability.]

**Selected source records:**

| Record | Governing source or preserved location | Revision or artifact ID | SHA-256 | Selection authority and purpose | Gaps or conflicts |
|---|---|---|---|---|---|
| Framework context | [Path.] | [Identity.] | [Hash or unknown with reason.] | [Source of accepted scope.] | [Gap or none.] |
| Skill-authoring contract | [Path.] | [Selected revision.] | [Hash.] | [Authoring/provider/packaging boundary.] | [Gap or none.] |
| Applicable artifact/execution contracts | [Paths.] | [Selected revisions.] | [Hashes.] | [Requirements that apply.] | [Gap or none.] |
| Governing design specification | [Preserved path.] | [Accepted revision/ID.] | [Hash.] | [User/owner selection.] | [Gap or none.] |
| Template used for this document | [Governing or package asset path.] | [Revision or preserved identity.] | [Hash.] | [Selected source and transformation.] | [Gap or none.] |

**Canonical source and generated runtime mapping:**

| Purpose | Selected path and provider | Identity or manifest reference | Ownership and refresh responsibility |
|---|---|---|---|
| Canonical framework source | [For Codex: selected framework checkout/providers/codex/plugins/devforgeai/skills/<name>.] | [Before/after manifest as applicable.] | [Assigned author/source owner.] |
| Project-specific source — when applicable | [Explicitly assigned durable source.] | [Manifest reference.] | [Owner.] |
| Installed project copy | [Consuming project/.agents/skills/<name> or explicitly selected mapping.] | [Installed manifest, or not generated.] | [Integration owner; generated from canonical source.] |
| Plugin export — when applicable | [Assigned export destination/provider.] | [Export manifest, or not generated.] | [Integration owner.] |
| Working specification | [Project artifact/document location.] | [Specification identity.] | [Authoring owner.] |

A provider source folder alone is not a discovered installation. Installed copies and exports are generated artifacts, never alternative canonical sources. Package-local resource paths resolve from the loaded SKILL.md directory; project output paths resolve separately.

**Package derivations:**

| Source path and exact revision/preserved bytes | Source SHA-256 | Package-relative destination | Destination SHA-256 | Transformation | Refresh condition and owner |
|---|---|---|---|---|---|
| [Shared contract/template/reference.] | [Hash.] | [Resource path.] | [Hash.] | [Exact copy / bounded adaptation and explanation.] | [Selected source change and responsible owner.] |

[Keep this metadata in a maintenance record when appropriate. Do not add a self digest to the record containing its own manifest.]

**Authority, contract, installation, or provider gaps:**  
[Missing source bytes, unsupported runtime behavior, unresolved ownership, required integration work, or conflicting selected revisions. Identify affected work and continue independent authorized authoring.]

**Preserved boundaries:**  
[Named sibling gates, shared contracts, accepted roster and unrelated provider/skill behavior that this assignment must not alter. A contract defect is reported to its owner.]

**Authoring and release status:**  
[Authored candidate / design only / reuse recommended. Evaluation and adoption remain separate; source or package identities do not establish native activation, quality, or release readiness.]

## 11. Validator remediation intake — when applicable

Use a supplied frozen validator handoff without restarting settled Q&A. Retain report/evidence bytes and existing requirement IDs. The validator evaluates; the builder changes the selected canonical source.

**Input handoff artifacts:**

| Record | Artifact type and identity | Retained path | SHA-256 | Purpose or intake gap |
|---|---|---|---|---|
| verification-results.md | [devforge.artifact/v1; skill-evaluation-report; SEVAL identity.] | [Path.] | [Hash.] | [Actual outcomes and limits.] |
| skill-enhancement-spec.md | [devforge.artifact/v1; local paired-utility skill-enhancement-spec; SENH identity.] | [Path.] | [Hash.] | [Not a registered companion CLI schema.] |
| handoff.md | [Selected devforge.artifact/v1 envelope and identity.] | [Path.] | [Hash.] | [Assigned authoring scope and input references.] |
| Frozen target source manifest | [Candidate identity.] | [Path.] | [Hash.] | [Complete package-relative file/SHA-256 map.] |
| Frozen accepted specification | [Revision/identity.] | [Path.] | [Hash.] | [Governing requirements.] |
| Plan, cases and rubric | [Selected identities.] | [Paths.] | [Hashes.] | [Preselected expectations and evidence.] |
| Previous iteration — when applicable | [Identity.] | [Paths.] | [Hashes.] | [Retained history; no silent replacement.] |

**Current target versus frozen target:**  
[Matching identities or observed drift, affected paths/requirements, owner/scope reconciliation, retained old/current baselines, and the new candidate chosen for edits. Do not apply stale findings blindly.]

**Finding and requested-change intake:**

| Finding ID | Severity | Change ID and type | Requirement/workflow IDs | Expected behavior and observed evidence | Proposed authoring scope | Status or missing evidence |
|---|---|---|---|---|---|---|
| [F-###.] | [BLOCKER / MAJOR / MINOR / ADVISORY.] | [CHG-###; required repair / authorized enhancement / unapproved proposal / bounded investigation.] | [Stable IDs.] | [Evidence locator plus relevant report reference.] | [Bounded source correction or investigation.] | [Accepted scope / proposed / blocked / needs evidence.] |

**Settled answers retained:**  
[Accepted decisions, requirement IDs, Optional/Enforced classifications and explicit named group answers that continue to apply.]

**New decisions — only if material:**  
[New unclassified workflow/phase/task items or scope conflicts requiring Q&A. Ask Optional/Enforced only for genuinely new unresolved items. An existing group answer persists.]

**Evaluation prerequisites:**  
[Missing native activation/loading observations, installed resources, unavailable runtime, or other unobserved conditions. These do not alone establish a target defect or authorize unsupported edits.]

**Specification amendments — only if authorized:**  
[Accepted changes, their source, preserved former specification identity, new revision/identity, and affected requirement IDs. Do not weaken fixed expectations to convert an old failure into a pass.]

**Remediation constraints:**  
[No target/helper execution, compilation, tests, validators, evaluations or hook activation by the builder. Preserve prior reports and route shared contract defects to their owner.]

## 12. Builder change receipt

Complete substantive change content after authoring or enhancement. This authoring record is not a runtime completion receipt or validation result. Runtime owns managed final identity checks, immutable state, receipt publication and readback; no manual phase/receipt helper fallback is permitted.

**Receipt identity and authoring scope:**  
[Receipt/artifact ID and date; actual owner/assignment reference; provider, target skill, permitted paths, and requested create/enhance/reuse action.]

**Input references:**  
[Selected handoff/report/enhancement-spec/specification/contracts/template paths, identities and SHA-256 values, or not applicable. Preserve the frozen source manifest reference and drift reconciliation.]

**Change mapping:**

| Finding IDs — if any | Change ID | Change type | Requirement IDs preserved or changed | Disposition | Old path and SHA-256 | New path and SHA-256 | Change summary or reason |
|---|---|---|---|---|---|---|---|
| [F-### or not applicable.] | [CHG-###.] | [Required repair / authorized enhancement / unapproved proposal / bounded investigation.] | [IDs.] | [applied / deferred / declined.] | [Path/hash; absent for new file.] | [Path/hash; absent for removed file.] | [Bounded result or reason.] |

**New canonical source manifest:**  
[Complete package-relative file-to-SHA-256 mapping, candidate identity, and a separate retained manifest path/hash reference. A manifest/receipt must not include its own self digest. Record missing identity values and reasons explicitly.]

**Resulting specification identity:**  
[Record this specification's stable ID, revision and path, and retain prior-revision references. Never include the containing document's own complete-byte digest. In managed operation the runtime binds final bytes in its external receipt after saving; absent runtime observations stay null with a reason. A standalone authoring record may reference a different, already completed specification.]

**Preserved behavior and requirements:**  
[Requirements and unrelated source behavior retained, including settled enforcement classifications and invocation policy.]

**Derivations and generated-copy work remaining:**  
[Package-local derivation changes; canonical-to-installed/export mapping; integration owner action required. Do not treat installed copies as authoring sources.]

**Deferred proposals, gaps, and evaluation prerequisites:**  
[Remaining items with reasons/owners. Missing evidence or unsupported enforcement stays explicit.]

**Finding status — when applicable:**  
Source changes recorded; reevaluation required.

**Validation status:**  
Not performed.

**Hook status:**  
[Design only / not applicable.]

**Next handoff:**  
[At authoring completion, transfer or recovery, populate assets/handoff.md with the allocated next owner and prerequisites. Distinguish prepared document, admitted runtime transition and actual receiving-skill invocation. Route adapter gaps to integration. No validation is launched; old results do not transfer to changed bytes.]
