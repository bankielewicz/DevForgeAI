---
name: skill-builder
description: "Design, create, or enhance Codex skills through user Q&A, an existing-skill search, and a populated specification. Use when a user wants a reusable workflow developed or changed. Includes optional/enforced step choices and hook proposals; excludes skill testing and validation."
---

# Skill Builder

Turn a user's workflow idea into a completed design specification and either a new skill or a focused enhancement. Reuse an existing skill when it already meets the need.

This MVP authors instructions and supporting resources. It does not run the generated skill, helper scripts, tests, validators, linters, or evaluations, directly or through another agent. Record expected behavior for a separate validation workflow. Hook work ends at a design proposal: do not install, activate, or execute hooks, edit active hook configuration, or claim enforcement is active. A target skill may itself perform testing or validation if that is the user's requested task.

## Start from the user's intent

Use the conversation and supplied materials before asking questions. Establish the intended workflow, a typical request, the result, and the target environment. If the user names an existing skill or supplies a draft specification, start there.

Distinguish a design-only request from authorization to create or enhance files. For an authoring request, continue through authoring once the necessary decisions are settled; do not add a blanket approval checkpoint. Ask only for unresolved choices that materially affect the work. Honor any approval or scope boundary the user actually sets.

Read [the interview guide](references/interview-guide.md) when developing requirements and [the selection guide](references/existing-skill-selection.md) when comparing candidates. Resolve these paths relative to this skill directory.

## Find a suitable existing skill

Search before deciding to create. Use the target environment's available skill catalog and relevant accessible project, user, and installed-plugin locations. Read candidate names and descriptions first, then inspect the instructions of plausible matches. Do not execute candidates.

Compare the requested target workflow's purpose, activating requests, scope, inputs, outputs, and core process. Shared names, roles, or tools alone do not establish duplication. Record the searched locations, candidates, gaps, and recommendation.

Choose reuse when a candidate already meets the need; enhancement when the same workflow can absorb the requested change coherently; creation when no suitable candidate exists or the workflow has a distinct boundary. Explain ambiguous choices and resolve the target through the interview. Do not silently edit installed caches or invent a global claim that no duplicate exists.

Repeat only the relevant comparison if the requested scope changes. Before writing, account for any existing file at the selected target.

## Build the specification through Q&A

Use a user-specified template when supplied; otherwise copy [the bundled specification template](assets/skill-design-specification-template.md). Never fill in the blank source template in place.

Save a working specification in the user's chosen location, an established project documentation location, or a proposed workspace document path. Keep design documents outside the installed skill's instruction files unless they are needed at runtime. Reuse the same working document across turns.

Ask one to three focused, related questions at a time. Propose concrete interpretations and defaults when helpful. Capture answers after each round; distinguish user requirements, proposed defaults, and open decisions. Do not silently turn unanswered questions into agreement.

Populate the eight design sections and the authoring record. Collect completion criteria and representative cases as requirements only; do not execute them. Optional information can be omitted or marked not applicable. Preserve important unresolved decisions as open rather than pretending the specification is complete.

## Classify workflows, phases, and tasks

Name meaningful workflow items and assign stable IDs and parent relationships. For every unclassified item, ask:

"Should [item] be optional, or should its completion be enforced before [dependent action]?"

Record Optional or Enforced, the circumstances where it applies, and any permitted skip condition. Reuse answers already supplied. A parent classification does not automatically apply to its children. The user may explicitly classify a named group together; record exceptions individually.

Treat Optional/Enforced as the user's requirement, not a claim about implemented runtime behavior. While an answer is pending, continue independent discovery or draft work, but do not invent the classification or finalize the dependent design.

## Propose hooks for enforced items

For every enforced item, fill the hook-proposal fields in the specification. A shared proposal may cover several items if each requirement remains traceable.

Identify the protected action, target runtime, supported event and matcher, observable evidence, state ownership and freshness, allow/block behavior, error behavior, recovery, permitted exceptions, configuration requirements, and coverage gaps. Separate intended failure behavior from what the runtime actually supports.

Consult current [official Codex hook documentation](https://learn.chatgpt.com/docs/hooks) for the target runtime. If documentation or runtime information is unavailable, record the unknowns rather than inventing an event or guarantee. A reminder or self-reported completion marker is not proof that a substantive phase occurred.

Mark feasibility Supported, Partial, Unsupported, or Unknown based on documented capability, and always mark the proposal itself "Design only; not installed, activated, executed, or validated." For incomplete coverage, retain the enforcement requirement and discuss a feasible alternative; never silently downgrade it to an instruction.

Keep any illustrative hook configuration inside the design document. Do not create executable hook files or active configuration as part of this MVP.

## Author or enhance

Proceed when the task boundary, necessary inputs, deliverable, essential process, material constraints, target destination, selection decision, and item classifications are settled. Do not wait for irrelevant optional details. Outstanding hook capability gaps may remain documented in a proposal, but must not be represented as delivered enforcement.

Use the current environment's skill-creator authoring guidance when available. Pass along the settled specification and the no-validation boundary. Reuse its authoring helpers only when useful; do not run its validation or forward-testing steps or delegate those steps to another agent. If it is unavailable, author directly from the specification and current skill-format requirements.

For a new skill, write a folder with SKILL.md containing YAML name and description and a focused Markdown body. Use a concise lowercase, hyphenated name. Put discovery triggers in the description, essential instructions in the body, and substantial conditional detail in references. Add scripts, assets, or metadata only when the actual workflow needs them. Keep normal automatic selection unless the user requests explicit-only invocation.

Respect the chosen installation scope. For project use, prefer .agents/skills/<name> under the chosen project. For personal use, resolve the appropriate skill location in the actual runtime rather than assuming Windows and WSL share it. Do not package or publish a plugin or change global settings unless that work is requested.

For an enhancement, edit the selected durable source and preserve unrelated instructions, resources, dependencies, names, and invocation policy. Describe the existing behavior being retained and the intended change. Do not reinitialize an existing skill.

Any generated supporting scripts remain unexecuted and unvalidated. Do not install dependencies or use external services merely to try out the authored output. Reading source material and confirming that requested file writes succeeded are authoring operations, not evidence of functional validation.

## Deliver and stop

Return links to the completed specification and authored or changed files, the reuse/enhancement/creation decision with search limits, and any material open dependencies or enforcement gaps. For reuse, link the existing skill and explain why no new skill was needed.

Report "Validation status: Not performed." When hooks are proposed, also report "Hook status: Design only." Do not describe the output as tested, validated, production-ready, or actively enforced. Finish after authoring; do not launch an evaluation or the target workflow.
