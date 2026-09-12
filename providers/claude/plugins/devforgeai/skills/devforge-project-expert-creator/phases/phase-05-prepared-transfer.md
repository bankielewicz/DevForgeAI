# Phase 05: Prepared transfer

**Classification:** Enforced, per the skill-authoring contract. **Applies:** whenever a candidate was authored or enhanced.

## Purpose

Record the candidate's identity and prepare the transfer to the next owner, so the detailed evidence exists and is retrievable before anything is summarised.

## Needed inputs

The candidate and its file list from [phase 04](phase-04-authoring.md), the working design document and specification from [phase 03](phase-03-design.md), and the assigned durable artifact location.

## Substantive work

Record the candidate's identity - the package file manifest, the specification identity, the working design document you filled in design, what changed and why - using [assets/expert-package.md](../assets/expert-package.md) for the package record. Then write the handoff from [assets/handoff.md](../assets/handoff.md).

Keep the handoff short enough to read: the result, the one decision that affects what happens next, the real limits, the next owner and the next action, and a reading order into the detailed records. The specification and package record hold the inventories; do not copy them into the handoff. No document carries its own digest - hash each output after its bytes are final, put those digests in the handoff, and never put the handoff's own digest inside itself.

The next owner is an independent evaluator. State plainly: **Validation status: Not performed.** Behavioural status is `NOT_EVALUATED` until someone records an actual evaluation. Structural binding, if an operator ran it, is a separate fact that says which bytes were referenced and nothing about whether the skill is any good.

Give one copyable next task that names something that actually exists. Check what is installed before naming it: much of the DevForge roster is specified but not implemented, and `devforge-evaluate-expert` may not be installed in this environment. If it is absent, say so as a capability gap and give a task the user can actually act on - a plain-language evaluation task with resolvable paths is a real next step; a slash command for a skill you have not confirmed is not. Keep three things separate in what you write and what you say: what you suggest, what is installed, and what you actually invoked.

Preparing a handoff is not invoking the receiver. See [manual operation](../references/manual-operation.md) for who owns which command and what each one actually proves.

## Produced outputs

The saved package record, the saved handoff, and the final digests of every completed output - written to the assigned durable location and read back, so that the next phase can point at paths that exist rather than paths you intended.

## Next phase

Continue to [phase 06, completion summary](phase-06-completion-summary.md). Do not summarise before the records are saved and read back; an unsaved artifact is not evidence, and a summary that links to it is wrong.
