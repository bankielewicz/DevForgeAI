# Phase 03: Record

**Classification:** A runtime phase. [`references/managed-runtime.md`](../references/managed-runtime.md) names `Record` as the third of the four phases, with its own checkpoint field; the skill-authoring contract classifies no brainstorm phase, so nothing here is labelled Enforced. **Applies:** on the ordinary path. `NOT_APPLICABLE` on an externally selected handoff-only task, which produces no ledger.

## Purpose

Write down what was actually said, in a form that still distinguishes the user's words from your proposals when someone comes back to it next week.

## Needed inputs

What [phase 02](phase-02-explore.md) explored, and the preserved bytes and identities from [phase 01](phase-01-recover.md). The ledger destination and, where a contract selected them, the ledger's artifact ID, revision and required sections - `SKILL.md`, *Where the artifacts go*, settles which applies.

## Substantive work

Write the ledger from [`../assets/idea-ledger.md`](../assets/idea-ledger.md). The columns exist for specific reasons:

- **Origin** is `user`, `AI proposal`, or a reference to actual evidence. When you summarize the user rather than quoting them, it is still theirs - but keep the summary faithful and keep the uncertainty they expressed.
- **State** is `proposed` until the user adopts it - in their own words here, or under an earlier instruction of theirs whose scope covers it. A decision row's `decision_ref` stays `null` until then, and the frontmatter `decision_ref` stays `null` while no adoption exists. When the adoption rests on a standing instruction rather than something said in this conversation, `decision_ref` names that record, so a later reader can see the actual basis instead of inferring a conversation that never happened. Enthusiasm is not adoption; "yeah that sounds right" about a specific statement is.
- **Related idea IDs** carry splits and merges. When two ideas merge, the new idea links to both origins and the originals stay in the table rather than being deleted. The user needs to be able to walk backwards.
- **Assumptions and open questions** are where uncertainty lives instead of being smoothed away. Each one gets a consequence and the smallest observation that would settle it.

Idea IDs are stable and never reused. A superseded idea keeps its ID and its row.

Read [`../references/recording-rules.md`](../references/recording-rules.md) as you write the frontmatter, and whenever one of its situations comes up - no session record exists, someone else is named as the writer, an upstream no longer matches the revision you referenced, or a check could not run.

## Produced outputs

The ledger, saved at its selected destination under its selected identity - or, where nothing was selected, at the project's artifact map under the next unused number. In a managed session the Record checkpoint's `ledger_path` is that destination, and it is where the runtime reads the bytes: a checkpoint naming the selected path while the file was written somewhere else is a true-looking record of a missing artifact.

A required field still holding a placeholder means the result is a draft and cannot be presented as ready. A missing fact goes in `missing_inputs`, never into template filler.

## Next phase

Continue to [phase 04, Focus](phase-04-focus.md). The ledger's bytes are finished here, but its digest is computed in the order [phase 05](phase-05-readback.md) sets out - hash after the last edit, not before.

Stop and hand back instead if the selected destination is unwritable, holds another owner's artifact, or its selected identity is absent or conflicts with what is already there. That is a dependent blocker: report what you found, where, and what you would need, save that record where you were authorized to save it, read it back at [phase 05](phase-05-readback.md), then continue to [phase 06](phase-06-completion-summary.md). A substitute ID, revision or path is no more yours to choose than the other.
