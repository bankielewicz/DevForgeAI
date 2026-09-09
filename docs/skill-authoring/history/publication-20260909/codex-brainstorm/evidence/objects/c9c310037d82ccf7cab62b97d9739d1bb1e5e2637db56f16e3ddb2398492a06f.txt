# Skill Design Specification

Fill in the placeholders below. Optional sections can be removed when they don't apply.

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

During the design conversation, ask the user for each unclassified item: "Should [item] be optional, or should its completion be enforced before [dependent action]?" Ask small groups of related questions and record the answers. Reuse answers already supplied; do not repeatedly request the same decision.

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
[Specify a location if required; otherwise leave for implementation.]

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
