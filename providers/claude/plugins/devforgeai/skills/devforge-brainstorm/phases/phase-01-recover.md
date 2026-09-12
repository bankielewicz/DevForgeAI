# Phase 01: Recover

**Classification:** A runtime phase. [`references/managed-runtime.md`](../references/managed-runtime.md) names `Recover` as the first of the four phases a managed session can admit, with its own checkpoint fields; the skill-authoring contract classifies no brainstorm phase, so nothing here is labelled Enforced. **Applies:** always, first, managed or not.

## Purpose

Find out what already exists before adding to it, and preserve the bytes you are about to replace. Everything downstream reads this ledger as the origin of intent, so an alternative lost here is lost for good.

## Needed inputs

The user's request. The selected ledger destination, if one was selected - `SKILL.md`, *Where the artifacts go*, settles which applies. Any `change-request` the user is pointing you at. Nothing here requires the DevForgeAI repository to be present.

## Substantive work

Look for an existing ledger before creating one: at the selected ledger destination when one was selected, otherwise `docs/devforge/ideas/` by default, or whatever artifact map the project has adopted (check `CLAUDE.md`, `AGENTS.md`, or an existing `docs/devforge/` tree). Read it if found. Also read a `change-request` if the user is pointing you at one. Reading it tells you what is out there; it does not tell you what to do with it. An `accepted` status on a change request is a decision recorded in that document's own process, about that document - it is not the user adopting it into this ledger, and it is not by itself your authorization to act. What you do with it is settled by what the user has actually authorized: in this request, or in an earlier instruction of theirs that still stands and covers this change.

Revise the existing ledger as a new revision rather than starting a parallel one. Losing the earlier alternatives is the specific harm this skill exists to prevent.

Before you overwrite it, keep the bytes you are replacing. A `supersedes` entry naming revision 1 and its digest is only true while those bytes are still reachable, and the path you are about to write is precisely where they will stop being reachable - the reference would then resolve to revision 2 at the digest of revision 1. So copy the current file somewhere stable and authorized first: the project's own archive convention if it has one, otherwise a sibling like `IDEAS-001.r1.md` next to the ledger. Verify the copy's digest against what you are about to cite, and point the reference at the copy's path, not at the live one. If you cannot preserve them - the archive location is not yours to write, or the earlier bytes were already gone when you arrived - record that in `missing_inputs` and cite only what actually exists. A digest with no reachable bytes behind it is a claim the next reader cannot check.

## When the upstream has moved on

Discovering that an upstream you cite has been superseded is a finding about context. Two separate things follow, and running them together is how a ledger quietly gains a commitment nobody made:

- **Repairing your reference** is mechanical. If the revision your ledger cites is archived somewhere reachable, find it, check that it hashes to the digest you cite, and point the locator at the archive. That fixes a broken path. It changes nothing about what has been adopted.
- **Adopting the newer revision** is a decision, and it needs what every decision needs: actual authorization from the user that covers this change. That can be the user asking in this request - or a standing instruction they recorded earlier and have not withdrawn, whose scope reaches this change. A delegation is real authority. Asking again for permission the user already gave, in writing, is its own failure: it hands work back to someone who did the deciding precisely so they would not have to be present for it.

  What cannot stand in for authorization: finding the old bytes, the newer document's `accepted` status, or its own `decision_ref` - that field records a decision made about that document, not the user's adoption of it here. So read the authorization you are relying on and check it actually covers *this* change, at this scope, for this artifact. A delegation about IDEA-001's scope says nothing about IDEA-002 or a stack choice, and one that has been withdrawn or expired says nothing at all.

  When you do act on a prior authorization, cite it as the authority - which record, its revision, and the scope it grants - and keep that separate from the change request whose content you applied. Authority and source are two different facts about the same act, and a reader who cannot see both cannot tell an authorized update from an invented one. Do not write it up as though the user said it fresh in this conversation; they did not, and the record should say what actually happened.

So when the task in front of you is "add an idea", add the idea. Record the newer revision as observed context: name it, state its scope, and flag exactly which of your recorded decisions it would affect and why - in your open questions, and in the handoff's continuation as the next thing worth the user's attention. The adopted decision stays standing, at the strength the user gave it, with its own basis intact.

What this rules out is the tempting version: supersede the adopted decision, write the newer scope into the idea rows, advance `decision_ref` to the newer document's date, and tell the user to say so if they disagree. That is adoption with an undo button. It puts the user in the position of having to notice and reverse a commitment they never made, which is exactly the silent promotion this skill exists to prevent. Surfacing the conflict is genuinely useful. Resolving it on their behalf is not yours to do.

None of which makes an adopted input unusable or requires re-approval of decisions that have not changed. A decision the user already made stays good for what it already covers, and so does an instruction they left standing. If the task really is "bring the ledger up to the new change request", or the user told you last week to keep doing exactly that, then that *is* the authorization and you do it - recording which one you relied on. The question is only ever whether real authorization covers this change, never whether you can construct a reason the user would probably approve.

## Produced outputs

What you know before you explore: the existing ledger and its identity and revision if one was found, the preserved bytes and their verified digest if you replaced any, the change request you were pointed at and what it does and does not authorize, and the inputs you could not resolve. In a managed session these are the `known_ideas`, `known_decisions` and `missing_inputs` of the Recover checkpoint; unmanaged, they are what you carry into Explore and what the ledger's `missing_inputs` will say.

## Next phase

Continue to [phase 02, Explore](phase-02-explore.md). A routed handoff-only task skips Explore and Record and goes straight to [phase 04, Focus](phase-04-focus.md) - that routing is the task owner's selection, never a mode to move into to get past a gate.

Stop and hand back instead if the selected ledger destination is unwritable, already holds someone else's artifact, or falls outside a fence you were given, or if the earlier bytes you must preserve are not yours to write. Report the condition rather than writing somewhere else, save that record where you were authorized to save it, and continue to [phase 06](phase-06-completion-summary.md) with a blocked outcome. Discussion can continue; the dependent write does not.
