# Brainstorm skill: the MVP and prototype path

**Status:** proposal, written 2026-11-18 by claude-code (session fa59a935-ed2e-4502-b6c4-93bb6d847546) for Bryan's
review. It changes no spec, skill or plugin version. It adds BEH-30 to BEH-33, ERR-10 and VER-35 to VER-38 to
`docs/specs/spec/SPEC-001.md` (version 17 today), which take effect only in SPEC-001's next version, approved by
Bryan and built in a plugin-dev iteration (`/plugin-dev:create-plugin`, `/plugin-dev:skill-development`). Read
[README.md](README.md) first: its rules R1 to R8, shapes C-01 to C-11 and ID ranges apply here unchanged.

## Workflow steps this changes

The skill's task list is these eight steps. Their lines in SKILL.md don't change (R2). This document adds work
inside steps 4 to 7 only.

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 4. Evaluate with the framework | value, effort, risk, score | Nothing. The ranking and the cut need step 5's proposals (they decide which ideas are in the cut), so they are made in step 5 (§3, Terms and the order of work) |
| 5. Propose dispositions and ask the user to confirm | Two questions: dispositions, convergence | After the proposals: rank the open assumptions (C-07), propose the first release cut (C-05), and add question 3 to the form (C-10) |
| 6. Write the BRN | Template, frontmatter, Change Log | Write the cut (status `proposed, not confirmed` unless the user accepted it) after the convergence prose in section 6 (before C-06 and C-11 in a brownfield BRN) and the ranking after the `assumptions` fence in section 7 |
| 7. Validate the BRN | `validate_brn.py`, then the read-back | New validator checks (§3.4); the read-back resets a `confirmed` cut line the user did not accept (R3) |

## 1. Scope

**In.**

- The assumption risk ranking (C-07): its inputs, its ordering rule, the `Cheapest test` cell.
- The proposed first release cut (C-05): its rule, its `Why` cell, and question 3 of step 5's form (C-10).
- Writing both at step 6, the read-back at step 7, and the validator checks that apply to a BRN with the
  `Project kind:` line.
- That section 8's success signals (C-08) follow the cut's `yes` rows. Their content is specified in
  [intake-and-evidence.md](intake-and-evidence.md).
- Two eval cases, one unit-test group, one manual item, and a staged reference and example.

**Out.**

- Project kind (C-01), target users (C-03), success signals (C-08), sources (C-09) and the template:
  intake-and-evidence.md. Existing product, already covered, previously decided (C-02, C-06) and question 4:
  brownfield-iteration.md. The frameworks: framework-catalog.md.
- Building a prototype, running an interview or pulling data. The `Cheapest test` cell names the method only.
- What the PRD skill does with the cut and the ranking: [prd-handoff-contract.md](prd-handoff-contract.md).
- Any new field or collection in a BRN (R1), and any change to SKILL.md's eight checklist lines (R2).

**When this applies.** Only to a BRN that passes README §4's "kind gate" (the project-kind line) and its "adoption
gate" (the file holds `### First release cut` or `### Assumption risk ranking`; §3.4). A BRN that fails the kind gate
gets no ranking, no cut, no question 3 and no MV check (ERR-10, case 5); intake-and-evidence.md's IV-05 still reports
a shape heading that such a BRN holds.
Placement in section 6 follows README §4: C-04's prose, then the cut (C-05), then, in a brownfield BRN, C-06 and C-11
(owned by brownfield-iteration.md). The ranking (C-07) is in section 7.

## 2. Changes by file

Paths are under `src/claude/DevForgeAI/` unless they start with `src/tests`, `src/staging` or `docs`.

| File | Change |
|---|---|
| `skills/brainstorm/references/mvp-path.md` | New. Staged complete: [staged/skills/brainstorm/references/mvp-path.md](staged/skills/brainstorm/references/mvp-path.md) |
| `skills/brainstorm/SKILL.md` | Five edits, below. Net about +18 lines; 316 today, so 334. With the other documents' edits (README §8) it must stay at or under 400 (R2). The eight checklist lines (the fenced list) are not touched |
| `skills/brainstorm/references/work-file.md` | Two edits, below |
| `skills/brainstorm/references/output-rules.md` | One new item in the validation checklist, below |
| `skills/brainstorm/scripts/validate_brn.py` | The checks of §3.4, in one new function `check_mvp_path`, called once at the end of `check()` with the parsed `items` and the file's lines. Standard library only; no use of PyYAML, so the verdict is the same with and without it (SPEC-001 BEH-09) |
| `src/tests/brainstorm/test_validate_brn.py` | One test for each row of §3.4's table, run the three ways the file already runs every test (VER-35) |
| `evals/brainstorm/proposes-first-release-cut/`, `evals/brainstorm/ranks-assumptions-by-rule/` | New, hand-written (VER-36, VER-37) |
| `src/staging/examples/brainstorm-greenfield-mvp/` | New. Staged complete: [staged/examples/brainstorm-greenfield-mvp/](staged/examples/brainstorm-greenfield-mvp/) |
| `docs/runbooks/brainstorm-manual-test.md` | One new test for VER-38 and one row in its results table |
| `skills/brainstorm/provenance.yaml`, SKILL.md `devforgeai-version`, `plugin.json`, `.claude-plugin/marketplace.json`, the pin in `src/tests/progress/test_adapter_structure.py` | Version bumps, as README §8 lists for every build |

**SKILL.md edit 1.** Section "Decisions that belong to the user". Replace

```text
Two decisions are the user's, never yours:

- **Each idea's disposition** (`promoted`, `parked` or `rejected`) and its `reason`.
- **Convergence**: whether the brainstorm is finished (`status: converged`).

Propose both, then ask. Anything the user has not explicitly confirmed stays `disposition: open`,
`reason: null` and `status: draft`.
```

with

```text
Three decisions are the user's, never yours:

- **Each idea's disposition** (`promoted`, `parked` or `rejected`) and its `reason`.
- **Convergence**: whether the brainstorm is finished (`status: converged`).
- **The first release cut**, in a BRN with the `Project kind:` line: whether it is confirmed. It stays
  `First release cut: proposed, not confirmed` until the user accepts it ([mvp-path.md](references/mvp-path.md)).

Propose each, then ask. Anything the user has not explicitly confirmed stays `disposition: open`,
`reason: null`, `status: draft` and the cut proposed.
```

**SKILL.md edit 2.** Step 5, the sentence before the numbered list. Replace (after brownfield-iteration.md's edit 4 the
last line reads `each question with` and not `both questions with`; replace whichever stands)

```text
only in text before it (the dialog hides that text). One form tagged step 5 (Workflow, item 4),
both questions with `header: "Step 5"`:
```

with

```text
only in text before it (the dialog hides that text). When the BRN has the `Project kind:` line, first rank the
open assumptions and propose the first release cut ([mvp-path.md](references/mvp-path.md)), and save both in the
work file with the proposals. One form tagged step 5 (Workflow, item 4), each question with
`header: "Step 5"`, its questions in the order of this list:
```

and after list item 2 (`2. "Has the brainstorm converged?", options `Converged` and `Not yet`.`) add

```text
3. When the BRN has the `Project kind:` line and the cut has a row: "Confirm the first release cut?", options
   `Accept as proposed` (Recommended) and `Leave it proposed` ([mvp-path.md](references/mvp-path.md)).
```

(brownfield-iteration.md, built before this, adds its question to the same list as item 3 and the words `each question`
in place of `both questions`. This edit renumbers that item 4, so the list order is README C-10's.)

**SKILL.md edit 3.** Step 6, after item 4 (`4. **Change Log.** ...`), add

```text
5. **First release cut and ranking.** When the BRN has the `Project kind:` line, write both shapes as
   [mvp-path.md](references/mvp-path.md) says: the cut after the convergence prose in section 6 (before the brownfield
   blocks), the ranking after the `assumptions` fence in section 7. Never write `confirmed by` unless the user
   accepted the cut.
```

**SKILL.md edit 4.** Step 7 item 2. At the end of item 2, after the last sentence that the earlier builds appended (or
after `or to `status: draft`.` when none did), add

```text
   A line `First release cut: confirmed by` stands only when the user accepted the cut
   ([mvp-path.md](references/mvp-path.md)); reset any other to `First release cut: proposed, not confirmed`.
```

**SKILL.md edit 5.** "References", after the last of the `references/intake.md` and `references/brownfield.md` bullets
that the earlier builds added (after the `output-rules.md` bullet when none did):

```text
- [references/mvp-path.md](references/mvp-path.md): read at step 5 once the proposals are made, and at steps 6
  and 7, when the BRN has the `Project kind:` line.
```

**work-file.md edit 1.** In "When to write it", item 3. After `…right away.` add: `With the Project kind: line, the
proposals include the cut block and the ranking block (mvp-path.md); the cut's status line is always
First release cut: proposed, not confirmed in a work file.`

**work-file.md edit 2.** In "Its shape", after the bullet that starts "Step 5's proposals, once made", add the
bullet:

```text
- With the project-kind line: `### First release cut` after the convergence prose in section 6 and `### Assumption risk ranking`
  after the `assumptions` fence in section 7, as mvp-path.md writes them, with the cut's status line always
  `First release cut: proposed, not confirmed`, even when the BRN would write it confirmed. Section 8's bullets are
  those of the cut's `yes` ideas (this replaces the rule of intake-and-evidence.md's edit 12, which takes the ideas
  proposed for promotion).
```

**output-rules.md edit.** In "Validation checklist", after the last item that the earlier builds added (13 after
brownfield-iteration.md, 12 after intake-and-evidence.md), add the following as item 14 (13 when brownfield-iteration.md
was not built):

```text
14. In a BRN with the `Project kind:` line: section 6 has `### First release cut` with its status line and a table
    or the line `No idea is promoted or proposed for promotion.`; section 7 has `### Assumption risk ranking`
    with a table or the line `None.`; section 8 has one bullet for each `yes` row of the cut; the cut says `confirmed by`
    only where the user accepted it. The validator
    checks the shapes and their order (mvp-path.md); the read-back checks the confirmation.
```

and in "When to use this", nothing else changes.

## 3. Behaviour

Rules in this section are complete: a builder implements them without further choices. The staged
`mvp-path.md` says the same to the skill at run time. Constants: the top three assumptions (`TOP`, 3) and at most
three ideas chosen by tests (`CAP`, 3).

### Terms and the order of work

- **A**: the ideas whose `status` is `active`.
- **E**: the ideas that are `promoted`, plus those whose `disposition` is `open` and that step 5's proposals
  propose to promote. The cut has one row for each idea in E.
- **An open assumption**: `status: active` and `state: open`. Their number is n.
- **The list of an assumption**: the ideas in E that would not deliver the value they are rated for if the
  assumption's `statement` were false, judged from the `statement` and each idea's `idea` and `addresses`.
- **X needs Y**: idea X cannot deliver the value it is rated for unless idea Y exists, judged from the two `idea`
  texts, over ideas in E only.

The list and "needs" are the only two judgments in this document. R1 forbids a field that would record them, so
they are recorded where the user can see and correct them: the list in the ranking's `If wrong` cell, "needs" in
the `Needed by` text of the cut's `Why` cell. Everything else is rule.

Order at step 5: (1) the proposals, which fix E; (2) the ranking; (3) the cut; (4) save the work file with the
proposals, the cut and the ranking, the cut's status line `First release cut: proposed, not confirmed`; (5) the
form. This is why the ranking and cut are not at step 4: E does not exist before the proposals. README's workflow
table puts them at step 5, as this document does.

A framework may rank assumptions its own way (risk-first-mvp's riskiness table, section 5, written before any idea
exists). The riskiness table is this framework's own working: it rates the test ideas and nothing else, and it is
never copied into the assumption risk ranking (C-07), which is the only ranking that decides the first release cut
(C-05). C-07 is ordered by §3.1's rule only, for every framework.

### 3.1 The assumption risk ranking (C-07)

One row for each open assumption, or the line `None.` when n is 0. Columns: `Rank`, `Assumption`, `If wrong`,
`Confidence`, `Cheapest test`.

**`If wrong`**: `<Level>` then, when the list is not empty, ` (IDEA-NN, IDEA-NN)` with each ID of the list once in
ascending order, then `: ` and one clause saying what breaks. The clause holds no `IDEA-` and no `|`.

| Level | Rule (E is the cut's rows) |
|---|---|
| `Fatal` | The list holds every idea in E (and E is not empty). No first-release idea works if the assumption is wrong |
| `Serious` | The list holds at least one idea in E but not all of them |
| `Minor` | The list is empty. Write no parentheses. With E empty every assumption is `Minor` |

**`Confidence`** (the definitions of risk-first-mvp, which C-07 shares):

| Value | When |
|---|---|
| `high` | The user gave data or a direct observation of this very thing: a problem's `evidence` that is not a `[NEEDS CLARIFICATION]` marker, or a `sources` entry, states it |
| `medium` | Indirect evidence, such as a similar product or an anecdote, or the user's own statement from experience |
| `low` | None. Always `low` for an assumption the skill added |

**Order.** Sort by (1) level: Fatal, Serious, Minor; (2) confidence: `low`, `medium`, `high`; (3) assumption number,
lower first. Rank is the position in the sorted order, from 1. Level comes first, so a Fatal assumption with
`medium` confidence ranks above a Serious one with `low` confidence. Confidence comes before the number, so a
`low` assumption ranks above a `medium` one of the same level. The number breaks every tie, so the order is total.

**Worked example.** E is IDEA-01, IDEA-02, IDEA-03. Four open assumptions:

| Assumption | List | Level | Confidence | Sort key | Rank |
|---|---|---|---|---|---|
| ASM-01 | IDEA-01, IDEA-02, IDEA-03 | Fatal | medium | (Fatal, medium, 01) | 1 |
| ASM-02 | IDEA-03 | Serious | low | (Serious, low, 02) | 2 |
| ASM-03 | none | Minor | low | (Minor, low, 03) | 4 |
| ASM-04 | IDEA-02 | Serious | low | (Serious, low, 04) | 3 |

```markdown
| Rank | Assumption | If wrong | Confidence | Cheapest test |
|---|---|---|---|---|
| 1 | ASM-01 | Fatal (IDEA-01, IDEA-02, IDEA-03): Nobody orders for the team, so no idea works | medium | Interview: Ask ten office managers whether they order for the whole team. |
| 2 | ASM-02 | Serious (IDEA-03): Teams will not pay the premium, so the premium plan fails | low | Interview: Show the price to ten teams and ask whether they would pay it. |
| 3 | ASM-04 | Serious (IDEA-02): The kitchen is not ready by 11:30, so the delivery promise fails | low | Prototype: Cook and deliver forty meals to one office for a week. |
| 4 | ASM-03 | Minor: Nobody wants badges, so only the parked badge idea stops | low | Interview: Ask ten teams whether a badge would change how they order. |
```

ASM-01 (Fatal) is first although its confidence is `medium`. ASM-02 and ASM-04 tie on level and confidence, so the
lower number goes first. ASM-03 is last although its confidence is `low`, because it is Minor.

**`Cheapest test`**: a method word, `: `, and the first sentence of the assumption's `validation`. The first
sentence runs up to and including the first full stop followed by a space, or the whole value when it has none; a
`|` in it is written `/`. `validation` itself is never changed. The `validation` field holds the full experiment
(its first sentence the test, its second the pass line, as risk-first-mvp writes it); the cell is its short form.
The method is the first rule that fits, read from the `statement`:

| # | The statement | Method |
|---|---|---|
| 1 | Says something about today (a rate, count, price, duration, current process) and `sources` holds an entry of kind `data`, `document`, `ticket` or `note` about that subject | `Data` |
| 2 | Says what people will do with something that does not exist yet (use, finish, return, pay, switch) | `Prototype` |
| 3 | Says whether something can be built, joined up or run within a stated limit | `Prototype` |
| 4 | Anything else: what people need, know, feel, do today or are willing to say | `Interview` |

### 3.2 The proposed first release cut (C-05)

One row for each idea in E, in ID order, or the line `No idea is promoted or proposed for promotion.` when E is
empty. Columns: `Idea`, `In first release`, `Why`.

**Which ideas are `yes`**, in this order:

1. **Candidates.** An idea in E is a candidate when it is in the list of a top-three assumption (ranks 1 to 3, or
   all when n is less than 3). Its best rank is the lowest rank number among those assumptions.
2. **Cut at `CAP`.** Sort the candidates by best rank (lower first), then `score` (higher first, `null` last), then
   ID (lower first). The first three are `yes`; every other idea is `no`. A score never comes from a framework's
   formula here: the field is read as it stands.
3. **No candidate** (every list of the top three is empty, or n is 0). The idea in E with the highest non-null
   `score` is `yes`, the lower ID on a tie. When every `score` is `null`, the lowest ID in E is `yes`. Every other
   idea is `no`. So a cut with a row always has a `yes`.
4. **Needs.** Repeat until nothing changes: when an idea is `yes` and it needs an idea Y in E that is `no`, Y becomes
   `yes`. These ideas do not count toward `CAP`. Ideas that need each other are both `yes` once one is.

The minimum of one `yes` binds this proposal only. A user may set every row to `no` (§3.3).

**The `Why` cell** is one of these sentences, then `; effort E; score S`. E is the idea's `effort` without quotes,
S its `score`; either is `unrated` when `null`. The row `First idea in the list` ends `; effort E; score unrated`.
ASM-NN is the best-ranked top-three assumption whose list holds the idea, R its rank.

| Case | Why starts with |
|---|---|
| `yes`, a candidate | `Tests ASM-NN (rank R)` |
| `yes`, by rule 4 | `Needed by IDEA-NN` (the lowest ID among the `yes` ideas that need it) |
| `yes`, rule 3, with a score | `Highest score in the list; no assumption ranked 1 to 3 depends on an idea` |
| `yes`, rule 3, no score | `First idea in the list; no score and no assumption ranked 1 to 3 depends on an idea` |
| `no`, a candidate cut at `CAP` | `Tests ASM-NN (rank R) but the first release holds at most three such ideas` |
| `no`, any other | `Tests no assumption ranked 1 to 3` |
| Any row the user changed | `Set by the user` (no ending) |

**Worked example.** E is IDEA-01 to IDEA-05. Ranking: 1 ASM-01 (Serious, IDEA-02 and IDEA-03), 2 ASM-02 (Serious,
IDEA-01), 3 ASM-03 (Serious, IDEA-05), 4 ASM-04 (Minor). Effort and score: IDEA-01 medium, 3; IDEA-02 low, 4;
IDEA-03 low, 4; IDEA-04 medium, 3; IDEA-05 high, 1. IDEA-01 needs IDEA-04.

| Idea | Best rank | Sort key (rank, score, ID) | Result |
|---|---|---|---|
| IDEA-02 | 1 (ASM-01) | (1, 4, 02) | `yes` |
| IDEA-03 | 1 (ASM-01) | (1, 4, 03) | `yes`: the tie on rank and score goes to the lower ID |
| IDEA-01 | 2 (ASM-02) | (2, 3, 01) | `yes` |
| IDEA-05 | 3 (ASM-03) | (3, 1, 05) | `no`: a fourth candidate, cut at three |
| IDEA-04 | none | not a candidate | `no` by rule 2, then `yes` by rule 4 because IDEA-01 needs it |

```markdown
| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Tests ASM-02 (rank 2); effort medium; score 3 |
| IDEA-02 | yes | Tests ASM-01 (rank 1); effort low; score 4 |
| IDEA-03 | yes | Tests ASM-01 (rank 1); effort low; score 4 |
| IDEA-04 | yes | Needed by IDEA-01; effort medium; score 3 |
| IDEA-05 | no | Tests ASM-03 (rank 3) but the first release holds at most three such ideas; effort high; score 1 |
```

Four `yes` rows: three by test, one by need. The staged example
[BRN-001.md](staged/examples/brainstorm-greenfield-mvp/BRN-001.md) shows a second case: three of four candidates
are `yes` and one is cut at three.

**Success signals** (C-08) follow the `yes` rows, one bullet each, whether or not the cut is confirmed
(README R7). The content is intake-and-evidence.md's. Once a BRN has the cut, this replaces intake-and-evidence.md's
transitional rule (while a BRN has no C-05 table, the first-release ideas are the ideas promoted or proposed for
promotion), and MV-30 checks it (§3.4).

**Section 6 prose.** When the cut is proposed and has a `yes` row, the convergence paragraph that starts
`Proposed, awaiting confirmation:` (or, after a partial confirmation, the prose) ends with the sentence
`The first release cut is proposed: IDEA-01, IDEA-04.` listing the `yes` ideas in ID order.

### 3.3 Confirmation: question 3 of step 5's form (C-10)

Asked when E is not empty, with AskUserQuestion available and the user answering (not under the waiver's
*Proceed without questions*). It is the third question of the form tagged `devforgeai_step:5`, after
"Has the brainstorm converged?", and has `header: "Step 5"`.

- Question text: `Confirm the first release cut?`
- Options, in this order: `Accept as proposed` (Recommended), description "Write the cut as confirmed by you,
  with today's date."; `Leave it proposed`, description "Keep the cut as proposed, not confirmed. You can confirm
  it later."
- Each option's `preview` holds the same text: the line `First release cut (proposed)`, the cut table, a blank
  line, the line `Assumption risk ranking (riskiest first)`, the ranking table, a blank line, and the line
  `Type changes under Other, such as IDEA-02 yes or IDEA-04 no.`
- When either table has more than 10 rows, the preview holds one line for each cut row (`IDEA-NN yes` or
  `IDEA-NN no`), the question text ends `The reasons and the ranking are in the reply.`, and both tables are
  written in the reply before the form.

Without AskUserQuestion the skill shows both tables in plain text, asks "Confirm the first release cut? Reply
accept, leave, or changes such as IDEA-02 yes", and ends its turn; the reply is the answer.

| Answer | Writes |
|---|---|
| `Accept as proposed` | The cut may be written confirmed (the rule after this table) |
| `Leave it proposed` | `First release cut: proposed, not confirmed` |
| Typed under Other | Every `IDEA-NN yes` and `IDEA-NN no` in the text (any letter case; separated by commas, semicolons, "and" or line breaks) sets that row's second column, and its `Why` becomes `Set by the user`; other rows stay; other text is ignored. The cut stays proposed. The skill asks once more, in a new form tagged step 5 with one question `Confirm the first release cut as changed?` and the options `Accept as changed` and `Leave it proposed`, the revised tables in each preview. Changes typed there are applied the same way and the cut stays proposed: never a third form |
| Dismissed, or text naming no `IDEA-NN yes` or `IDEA-NN no` | As `Leave it proposed` |
| No question asked (waiver, no AskUserQuestion, no user) | `First release cut: proposed, not confirmed`, and the section 6 sentence of §3.2 |

**At step 6**, E is recomputed from what is about to be written (the `promoted` ideas, plus the `open` ones the
proposals paragraph proposes to promote). Then:

1. The answer was an accept, the table shown has exactly E's IDs, every one of those ideas is written `promoted`,
   and no assumption's `state` changed after the form: write the table as shown with
   `First release cut: confirmed by NAME on DATE`. NAME is the frontmatter `owner` without its quotes, or `the
   user` when `owner` is a `[NEEDS CLARIFICATION]` marker. DATE is today, `YYYY-MM-DD`.
2. Otherwise, the table shown has exactly E's IDs and no `state` changed: write the table as shown,
   `First release cut: proposed, not confirmed`. This is what happens when the user accepted the cut but left an
   idea `open` (question 1 *Leave them open*): a cut is never `confirmed` over ideas that are not promoted.
3. Otherwise: run §3.1 and §3.2 again over E and the current states, write them `proposed, not confirmed`, and say in
   the reply that the cut is proposed again because the dispositions or assumptions changed.
4. The ranking is written from the current states and the cut's rows; when the cut was kept as shown, so is the
   ranking shown.

**A later confirmation** (SKILL.md, "Decisions that belong to the user"): when the user confirms later what a run
left unconfirmed, the step-5 form carries question 3 whenever the BRN's status line reads `proposed, not
confirmed` and the table has a row. Its tables are the BRN's, unless E at the write now differs from the table's
rows: then §3.1 and §3.2 run again first. No work file is saved again. Step 6 edits the BRN in place by the rules
above.

**Extending a BRN**: §3.1 and §3.2 run again from the current items. An earlier `confirmed by` line stays only
when the new table's `Idea` and `In first release` columns equal the earlier table's; the `Why` cells and the
ranking are always the new ones. Otherwise the line is `proposed, not confirmed`.

### 3.4 Step 7: read-back and validator

**Read-back** (R3), after the validator passes, in addition to SKILL.md step 7 item 2: a line
`First release cut: confirmed by` stands only when the user accepted the cut in this run's step 5, or, when
extending, when the earlier version held the same line and the two columns have not changed; reset any other to
`First release cut: proposed, not confirmed`. Every assumption `state` other than `open` stands only when the user
confirmed it (a C-11 row confirmed through question 4, or an edit the user asked for when extending; brownfield-iteration.md); a BRN built from nothing has every `state` `open`. Run the
validator again after any reset.

**Validator additions.** Two gates, both required, as README §4 states them (the kind gate, which is
intake-and-evidence.md's IV-01, and the adoption gate). A BRN that passes the kind gate but holds neither heading was
written by a build that stops before this one; it stays valid and none of the checks runs. A BRN that holds one
heading must hold both (MV-01, MV-15). Without the kind gate none runs.
Conventions: the sections are found by their exact heading lines (`## 6. Convergence`,
`## 7. Assumptions and open questions`, which the validator already requires); a table is the consecutive lines that
start with `|`; its cells are the text between `|` characters, trimmed; line numbers are the file's, from 1. Each
message prints in the validator's form, `line N: <message>`. "The cut's rows" are the IDs in the cut table's first
column. Ideas and assumptions come from the parsing the validator already does for its item blocks.

| # | Check | Line N | Message |
|---|---|---|---|
| MV-01 | Section 6 holds the line `### First release cut` | `## 6. Convergence` | `a BRN with a Project kind line needs '### First release cut' in section 6` |
| MV-02 | The first non-blank line after it is `First release cut: proposed, not confirmed` or matches `^First release cut: confirmed by \S.* on \d{4}-\d{2}-\d{2}$` | that line, else the heading | `the first release cut needs the status line 'First release cut: proposed, not confirmed' or 'First release cut: confirmed by NAME on YYYY-MM-DD'` |
| MV-03 | The date in a `confirmed by` line is a real calendar date | the status line | `the first release cut date DATE is not a real calendar date` |
| MV-04 | After the status line (blank lines skipped) comes the line `No idea is promoted or proposed for promotion.` or the header `\| Idea \| In first release \| Why \|` and the separator `\|---\|---\|---\|` | that line, else the heading | `the first release cut needs the table '\| Idea \| In first release \| Why \|' or the line 'No idea is promoted or proposed for promotion.'` |
| MV-05 | Each row has 3 cells | the row | `first release cut row has N cells, expected 3` |
| MV-06 | The first cell is `IDEA-` and two digits | the row | `first release cut row must start with an idea ID, not 'X'` |
| MV-07 | That idea exists and its `status` is `active` | the row | `first release cut row IDEA-NN is not an active idea of this document` |
| MV-08 | Its `disposition` is not `parked` or `rejected` | the row | `first release cut row IDEA-NN is parked, so it can't be in the cut` (`rejected` likewise) |
| MV-09 | Row IDs ascend and none repeats | the row | `first release cut rows must be unique and in ID order` |
| MV-10 | The second cell is `yes` or `no` | the row | `'In first release' must be yes or no, not 'X'` |
| MV-11 | The third cell is not empty | the row | `first release cut row IDEA-NN has an empty Why` |
| MV-12 | With the `No idea ...` line, no active idea is `promoted` | that line | `the cut says no idea is promoted, but IDEA-NN is promoted` (the lowest such ID) |
| MV-13 | A `confirmed by` line is not followed by the `No idea ...` line | the status line | `a first release cut with no rows can't be confirmed` |
| MV-14 | With a `confirmed by` line, the cut's rows are exactly the active ideas whose `disposition` is `promoted` | the status line | `a confirmed first release cut must list exactly the promoted ideas (missing: IDEA-NN, IDEA-NN; extra: IDEA-NN)`, `none` for an empty list |
| MV-15 | Section 7 holds the line `### Assumption risk ranking` | `## 7. Assumptions and open questions` | `a BRN with a Project kind line needs '### Assumption risk ranking' in section 7` |
| MV-16 | The first non-blank line after it is `None.` or the header `\| Rank \| Assumption \| If wrong \| Confidence \| Cheapest test \|` and the separator `\|---\|---\|---\|---\|---\|` | that line, else the heading | `the assumption risk ranking needs the table '\| Rank \| Assumption \| If wrong \| Confidence \| Cheapest test \|' or the line 'None.'` |
| MV-17 | With `None.`, no assumption is active with `state: open` | that line | `the ranking says None. but ASM-NN is active and open` (the lowest such ID) |
| MV-18 | Each row has 5 cells | the row | `ranking row has N cells, expected 5` |
| MV-19 | The first cell is the row's position, 1, 2, 3 and so on | the row | `rank must be K, not 'X'` |
| MV-20 | The second cell is an active assumption with `state: open` | the row | `ranking row ASM-NN is not an active assumption with state open` |
| MV-21 | No assumption appears twice | the second row | `ASM-NN is ranked twice` |
| MV-22 | The fourth cell is `high`, `medium` or `low` | the row | `Confidence must be high, medium or low, not 'X'` |
| MV-23 | The fifth cell matches `^(Data\|Prototype\|Interview): \S` | the row | `'Cheapest test' must start with 'Data: ', 'Prototype: ' or 'Interview: ' and then words` |
| MV-24 | The third cell matches `^(Fatal\|Serious\|Minor)( \(IDEA-\d{2}(, IDEA-\d{2})*\))?: \S.*$` and the words after the colon hold no `IDEA-` and no `\|` | the row | `'If wrong' must be a level (Fatal, Serious or Minor), an optional list of idea IDs in parentheses, ': ', then words with no idea ID` |
| MV-25 | The listed IDs ascend, none twice | the row | `'If wrong' must list each idea once, in ID order` |
| MV-26 | Every listed ID is a row of the cut | the row | `'If wrong' lists IDEA-NN, which is not a row of the first release cut` |
| MV-27 | With K rows in the cut and J of them listed: level is `Minor` when J is 0, `Fatal` when J equals K, else `Serious` | the row | `'If wrong' says L, but the listed ideas make it W (the cut has K rows, the list names J of them)` |
| MV-28 | Compare consecutive rows that passed MV-22 and MV-24 by (level, confidence, assumption number) with Fatal < Serious < Minor and low < medium < high; each row's key is at least the previous | the later row | `ASM-NN must be ranked before ASM-MM (level, then confidence low first, then assumption number)` |
| MV-29 | Every assumption that is active with `state: open` is in the ranking (not run with `None.`) | the heading | `active open assumption ASM-NN is missing from the ranking` (once for each) |
| MV-30 | When the cut heading is present and the cut has rows or the `No idea ...` line: the section 8 bullets that start `- IDEA-NN:` name exactly the cut's `yes` ideas, once each, in the cut's order (none, or the line `- None.`, when it has no `yes` row). The shape of each bullet is intake-and-evidence.md's check | `## 8. Candidate success signals` | `section 8 must hold one bullet for each first release idea, in ID order (expected: IDEA-01, IDEA-04; found: IDEA-01)`, `none` for an empty list |

MV-26 and MV-27 run only when the cut heading is present, so a missing cut reports MV-01 alone.

**MV-30 replaces the transitional rule.** intake-and-evidence.md, built before this document, says that while a BRN has
no C-05 table the first-release ideas are the ideas promoted or proposed for promotion, and checks only the shape of
section 8's bullets. From the first BRN that has the `### First release cut` heading the first-release ideas are
exactly the cut's `yes` rows (README R7), and MV-30 checks it. The skill writes section 8 from the `yes` rows (§3.2).

A prototype of MV-01 to MV-30, written in the scratch folder while drafting this document, passes the staged example
and the three PRD-eval fixtures and, for eleven one-line changes to the example (rows swapped, a level changed, a bad
confidence value, an impossible date, a `parked` idea in a confirmed cut, a missing method word, a missing row, a
`maybe`, one heading removed (twice, each heading), a section 8 bullet changed), prints the message of the check each
one breaks. Three also trip a check that follows from the first (a changed level changes the order; a swapped idea
changes the list checks and section 8). It also confirms the gates: a BRN with no project-kind line, one whose line is
written `PROJECT   KIND:greenfield`, and one with the line but neither heading, all print nothing. It is not part of the repository; the builder writes the real function first,
test by test (VER-35).

### 3.5 The items

```yaml items
behaviors:
  - id: BEH-30
    status: proposed
    rule: "In a BRN with the Project kind: line, after step 5's proposals, rank the open assumptions and write the ranking as C-07's table (or the line None. when no assumption is active and open). For each row: Level is Fatal when the assumption's list (the ideas in E that would not deliver their rated value if its statement were false) holds every idea in E, Serious when it holds some but not all, Minor when it holds none, where E is the ideas promoted or proposed for promotion (§3, Terms and the order of work); the If wrong cell is the level, the list in parentheses in ascending ID order when not empty, a colon, and one clause with no idea ID and no pipe. Confidence is high (the user gave data or a direct observation of this very thing: a problem's evidence that is not a marker, or a sources entry), medium (indirect evidence or the user's own statement from experience) or low (none; always for an assumption the skill added). Order the rows by level (Fatal, Serious, Minor), then confidence (low, medium, high), then assumption number; rank is the position from 1. Cheapest test is Data, Prototype or Interview, a colon and a space, and the first sentence of the assumption's validation (up to and including the first full stop followed by a space, or all of it; a pipe written as a slash), the method being the first rule that fits: 1 Data when the statement is about today and sources holds an entry of kind data, document, ticket or note about it; 2 Prototype when it is about what people will do with something that does not exist; 3 Prototype when it is about whether something can be built or run within a stated limit; 4 Interview otherwise. Never change validation, and never start a prototype, interview or data pull. A framework's own ranking is never copied into the table."
    changes: new
    lands_in: "skills/brainstorm/references/mvp-path.md, 'Rank the assumptions'; output-rules.md checklist item 14"
  - id: BEH-31
    status: proposed
    rule: "In a BRN with the Project kind: line, after the ranking, propose the first release cut as C-05's table with one row for each idea in E in ID order (or the line No idea is promoted or proposed for promotion. when E is empty). Candidates are the ideas in E in the list of a top-three assumption (ranks 1 to 3); sort them by best rank, then score (higher first, null last), then ID; the first three are yes and all other ideas no. With no candidate, the idea in E with the highest non-null score (lower ID on a tie; the lowest ID when every score is null) is yes. Then every idea that a yes idea needs and that is no becomes yes, repeatedly, without counting toward the three. A cut with a row therefore has at least one yes. The Why cell is one fixed sentence of §3.2's table followed by '; effort E; score S' (unrated for null). Section 8's success signals follow the yes rows. When the cut is proposed and has a yes row, the section 6 convergence prose ends with 'The first release cut is proposed: IDEA-NN, ...' listing the yes ideas."
    changes: new
    lands_in: "skills/brainstorm/references/mvp-path.md, 'Propose the first release cut'"
  - id: BEH-32
    status: proposed
    rule: "Ask question 3 of step 5's form (README C-10) when E is not empty and the user is answering: header 'Step 5', text 'Confirm the first release cut?', options 'Accept as proposed' (Recommended) and 'Leave it proposed', each option's preview holding the cut table and the ranking table (or, over 10 rows in either, one 'IDEA-NN yes|no' line per cut row, with the question text ending 'The reasons and the ranking are in the reply.' and both tables in the reply). Accept as proposed lets the cut be written confirmed; Leave it proposed, a dismissal and text naming no 'IDEA-NN yes|no' write it proposed; typed 'IDEA-NN yes|no' changes set those rows ('Set by the user'), keep the cut proposed and lead to one more form with 'Confirm the first release cut as changed?' (options 'Accept as changed', 'Leave it proposed'), never a third. At step 6 write 'First release cut: confirmed by NAME on DATE' (NAME the owner, or 'the user' when the owner is a marker) only when an accept was given, the table shown has exactly the IDs of E at the write, every one of those ideas is written promoted and no assumption state changed after the form; with the same table but any other condition write 'First release cut: proposed, not confirmed'; with a different set of IDs run the ranking and the cut again and write them proposed, saying so. Without a question (waiver, no AskUserQuestion, no user) write it proposed. A later confirmation adds question 3 to the step-5 form whenever the status line is proposed and the table has a row; extending a BRN runs both again and keeps an earlier confirmed line only when the Idea and In first release columns are unchanged. A work file always holds the proposed line."
    changes: "extends SPEC-001 BEH-06 (the step-5 form) and the 'Decisions that belong to the user' rule"
    lands_in: "SKILL.md edits 1 to 3 and skills/brainstorm/references/mvp-path.md, 'Ask question 3' and 'Write the shapes at step 6'; work-file.md edits"
  - id: BEH-33
    status: proposed
    rule: "Step 7's read-back (R3) resets a 'First release cut: confirmed by' line to 'First release cut: proposed, not confirmed' unless the user accepted the cut in this run's step 5 or, when extending, the earlier version held the same line and the Idea and In first release columns are unchanged; every assumption state other than open stands only when the user confirmed it. validate_brn.py, only for a file that passes the kind gate (a line after the frontmatter and outside every fenced block whose text, lowercased with spaces collapsed, starts with 'project kind:') and the adoption gate (the line '### First release cut' or '### Assumption risk ranking'), runs checks MV-01 to MV-30 of §3.4 with their exact messages, MV-30 being that section 8's idea bullets equal the cut's yes rows, standard library only and with no use of PyYAML, so its verdict is the same with and without it; for any other file its output is unchanged."
    changes: "extends SPEC-001 BEH-09 (validation and the read-back)"
    lands_in: "scripts/validate_brn.py (check_mvp_path); SKILL.md edit 4; mvp-path.md, 'Read back at step 7'; output-rules.md item 14"
```

## 4. Errors and edge cases

```yaml items
errors:
  - id: ERR-10
    status: proposed
    condition: "An input of the ranking or the cut is missing or unusual (cases 1 to 9 below)"
    handling: "Case 1, E is empty (no idea promoted or proposed): write the line 'No idea is promoted or proposed for promotion.' under the status line 'First release cut: proposed, not confirmed', ask no question 3, write every ranking row as Minor. Case 2, no open assumption: write 'None.' as the ranking; the cut uses its no-candidate rule (BEH-31) and says 'no assumption ranked 1 to 3 depends on an idea'. Case 3, the user accepted the cut but left an idea open: write the table as shown with the proposed line (BEH-32, rule 2). Case 4, the user typed changes that make every row no: write them as typed with 'Set by the user'; the minimum of one yes binds the proposal only. Case 5, the BRN fails the kind gate (any BRN from before intake-and-evidence.md), or passes it but holds neither '### First release cut' nor '### Assumption risk ranking' (a BRN written by a build that stops before this one): none of this applies, no MV check runs, and the PRD skill treats it as it does today (a BRN that fails the kind gate but holds one of the new headings is still reported by intake-and-evidence.md's IV-05). Case 6, typed text in question 3 names an idea that is not a row of the cut, or a word other than yes or no: ignore that part and list what was ignored in the reply. Case 7, a validation text with a pipe: write the pipe as a slash in the cell. Case 8, an assumption's own state changes in the same run: only a run that extends a BRN edits that BRN's assumption states in place (question 4 only sets the status of C-11 rows about earlier BRNs' assumptions, so a new BRN needs no recompute after it): run the ranking and the cut again from the current items at step 6 (BEH-32, rule 3). Case 9, an extended BRN holds C-06 and C-11 in section 6: the cut stays after C-04's prose and before them, and its table ends at the first blank line."
    user_result: "A BRN whose two shapes are always present in the same form, a cut never worded as confirmed without the user's accept, and no behaviour change for earlier BRNs"
    changes: "new"
    lands_in: "skills/brainstorm/references/mvp-path.md ('Ask question 3', 'Write the shapes at step 6'); scripts/validate_brn.py (check_mvp_path)"
```

## 5. Verification

Eval cases are hand-written under `src/claude/DevForgeAI/evals/brainstorm/`, one folder each, with `prompt.md` and
`graders/*.md`, tagged `brainstorm` and `ver-NN`, like the existing cases. Neither needs a scaffold. Eval runs have
no user to answer (R5): both prompts say to skip questions, and VER-36 grades the unconfirmed form. Every regex
below was run with `node` against the staged example and against a variant of it written in the unconfirmed form
(status `draft`, every idea `open`, `First release cut: proposed, not confirmed`), as `.claude/rules/evals.md`
requires: graders (3), (4), (6), (10), (11) and (12) of VER-36 pass on the variant and fail on the confirmed
example, as they should, and graders (7) and (9) of VER-36 and (4) to (7) of VER-37 fail on one-line changes made to
break each. The builder repeats that against the files it writes, after the cases are made.

```yaml items
verifications:
  - id: VER-35
    status: proposed
    covers:
      - BEH-33
      - ERR-10
    level: unit
    obligation: "src/tests/brainstorm/test_validate_brn.py gains, for each of MV-01 to MV-30, one test that changes the staged example (src/staging/examples/brainstorm-greenfield-mvp/BRN-001.md, read from disk) so that only that check fails and asserts the exact message and its line; one test that the unchanged example prints OK; one that a BRN failing the kind gate (the file's own VALID text and the repository's docs/specs/brainstorm/BRN-001.md) prints what it printed before; one that the 'None.' and 'No idea is promoted or proposed for promotion.' forms pass; one that the 'Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]' form passes the kind gate and the MV checks run on it, and one that the spelling 'PROJECT   KIND:greenfield' also switches the gate on (intake-and-evidence.md's IV-02 reports the spelling, and the MV checks run when a heading is present); one that a line inside a fenced block or in the frontmatter does not, and a prose line `Project kinds vary.` does not; one that a BRN passing the kind gate but holding neither heading prints OK unchanged (the adoption gate); one that removing either heading alone reports MV-01 or MV-15 only. Each runs the three ways the file already runs every test (with this interpreter's packages, with a throwaway HOME, and with -S), and the verdict must be the same in all three. The tests are written before the checks and fail until they exist."
  - id: VER-36
    status: proposed
    covers:
      - BEH-30
      - BEH-31
      - BEH-32
      - BEH-33
    level: eval
    obligation: |-
      With nobody to confirm, the BRN holds the cut proposed, never confirmed, and the ranking, each in its fixed shape.
      Every grader is on docs/specs/brainstorm/BRN-001.md unless it says last_message. The rows of risk-first-mvp's
      riskiness table in section 5 are not rows of the ranking: grader ranking-row-shape skips them.
    case: proposes-first-release-cut
    prompt: |-
      I am starting a new product from scratch and nothing is built or sold yet: an app that helps people in a shared flat split bills and chores. Brainstorm what to build first for an MVP and what could make the idea fail. Skip any questions and write it up.
    scaffold: none
    frontmatter: "as writes-valid-brn: max_turns 60, timeout_seconds 900, allowed_tools Skill, Read, Glob, Grep, Write, Edit, Bash"
    graders:
      - name: brn-exists
        type: file_exists
        path: docs/specs/brainstorm/BRN-001.md
        exists: true
      - name: cut-heading
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: contains
        flags: m
        pattern: |-
          ^### First release cut[ \t]*$
      - name: cut-status-proposed
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: contains
        flags: m
        pattern: |-
          ^First release cut: proposed, not confirmed[ \t]*$
      - name: cut-not-confirmed
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        flags: m
        pattern: |-
          ^First release cut: confirmed
      - name: has-yes-row
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: contains
        flags: m
        pattern: |-
          ^\| IDEA-\d{2} \| yes \| \S
      - name: cut-block-shape
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: contains
        flags: m
        pattern: |-
          ^### First release cut[ \t]*\n\nFirst release cut: proposed, not confirmed[ \t]*\n\n\| Idea \| In first release \| Why \|\n\|---\|---\|---\|\n(?:\| IDEA-\d{2} \| (?:yes|no) \| [^\n]+\n)+
      - name: why-sentences
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        flags: m
        pattern: |-
          ^\| IDEA-\d{2} \| (?:yes|no) \| (?!Tests ASM-\d{2} \(rank \d+\)|Needed by IDEA-\d{2}|Highest score in the list; |First idea in the list; |Tests no assumption ranked 1 to 3)
      - name: ranking-block-shape
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: contains
        flags: m
        pattern: |-
          ^### Assumption risk ranking[ \t]*\n\n\| Rank \| Assumption \| If wrong \| Confidence \| Cheapest test \|\n\|---\|---\|---\|---\|---\|\n\| 1 \| ASM-\d{2} \| (?:Fatal|Serious|Minor)(?: \(IDEA-\d{2}(?:, IDEA-\d{2})*\))?: \S[^|\n]* \| (?:high|medium|low) \| (?:Data|Prototype|Interview): \S[^\n]* \|[ \t]*\n
      - name: ranking-row-shape
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        flags: m
        pattern: |-
          ^\| \d+ \| ASM-\d{2} \| (?![^|\n]* \| (?:high|medium|low) \| (?:high|medium|low) \| [1-9] \|[ \t]*$)(?!(?:Fatal|Serious|Minor)(?: \(IDEA-\d{2}(?:, IDEA-\d{2})*\))?: \S[^|\n]* \| (?:high|medium|low) \| (?:Data|Prototype|Interview): \S)
      - name: cut-sentence-in-prose
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: contains
        pattern: |-
          The first release cut is proposed: IDEA-\d{2}(?:, IDEA-\d{2})*\.
      - name: no-decided-disposition
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        pattern: |-
          disposition:[ \t]*["]?(?:promoted|parked|rejected)
      - name: not-converged
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        flags: m
        pattern: |-
          ^status:[ \t]*["]?converged
      - name: ran-validator-alone
        type: tool_used
        tool: Bash
        input_match: '"command"\s*:\s*"(?:[^"\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*validate_brn\.py(?:[^"\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*"'
      - name: cut-agrees-with-ranking
        type: llm
        focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        question: |-
          PASS if every ideas block is valid for the skill's output rules, the cut's yes rows and Why cells agree with the ranking (a row that says Tests ASM-NN (rank R) names an assumption ranked R whose If wrong list holds that idea), and the Project kind line says greenfield; FAIL otherwise, quoting the row.
  - id: VER-37
    status: proposed
    covers:
      - BEH-30
    level: eval
    obligation: |-
      The four beliefs of the prompt are the only assumptions. The ranking's rows are in the order of §3.1 and each has
      its Confidence and Cheapest test as the rules give. Order is checked by the regex graders 4 to 7 because the
      prompt can't fix the level.
    case: ranks-assumptions-by-rule
    prompt: |-
      A friend and I are starting a meal-kit service for office teams; nothing is built or sold yet. Brainstorm what to build first for an MVP. Use exactly these four beliefs as the assumptions and add no others: first, offices will order for a whole team at once, but nobody has measured that; second, our kitchen can deliver by 11:30 for orders placed by 09:00, and in a three-week trial we delivered on time for 57 of 60 meals; third, teams will pay 20 percent more than lunch delivery costs, and a pilot with 40 people last month showed that they would; fourth, teams will want a loyalty badge, which is only a hunch. Skip any questions and write it up.
    scaffold: none
    frontmatter: "as VER-36"
    graders:
      - {name: ranking-block-shape, type: regex, note: "VER-36's grader of that name, unchanged"}
      - {name: ranking-row-shape, type: regex, note: "VER-36's grader of that name, unchanged"}
      - name: rank-4-exists
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: contains
        flags: m
        pattern: |-
          ^\| 4 \| ASM-\d{2} \|
      - name: no-rank-5
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        flags: m
        pattern: |-
          ^\| 5 \| ASM-
      - name: fatal-not-after-lower
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        flags: m
        pattern: |-
          ^\| \d \| ASM-\d{2} \| (?:Serious|Minor)[^\n]*\n\| \d \| ASM-\d{2} \| Fatal
      - name: minor-not-before-higher
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        flags: m
        pattern: |-
          ^\| \d \| ASM-\d{2} \| Minor[^\n]*\n\| \d \| ASM-\d{2} \| (?:Fatal|Serious)
      - name: confidence-low-first
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        flags: m
        pattern: |-
          ^\| \d \| ASM-\d{2} \| (Fatal|Serious|Minor)[^|\n]* \| (?:medium|high) \| [^\n]*\n\| \d \| ASM-\d{2} \| \1[^|\n]* \| low \|
      - name: confidence-medium-before-high
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: not_contains
        flags: m
        pattern: |-
          ^\| \d \| ASM-\d{2} \| (Fatal|Serious|Minor)[^|\n]* \| high \| [^\n]*\n\| \d \| ASM-\d{2} \| \1[^|\n]* \| medium \|
      - name: ran-validator-alone
        type: tool_used
        tool: Bash
        input_match: '"command"\s*:\s*"(?:[^"\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*validate_brn\.py(?:[^"\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*"'
      - name: confidence-method-and-test
        type: llm
        focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        question: |-
          PASS if the ranking's Confidence column gives high for the assumption about the kitchen's 57 of 60 and for the one about the 40-person pilot, and low for the one nobody measured and for the hunch; each Cheapest test cell starts with the method its statement calls for (the kitchen's and the pilot's, being about today with a figure given, Data when the figures are in sources and otherwise Interview; the others Interview or Prototype); and each cell after the colon is the first sentence of that assumption's validation in the assumptions block. FAIL otherwise, quoting the row. Order is checked by graders 4 to 7 because level cannot be fixed by the prompt.
  - id: VER-38
    status: proposed
    covers:
      - BEH-32
      - BEH-33
      - ERR-10
    level: manual
    obligation: "Manual, interactive, in the brainstorm runbook (docs/runbooks/brainstorm-manual-test.md, a new test; the plugin copied and loaded with claude --plugin-dir as the runbook's section 0 says), in a session with the task tools and AskUserQuestion, on a topic of a product that does not exist. (a) At step 5 the form holds three questions in order, 'Confirm these dispositions?', 'Has the brainstorm converged?', 'Confirm the first release cut?', each headed 'Step 5', the third with the options 'Accept as proposed' (Recommended) and 'Leave it proposed', each preview holding both tables. (b) Accept all, Converged, Accept as proposed: the BRN says 'First release cut: confirmed by <the owner> on <today>' and the validator prints OK. (c) A second run: Accept all, Converged, and 'IDEA-02 yes' typed under Other in question 3: a second form with 'Confirm the first release cut as changed?' appears once; answer Accept as changed; the changed row's Why reads 'Set by the user'. (d) A third run: Accept all, Converged, Leave it proposed: the line reads 'First release cut: proposed, not confirmed'. (e) A fourth run: Leave them open, Not yet, Accept as proposed: the BRN's cut is proposed, not confirmed, the reply says why. (f) A fifth run: question 1 changes one proposed idea to parked under Other and question 3 is accepted: the cut is proposed again over the new set, with the reply saying so. (g) After a waiver run (Proceed without questions), reply 'confirm everything': step 5 is marked again, the form holds questions 1 to 3, and the BRN is edited in place and validated again. (h) Extend a BRN whose cut was confirmed with a change that leaves the yes and no column as it was: the line stays confirmed; with a change that alters it: the line is proposed. Recorded in SPEC-001 §9."
```

## 6. Staged files

| Staged file | Destination | Checked by |
|---|---|---|
| [staged/skills/brainstorm/references/mvp-path.md](staged/skills/brainstorm/references/mvp-path.md) | `src/claude/DevForgeAI/skills/brainstorm/references/mvp-path.md` (new) | `src/tests/brainstorm/test_structure.py` (new, specified in framework-catalog.md): the file exists, opens with a contents list and is linked from SKILL.md's References list |
| [staged/examples/brainstorm-greenfield-mvp/BRN-001.md](staged/examples/brainstorm-greenfield-mvp/BRN-001.md) | `src/staging/examples/brainstorm-greenfield-mvp/BRN-001.md` (new) | `validate_brn.py` prints OK on it (run from a path ending `docs/specs/brainstorm/BRN-001.md`); VER-35 runs MV-01 to MV-30 on it |
| [staged/examples/brainstorm-greenfield-mvp/README.md](staged/examples/brainstorm-greenfield-mvp/README.md) | `src/staging/examples/brainstorm-greenfield-mvp/README.md` (new) | none |

## 7. Open questions

1. **The two judgments.** The list of an assumption and "X needs Y" are the only semantic judgments left, because R1
   forbids a field that would record them. Options: (a) keep them as judgments shown to the user in the `If wrong`
   and `Why` cells (this document); (b) add an optional `supports` list on assumptions and a `needs` list on ideas,
   which changes `brainstorm.schema.json`, `validate_brn.py`, `output-rules.md`, the PRD mapping, `dsn_check.py`, the
   Codex fork and four skills' eval fixtures (R1).
2. **Two constants.** `TOP` (3 assumptions) and `CAP` (3 ideas chosen by tests) are my choices, matching the three
   highest-ranked assumptions of risk-first-mvp and "usually 1 to 3 promoted" in diverge-converge. Options: keep 3 and
   3; or 3 and 5; or make `CAP` the number of top assumptions.
3. **Marking `Accept as proposed` as Recommended.** I followed question 1's pattern. Options: keep it; or recommend
   neither option, because a rule-made scope is a decision the skill should not nudge.
4. **README's step 4 row** listed the ranking and the cut at step 4. This document puts them in step 5 (§3, Terms and the order of work).
   Settled in review: the README's workflow table now says step 5 (option a). The other option, giving the ranking its
   own step-4 form with a provisional E, is not taken. Bryan: confirm.
