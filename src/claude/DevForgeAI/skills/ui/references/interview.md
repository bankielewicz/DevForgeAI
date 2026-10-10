# The interview

## Contents

- When to use this
- Draft first
- The batches, in order
- Writing what the answers give
- The canvas facts
- Surfaces
- Candidates in an amend run
- Answers stated in the request
- Proceed without questions
- When the user stops (ERR-13)

## When to use this

Read this at step 3 of SKILL.md, and before any other question the run asks. The interview confirms the
mappings; it fills nothing a board or a promoted idea already answers, and it never decides for the user.

## Draft first

Before asking anything, draft from the boards and the promoted ideas, and write none of it: each board's
title, flow, surface and ideas, and each promoted idea's coverage. Then ask only what the request does not
answer. Group the boards into proposed flows by what the lines of each board show, and name a flow as a
lowercase slug (`day-to-day`).

## The batches, in order

A call holds at most 4 questions, each with 2 to 4 options, the recommended option first and marked
"(Recommended)". The user may answer in their own words. Fill each call in this order and carry the rest to
the next call. The interview is bounded by this structure, not by a call budget.
1. **The canvas facts,** in a create run, or in an amend run in which a board changed, was added or was
   removed, when the request does not state them: the canvas URL and the canvas version copied (below).
2. **One question for each proposed flow,** showing its boards, each with the proposed title, surface and
   ideas. Options: confirm the group as shown (Recommended); change a board's flow, surface or ideas; leave the
   flow unconfirmed. The user confirms or changes the group.
3. **One question for the promoted ideas that no board shows.** For each: `not a screen` or `no board yet`.
   Propose `not a screen` (first, Recommended) only for an idea that names no screen, flow or user
   interface; otherwise propose `no board yet` first. An idea is recorded as `not a screen` only when the user
   said so.
4. **Amend runs only: one question for each group of changed, new or removed boards.** Show the candidates (see "Candidates in an
   amend run") that could bear on each, so the user can name the board that answers a candidate, or
   decline it. For a changed board, ask whether its mapping stands; for a removed one, whether to deprecate its
   item; for a withdrawn idea, whether to keep or drop the mapping.
5. **The approver and approval,** only at step 6 of SKILL.md.

Write nothing that an unanswered question affects until the answer arrives. When AskUserQuestion is not
available, ask in plain text, at the end of the reply, and end the turn.

## Writing what the answers give

- Write a flow, surface, idea list, title or coverage status only when the user supplied or confirmed it.
- Otherwise write `null` (for a title, the file name up to its first dot; for an idea no board shows,
  `no board yet`) with a `[NEEDS CLARIFICATION: …]` marker, in the board's `notes` or in section 5.
- A mapping the user changes is written as changed. A mapping the user leaves open is written `null` with its
  marker.

## The canvas facts

- Record the canvas URL and `canvas_version` as the user states them, and the date of the copy when the user
  gives it. Read `canvas_format` from the script's output, never from the user.
- A fact the user does not give is `null`, with `[NEEDS CLARIFICATION: canvas URL and version copied]` in
  section 4. Never take the version from a file in the boards folder, and never infer it.
- In an amend run in which a board changed, was added or was removed, the recorded `canvas_version` describes
  the copy that was in the boards folder before: ask for the new one with the canvas facts. When the user gives
  none, write `null` with the marker, never the old value, which would name a copy the skill no longer holds.
  When no board changed, keep it.

## Surfaces

Treat graphical and terminal screens alike. Every board gets a surface of `web`, `desktop`, `mobile` or
`terminal`, confirmed by the user. A terminal screen is a command-line or other text-mode screen, designed in
Claude Design like any other board. A board whose surface the user has not confirmed has surface `null` and a
marker. A terminal board is mapped to flows and ideas, counted and reported exactly as the others are.

## Candidates in an amend run

The candidates come from the PRDs and the accepted ADRs (SKILL.md step 2). Put at most 4 in a call and at most
12 in a run; report the rest as left for a later run. Each carries its citation: the file, the item and the
version. The user either names the board that answers it (recorded in that board's `answers`), or declines it
(recorded in `considered`), or leaves it for a later run.

## Answers stated in the request

An answer the request states counts as confirmed: the canvas URL and version, a board's flow, surface and
ideas, which idea names no screen, which idea has no board yet, who approves. Ask only about the rest.

## Proceed without questions

A request that says to proceed without questions, or not to ask anything, asks nothing in this run:
- every mapping the request does not state is `null` with its marker, and so is every unstated canvas fact;
- every promoted idea no board shows, and that the request does not say names no screen, is `no board yet`;
  never `not a screen` on the skill's own judgement;
- no candidate is put to the user: report every candidate as left for a later run, with their number.
  `considered` gains no `PRD-NNN@N` or `ADR-NNN@N` entry for their documents. A `declined:` entry the request
  states is still recorded, and counts toward the caps;
- no approval is offered (an approval the request itself gives, with a name, still applies at step 6 of
  SKILL.md).

Every other step still runs. It never answers the gates: which BRN, an unconverged BRN, which of several DSNs
to amend.

## When the user stops (ERR-13)

When the user stops before the interview ends, offer to save the DSN with every unanswered mapping `null` and
marked (a create run) or unchanged (an amend run). On a yes, write it, then validate and report it as any
other write. With no answer to the offer, write nothing and say how to resume: run the skill again with the
BRN ID.
