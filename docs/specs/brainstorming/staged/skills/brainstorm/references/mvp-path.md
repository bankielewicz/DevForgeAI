# The MVP path: assumption risk ranking and the first release cut

How to rank the open assumptions, propose which ideas go into a first release, ask the user to confirm the
cut, and write both into the BRN. Both are proposals: the user decides. Nothing here changes an idea's
fields or an assumption's `state`.

## Contents

- [When this applies](#when-this-applies)
- [Words used here](#words-used-here)
- [Order of work at step 5](#order-of-work-at-step-5)
- [Rank the assumptions](#rank-the-assumptions)
- [Propose the first release cut](#propose-the-first-release-cut)
- [Ask question 3](#ask-question-3)
- [Write the shapes at step 6](#write-the-shapes-at-step-6)
- [Read back at step 7](#read-back-at-step-7)
- [A later confirmation, and extending a BRN](#a-later-confirmation-and-extending-a-brn)
- [Never](#never)

## When this applies

Only when the BRN you write has the project-kind line: the line `Project kind:` that opens section 1, or any line
after the frontmatter and outside every fenced block whose text, lowercased with its spaces collapsed, starts with
`project kind:`. Otherwise skip this file: write neither shape and ask no third question.

Read it at step 5, once the proposals are made, and again at steps 6 and 7. Write the BRN's
`### First release cut` block in section 6, right after the convergence prose (in a brownfield BRN the `### Already
covered`, `### Previously decided` and `### Assumption updates` blocks come after it), and its
`### Assumption risk ranking` block after the `assumptions` fence in section 7.

## Words used here

- **A** is the set of ideas whose `status` is `active`.
- **E** is the set of ideas that are `promoted` or, when their `disposition` is `open`, proposed for promotion
  in step 5's proposals. The cut has one row per idea in E. When E is empty there is no cut and no question 3.
- **An open assumption** is an assumption whose `status` is `active` and whose `state` is `open`. Their number
  is n.
- **The list of an assumption** is the ideas in E that would not deliver the value they are rated for if the
  assumption's `statement` were false. Judge it from the assumption's `statement` and each idea's `idea` and
  `addresses`. This is the one judgment in this file; the user sees it in the ranking's `If wrong` cell.
- **X needs Y** means idea X cannot deliver the value it is rated for unless idea Y exists. Judge it from the
  two `idea` texts. Only ideas in E are compared.
- **Top three** are the open assumptions ranked 1, 2 and 3, or all of them when n is less than 3.

## Order of work at step 5

1. Make the proposals as SKILL.md step 5 says. This fixes E.
2. Rank the open assumptions.
3. Propose the cut.
4. Save the work file: the proposals table, the cut block and the ranking block, with the cut's status line
   always `First release cut: proposed, not confirmed`, whatever follows.
5. Ask the form: questions 1 and 2 as SKILL.md says, then question 3 here. Question 3 is asked only when the cut
   has a row.

## Rank the assumptions

Write one row for each open assumption. With none, write the single line `None.` instead of the table.

A framework may keep its own ranking of the assumptions in section 5 (`risk-first-mvp` does). That table is the
framework's own working: it rates the test ideas and nothing else, and it is never copied into this ranking, which
is the only ranking that decides the first release cut.

**Columns.** `Rank`, `Assumption`, `If wrong`, `Confidence`, `Cheapest test`.

**`If wrong`.** Three parts: a level, the assumption's list when it is not empty, and words:

```text
Fatal (IDEA-01, IDEA-02, IDEA-04): Nobody lends, so no first-release idea works
Serious (IDEA-01): Nobody checks the list, so the list goes unused
Minor: The shed has no permit, so only the parked shed idea stops
```

- The level comes from the list and E, and from nothing else:
  - `Fatal`: the list holds every idea in E.
  - `Serious`: the list holds at least one idea in E, but not all.
  - `Minor`: the list is empty. Write no parentheses.
- Write the list in parentheses after the level, IDs in ascending order, each once, then a colon and a space.
- The words are one clause on what breaks. They hold no idea ID and no `|`.

**`Confidence`.** `high`, `medium` or `low`:

- `high`: the user gave data or a direct observation of this very thing: a problem's `evidence` (not a
  `[NEEDS CLARIFICATION]` marker) or a `sources` entry states it.
- `medium`: indirect evidence, such as a similar product or an anecdote, or the user's own statement from
  experience.
- `low`: none. It is always `low` for an assumption you added.

**Order.** Sort by three keys, in this order, and number the rows from 1 in the sorted order:

1. Level: Fatal, then Serious, then Minor.
2. Confidence: `low`, then `medium`, then `high`.
3. The assumption's number, lower first. This breaks every tie.

**`Cheapest test`.** A method word, a colon, a space, and the first sentence of the assumption's `validation`:

- The first sentence runs up to and including the first full stop followed by a space, or the whole text when
  there is none. Replace any `|` in it with `/`. Never change `validation` itself.
- The method is the first rule below that fits, read from the assumption's `statement`:
  1. It says something about today (a rate, count, price, duration or current process), and `sources` holds
     an entry of kind `data`, `document`, `ticket` or `note` about that subject: `Data`.
  2. It says what people will do with something that does not exist yet (use, finish, return, pay, switch):
     `Prototype`.
  3. It says whether something can be built, joined up or run within a stated limit: `Prototype`.
  4. Anything else, which is what people need, know, feel, do today or are willing to say: `Interview`.
- Only name the method. Never start a prototype, an interview or a data pull.

**Worked example.** E is IDEA-01, IDEA-02 and IDEA-03. Four open assumptions:

| Assumption | List | Level | Confidence |
|---|---|---|---|
| ASM-01 | IDEA-01, IDEA-02, IDEA-03 | Fatal | medium |
| ASM-02 | IDEA-03 | Serious | low |
| ASM-03 | none | Minor | low |
| ASM-04 | IDEA-02 | Serious | low |

Fatal sorts first, even though its confidence is medium: ASM-01 is rank 1. ASM-02 and ASM-04 tie on level and
confidence, so the lower number goes first: ASM-02 is rank 2 and ASM-04 rank 3. ASM-03 is Minor, so it is last,
rank 4, although its confidence is low.

## Propose the first release cut

Write one row for each idea in E, in ID order. With no idea in E, write the single line
`No idea is promoted or proposed for promotion.` instead of the table.

**The rule.** Two constants: the top three assumptions, and at most three ideas chosen by tests (`CAP`, 3).

1. **Candidates.** An idea in E is a candidate when it is in the list of a top-three assumption. Its best rank
   is the lowest rank number among those assumptions.
2. **Cut at three.** Sort the candidates by best rank (lower first), then `score` (higher first; `null` last),
   then ID (lower first). The first three are `yes`; the others are `no`.
3. **No candidate.** When there is no candidate, the idea in E with the highest `score` is `yes` (the lower ID
   on a tie). When every `score` is `null`, the lowest ID in E is `yes`. Every other idea is `no`.
4. **Needs.** Repeat until nothing changes: when an idea is `yes` and it needs idea Y in E, and Y is `no`, set Y
   to `yes`. These do not count toward the three. Every cut therefore has at least one `yes`.

**The `Why` cell.** Use these sentences exactly, each followed by `; effort E; score S`. E is the idea's `effort`
without quotes, S its `score`; write `unrated` for a `null`. The ASM-NN is the best-ranked top-three assumption
whose list holds the idea, and R its rank.

| Case | Why starts with |
|---|---|
| `yes`, a candidate | `Tests ASM-NN (rank R)` |
| `yes`, set by rule 4 | `Needed by IDEA-NN` (the lowest ID of the `yes` ideas that need it) |
| `yes`, rule 3 with a score | `Highest score in the list; no assumption ranked 1 to 3 depends on an idea` |
| `yes`, rule 3 with no score | `First idea in the list; no score and no assumption ranked 1 to 3 depends on an idea` |
| `no`, a candidate cut at three | `Tests ASM-NN (rank R) but the first release holds at most three such ideas` |
| `no`, any other | `Tests no assumption ranked 1 to 3` |

The `First idea` row ends `; effort E; score unrated`.

**Worked example.** E is IDEA-01 to IDEA-05. The ranking is: rank 1 ASM-01 (Serious, list IDEA-02 and IDEA-03),
rank 2 ASM-02 (Serious, IDEA-01), rank 3 ASM-03 (Serious, IDEA-05), rank 4 ASM-04 (Minor). Efforts and scores:
IDEA-01 medium, 3; IDEA-02 low, 4; IDEA-03 low, 4; IDEA-04 medium, 3; IDEA-05 high, 1. IDEA-01 needs IDEA-04.

- Candidates: IDEA-02 (best rank 1), IDEA-03 (1), IDEA-01 (2), IDEA-05 (3). IDEA-04 is in no list.
- Sorted: IDEA-02 (1, 4), IDEA-03 (1, 4), IDEA-01 (2, 3), IDEA-05 (3, 1). The tie on rank and score goes to the
  lower ID. The first three are `yes`; IDEA-05 is `no`.
- IDEA-01 needs IDEA-04, so IDEA-04 becomes `yes`.

```markdown
| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Tests ASM-02 (rank 2); effort medium; score 3 |
| IDEA-02 | yes | Tests ASM-01 (rank 1); effort low; score 4 |
| IDEA-03 | yes | Tests ASM-01 (rank 1); effort low; score 4 |
| IDEA-04 | yes | Needed by IDEA-01; effort medium; score 3 |
| IDEA-05 | no | Tests ASM-03 (rank 3) but the first release holds at most three such ideas; effort high; score 1 |
```

The first-release ideas are the `yes` rows. Section 8's success signals follow them: one bullet for each `yes` idea,
in ID order, or the line `- None.` when there is none. From the moment a BRN has this block, this replaces the
intake reference's transitional rule (the ideas promoted or proposed for promotion), and the validator checks it.

## Ask question 3

Ask it only when the cut has a row, as the third question of step 5's form, after "Has the brainstorm
converged?". The form stays one AskUserQuestion call tagged `devforgeai_step:5`, and the question's header is
`Step 5`.

- Question: `Confirm the first release cut?`
- Options, in this order:
  - `Accept as proposed` (Recommended), description "Write the cut as confirmed by you, with today's date."
  - `Leave it proposed`, description "Keep the cut as proposed, not confirmed. You can confirm it later."
- Each option's `preview` holds the same text: the line `First release cut (proposed)`, the cut table, a blank
  line, the line `Assumption risk ranking (riskiest first)`, the ranking table, a blank line, and the line
  `Type changes under Other, such as IDEA-02 yes or IDEA-04 no.`
- When either table has more than 10 rows, the preview holds only one line for each cut row, `IDEA-NN yes` or
  `IDEA-NN no`, and the question text ends `The reasons and the ranking are in the reply.` Then also write both
  tables in your reply before the form.

Without AskUserQuestion, show both tables in plain text, ask "Confirm the first release cut? Reply accept, leave,
or changes such as IDEA-02 yes", and end your turn.

**What each answer does.**

| Answer | Result |
|---|---|
| `Accept as proposed` | The cut may be written as confirmed (next section). |
| `Leave it proposed` | The cut is written as proposed, not confirmed. |
| Typed changes under Other | Read every `IDEA-NN yes` and `IDEA-NN no` in the text (letters in any case, separated by commas, semicolons, "and" or line breaks); ignore the rest. Set the second column of each named row, and write its `Why` as `Set by the user`. Leave every other row as it was. The cut stays proposed. Ask once more in a new form tagged step 5, holding one question, `Confirm the first release cut as changed?`, with the options `Accept as changed` and `Leave it proposed`, and the revised tables in each preview. Changes typed there are applied the same way and the cut stays proposed: never ask a third time. |
| Dismissed, or typed text that names no `IDEA-NN yes` or `IDEA-NN no` | The same as `Leave it proposed`. Confirm nothing. |

A user may set every row to `no`. Write it as the user said: the rule that a cut has a `yes` binds the proposal,
not the user.

## Write the shapes at step 6

1. **E at the write.** Take E from what you are about to write: the ideas written `promoted`, plus the ideas
   written `open` that the proposals paragraph in section 6 proposes to promote.
2. **Choose the cut.**
   - The answer was an accept, the table shown in the form has exactly the IDs of E, every one of those ideas
     is written `promoted`, and no assumption's `state` changed after the form: write the table as shown, with
     the status line `First release cut: confirmed by NAME on DATE`. NAME is the `owner` value without its
     quotes, or `the user` when `owner` is a `[NEEDS CLARIFICATION]` marker. DATE is today as `YYYY-MM-DD`.
   - Otherwise, the table shown has exactly the IDs of E and no assumption's `state` changed: write the table as
     shown, with `First release cut: proposed, not confirmed`.
   - Otherwise, run the ranking and the cut again over E and the current states, and write them with
     `First release cut: proposed, not confirmed`. Say in the reply that the cut is proposed again because the
     dispositions or assumptions changed.
   - No question was asked (the waiver, no AskUserQuestion, no user): write the table with
     `First release cut: proposed, not confirmed`.
3. **Write the ranking** from the current states and the cut's rows. When the cut was kept as shown, so is the
   ranking shown.
4. **Section 6 prose.** When the cut is proposed and has a `yes` row, end the paragraph that starts
   `Proposed, awaiting confirmation:` (or the convergence prose) with the sentence
   `The first release cut is proposed: IDEA-01, IDEA-04.` listing the `yes` ideas in ID order.
5. **Layout.** Section 6: the convergence prose, a blank line, `### First release cut`, a blank line, the status
   line, a blank line, the table or the line `No idea is promoted or proposed for promotion.`, and in a brownfield
   BRN a blank line and the blocks that follow the cut. Section 7: after
   the `assumptions` fence, a blank line, `### Assumption risk ranking`, a blank line, the table or `None.`, a
   blank line, then the open-question bullets.
6. Section 8's bullets are written from the `yes` rows, as the section's own rule says.

## Read back at step 7

After the validator passes, in addition to SKILL.md step 7 item 2:

- A line `First release cut: confirmed by` stands only when the user accepted the cut in this run's step 5, or,
  when extending, when the earlier version already held the same line and the `Idea` and `In first release`
  columns have not changed. Otherwise reset the line to `First release cut: proposed, not confirmed`.
- Every assumption `state` other than `open` stands only when the user confirmed it (an assumption update confirmed
  through question 4, or an edit the user asked for when extending; the brownfield reference, when it exists, gives
  both). A BRN built from nothing has every `state` `open`.
- Run the validator again after any reset.

## A later confirmation, and extending a BRN

- **A later confirmation.** When the user confirms later what a run left unconfirmed (SKILL.md, "Decisions that
  belong to the user"), step 5's form carries question 3 whenever the BRN's status line reads
  `First release cut: proposed, not confirmed` and the table has a row. Its tables are the BRN's, unless E at
  the write now differs from the table's rows: then run the ranking and the cut again first. Save no work file
  again. Step 6 edits the BRN in place by the rules above.
- **Extending a BRN** (version plus one). Run the ranking and the cut again from the current items. An earlier
  `confirmed by` line stays only when the new table's `Idea` and `In first release` columns equal the earlier
  table's; the `Why` cells and the ranking are always the new ones. Otherwise the status line is proposed.

## Never

- Write `First release cut: confirmed by` without the user's explicit accept.
- Call the cut decided, agreed or final anywhere in the BRN or the reply while its status line is proposed.
- Put an idea ID in the words after the colon of an `If wrong` cell.
- Change a disposition, a `reason`, a score or an assumption's `state` because of the ranking or the cut.
- Start a prototype, an interview or a data pull: the `Cheapest test` cell only names it.
