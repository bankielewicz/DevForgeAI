# Phase 06: Completion summary

**Classification:** `PROPOSED - not adopted.` The skill-authoring contract classifies five creator phases and does not classify a sixth; only the contract's owner can classify this one. See [phase mapping](../references/phase-mapping.md) for the proposal and the two options put to that owner. Nothing in this package implements, activates or proposes a runtime check for this phase.

**Applies:** always, and it is the only finish. Every path arrives here - a completed candidate, a reuse recommendation, a partial result, or a blocked one.

## Purpose

Separate what is presented from what is retained. The detailed record is saved; the terminal response is short enough to be read.

## Needed inputs

The saved outputs and their read-back paths and digests from [phase 05](phase-05-prepared-transfer.md); or, when no candidate was authored, the reuse recommendation from [phase 02](phase-02-selection.md) or the blocked record from whichever phase stopped.

## Substantive work

The detailed record for this route is already saved and read back - the package record and handoff from phase 05, or the reuse recommendation or blocked record from the phase that stopped. Do not restate them. Print a short terminal summary carrying exactly these:

1. The actual outcome, as one of the outcome words - draft-ready, completed, partial, blocked, or a reuse recommendation. These are outcome words, not the result-status vocabulary in `SKILL.md`; do not substitute one set for the other. Never a status the evidence does not support.
2. One sentence saying what is now useful that was not before.
3. Links to the primary artifact and to the handoff or report, as paths that resolve for the reader.
4. The material decision or blocker, if there is one. If there is not, say nothing rather than filling the slot.
5. One next action and its owner.

[assets/completion-summary.md](../assets/completion-summary.md) is the template, with a worked example for each of the four outcomes. Aim for 60 to 120 words where that is practical. The count is a target for a summary that is padding itself, never a reason to drop a failure, a blocker or an unobserved result: if honesty needs more words, use more words.

By default the terminal response carries no file inventories, no digest tables, no research narrative, no verification matrix and no run bookkeeping. Those belong in the saved artifacts, where they stay retrievable. When a receipt has to leave this session, use the existing permitted evidence or outbox route rather than pasting the inventory into the summary.

Write the summary yourself from what you already have. Do not spend another model call, another agent or another tool run solely to format it.

## Produced outputs

The terminal summary only. It is presentation, not an artifact: it has no envelope, no identity and no digest, and it adds nothing to the saved record.

## Next phase

None. This is the end of the workflow; `SKILL.md` states the stopping condition.
