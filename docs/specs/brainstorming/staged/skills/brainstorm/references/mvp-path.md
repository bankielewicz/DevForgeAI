# The path to a first release

Read this at step 5, once every idea has a proposed disposition and before the work file is saved. It tells
you how to rank the open assumptions by risk, how to propose which ideas go into the first release, and how
that proposal becomes the user's decision. The validator checks every table here (its messages end with the
check's number, `(MV-01)` to `(MV-12)`), so follow the wording to the character.

## Contents

- [Order of work](#order-of-work)
- [The cut rows](#the-cut-rows)
- [Rank the assumptions](#rank-the-assumptions)
- [Propose the cut](#propose-the-cut)
- [Write both tables](#write-both-tables)
- [Confirm the cut](#confirm-the-cut)
- [Later runs](#later-runs)
- [Worked example](#worked-example)

## Order of work

1. Propose a disposition for each idea (SKILL.md step 5).
2. List the cut rows.
3. Rank the assumptions.
4. Propose the cut.
5. Save the work file with both tables, then ask step 5's form, or ask nothing when no question is asked.
6. Apply the answers: dispositions and, in a brownfield run, assumption updates first, then the cut.

The ranking is made before the cut and never reads it. The cut reads the ranking and nothing else about risk.

## The cut rows

The cut rows are the active ideas whose `disposition` is `promoted`, or is `open` with a step-5 proposal of
`promoted`. List them in ID order. Call their number M. Ideas with `status: deprecated` are never rows.

## Rank the assumptions

Rank every active assumption whose `state` is `open`. Fill four cells for each.

**1. Which cut rows it stops.** An idea *depends on* an assumption when this is true: if the assumption's
statement were false, the idea, as worded, would no longer relieve any problem it `addresses`. Decide it for
each cut row. Count the rows that depend on the assumption: N.

- Depends: "Text a reminder two days before the visit" depends on "We believe that patients read texts from the
  clinic the same day". Unread texts remind nobody.
- Does not depend: "Phone patients who booked more than four weeks ahead" does not depend on it. The call
  works whether or not texts are read.

**2. `If wrong`.** Write one of these, with the stopped rows in ID order:

| When | Cell |
|---|---|
| N = M and M is at least 1 | `Fatal: stops IDEA-01, IDEA-03 (2 of 2 in the cut table).` |
| N is at least 1 and less than M | `Serious: stops IDEA-02 (1 of 3 in the cut table).` |
| N = 0 | `Minor: stops no idea in the cut table (0 of 3).` |

**3. `Confidence`.** A source *supports* an assumption when it states a fact about the people or the system
the assumption names, and that fact makes the statement more likely to be true. Use only the entries of the
frontmatter `sources` list.

| Cell | When |
|---|---|
| `high` | An entry of kind `data`, `document` or `ticket` supports it |
| `medium` | No such entry supports it, and an entry of kind `interview`, `url` or `note` does |
| `low` | No entry supports it |

- Supports: `data: reminder pilot export, October 2026`, which shows 8 of 10 reminder texts opened within a
  day, supports "patients read texts from the clinic the same day": `high`.
- Does not support: `url: an article on average text open rates` says nothing about this clinic's patients.
  It is no support, so with no other entry the cell is `low`.

**4. `Cheapest test`.** Take the assumption's `validation` value without its quotes. Cut it after the first
`.`, `?` or `!` that a space or the end of the value follows; when there is none, take the whole value and
add a full stop. Write `/` for every `|`. Then choose the kind with the first rule that matches the sentence,
ignoring case and matching whole words only:

1. `Prototype` when it holds one of: prototype, prototypes, mock-up, mock-ups, mockup, mockups, pilot, pilots,
   trial, trials, beta, demo, demos, experiment, experiments, a/b, landing page, smoke test, fake door, build,
   launch.
2. `Interview` when it holds one of: ask, asks, interview, interviews, survey, surveys, poll, polls, observe,
   shadow, talk to, speak to, questionnaire, focus group, workshop.
3. `Data` otherwise.

The cell is the kind, a colon, a space and the sentence: `Interview: Ask ten patients at the desk whether they
read texts from the clinic the same day.` When the `validation` is empty or starts with
`[NEEDS CLARIFICATION:`, the cell is `[NEEDS CLARIFICATION: how to test ASM-NN]` with the assumption's ID.

When the kind the rules give is not the test the `validation` describes, reword the `validation` so its first
sentence names the test with one of the words above, then derive the cell again. Never edit the cell alone.

**Order.** Give each assumption its risk points: impact times doubt, where impact is Fatal 3, Serious 2,
Minor 0, and doubt is `low` 3, `medium` 2, `high` 1. Sort by, in this order:

1. risk points, highest first;
2. impact, highest first (a Fatal with 6 points comes before a Serious with 6);
3. doubt, highest first (`low` confidence before `medium` before `high`);
4. N, highest first;
5. assumption ID, lowest first.

Number the sorted rows 1, 2, 3 and so on in the `Rank` column.

## Propose the cut

The *counted* assumptions are those ranked 1 to 3 that stop at least one cut row. Take these steps in order.

1. **Pick one idea for each counted assumption**, going from rank 1 down. When a row the assumption stops is
   already `yes`, the assumption is covered: pick nothing. Otherwise pick, among the rows it stops, the idea
   with the highest `score`. A `null` score counts as lower than any number. On a tie, pick the lowest ID.
   The picked row is `yes` with `Tests ASM-NN, ranked R.`
2. **When no row is `yes` after step 1** and the table has a row, the row with the highest `score` (lowest ID
   on a tie) is `yes` with `Highest score; no assumption ranked 1 to 3 picks an idea.`
3. **Add what a `yes` idea needs.** An idea *needs* another when, as worded, it cannot be built or used unless
   the other exists. Look only at cut rows. Find every row that is not `yes` and that a `yes` idea needs.
   Each becomes `yes` with `Needed by IDEA-NN, which is in the first release.`, naming the lowest-ID `yes` idea
   that needs it. Repeat until a pass adds no row.
   - Needs: "Let patients move a booking from the reminder link" needs "Text a reminder two days before the
     visit". There is no link without the text.
   - Does not need: "Keep a waiting list for freed slots" does not need the reminder text. Staff can fill it
     by phone.
4. **Every other row is `no`.** When it depends on a counted assumption, take the highest-ranked one and write
   `Tests ASM-NN, ranked R, which IDEA-MM already tests.`, where IDEA-MM is the lowest-ID `yes` row that the
   assumption stops. Otherwise write `Tests no assumption ranked 1 to 3.`

Step 1 picks at most three ideas. Step 3 has no limit: an idea in the first release without what it needs
could not ship.

When a `yes` idea needs an active idea that is not a cut row, add this bullet to section 7 and leave the cut
as it is: `- [NEEDS CLARIFICATION: IDEA-NN is in the proposed first release and needs IDEA-MM, which is not
promoted or proposed for promotion. Promote IDEA-MM, or leave IDEA-NN out?]`

## Write both tables

The ranking goes into section 7, after the `assumptions` item block and before the bullets:

```markdown
### Assumption risk ranking

| Rank | Assumption | If wrong | Confidence | Cheapest test |
|---|---|---|---|---|
| 1 | ASM-01 | Serious: stops IDEA-01, IDEA-02 (2 of 4 in the cut table). | low | Interview: Ask ten patients at the desk whether they read texts from the clinic the same day. |
```

With no active assumption whose `state` is `open`, write the line `None.` under the heading instead of the
table.

The cut goes into section 6, after the convergence prose:

```markdown
### First release cut

First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Needed by IDEA-02, which is in the first release. |
| IDEA-02 | yes | Tests ASM-01, ranked 1. |
```

With no cut row, write the line `No idea is promoted or proposed for promotion.` under the status line
instead of the table. Never put a `|` inside a cell. Write nothing else under either heading.

Section 8 then holds one bullet for each `yes` row, in ID order, and `- None.` when there is none
([intake.md](intake.md) gives the bullet's form).

A draft BRN saved before step 5's proposals exist (the user stopped) has no cut row: write the line for no
cut row, and rank the assumptions with M = 0, which makes every one `Minor: stops no idea in the cut table
(0 of 0).`

## Confirm the cut

The cut is the user's decision. Until the user confirms it, its status line is exactly
`First release cut: proposed, not confirmed`.

**Ask** it as the third question of step 5's form, only when the cut has a row:

- question: "Confirm the first release cut?", `header: "Step 5"`;
- options, in this order: `Accept as proposed`, description "The ideas marked yes are the first release.";
  and `Leave it proposed`, description "The table stays a proposal; you can confirm it later.";
- each option's `preview`: the status line, a blank line and the cut table. When the table is too long for a
  preview, list each row's idea ID with `yes` or `no` there, and say in the question that the reasons are in
  the reply.

Mark no option recommended. Changes come typed under Other. Without AskUserQuestion, show the status line and
the table in plain text with the dispositions and ask the same question. When no question is asked (the waiver's
*Proceed without questions*, or nobody to ask), the cut stays proposed.

**Apply the answers in this order.**

1. Write the dispositions the first question's answer confirms (SKILL.md step 5) and, in a brownfield run,
   the assumption updates the fourth question's answer confirms ([brownfield.md](brownfield.md)).
2. List the cut rows again from the dispositions as they now stand, and the assumptions to rank again (a
   confirmed update of one of this BRN's own assumptions set its `state` to `validated` or `invalidated`, so
   it is no longer ranked). When either list differs from the one the form showed, the user answered about
   another table: rank and propose again from the new lists, keep `First release cut: proposed, not confirmed`
   whatever the third answer was, and say so in the reply, naming the ideas that entered or left the table and
   the assumptions that left the ranking.
3. Otherwise read the third answer:

| Answer | Rows | Status line |
|---|---|---|
| `Accept as proposed`, or typed text that accepts the table ("yes", "accept") | As proposed | Confirmed, when step 4 allows |
| Typed changes | Each named row takes the stated value; its `Why` becomes `Included by the user.` for `yes` or `Left out by the user.` for `no`. Unnamed rows keep their value (see *Typed changes* below for their `Why`) | Confirmed, when step 4 allows |
| `Leave it proposed`, a dismissal, no answer, or typed text that states neither an acceptance nor a change | As proposed | `First release cut: proposed, not confirmed` |

4. Write `First release cut: confirmed by <owner> on <today>` only when every row's idea now has
   `disposition: promoted`. `<owner>` is the frontmatter `owner` without its quotes, and `<today>` is
   `YYYY-MM-DD`. When a row's idea is still `open`, keep `proposed, not confirmed`, keep the rows as step 3
   left them, and say in the reply which ideas are not promoted. When `owner` is a NEEDS CLARIFICATION marker,
   ask for the owner's name first; without it the cut stays proposed.

**Typed changes.** A typed change names a row's idea and puts it in or out: "add IDEA-04", "IDEA-02 out",
"only IDEA-01" (IDEA-01 `yes`, every other row `no`). "IDEA-04 looks risky" states no change. A change that
names an idea with no row is not written: say that only a promoted idea can be in the first release. After a
typed answer, never show the options again for the same question; act on the text, or say what you could not
read. The user may leave every row `no`: that is their decision.

A change can make an unnamed row's `Why` untrue: `Needed by IDEA-NN, which is in the first release.` and
`Tests ASM-NN, ranked R, which IDEA-MM already tests.` each name an idea that must say `yes`. When the change
set that idea to `no`, the unnamed row keeps its value and its `Why` becomes the user sentence for that value.
Every other unnamed row keeps its `Why`.

After typed changes, name in the reply each `yes` idea that needs a `no` row, and change nothing for it.

## Later runs

- **The user confirms later**, after the BRN was written with the cut proposed. Don't edit from that message
  alone. Follow SKILL.md's *Decisions that belong to the user*: mark step 5, ask the form again with the
  table as the BRN holds it, then edit the BRN in place, validate it and report.
- **Extending a BRN.** Rank and propose again from the BRN as it now stands. When the new cut table is
  identical to the one in the BRN (same rows, values and `Why` cells), keep its status line. Otherwise write
  the new table with `First release cut: proposed, not confirmed`, ask the third question about it, and say in
  the reply and in the Change Log row that the earlier cut was replaced. An earlier-shape BRN (no
  `Project kind:` line) gets neither table when it is extended.
- **Continuing a run** from a work file that holds both tables: keep them, and ask step 5 from them.
- **A framework switch** at step 5 that redoes the evaluation: make both tables again from the new proposals
  before the form is asked again.
- **Step 7's read-back.** The status line says `confirmed` only when the user confirmed the cut at step 5 of
  this run, or the BRN being extended already said so and the table is unchanged. Anything else is reset to
  `First release cut: proposed, not confirmed`.

## Worked example

Four ideas are proposed for promotion: IDEA-01 "Text a reminder two days before the visit" (score 3), IDEA-02
"Let patients move a booking from the reminder link" (score 4), IDEA-04 "Keep a waiting list for freed slots"
(score 2) and IDEA-05 "Send a thank-you card after a kept visit" (score 1). M = 4. `sources` holds one entry,
`"url: booking system vendor's page on text messages"`.

| Assumption | Rows that depend on it | Support | `validation` |
|---|---|---|---|
| ASM-01 patients read texts from the clinic the same day | IDEA-01, IDEA-02 | none | "Ask ten patients at the desk whether they read texts from the clinic the same day." |
| ASM-02 a patient who can't come will move the visit rather than skip it | IDEA-02, IDEA-04 | none | "Count how many of last quarter's no-shows had phoned to cancel late, in the appointment book." |
| ASM-03 the booking system can send texts | IDEA-01, IDEA-02 | the `url` entry | "Run a one-week trial that sends test reminders from the booking system to staff phones. Check delivery." |
| ASM-04 the front desk has 20 minutes a day for calls | none (its idea, IDEA-07, is proposed for parking) | none | "[NEEDS CLARIFICATION: how to measure front-desk time]" |

Risk points: ASM-01 2 × 3 = 6, ASM-02 2 × 3 = 6, ASM-03 2 × 2 = 4, ASM-04 0 × 3 = 0. ASM-01 and ASM-02 tie on
points, impact, doubt and N, so the lower ID comes first.

```markdown
### Assumption risk ranking

| Rank | Assumption | If wrong | Confidence | Cheapest test |
|---|---|---|---|---|
| 1 | ASM-01 | Serious: stops IDEA-01, IDEA-02 (2 of 4 in the cut table). | low | Interview: Ask ten patients at the desk whether they read texts from the clinic the same day. |
| 2 | ASM-02 | Serious: stops IDEA-02, IDEA-04 (2 of 4 in the cut table). | low | Data: Count how many of last quarter's no-shows had phoned to cancel late, in the appointment book. |
| 3 | ASM-03 | Serious: stops IDEA-01, IDEA-02 (2 of 4 in the cut table). | medium | Prototype: Run a one-week trial that sends test reminders from the booking system to staff phones. |
| 4 | ASM-04 | Minor: stops no idea in the cut table (0 of 4). | low | [NEEDS CLARIFICATION: how to test ASM-04] |
```

The cut: ASM-01 picks IDEA-02 (score 4 beats 3). ASM-02 and ASM-03 each stop IDEA-02, which is already `yes`,
so they pick nothing. IDEA-02 needs IDEA-01. IDEA-04 depends on ASM-02, ranked 2. IDEA-05 depends on no
counted assumption.

```markdown
### First release cut

First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Needed by IDEA-02, which is in the first release. |
| IDEA-02 | yes | Tests ASM-01, ranked 1. |
| IDEA-04 | no | Tests ASM-02, ranked 2, which IDEA-02 already tests. |
| IDEA-05 | no | Tests no assumption ranked 1 to 3. |
```

The user accepts every disposition, says the brainstorm has converged, and types "add IDEA-04" under the third
question. All four ideas are now `promoted`, so the cut is confirmed with one changed row:

```markdown
First release cut: confirmed by Dana Reyes on 2026-11-18

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Needed by IDEA-02, which is in the first release. |
| IDEA-02 | yes | Tests ASM-01, ranked 1. |
| IDEA-04 | yes | Included by the user. |
| IDEA-05 | no | Tests no assumption ranked 1 to 3. |
```
