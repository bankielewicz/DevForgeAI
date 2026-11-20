# Brainstorming frameworks

Read this at step 2. Take the first selection rule that matches, read that framework's file, which
sits next to this index, and follow it from then on.

## Contents

- [Selection rules](#selection-rules)
- [Frameworks](#frameworks)
- [Names a user may use](#names-a-user-may-use)
- [A name the index lacks](#a-name-the-index-lacks)
- [Switching](#switching)
- [Required sections](#required-sections)

## Selection rules

Go down the table and stop at the first rule whose test holds. Ask nothing to decide. Then tell the
user with that rule's sentence, word for word, as a line of its own. In a run that continues an
earlier one, don't select again when the work file's section 5 opens with a framework's method text:
that framework is in use.

| # | When | Framework | Tell the user |
|---|---|---|---|
| 1 | The user names a framework that this index lists | the one named | Framework: `<name>`, because you named it. |
| 2 | The request gives candidates and asks to rank or cut them | `shortlist-ranking` | Framework: `shortlist-ranking`, because you gave a list of candidates and asked to rank or cut it. |
| 3 | The request asks what to build first or what could make it fail | `risk-first-mvp` | Framework: `risk-first-mvp`, because you asked what to build first or what could make this fail. |
| 4 | The product exists and the request asks to improve, extend or fix it | `improve-existing` | Framework: `improve-existing`, because the product exists and you asked to improve, extend or fix it. |
| 5 | No problem can be stated yet with an affected person and what hurts them | `problem-reframing` | Framework: `problem-reframing`, because the request doesn't yet say who is affected and what hurts them. |
| 6 | Otherwise | `diverge-converge` | Framework: `diverge-converge`, because no other rule in the index matched. |

**The request** is the arguments plus everything the user wrote in this run before step 2 ends,
intake answers included. **A phrase matches** when the request holds it as whole words, ignoring
case, with a hyphen and a space counting as the same; a phrase ending in `*` matches any word that
starts with it.

**Rule 1.** The request holds a framework's name from the table below, or one of its other names
(*Names a user may use*). When it holds names of two frameworks, take the one that comes first in the
request. A name the request says not to use does not count, and no later rule selects that
framework: skip a rule that would. If rule 6 is the one skipped, take `problem-reframing` and say
"Framework: `problem-reframing`, because you asked not to use `diverge-converge`."

**Rule 2.** Both parts hold:

1. *Candidates.* The request lists three or more candidate ideas (the items of a bulleted or
   numbered list, or of a run separated by commas, semicolons, "and" or "or"), or it names a
   backlog, shortlist or list to use and gives a file path in the project. Read that file now; its
   candidates are its top-level list items, or, when it has none, its table's body rows, or, when it
   has neither, its non-empty lines that are not headings. A file must give two or more candidates.
   Whether a listed item is a candidate idea is a judgment: it is something to build, change or do.
   "Dark mode, CSV export, SSO" are candidates; "nurses, porters, cleaners" (people) and "Leeds,
   York, Hull" (places) are not.
2. *The ask.* The request holds one of: `rank*`, `priorit*`, `choose`, `choosing`, `pick`,
   `picking`, `select`, `selecting`, `cut`, `trim`, `narrow`, `shortlist`, `compare`, `which of`,
   `which one`, `which should`, `in what order`, `in which order`.

Matches: "Rank these for next quarter: dark mode, CSV export, SSO, an audit log." Does not match:
"Brainstorm ways we could cut down on no-shows" (it holds `cut`, but no candidates), and "We thought
of reminders, deposits and overbooking. What else could we do?" (candidates, but no ask).

When part 2 holds and the request names a backlog that can't be read (no path, a path that doesn't
exist, or fewer than two candidates in the file), rule 2 does not match. Say "I can't read `<what the request
named>` as a list of candidates. Paste the list, or give a file path, and ask me to switch to
`shortlist-ranking`." and go on to rule 3.

**Rule 3.** The request holds one of: `mvp`, `minimum viable`, `prototype*`, `proof of concept`,
`first release`, `first version`, `version one`, `v1`, `build first`, `ship first`, `do first`,
`where to start`, `what to start with`, `smallest thing`, `riskiest`, `biggest risk*`, `could fail`,
`might fail`, `would fail`, `make it fail`, `make this fail`, `could go wrong`, `might go wrong`,
`pre-mortem`, `premortem`.

Matches: "What should the MVP of a meal-planning app be?" Does not match: "Brainstorm ways to reduce
the risk of falls in care homes" (it holds `risk`, which is not a listed phrase).

**Rule 4.** Both parts hold:

1. The project kind is brownfield: step 1 decided that the product the topic is about exists (it is
   built or in use), or, when the kind is undecided, the kind step 1 works with is brownfield. A run
   has one kind, the same here as everywhere else. With no kind decided or worked with, this part does
   not hold.
2. The request holds one of: `improv*`, `enhanc*`, `extend*`, `fix*`, `upgrad*`, `rework*`,
   `redesign*`, `refin*`, `optimi*`, `revamp*`, `moderni*`, `next version`, `next release`,
   `version 2`, `v2`, `add to`, `new feature*`.

Matches: "Our booking app is live. How could we improve the rebooking flow?" Does not match:
"Our booking app is live. Brainstorm a referral scheme for it" (brownfield, but no listed phrase).

**Rule 5.** This one is a judgment. Try to fill both blanks of "*who* struggles with *what*" with
words from the request, rephrased if needed but never invented. The rule matches when either blank
stays empty: the topic is a symptom, a goal or a solution.

Matches: "Sign-ups have been flat for six months" (a symptom: no person, no hurt), "Grow revenue by
20% next year" (a goal), "Build a chatbot for our website" (a solution: nobody's hurt is named).
Does not match: "Patients forget appointments booked weeks ahead" (who: patients; what: remembering
appointments), and "A feature that helps remote teams run better stand-ups" (a solution, but it
names who and what they struggle with).

**When two rules could match**, the lower number wins. "Which of these should we build first: A, B,
C or D?" matches rules 2 and 3: rule 2. "Our app is live. What should we build first for version 2?"
matches rules 3 and 4: rule 3.

## Frameworks

| framework | file | use when | avoid when |
|---|---|---|---|
| shortlist-ranking | [shortlist-ranking.md](shortlist-ranking.md) | The user already has a shortlist or backlog and wants it ranked or cut | The options are still open, or the list has fewer than two candidates |
| risk-first-mvp | [risk-first-mvp.md](risk-first-mvp.md) | The user asks what to build first, for an MVP or a prototype, or what could make the idea fail | The user only wants a list ranked |
| improve-existing | [improve-existing.md](improve-existing.md) | The product exists and the topic is improving, extending or fixing it | Nothing is built or in use yet |
| problem-reframing | [problem-reframing.md](problem-reframing.md) | The topic is a symptom, a goal or a solution: nobody's problem is stated yet | The request already says who is affected and what hurts them |
| diverge-converge | [diverge-converge.md](diverge-converge.md) | A new product, feature or problem space where options are wide open; the default | The user already has a fixed shortlist and only wants it ranked |

## Names a user may use

A name written here with capital letters matches only with those capitals; the others match as
phrases do.

- `shortlist-ranking`: `RICE`, `MoSCoW`
- `risk-first-mvp`: `risk-first`, `pre-mortem`, `premortem`
- `improve-existing`: `SCAMPER`
- `problem-reframing`: `five whys`, `5 whys`, `JTBD`, `HMW`
- `diverge-converge`: `diverge and converge`

Ordinary wording is not a name: "How might we cut no-shows?" and "reframing our pricing" name no
framework.

## A name the index lacks

The request asks for a framework by a name that matches none above. This is a judgment: the named
thing must be a way of working through ideas (a framework, method, technique, canvas or analysis),
not a tool, a data source or a document. "Use SWOT" and "run a design sprint on this" ask for one;
"use our CRM data" and "use the PRD" do not.

Then say, word for word: "`<the name as the user wrote it>` is not a framework in this skill's
index, which lists `shortlist-ranking`, `risk-first-mvp`, `improve-existing`, `problem-reframing`
and `diverge-converge`." (name the table's frameworks, in its order). Ask nothing. Go on from rule
2, and give that rule's sentence next.

## Switching

The user asks to switch when, after the step-2 sentence, they name another listed framework to use.
For a name the index lacks, say the sentence above and keep the current framework. Otherwise tell
the user "Framework: `<new>`, because you asked to switch from `<old>`." and:

- **Before step 3 is completed:** start the new framework's *Steps* from its first step. Keep every
  problem, idea and assumption already captured, with its ID.
- **After step 3 is completed and before step 5's form is answered** (a switch typed as that form's
  answer counts as before: write no disposition and no convergence from that answer):
  1. Keep every problem, idea and assumption, with its ID and its text. Don't redo step 3, and
     generate no new idea. Switching to `shortlist-ranking`, every idea already captured is a
     candidate.
  2. Leave the task list as it is: the step in progress stays in progress. Ask none of the new
     framework's questions: use what the user has said, the figures given with the request to
     switch included, and the framework's fallbacks for the rest. Set every idea's `value`,
     `effort`, `risk` and `score` back to `null` and fill them again by the new framework's
     *Mapping to the BRN*. Drop the old proposals.
  3. Section 5 holds, in this order: the new framework's method text; the line "Switched from
     `<old>` after step 3: the problems, ideas and assumptions were kept and only the evaluation was
     redone."; the lines the new framework writes while evaluating; then the old framework's
     section-5 lines that say where the items came from, unchanged. Lines the new framework would
     have written during step 3 are left out.
  4. Make the proposals by the new framework's rule, mark step 5 in_progress if it is not, save
     the work file, and ask step 5's form.
- **After step 5's form is answered, or once the BRN is written:** don't switch in this run. Say
  "The brainstorm is already written as BRN-NNN. To evaluate it with `<new>`, run
  `/devforgeai:brainstorm` again and choose to extend BRN-NNN." and change nothing.

The report at step 8 names the framework in use at the end.

## Required sections

Every framework file has these `##` headings, with this text, in this order, and no other `##`
heading. A file that lacks one is malformed: use `diverge-converge` instead and tell the user which
file was the problem.

1. `## When to use / When not to use`
2. `## Steps`
3. `## Questions to ask`
4. `## Mapping to the BRN`
5. `## Evaluation method text`
6. `## Example`

*Mapping to the BRN* states the rating method exactly. *Steps* say how dispositions are proposed:
proposals only, never written without the user's answer. *Evaluation method text* is a quoted
paragraph that opens with words no other framework's text starts with, up to its first colon.

To add a framework, add its file here and one row to the *Frameworks* table. A framework with no
selection rule of its own is chosen only when the user names it. `SKILL.md` does not change.
