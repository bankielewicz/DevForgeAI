# Phase 01: Intake

**Classification:** Enforced, per the skill-authoring contract. **Applies:** always; this is where every request starts, including a repair.

## Purpose

Establish what is actually being asked for, which kind of target it is, and what the supplied sources already answer - before spending any of the user's attention on questions.

## Needed inputs

The required-input rows named in `SKILL.md`: the concrete story, task, goal or accepted requirement; the grounding set for the target kind you identified; the existing expertise map and any existing package; the write fence, provider and destination. For a repair, the evaluator report or change request row as well.

Nothing here requires the DevForgeAI repository to be present.

## Substantive work

Recover before you ask. The request, the goal, the accepted decisions, the sources that will be touched, the write fence and the provider are usually already in the conversation or in the supplied material. Asking the user to restate them spends the attention you will need later for the decisions only they can make.

Decide the target kind explicitly and record it, because it decides which grounding is required:

- **Project expert.** Ground it in the actual project: the story, the accepted architecture and decisions, the pinned dependencies, and the real source the work will touch. When the operator has supplied a policy file and the DevForge CLI, `devforge expert prepare --project <abs-project> --policy <abs-policy>` returns the project's grounding context. Use the paths the owner gave you. Do not go looking for a more permissive policy, and do not edit a policy or a gate so that a candidate will pass - a gate that rejects your work is telling you something; report it to its owner instead.
- **Framework workflow skill.** Ground it in the accepted framework requirements, the governing contracts, the provider's documented conventions, and the capabilities that actually exist in the target client. A framework skill does not need a production application, a deployed service, or an application architecture document, and demanding one before refactoring a framework skill is a defect in the intake, not a missing input. `devforge expert prepare` is a project-expertise command and does not apply here; say so rather than recording a blocked step.

Record what you actually found: source paths, revisions or preserved-byte digests, the specification and template identities you are working from, and every input you could not resolve. If the project is new and the required decisions do not exist yet, draft them and put them in front of the user as drafts. Missing approval is not implied approval.

## When the input is an evaluator's findings

A repair starts from the frozen handoff and its named evidence, not from a fresh interview. [Validator handoff](../references/validator-handoff.md) covers recovering the frozen baseline, comparing current bytes against the supplied manifest before editing, keeping severities and finding IDs exactly as supplied, and classifying each requested change as a required repair, an authorised enhancement, an unapproved proposal, or a bounded investigation.

Two things that look like permission and are not. A severity label is not authority to change a specification, weaken an expectation or drop a case. And a missing observation - no discovery evidence, no installed-resource check, an evaluation that could not run - is an evaluation prerequisite, not a defect in the skill; it does not justify editing the candidate to make the gap go away.

## Produced outputs

An intake record: the target kind and why; the recovered sources with their identities; the unresolved inputs and what each blocks; for a repair, the frozen baseline identities, the finding and change IDs, and any drift observed against the supplied manifest.

## Next phase

Continue to [phase 02, selection](phase-02-selection.md). A repair carries its frozen target and the prior selection decision into phase 02 rather than repeating the inventory.

Stop and hand back instead if the write fence, the provider or the destination is contested or unknown, or if a required approval does not exist; report what is blocked and who owns it, save that record to the assigned durable location and read it back, then continue to [phase 06](phase-06-completion-summary.md) with a blocked outcome.
