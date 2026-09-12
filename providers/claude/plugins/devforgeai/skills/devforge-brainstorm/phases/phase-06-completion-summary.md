# Phase 06: Completion summary

**Classification:** `PROPOSED - not adopted`, and a package-local step rather than a runtime phase. The skill-authoring contract classifies no brainstorm phase, and [`references/managed-runtime.md`](../references/managed-runtime.md) names exactly four - Recover, Explore, Record, Focus - so `06` is never a checkpoint `phase` value. See [phase mapping](../references/phase-mapping.md) for the proposal put to the contract's owner. Nothing in this package implements, activates or proposes a runtime check for this step.

**Applies:** always, and it is the only finish. Every route arrives here - an ordinary ledger-plus-handoff run, a routed handoff-only task, a partial result, or a blocked one.

## Purpose

Separate what is presented from what is retained. The detailed record is saved and read back; the terminal response is short enough to be read.

## Needed inputs

The saved artifacts and their read-back paths and digests from [phase 05](phase-05-readback.md); or, when nothing was written, the blocked record from whichever phase stopped.

## Substantive work

The detailed record for this route is already saved and read back. Do not restate it. Print a short terminal summary carrying exactly these:

1. The actual outcome, as one of the outcome words - draft-ready, completed, partial or blocked. A genuinely blocking question is not one of them: that pauses in the phase you were in and does not reach this step. These are outcome words, not the result-status vocabulary (`NOT_RUN`, `COULD_NOT_RUN`, `NOT_APPLICABLE`, `NOT_EVALUATED`); do not substitute one set for the other. Never a status the evidence does not support.
2. One sentence saying what is now useful that was not before.
3. Links to the ledger and to the handoff, as paths that resolve for the reader.
4. **What is newly proposed versus what the user actually adopted, and what remains open.** This one is not optional and not a slot to omit: it is the whole point of the ledger, and a summary that lets a proposal read as a decision has committed the failure this skill exists to prevent. If nothing was adopted, say nothing was adopted.
5. The material blocker, if there is one. If there is not, say nothing rather than filling the slot.
6. One next action and its owner.

Be exact about what was and was not checked, in one sentence. If no runtime verified these artifacts, they are unverified drafts and the summary says so, with completion and any receipt at `NOT_RUN`. Do not announce a receipt and do not write one; where a runtime published one, it returns the locator and digest itself.

[`../assets/completion-summary.md`](../assets/completion-summary.md) is the template, with a worked example for each outcome. Aim for 60 to 120 words where that is practical. The count is a target for a summary that is padding itself, never a reason to drop a failure, a blocker, an unadopted proposal or an unobserved result: if honesty needs more words, use more words.

By default the terminal response carries no file inventories, no digest tables, no research narrative, no verification matrix and no run bookkeeping. Those belong in the saved artifacts, where they stay retrievable. When a receipt has to leave this session, that is the runtime's to publish through its own route.

Write the summary yourself from what you already have. Do not spend another model call, another agent or another tool run solely to format it.

## Produced outputs

The terminal summary only. It is presentation, not an artifact: it has no envelope, no identity and no digest, it is not a checkpoint, and it adds nothing to the saved record.

## Next phase

None. This is the end of the workflow; `SKILL.md` states the stopping condition.
