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
| Typed changes | Each named row takes the stated value; its `Why` becomes `Included by the user.` for `yes` or `Left out by the user.` for `no`. Unnamed rows keep their value; refresh their reasons (below) | Confirmed, when step 4 allows |
| `Leave it proposed`, a dismissal, no answer, or typed text that states neither an acceptance nor a change | As proposed | `First release cut: proposed, not confirmed` |

4. Write `First release cut: confirmed on <today>` only when every row's idea now has
   `disposition: promoted` and no row is flagged for review (below). `<today>` is `YYYY-MM-DD`. The line
   names nobody: never add a name to it, and never ask for one. When a row's idea is still `open`, keep
   `proposed, not confirmed`, keep the rows as step 3 left them, and say in the reply which ideas are not
   promoted.

**Typed changes.** A typed change names a row's idea and puts it in or out: "add IDEA-04", "IDEA-02 out",
"only IDEA-01" (IDEA-01 `yes`, every other row `no`). "IDEA-04 looks risky" states no change. A change that
names an idea with no row is not written: say that only a promoted idea can be in the first release. After a
typed answer, never show the options again for the same question; act on the text, or say what you could not
read. The user may leave every row `no`: that is their decision.

**The two user sentences are reserved.** Write `Included by the user.` or `Left out by the user.` only on a row
whose value the user stated: a row a typed change names, or a flagged row the user then accepted (below). Never
write either for any other reason.

**Refresh the reasons** after typed changes. Every value stays. The user's rows stay. For each other row, derive
the `Why` again, in this order:

1. For each counted assumption, from rank 1 down: when a row it stops is a user row that says `yes`, or got a
   `Tests` sentence earlier in this pass, do nothing. Otherwise, among the rows it stops that say `yes` and are
   not the user's, the one with the highest `score` (lowest ID on a tie) gets `Tests ASM-NN, ranked R.`
2. Each `yes` row still without a reason: when a `yes` idea needs it, `Needed by IDEA-NN, which is in the first
   release.`, naming the lowest-ID such idea. Otherwise, when no assumption is counted and the row has the
   highest `score` of all rows (lowest ID on a tie), `Highest score; no assumption ranked 1 to 3 picks an idea.`
   Otherwise flag it.
3. Each `no` row still without a reason: when a `yes` idea needs it, flag it. Otherwise, when it depends on a
   counted assumption, take the highest-ranked one: when a row that assumption stops says `yes`, `Tests ASM-NN,
   ranked R, which IDEA-MM already tests.`, naming the lowest-ID such row; when none does, flag it. Otherwise
   `Tests no assumption ranked 1 to 3.`

**A flagged row** keeps its value, and its `Why` is exactly `Needs review: no rule supports this value.` While
a row is flagged the status line is `First release cut: proposed, not confirmed`, whatever the answer was.

When a row is flagged and a question can be asked, ask the third question once more, and only once, alone in
a form tagged step 5, with the same options and the refreshed table in each preview. Its text shows each
flagged row as its idea ID and its current value: "Confirm the first release cut? Needs review: IDEA-04 (no),
IDEA-06 (yes)." Then:

- `Accept as proposed`, or typed text that accepts those values: the user has chosen them. Each flagged row's
  `Why` becomes `Included by the user.` for `yes` or `Left out by the user.` for `no`. Refresh the reasons once
  more, then go to step 4.
- Typed changes: apply them as typed changes (each named row takes its value and its user sentence), refresh
  the reasons once more, then go to step 4. A flagged row the text doesn't name stays as the refresh leaves it.
- `Leave it proposed`, a dismissal or no answer: every flag stays.

Never ask again after that. Whenever a row is still flagged at the end of the run (the answer left it, a new
flag came up, or no question could be asked: the waiver's *Proceed without questions*, or no AskUserQuestion
and nobody to ask), keep every flag and the proposed status line, and report the flagged rows in the final
reply's discussion with this sentence, each row as its idea ID and value, in ID order:
`Needs review: IDEA-04 (no), IDEA-06 (yes). No rule supports these values, so the first release cut stays proposed.`

A user row that says `no` while a `yes` idea needs it stays as the user set it: name it in the reply.

## Later runs

- **The user confirms later**, after the BRN was written with the cut proposed. Don't edit from that message
  alone. Follow SKILL.md's *Decisions that belong to the user*: mark step 5, ask the form again with the
  table as the BRN holds it, then edit the BRN in place, validate it and report. When that table holds a
  flagged row, word the third question as *A flagged row* says ("Confirm the first release cut? Needs
  review: IDEA-04 (no).") and read its answer the same way: that is the one asking for that run, and a row
  still flagged afterwards is reported as above.
- **Extending a BRN.** Rank again from the BRN as it now stands and list the cut rows. Compare their idea IDs
  with the rows of the BRN's cut table.
  - *The same IDs.* Keep each row whose `Why` is `Included by the user.` or `Left out by the user.`: its value
    and its sentence. Work every other row out again from the current ranking and scores, its value
    included when the rules now give the other answer, with the four steps of *Propose the cut*, where: a user
    row that says `yes` counts as already `yes`; steps 1 and 2 pick only among rows that are not the user's;
    step 2 applies only when no assumption is counted; steps 3 and 4 never change a user row. A row the BRN
    holds as flagged is not the user's: propose it again. When the result equals the BRN's table in every
    cell, keep its status line. Otherwise (any cell changed) write it with `First release cut: proposed, not
    confirmed`, ask the third question about it, and write this sentence in the reply and in the Change Log
    row, naming in ID order each row with a changed cell: `First release cut returned to proposed: IDEA-02 changed.`
  - *Different IDs* (an idea entered or left the cut rows). Propose every row again with *Propose the cut*
    and keep none. Write `First release cut: proposed, not confirmed` and ask the third question. Show the
    user's previous choices, each row the BRN held with a user sentence as its idea ID and value, in ID
    order, in both places: in the reply, `Earlier choices, not carried over: IDEA-04 (yes), IDEA-02 (no). Tell me which still stand.`; in the
    Change Log row, `First release cut proposed again: the eligible ideas changed. Earlier choices by the user: IDEA-04 (yes), IDEA-02 (no).` With no such row, the Change Log row ends after "changed." and the reply
    has no such sentence.

  An earlier-shape BRN (no `Project kind:` line) gets neither table when it is extended.
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
First release cut: confirmed on 2026-11-18

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Needed by IDEA-02, which is in the first release. |
| IDEA-02 | yes | Tests ASM-01, ranked 1. |
| IDEA-04 | yes | Included by the user. |
| IDEA-05 | no | Tests no assumption ranked 1 to 3. |
```

Had the user typed "IDEA-02 out" instead, IDEA-02 becomes `no` with `Left out by the user.` and the reasons
are refreshed. ASM-01 stops IDEA-01, which says `yes`, so IDEA-01 gets `Tests ASM-01, ranked 1.` in place of
`Needed by IDEA-02, …`. IDEA-04 depends on ASM-02, and no row ASM-02 stops says `yes` any more, so nothing
supports its `no`: it is flagged, the cut stays proposed, and the third question is asked once more.

```markdown
First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Tests ASM-01, ranked 1. |
| IDEA-02 | no | Left out by the user. |
| IDEA-04 | no | Needs review: no rule supports this value. |
| IDEA-05 | no | Tests no assumption ranked 1 to 3. |
```

`Accept as proposed` on that question makes IDEA-04's row `Left out by the user.` and confirms the cut.
