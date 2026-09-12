# Phase 02: Explore

**Classification:** A runtime phase. [`references/managed-runtime.md`](../references/managed-runtime.md) names `Explore` as the second of the four phases, with its own checkpoint fields; the skill-authoring contract classifies no brainstorm phase, so nothing here is labelled Enforced. **Applies:** on the ordinary path. `NOT_APPLICABLE` on an externally selected handoff-only task.

## Purpose

Help the user think. The ledger exists to serve the thinking, not the reverse - so this phase is a conversation, and what it produces is the material the ledger will honestly hold.

## Needed inputs

What [phase 01](phase-01-recover.md) recovered: the existing ledger and its open questions if there was one, the decisions already standing, and the inputs that stayed missing.

## Substantive work

Draw out, in whatever order the conversation actually goes: the problem, who is affected, what a good outcome looks like, what alternatives exist, and what is genuinely uncertain.

Ask when the answer would change direction. If the user has given you almost nothing ("I want to build something"), ask one concrete, useful question and wait - do not populate a ledger with a plausible-sounding user and problem to have something to show. An empty field the user can fill is more valuable than a filled field they have to notice and correct.

Research is optional and only for factual claims that matter. When you do, record the URL, retrieval date, and the specific claim supported; that goes in `evidence`, and it stays distinguishable from inference.

Do not select a stack yourself. Naming a technology as an illustration is fine; turning it into a choice is not - that belongs to a later architecture phase, and it needs a product brief first.

When the *user* has already stated a technology decision or preference, that is different: record it, with `user` origin and its actual scope. "It has to run offline on iOS" and "I'd probably reach for Postgres, but I'm not attached" are both theirs and neither is yours, but they are not the same commitment. Keep them at the strength the user gave them - do not widen a preference into a decision, do not soften a decision into a preference, and do not drop a real constraint on the grounds that architecture comes later. A later phase revisits what the user decided; it does not make the decision unrecordable now.

## Produced outputs

The material Record will write down: the ideas with their people, problem, outcome, alternatives and open questions, each attributable to the user, to an AI proposal, or to cited evidence - and the unknowns that stayed unknown. In a managed session this is the Explore checkpoint's `ideas` list and `missing_inputs`. A `people`, `problem` or `outcome` you genuinely do not know is `null` paired with a real open question; inventing a plausible user to fill a field is the failure this skill is built against, and no checkpoint shape changes that.

## Next phase

Continue to [phase 03, Record](phase-03-record.md).

Stop and hand back instead if something other than a question blocks the work - a write fence or a destination that turns out not to be yours, an authorization that does not cover what the conversation has moved on to. Report what is blocked and who owns it, save that record where you were authorized to save it, read it back at [phase 05](phase-05-readback.md), and continue to [phase 06](phase-06-completion-summary.md) with a blocked outcome.

Stop and wait instead when a question genuinely blocks - ask it and, in a managed session, write the `awaiting_user` checkpoint form that [`references/managed-runtime.md`](../references/managed-runtime.md) describes. Waiting is not a result: the user's next message resumes this phase. An unknown you can work around is not a blocker; it stays in `missing_inputs` and in the open questions, and exploration continues.
