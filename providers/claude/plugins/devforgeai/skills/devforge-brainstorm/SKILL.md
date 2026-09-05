---
name: devforge-brainstorm
description: Explore an undeveloped or contested product idea with the user and keep it in a durable idea ledger that separates the user's own words from AI proposals, evidence, and actual decisions. Use this whenever someone is figuring out what to build, weighing several ideas, cannot decide which problem is worth solving, or says they want to build something without having named the problem, the people affected, or the outcome - even when they never say the word "brainstorm". Do not use it to implement an already-accepted story (that is devforge-develop) or to revise a decision that has already been adopted (that is devforge-change).
---

# Brainstorm and preserve ideas

The user is early. Your job is to help them think, and to leave behind a record they can come back to next week without having lost the alternatives they rejected or gained commitments they never made.

Two failure modes matter more than anything else here:

- **Fabrication.** Inventing a target user, a market size, or a technology choice the user never mentioned. An early ledger full of confident invention is worse than an empty one, because the user cannot tell which parts came from them.
- **Silent promotion.** Recording your own suggestion as the user's decision. Everything downstream (product scope, architecture, stories) reads this ledger as the origin of intent. A proposal that quietly becomes a decision here becomes a production constraint three skills later.

Keep the conversation useful. This is discovery, not compliance paperwork - the ledger exists to serve the thinking, not the reverse.

## 1. Recover what already exists

Look for an existing ledger before creating one: `docs/devforge/ideas/` by default, or whatever artifact map the project has adopted (check `CLAUDE.md`, `AGENTS.md`, or an existing `docs/devforge/` tree). Read it if found. Also read a `change-request` if the user is pointing you at one - but an accepted change gives you direction to revisit an idea, while a proposed one is still only a proposal.

Revise the existing ledger as a new revision rather than starting a parallel one. Losing the earlier alternatives is the specific harm this skill exists to prevent.

## 2. Explore

Draw out, in whatever order the conversation actually goes: the problem, who is affected, what a good outcome looks like, what alternatives exist, and what is genuinely uncertain.

Ask when the answer would change direction. If the user has given you almost nothing ("I want to build something"), ask one concrete, useful question and wait - do not populate a ledger with a plausible-sounding user and problem to have something to show. An empty field the user can fill is more valuable than a filled field they have to notice and correct.

Research is optional and only for factual claims that matter. When you do, record the URL, retrieval date, and the specific claim supported; that goes in `evidence`, and it stays distinguishable from inference.

Do not select a stack. Naming a technology as an illustration is fine; recording it as a choice is not - that decision belongs to devforge-architect and it needs a product brief first.

## 3. Record

Write the ledger from `assets/idea-ledger.md`. The columns exist for specific reasons:

- **Origin** is `user`, `AI proposal`, or a reference to actual evidence. When you summarize the user rather than quoting them, it is still theirs - but keep the summary faithful and keep the uncertainty they expressed.
- **State** is `proposed` until the user adopts it in their own words. A decision row's `decision_ref` stays `null` until then, and the frontmatter `decision_ref` stays `null` while no adoption exists. Enthusiasm is not adoption; "yeah that sounds right" about a specific statement is.
- **Related idea IDs** carry splits and merges. When two ideas merge, the new idea links to both origins and the originals stay in the table rather than being deleted. The user needs to be able to walk backwards.
- **Assumptions and open questions** are where uncertainty lives instead of being smoothed away. Each one gets a consequence and the smallest observation that would settle it.

Idea IDs are stable and never reused. A superseded idea keeps its ID and its row.

## 4. Focus

Close on one concrete next step: the smallest discovery task or experiment that would resolve the most consequential open question, with its non-goals stated. If it needs a capability the project does not have, name that need - route a real capability gap to devforge-project-expert-creator, but do not manufacture an expert to fill an org chart.

Then write a handoff from `assets/handoff.md` into `docs/devforge/handoffs/`.

The handoff's next-session prompt must name something that actually exists. Check the installed skills before naming one: much of the DevForge roster is specified but not implemented, and `devforge-define-product` in particular may not be installed. If the capability is not there, the honest next task is authoring or evaluating it, or continuing in plain language. Never present a slash command or `devforge` subcommand you have not confirmed.

## Before you call it done

Run `scripts/check_artifact.py` on each file you wrote. It reports leftover `{{...}}` placeholders and prints the SHA-256 digests the handoff table needs:

```bash
python3 scripts/check_artifact.py docs/devforge/ideas/IDEAS-001.md docs/devforge/handoffs/HANDOFF-001.md
```

A required field still holding a placeholder means the result is a draft and cannot be presented as ready. A missing fact goes in `missing_inputs`, never into template filler.

Tell the user: where the ledger is saved, what is newly proposed versus actually adopted, what remains open, and the one next action. Say plainly that nothing here has been mechanically validated - no tool checks whether a brainstorm is any good, and structural checks do not establish semantic quality.

## Filling the envelope honestly

Read `references/recording-rules.md` when you write the artifact frontmatter, or when any of these come up: no session record exists (the usual case), a concurrent writer holds the worktree, an upstream input changed, or a check you wanted to run could not run. It covers the envelope fields, bootstrap mode, and how to report those conditions without inventing an identifier.
