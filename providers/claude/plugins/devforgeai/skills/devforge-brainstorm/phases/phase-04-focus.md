# Phase 04: Focus

**Classification:** A runtime phase. [`references/managed-runtime.md`](../references/managed-runtime.md) names `Focus` as the fourth and last of the four phases, with its own checkpoint fields; the skill-authoring contract classifies no brainstorm phase, so nothing here is labelled Enforced. **Applies:** always, including a routed handoff-only task and a blocked or partial result.

## Purpose

Close on one thing worth doing next, and leave a handoff that names what actually exists.

## Needed inputs

The ledger written in [phase 03](phase-03-record.md) and its selected identity - or, on a routed handoff-only task, the [phase 01](phase-01-recover.md) recovery alone, with Explore and Record `NOT_APPLICABLE`. The handoff destination, per `SKILL.md`, *Where the artifacts go*.

## Substantive work

Close on one concrete next step: the smallest discovery task or experiment that would resolve the most consequential open question, with its non-goals stated. If it needs a capability the project does not have, name that need - route a real capability gap to devforge-project-expert-creator, but do not manufacture an expert to fill an org chart.

Then write a handoff from [`../assets/handoff.md`](../assets/handoff.md) to the selected handoff destination - `docs/devforge/handoffs/` only when nothing was selected. *Where the artifacts go* in `SKILL.md` covers which applies and what to do when the selected path is not available.

The next-session prompt must name something that actually exists. Much of the DevForge roster is specified but not implemented, so check what is really installed before naming it rather than reading a name off the roster. At the time of writing, `devforge-define-product` and `devforge-change` are specified but absent, which matters because define-product is the ledger's usual consumer.

When the natural next step has no installed skill, say so as a capability gap: name the capability, say it is not installed, and give a next task the user can actually act on - authoring or evaluating that skill, or simply continuing in plain language. A gap reported honestly is a useful result. A gap papered over with a plausible skill name is not.

Keep three things separate, in the handoff and in what you tell the user: what you *suggest* as a continuation, what is *installed and available*, and what you *actually invoked*. Suggesting a skill is not evidence it exists, and its existence is not evidence you ran it. Never present a slash command or `devforge` subcommand you have not confirmed.

## Produced outputs

The handoff, saved at its selected destination, carrying the ledger's digest in its output row and - on the ordinary ledger-plus-handoff path - the `upstream` binding that [phase 05](phase-05-readback.md) specifies. In a managed session the Focus checkpoint carries `next_action`, `owner`, `completion_evidence`, `non_goals` and a `handoff_path` equal to that destination; on the ordinary path the runtime checks the handoff's `upstream` binding here, against the ledger bytes it just read.

A routed handoff-only task produces the handoff alone and carries no such binding, because it has no ledger. Mark an unproduced ledger as not produced with the reason; do not create one to fill a row.

## Next phase

Continue to [phase 05, read back and verify](phase-05-readback.md). Do not tell the user it is done until the writes and their references have been checked there.
