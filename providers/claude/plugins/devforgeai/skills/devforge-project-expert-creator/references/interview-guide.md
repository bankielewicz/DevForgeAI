# Interview guide

These are prompts for filling material gaps, not a questionnaire to read out. Ask one to three related questions per round, and only where the answer changes the design.

## Recover before you ask

Read the current request, the accepted working specification, the source and assignment identity, and any repair handoff first. Record the governing framework, provider and contract, and the canonical-to-installed mapping - [framework context](framework-context.md) covers how those resolve. Do not ask a user to reconstruct a fact that is already in the supplied sources; that spends the attention you will need for the decisions only they can make.

When resuming, continue the same specification document. Revisit a settled answer only when the user changes it, or when identified evidence materially conflicts with it - and then record which requirement IDs are affected and why. A newer checkout, template or library release does not by itself authorise replacing an accepted input.

For a repair from an evaluator, use [validator handoff](validator-handoff.md). Ask about an unapproved proposal or a genuinely new scope decision. Do not ask whether to repeat a repair that was already authorised, and do not turn a missing native observation into an invented source defect.

## Start from a concrete case

Establish the work that needs to be repeatable and what the finished result looks like. One typical request and one expected output are usually enough to begin discovery.

- What task should this expertise complete, and what would you normally hand it?
- What should the finished result look like, and how would you know it was wrong?
- Which current behaviour needs to change?

Do not demand another example when the task is already clear. Propose a concrete interpretation and ask only about the uncertain parts.

## Questions that map to the specification

| Section | What to establish | Useful follow-up |
| --- | --- | --- |
| Identity and purpose | The task, the benefit, the discovery description, who uses it | What does this project know that a competent generalist would get wrong here? |
| Scope and activation | Activating requests, boundaries, nearby exclusions | Which related work belongs to a different skill? |
| Inputs and results | Required inputs, missing-input behaviour, deliverable, format, completion criteria | Can it proceed when this input is missing, or must it stop? |
| Workflow | Stable workflow, phase and task IDs, decisions, dependencies | What changes the path, and what has to wait? |
| Task-specific rules | Requirements versus preferences; the real authorisation boundary | Which decisions are fixed, and which may the worker make alone? |
| Tools and resources | Actual runtime and version, available integrations, fallbacks | Which of these are actually available in the consuming project? |
| Acceptance cases | Representative cases and expected behaviour, captured only | Which observable result would show the requirement was met? |
| Placement and maintenance | Provider, canonical source, installation destination, owner | Who owns the durable source and the installation mapping? |
| Authoring decision | Search scope, candidates, gaps, reuse/enhance/create rationale | Does an existing workflow already own this change? |
| Framework authority | Selected contract and specification bytes, assignment, source identities, gaps | Which conflicting source, if any, needs an owner's decision? |
| Repair intake | Frozen inputs, finding and change IDs, permitted changes, retained requirements | Is this a required repair, an authorised enhancement, a proposal, or an investigation? |

Derive routine details such as a proposed skill name and its discovery description rather than asking. Keep a proposed default visibly distinct from a user requirement. Never request a credential or secret value.

## The expert specification's content checklist

The expert specification is written before the expert. These are the contracts it has to state, whatever the eventual shape of the document:

| Contract | Required content |
| --- | --- |
| Responsibility | The outcome this capability owns, and the limits of that responsibility. |
| Activation | Requests that require it and nearby requests that do not. |
| Knowledge | Approved architecture, selected dependencies, exact API references, and the questions still open. |
| Inputs | Task packet, source locations, acceptance conditions, required tools. |
| Decisions | What the worker may decide, and what needs a project amendment. |
| Output | Reviewable deliverables, evidence, and the handoff. |
| Evaluation | Realistic positive, negative, ambiguous and unrelated cases, with independently stated expectations. |
| Refresh | The changes that invalidate this knowledge or its evaluation. |

Keep AI proposals separate from user decisions throughout. Record sources and uncertainty instead of filling a gap with an assumed organisational convention. `assets/expert-spec.md` is the template that carries these into the framework envelope, and `assets/evaluation-cases.md` is the starting set for the Evaluation row.

## Recording an enforcement requirement

Give meaningful workflows, phases and tasks stable IDs and parent relationships. Do not enumerate every internal model action; decompose only the items a person would recognise as a step.

For a genuinely new, unclassified item, ask:

> Should [item] be optional, or should its completion be required before [dependent action]?

Record the answer, what it applies to, the dependent action, and any permitted skip. An explicit answer for a named group covers its named members; a parent's classification does not automatically classify its children. Retain those answers across revisions and repairs, and ask again only for a new item or a material conflict.

Two things this recording is not. It is not a claim that anything enforces the requirement - the classification is design input, and a check that actually blocks a dependent action is compiled into the DevForge CLI and wired by the integration owner. And it is not a licence to write enforcement theatre into the skill you are authoring: no phase acknowledgements, no self-issued PASS, no simulated gate sequence.

So for each required item, record the observable evidence that would show completion, where that evidence lives, who writes it, and when it goes stale - then route the requirement to the integration owner and mark its feasibility unknown until that owner confirms it. Keep an unmet enforcement requirement visible rather than quietly downgrading it to advisory prose. For a subjective requirement, distinguish a concrete evidence or human-decision condition from proof that the whole task was done well.

Continue independent work while a classification answer is pending. Do not invent the answer and do not finalise the dependent part of the design without it.

## Keeping the working document useful

After each material round, save the accepted requirements, source references, proposals, open questions and the selection rationale. Preserve stable IDs when wording changes, so later findings and change records stay traceable.

Leave an unanswered decision open and keep working on what does not depend on it. When a gap blocks a specific change, record that status and ask the focused question; do not mark that part complete.

## When to stop interviewing

You have enough when you have: the task and activation boundary, the inputs, the output, the core process and its branches, the material constraints, the existing-skill decision, the canonical destination and assignment, and a classification for every proposed workflow item.

An authorisation to build plus the settled relevant decisions is enough to proceed. Do not add an approval ceremony, and do not let optional references, maintenance details or extra examples block an otherwise sufficient design. Document unavailable contract or source information and any enforcement limitation truthfully - capturing acceptance cases is not authorisation to run them.
