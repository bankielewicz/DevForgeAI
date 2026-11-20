# Framework catalog

**Status:** proposal, written 2026-11-18 by claude-code on the model Fable 5.2 (session
fa59a935-ed2e-4502-b6c4-93bb6d847546) for Bryan's review. It changes no spec, skill or plugin version. It feeds
SPEC-001's next version and is the first of the four commits of SKL-001 version 12 ([README.md](README.md) §8).
Read the README first: this document uses its rules (R1 to R10), shapes (C-01 to C-11) and ID ranges.

## Workflow steps this changes

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 2. Select a framework | The one named, else `diverge-converge` | Five frameworks in the index; six selection rules taken in order, each with its test and a fixed sentence for the user (BEH-15); a named framework the index lacks (ERR-06); what a switch keeps (BEH-19) |
| 3. Diverge: problems, ideas, assumptions | Problems, 5 to 15 ideas, assumptions | The chosen framework's own steps and its own idea count: `shortlist-ranking` generates none, `improve-existing` takes what its seven prompts give (BEH-17, BEH-18) |
| 4. Evaluate with the framework | value, effort, risk, score | Each framework's exact rating method and its fixed lines in section 5 (BEH-17, BEH-18) |
| 5. Propose dispositions and ask the user to confirm | Two questions: dispositions, convergence | Each framework's rule for what it proposes; `shortlist-ranking`'s cut in section 6 (BEH-17, BEH-18). The questions don't change |

SKILL.md itself is reordered so the task list comes first (BEH-16). Its eight checklist lines don't change (R2).

## 1. Scope

**In.**

- The index `references/frameworks/INDEX.md`, replaced: five frameworks, the selection rules with their tests, the
  sentence that tells the user, the names a user may use, a name the index lacks, switching.
- Four new framework files: `shortlist-ranking.md`, `risk-first-mvp.md`, `improve-existing.md`,
  `problem-reframing.md`. Each has the six sections SPEC-001 §4 requires, under fixed headings.
- SKILL.md: the task list moved to the front, step 2 rewritten, one sentence of step 3 changed, three references
  to the old heading reworded. Exact edits in §2.
- One edit each to `diverge-converge.md` and `output-rules.md`, and three to `work-file.md`.
- A new unit test file, `src/tests/brainstorm/test_structure.py`.
- Five eval cases and one manual runbook section.

**Out.**

- The project kind (C-01) and the sources' form (C-09): intake-and-evidence.md. Rule 4 reads the kind step 1
  decided or, when undecided, works with; it does not decide it.
- The assumption risk ranking (C-07) and the first release cut (C-05): mvp-and-prototype-path.md.
  `risk-first-mvp` defines neither.
- Any new field or collection in a BRN (R1), any change to `validate_brn.py`, to the schema or to the progress
  manifest.
- `diverge-converge`'s own steps and ratings, apart from one pointer in its *Avoid when*.
- A requirement priority in a BRN. MoSCoW `priority` stays the PRD's (ADR-003, the *Document contract* row).

## 2. Changes by file

All paths are under `src/claude/DevForgeAI/skills/brainstorm/` unless they start with `src/tests/` or `docs/`.

| File | Change |
|---|---|
| `references/frameworks/INDEX.md` | Replaced by the staged file (§6) |
| `references/frameworks/shortlist-ranking.md`, `risk-first-mvp.md`, `improve-existing.md`, `problem-reframing.md` | New, from the staged files (§6) |
| `SKILL.md` | Edits S1 to S9 below, in that order |
| `references/frameworks/diverge-converge.md` | Edit D1 |
| `references/output-rules.md` | Edit O1 |
| `references/work-file.md` | Edits W1 to W3 |
| `src/tests/brainstorm/test_structure.py` | New; its whole text is in §5.1 |
| `src/claude/DevForgeAI/evals/brainstorm/<case>/` | Five new case folders (§5.2) |
| `docs/runbooks/brainstorm-manual-test.md` | Edits R1 to R3 (§5.3) |

Each edit gives the old text and the new text (R7). Each old text occurs exactly once in its file when the edits
are applied in the order given, ignoring line breaks. A fence here has four backticks, so that it can hold the
three-backtick fences of the files.

### 2.1 SKILL.md

**S1. The task list goes first.** After the opening paragraph, insert the `## Workflow` heading, its sentence and
the fenced checklist.

````text old S1
claim decisions the user actually made.

## Inputs
````

````text new S1
claim decisions the user actually made.

## Workflow

Work through this checklist:

```
- [ ] 1. Intake: topic, existing BRNs, clarifying questions
- [ ] 2. Select a framework
- [ ] 3. Diverge: problems, ideas, assumptions
- [ ] 4. Evaluate with the framework
- [ ] 5. Propose dispositions and ask the user to confirm
- [ ] 6. Write the BRN
- [ ] 7. Validate the BRN
- [ ] 8. Report and hand off
```

## Inputs
````

**S2. The old Workflow section becomes "Working through the steps".** Its heading, sentence and checklist go; all
that followed the checklist stays under the new heading.

````text old S2
## Workflow

Work through this checklist:

```
- [ ] 1. Intake: topic, existing BRNs, clarifying questions
- [ ] 2. Select a framework
- [ ] 3. Diverge: problems, ideas, assumptions
- [ ] 4. Evaluate with the framework
- [ ] 5. Propose dispositions and ask the user to confirm
- [ ] 6. Write the BRN
- [ ] 7. Validate the BRN
- [ ] 8. Report and hand off
```

**Keep the checklist in the task list**
````

````text new S2
## Working through the steps

**Keep the checklist in the task list**
````

**S3 and S4. Inputs moves after Decisions.** S3 removes it from its old place; S4 puts it back, unchanged, before
`## Working through the steps`.

````text old S3
## Inputs

- The arguments (the `ARGUMENTS:` line at the end of this text, when given): the topic. They may be empty; then take the topic from the conversation, or ask for it.
- Existing BRNs: `docs/specs/brainstorm/BRN-*.md` in the current project.
- The template: `${CLAUDE_SKILL_DIR}/assets/brainstorm.md`.
- The work file: `devforgeai/drafts/brainstorm/${CLAUDE_SESSION_ID}.md` (or the draft path the progress
  tracker's line on continuing names, below), the work so far, saved after steps 3 and 4 and at
  step 5 ([work-file.md](references/work-file.md)).

## Decisions that belong to the user
````

````text new S3
## Decisions that belong to the user
````

````text old S4
choice nobody made. That is why this rule matters more than any other in this skill.

## Working through the steps
````

````text new S4
choice nobody made. That is why this rule matters more than any other in this skill.

## Inputs

- The arguments (the `ARGUMENTS:` line at the end of this text, when given): the topic. They may be empty; then take the topic from the conversation, or ask for it.
- Existing BRNs: `docs/specs/brainstorm/BRN-*.md` in the current project.
- The template: `${CLAUDE_SKILL_DIR}/assets/brainstorm.md`.
- The work file: `devforgeai/drafts/brainstorm/${CLAUDE_SESSION_ID}.md` (or the draft path the progress
  tracker's line on continuing names, below), the work so far, saved after steps 3 and 4 and at
  step 5 ([work-file.md](references/work-file.md)).

## Working through the steps
````

**S5 to S7. The three references to the old heading.** These are every place where SKILL.md's text says
"Workflow" to point at the task-list rules or the saving rule. No file under `references/` says it. The lowercase
"workflow checklist" in step 8 names the checklist, not the heading, and stays.

````text old S5
Use AskUserQuestion for questions and confirmations when it is available, tagged with its step
(Workflow); otherwise ask in plain text and end your turn.
````

````text new S5
Use AskUserQuestion for questions and confirmations when it is available, tagged with its step
(Working through the steps, item 4); otherwise ask in plain text and end your turn.
````

````text old S6
Mark step 3 completed, then save the work file (Workflow) before marking step 4 in progress.
````

````text new S6
Mark step 3 completed, then save the work file (Working through the steps) before marking step 4 in
progress.
````

````text old S7
only in text before it (the dialog hides that text). One form tagged step 5 (Workflow, item 4),
both questions with `header: "Step 5"`:
````

````text new S7
only in text before it (the dialog hides that text). One form tagged step 5 (Working through the
steps, item 4), both questions with `header: "Step 5"`:
````

**S8. Step 2.** Its first paragraph is replaced. Its second paragraph (the fallback, ERR-04) stays as it is.

````text old S8
Read `${CLAUDE_SKILL_DIR}/references/frameworks/INDEX.md`. Pick the framework the user named, or
the one whose *use when* criteria best fit the topic; use `diverge-converge` when nothing fits
better. Read the chosen framework file and follow it from here on. Tell the user in one
sentence which framework you chose and why, and switch if they ask.
````

````text new S8
Read `${CLAUDE_SKILL_DIR}/references/frameworks/INDEX.md` and take the first of its selection rules
that matches, in the table's order: the framework the user named, else the one whose test the
request meets, else `diverge-converge`. Ask nothing to choose. Read the chosen framework file and
follow it from here on. Tell the user which framework and why with that rule's sentence from the
index, word for word, as a line of its own. When the user names a framework the index lacks, or
asks to switch, do what the index says under *A name the index lacks* and *Switching*.
````

**S9. Step 3's idea count.**

````text old S9
Generate between 5 and 15 ideas unless the user asks for another number.
````

````text new S9
Generate between 5 and 15 ideas unless the user asks for another number or the framework's *Steps*
set their own count.
````

**What stays, for the documents built after this one.** After S1 to S9:

- The `##` headings of SKILL.md are, in order: `## Workflow`, `## Decisions that belong to the user`, `## Inputs`,
  `## Working through the steps`, `## Output contract`, `## Examples`, `## References`.
- `## Workflow` holds only the sentence "Work through this checklist:" and the fence. A later document adds
  nothing to it.
- The texts under `## Decisions that belong to the user` and `## Inputs` are version 11's, byte for byte.
- `## Working through the steps` opens with the paragraph "**Keep the checklist in the task list** …" and holds, in
  version 11's order and wording, the four numbered task-list rules, "Without task-list tools …", "**Save the work
  as it goes.** …", "**Continuing an earlier run.** …" and `### 1. Intake` to `### 8. Report and hand off`.
- Step 1 is version 11's text except its last paragraph, which is S5's new text.
- Step 2 is S8's new text, a blank line, and version 11's paragraph "If the index is missing, or the chosen file is
  missing or lacks any section the index requires, fall back to `diverge-converge` and tell the user which file was
  the problem."
- Step 3 is version 11's text except the sentences of S9 and S6. Step 4 is version 11's text.
- Step 5 is version 11's text except the sentence of S7. Steps 6, 7 and 8, `## Output contract`, `## Examples` and
  `## References` are version 11's text.
- The file has 322 lines. With `devforgeai-version: "11"` still in place, its SHA-256 is
  `3042c73c6ad12d37deb4a4f48217fb3c03161aec362f0399f2d7dd8b1fc33d2d`.

### 2.2 diverge-converge.md

**D1.** Its *Avoid when* points to the framework to use instead.

````text old D1
adds noise.
````

````text new D1
adds noise: use `shortlist-ranking`.
````

Nothing else in the file changes. Its method text already opens with `Diverge-converge:`, and its *When to use*
heading is on line 3.

### 2.3 output-rules.md

**O1.** A number in `value`, `effort` or `risk` is written in quotes (R1: the schema types them as strings).

````text old O1
| `value`, `effort`, `risk` | `null`, a quoted rating such as `"high"`, or a number, per the framework |
````

````text new O1
| `value`, `effort`, `risk` | `null`, or a quoted string per the framework: a rating such as `"high"`, or a number written in quotes such as `"800"` |
````

### 2.4 work-file.md

**W1.** A switch that redoes the evaluation (BEH-19) saves the work file once more, with the new proposals.

````text old W1
Write the whole file with the Write tool, three times:
````

````text new W1
Write the whole file with the Write tool, three times (and once more, as at point 3, after a
framework switch that redoes the evaluation):
````

**W2 and W3.** The work file names the framework from its first save, so a continued run (SPEC-001 BEH-14) keeps
it. Today section 5 holds "not reached" until step 4, and nothing tells a continued run which framework was in
use.

````text old W2
- Sections not reached yet hold `[NEEDS CLARIFICATION: not reached]`.
````

````text new W2
- Sections not reached yet hold `[NEEDS CLARIFICATION: not reached]`, except section 5: from the first
  save on it holds the chosen framework's method text, which tells a continued run the framework in use.
````

````text old W3
Keep its problems, ideas, assumptions,
   scores and IDs.
````

````text new W3
Keep its problems, ideas, assumptions,
   scores and IDs, and its framework: the one whose method text opens its section 5 (with none there,
   select at step 2 as usual).
````

## 3. Behaviour

```yaml items
behaviors:
  - id: BEH-15
    status: proposed
    changes: "BEH-03 (replaces it); BEH-14 and §4's work-file shape (extends them: section 5 from the first save, and a continued run's framework)"
    lands_in: "SKILL.md, step 2 (edit S8); references/frameworks/INDEX.md, sections Selection rules and Names a user may use; references/work-file.md (edits W2, W3)"
    rule:
      - >-
        At step 2 the skill reads references/frameworks/INDEX.md and takes the first of its six selection rules
        whose test holds, in the order 1 to 6, asking no question to decide: 1, the user names a listed framework;
        2, shortlist-ranking; 3, risk-first-mvp; 4, improve-existing; 5, problem-reframing; 6, diverge-converge.
      - >-
        The request is the arguments plus everything the user wrote in the run before step 2 ends, intake answers
        included. A phrase matches when the request holds it as whole words, ignoring case, a hyphen and a space
        counting as the same; a phrase ending in * matches any word that starts with it.
      - >-
        Rule 1 matches when the request holds a framework's name from the index's Frameworks table or one of its
        other names in the index's list (a name listed with capital letters matches only with those capitals).
        With two frameworks named, the one named first in the request is taken. A name the request says not to
        use does not count, and a later rule that would select that framework is skipped; when rule 6 is the one
        skipped, problem-reframing is taken with the sentence "Framework: `problem-reframing`, because you asked
        not to use `diverge-converge`.". Ordinary wording is not a name: "How might we cut no-shows?" names no
        framework.
      - >-
        Rule 2 matches when both hold: (a) the request lists three or more candidate ideas (items of a bulleted
        or numbered list, or of a run separated by commas, semicolons, "and" or "or"), or it names a backlog,
        shortlist or list to use with a file path in the project whose file, read at step 2, gives two or more
        candidates (its top-level list items; with none, its table's body rows; with neither, its non-empty lines
        that are not headings); whether a listed item is a candidate idea is a judgment (R9): it is something
        to build, change or do ("dark mode, CSV export, SSO" are candidates; "nurses, porters, cleaners" are
        not); (b) the request holds one of: rank*, priorit*, choose, choosing, pick, picking,
        select, selecting, cut, trim, narrow, shortlist, compare, which of, which one, which should, in what
        order, in which order.
      - >-
        Rule 3 matches when the request holds one of: mvp, minimum viable, prototype*, proof of concept, first
        release, first version, version one, v1, build first, ship first, do first, where to start, what to
        start with, smallest thing, riskiest, biggest risk*, could fail, might fail, would fail, make it fail,
        make this fail, could go wrong, might go wrong, pre-mortem, premortem.
      - >-
        Rule 4 matches when both hold: (a) the project kind is brownfield: the kind step 1 decided (README
        C-01), or, when it is undecided, the kind step 1 works with (intake-and-evidence.md, BEH-20); a run has
        one kind, the same for selection as everywhere else; with no kind decided or worked with, (a) does not
        hold (an earlier-shape BRN being extended has none); (b) the
        request holds
        one of: improv*, enhanc*, extend*, fix*, upgrad*, rework*, redesign*, refin*, optimi*, revamp*, moderni*,
        next version, next release, version 2, v2, add to, new feature*.
      - >-
        Rule 5 is a judgment (R9): the skill tries to fill both blanks of "who struggles with what" with words
        from the request, rephrased if needed but never invented, and the rule matches when either blank stays
        empty. "Sign-ups have been flat for six months" matches; "Patients forget appointments booked weeks
        ahead" does not.
      - >-
        The skill then tells the user which framework and why with the matching rule's sentence from the index,
        word for word, as a line of its own: "Framework: `<name>`, because you named it." (1); "Framework:
        `shortlist-ranking`, because you gave a list of candidates and asked to rank or cut it." (2); "Framework:
        `risk-first-mvp`, because you asked what to build first or what could make this fail." (3); "Framework:
        `improve-existing`, because the product exists and you asked to improve, extend or fix it." (4);
        "Framework: `problem-reframing`, because the request doesn't yet say who is affected and what hurts
        them." (5); "Framework: `diverge-converge`, because no other rule in the index matched." (6).
      - >-
        When rule 2 (b) holds and the request names a backlog that can't be read as (a) requires (no path, a path
        that doesn't exist, fewer than two candidates), rule 2 does not match; the skill says "I can't read `<what the request
        named>` as a list of candidates. Paste the list, or give a file path, and ask me to switch to
        `shortlist-ranking`." and goes on to rule 3.
      - >-
        The work file's section 5 holds the chosen framework's method text from its first save on. A run that
        continues an earlier one (BEH-14) does not select again when its work file's section 5 opens with a
        framework's method text: that framework is in use.
  - id: BEH-16
    status: proposed
    changes: "new (Bryan, 2026-11-18: the task list at the front); extends QR-01 and BEH-12's wording of where the checklist stands"
    lands_in: "SKILL.md (edits S1 to S7); references/frameworks/INDEX.md; every file under references/"
    rule:
      - >-
        SKILL.md's ## headings are exactly, in this order: Workflow; Decisions that belong to the user; Inputs;
        Working through the steps; Output contract; Examples; References.
      - >-
        The Workflow section holds only the sentence "Work through this checklist:" and the fenced checklist of
        the eight unchanged lines; the fence opens within the file's first 25 lines.
      - >-
        Working through the steps holds the task-list rules, the saving rule, the continuing rule and the
        sections ### 1. Intake to ### 8. Report and hand off, in that order.
      - "SKILL.md has at most 400 lines."
      - >-
        Every .md file in references/ and references/frameworks/ has, within its first 15 lines, a line that is
        exactly "## Contents" or a line that starts with "## When to use".
  - id: BEH-17
    status: proposed
    changes: "SPEC-001 §4, Extension point (extends it); BEH-04 (unchanged, relied on); BEH-05 (the count, for improve-existing)"
    lands_in: "references/frameworks/INDEX.md, section Required sections; references/frameworks/problem-reframing.md, improve-existing.md, risk-first-mvp.md"
    rule:
      - >-
        Every framework file has exactly these ## headings, with this text, in this order: When to use / When not
        to use; Steps; Questions to ask; Mapping to the BRN; Evaluation method text; Example. Mapping to the BRN
        states the rating method exactly; Steps say how dispositions are proposed, as proposals only (R3);
        Evaluation method text is a quoted paragraph whose opening words, up to its first colon, no other
        framework's text starts with; Example holds item blocks that pass validate_brn.py.
      - >-
        The opening words are: "Diverge-converge:", "Shortlist ranking (RICE):", "Problem reframing:", "Improve
        existing (SCAMPER):" and "Risk-first MVP:". The skill writes the framework's method text as the first
        paragraph of the BRN's section 5.
      - >-
        problem-reframing, improve-existing and risk-first-mvp rate value, effort and risk as the quoted strings
        "high", "medium" or "low" and compute score = 2 × value − effort − risk with high = 3, medium = 2 and
        low = 1, written unquoted; an idea that can't be rated has all four null. Each file defines the three
        ratings in its own terms (its Mapping to the BRN, Ratings).
      - >-
        Those three frameworks propose: promoted for the ideas with a score of 2 or more, at most three, taken by
        highest score, then lower effort, then lower ID; rejected for every idea with a score of −1 or less;
        parked for every other idea and for an unrated one; each proposed reason is one sentence starting
        "Score N: ".
      - >-
        problem-reframing: each start point (a symptom, goal or solution the request states) gets one why chain
        of at most five answers; an answer the skill supplies itself is recorded as an assumption and marked
        "(assumed: ASM-NN)"; a chain stops at five answers, at the user's "don't know", or after two of the
        skill's own answers in a row; the last answer is the root cause. Each chain gives one problem (statement:
        who, what hurts, "because" and the root cause; evidence: the last answer that is not the
        skill's own, with its source, else "[NEEDS CLARIFICATION: is it true that <the first assumed answer>?]"). Section 5 holds,
        per problem in ID order, the lines "- Why chain for PRB-NN: <start point> → because <answer> …",
        "- Job for PRB-NN: When <situation>, <who> wants to <motivation>, so that <outcome>." and, for each of
        its one to three questions, "- HMW-NN (PRB-NN): How might we <question>? Ideas: IDEA-NN, IDEA-NN.".
        Every HMW has at least one idea and the ideas number 5 to 15.
      - >-
        improve-existing: the skill lists up to seven things the product does today, each from a source (the
        project's documents, the user's description, data, tickets), and writes nothing about the product that no
        source says. It then asks the seven SCAMPER prompts in order (Substitute, Combine, Adapt, Modify, Put to
        another use, Eliminate, Reverse), at most two ideas each. A prompt yields nothing when no answer both
        changes something in the baseline and addresses a framed problem: no idea is written for it. Section 5
        holds exactly seven lines in that order, "- <Prompt>: IDEA-NN, IDEA-NN" or "- <Prompt>: no idea
        (<reason>)", and an eighth, "- The user's own: IDEA-NN", when the user gave ideas. The 5-to-15 rule does
        not apply. With no idea at all, the skill says "Framework: `diverge-converge`, because SCAMPER produced no
        idea for this product." and continues with diverge-converge from its step 2.
      - >-
        risk-first-mvp: the skill states the bet, records the user's reasons the idea could fail and adds its own
        until there are at least three, stopping at seven; each reason becomes one problem when it is true today
        for a person whether or not anything is built, otherwise one assumption. For each assumption in ID order
        it writes one idea, the smallest thing that would show whether the assumption holds (of the candidates,
        the one that gives a result soonest), then second tests in the same order until there are five ideas, at
        most 15. Section 5 holds "- Bet: …", "- Reason N: <reason> (ASM-NN)" or "(PRB-NN)" for each reason, and
        "- IDEA-NN tests ASM-NN, ASM-NN" or "- IDEA-NN tests no assumption" for each idea. value is high for two
        or more assumptions tested, medium for one, low for none. The framework ranks no assumption and chooses
        no first release: README C-07 and C-05 do.
  - id: BEH-18
    status: proposed
    changes: "BEH-05 (the 5-to-15 rule does not apply to shortlist-ranking); new otherwise"
    lands_in: "references/frameworks/shortlist-ranking.md; SKILL.md, step 3 (edit S9); references/output-rules.md (edit O1)"
    rule:
      - >-
        With shortlist-ranking, each candidate of the user's list becomes one idea, in list order and in the
        user's words; the skill generates no idea of its own, whatever the count; at most 99 are taken.
      - >-
        Each idea has four inputs. Reach: a whole number per period, from the user's figure for that idea, else
        from a figure in one of the BRN's sources, never the skill's estimate; if reach is unknown for any rated
        idea, reach counts as 1 for every idea. Impact: 3, 2, 1, 0.5 or 0.25, the user's value else the skill's
        estimate. Confidence: 100 when both grounds hold, 80 when one does, 50 when neither (ground 1: reach is
        known; ground 2: the idea addresses a problem whose evidence is not a NEEDS CLARIFICATION marker).
        Effort: person-weeks, the user's figure rounded up to the next 0.5 (a person-day is 0.2, a person-month
        is 4), else the skill's estimate from 0.5, 1, 2, 4, 8, 16, 32.
      - >-
        The fields: value = reach × impact; effort = the person-weeks; risk = 100 − confidence; each a number in
        double quotes with no thousands separator and no trailing zeros. score = value × (100 − risk) ÷ 100 ÷
        effort, computed from the written values, rounded to one decimal with a 5 rounding up, written unquoted
        with one decimal. An idea too vague to rate has all four null.
      - >-
        Rank: highest score first; on a tie the smaller effort, then the lower ID; an unrated idea has no rank.
      - >-
        Cut: with capacity C in person-weeks (the user's figure, else half of the rated ideas' summed effort,
        labelled as an assumption in the capacity line), an idea whose running total of effort down the ranking is at
        most 0.6 × C is a must, at most 0.8 × C a should, at most C a could, beyond that a won't.
      - >-
        Proposals: promoted for every must and should; parked for every could, won't and unrated idea; never
        rejected. The proposed reason is "<Cut word> in the proposed cut: rank R of N, score S." or "Not rated:
        <what is missing>.". The cut word is not a requirement priority and the cut is not the first release cut
        (C-05).
      - >-
        Section 5 holds the method text, the line "Reach unit: <unit> per <period>." (or "Reach unit: not known
        for every candidate, so reach is counted as 1 for all.") and the table | Idea | Reach | Impact |
        Confidence | Effort |. Section 6 holds, before any ### heading: the proposal paragraph ("Proposed,
        awaiting confirmation: promote <IDs in rank order>; park <IDs in rank order, unrated last>.", three or
        more IDs joined by commas with "and" before the last, "none" for an empty list); the line
        "Capacity: <C> person-weeks (given by the user)." or, when the user gave none, "Capacity: <C>
        person-weeks (assumed: half of the candidates' summed effort)."; the table | Rank |
        Idea | Score | Effort | Cumulative effort | Cut |; and the sentence "The cut proposes dispositions only:
        it is not the first release cut, and it sets no requirement priority."
  - id: BEH-19
    status: proposed
    changes: "BEH-03's clause 'and switch if they ask' (replaces it); BEH-14 (extends it: one more save after a switch)"
    lands_in: "references/frameworks/INDEX.md, section Switching; references/work-file.md (edit W1)"
    rule:
      - >-
        The user asks to switch when, after the step-2 sentence, they name another listed framework to use. The
        skill says "Framework: `<new>`, because you asked to switch from `<old>`."
      - >-
        Before step 3 is completed, the new framework's Steps start from its first step and every problem, idea
        and assumption already captured is kept with its ID.
      - >-
        After step 3 is completed and before step 5's form is answered (a switch typed as that form's answer
        counts as before, and no disposition or convergence is written from that answer): every problem, idea and
        assumption is kept with its ID and text; step 3 is not redone and no idea is generated; the task list is
        left as it is (the step in progress stays in progress); none of the new framework's questions is asked:
        what the user has said, the figures given with the request to switch included, and the framework's
        fallbacks are used; every idea's value, effort, risk and score is set to null and filled again by the new
        framework's mapping; the old proposals are dropped; the work file is saved once more, with the new
        proposals, before step 5's form is asked with them.
      - >-
        After such a switch, section 5 holds in this order: the new framework's method text; the line "Switched
        from `<old>` after step 3: the problems, ideas and assumptions were kept and only the evaluation was
        redone."; the lines the new framework writes while evaluating; the old framework's section-5 lines that
        say where the items came from, unchanged. Lines the new framework would have written during step 3 are
        left out. Switching to shortlist-ranking, every idea already captured is a candidate.
      - >-
        After step 5's form is answered, or once the BRN is written, the skill does not switch in that run: it
        says "The brainstorm is already written as BRN-NNN. To evaluate it with `<new>`, run
        `/devforgeai:brainstorm` again and choose to extend BRN-NNN." and changes nothing.
      - "A switch to a name the index lacks is handled by ERR-06 and the current framework stays."
```

### 3.1 Worked examples

**Selection.** Each request is run down the rules in order.

| Request | Rule | Why |
|---|---|---|
| "Let's brainstorm using the diverge-converge framework: how could a library get more teenagers in?" | 1 | It holds a listed name |
| "Do a RICE on these: dark mode, CSV export, SSO." | 1 | `RICE`, in capitals, is another name of `shortlist-ranking` |
| "Ideas for a rice-delivery start-up" | not 1 | `RICE` matches only in capitals; the request then falls to rule 5 (a solution, nobody's hurt named) |
| "Rank these for next quarter: dark mode, CSV export, SSO, an audit log." | 2 | Four candidates, and `rank*` |
| "Brainstorm ways we could cut down on no-shows" | not 2 | `cut` is there, but no candidates; it ends at rule 6 |
| "Which of these should we build first: A, B, C or D?" | 2 | Rules 2 and 3 both hold; the lower number wins |
| "What should the MVP of a meal-planning app be?" | 3 | `mvp` |
| "Our app is live. What should we build first for version 2?" | 3 | Rules 3 and 4 both hold; the lower number wins |
| "Our booking app is live. How could we improve the rebooking flow?" | 4 | The kind is brownfield, and `improv*` |
| "Our booking app is live. Brainstorm a referral scheme for it" | not 4 | Brownfield, but no listed phrase; rule 5 then asks who struggles with what |
| "Sign-ups have been flat for six months" | 5 | No person and no hurt can be filled in |
| "Patients forget appointments booked weeks ahead" | 6 | Who: patients. What: remembering appointments |

The ten existing eval prompts and the runbook's T1 to T7 prompts were scanned against the lists: none holds a
framework's name except `uses-named-framework` (rule 1, as today), none holds a rule-3 or rule-4 phrase, and the
three dental-clinic prompts hold `cut` but list no candidates. Rule 5, a judgment, may choose `problem-reframing`
for a prompt that names nobody affected (`hands-off-to-prd` is the nearest); only `uses-named-framework`'s graders
name a framework, so no existing case depends on it.

**The shortlist score.** Reach 400, impact 1, confidence 80 and effort 2 are written `value: "400"`,
`effort: "2"`, `risk: "20"`; the score is 400 × 80 ÷ 100 ÷ 2 = `160.0`. Reach 150 and impact 0.25 give
`value: "37.5"`. Written values `"9"`, `"50"` and `"2"` give 9 × 50 ÷ 100 ÷ 2 = 2.25, written `2.3`.

**The cut.** Four ranked ideas with efforts 2, 3, 4 and 6 and a capacity of 10 person-weeks: the limits are 6, 8
and 10. The running totals are 2 (must), 5 (must), 9 (could, since 9 is more than 8) and 15 (won't). With no
capacity given, C is half of 2 + 3 + 4 + 6, which is 7.5: the limits are 4.5, 6 and 7.5, and the totals 2 (must),
5 (should), 9 (won't) and 15 (won't). The staged `shortlist-ranking.md` holds the first case in full.

**The reach fallback.** The user gives reach for three of four candidates. Reach is then counted as 1 for all
four, ground 1 of the confidence fails for all four, and section 5 says "Reach unit: not known for every
candidate, so reach is counted as 1 for all."

**A switch.** The user ran `diverge-converge` to step 5 with eight ideas, three of them their own, and types
"switch to RICE" under Other in the step-5 form. The skill writes no disposition, says "Framework:
`shortlist-ranking`, because you asked to switch from `diverge-converge`.", keeps IDEA-01 to IDEA-08, sets their
four rating fields to `null` and rates them without asking anything: no reach was given, so reach counts as 1
for all, and no capacity, so half of the summed effort is used and labelled as assumed. It makes the cut, saves
the work file and asks step 5's form again. Section 5 opens with the shortlist method text and the "Switched
from" line. Had the user typed "switch to RICE, we have 10 person-weeks", the capacity line would read "given
by the user".

## 4. Errors and edge cases

```yaml items
errors:
  - id: ERR-06
    status: proposed
    changes: "new"
    lands_in: "references/frameworks/INDEX.md, section A name the index lacks; SKILL.md, step 2 (edit S8)"
    condition: >-
      The request, or a later request to switch, asks for a framework by a name that matches no name in the
      index. Whether the named thing is a framework is a judgment (R9): it must be a way of working through
      ideas (a framework, method, technique, canvas or analysis), not a tool, a data source or a document. "Use
      SWOT" asks for one; "use our CRM data" does not.
    handling: >-
      Say, word for word, "`<the name as the user wrote it>` is not a framework in this skill's index, which
      lists `shortlist-ranking`, `risk-first-mvp`, `improve-existing`, `problem-reframing` and
      `diverge-converge`." (the table's frameworks, in its order). Ask nothing. At step 2, go on from rule 2 and
      give the matching rule's sentence next. On a request to switch, keep the current framework.
    user_result: "The sentence naming what the index lists, then the framework selected by rules 2 to 6; the session continues"
```

Edge cases that need no new item:

- **A missing or malformed framework file.** SPEC-001's ERR-04 stays: fall back to `diverge-converge` and name the
  file. The index's *Required sections* now gives the six headings character for character, so "malformed" is a
  heading missing or out of order.
- **A framework the user says not to use.** BEH-15, rule 1: the name does not count and the framework is skipped.
- **A backlog that can't be read.** BEH-15's last rule.
- **More than 99 candidates.** BEH-18: the first 99 are taken, and section 5 says so (item IDs have two digits).
- **Capacity or reach not given, and no question can be asked.** BEH-18's fallbacks, each written in the BRN in
  its fixed sentence; the capacity line says "assumed".
- **SCAMPER yields no idea at all.** BEH-17: the fixed sentence, then `diverge-converge`.
- **A continued run** (SPEC-001 BEH-14). BEH-15's last rule and edits W2 and W3: the work file's section 5 opens
  with the method text from the first save, and the continued run uses that framework without selecting again.

## 5. Verification

```yaml items
verifications:
  - id: VER-18
    status: proposed
    covers: [BEH-15, BEH-16, BEH-17]
    level: unit
    obligation: >-
      src/tests/brainstorm/test_structure.py, whose whole text is in §5.1, passes: the checklist's eight lines
      equal the pinned list and their hash equals the progress manifest's; the Workflow section holds only its
      sentence and the fence, which opens within the first 25 lines and before Decisions; the ## headings and the
      ### step headings are the pinned lists; SKILL.md has no "(Workflow" and at most 400 lines; every reference
      file shows its guide within 15 lines; the index's table and the files in frameworks/ name the same
      frameworks; the selection rules are numbered 1 to n, name listed frameworks, end with diverge-converge and
      follow the table's order; each framework file has the six headings in order; the method texts' opening
      words are distinct and none starts another; each file's Example passes validate_brn.py with and without
      site-packages.
  - id: VER-19
    status: proposed
    covers: [BEH-15, BEH-18, BEH-04]
    level: eval
    obligation: >-
      Named, shortlist-ranking is used on the four given candidates: no idea is added, the given reach and
      effort are used, the ratings are quoted numbers, the cut table and the capacity line are in section 6, and
      no disposition is written.
    case: uses-shortlist-ranking
    prompt_frontmatter: |-
      description: "VER-19: shortlist-ranking, named: the user's four candidates only, RICE numbers quoted, the cut proposed in section 6."
      tags: [brainstorm, ver-19]
      max_turns: 60
      timeout_seconds: 900
      allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
    prompt: |-
      Use the shortlist-ranking framework on our invoicing app's backlog. Reach is accounts affected
      per quarter. The candidates: CSV export of invoices (400 accounts, 2 person-weeks); single
      sign-on with SAML (60 accounts, 6 person-weeks); dark mode (900 accounts, 3 person-weeks); an
      audit log of invoice changes (150 accounts, 4 person-weeks). We have 10 person-weeks. Proceed
      without questions and write the brainstorm document.
    scaffold: none
    graders:
      - name: brn-exists
        type: file_exists
        path: docs/specs/brainstorm/BRN-001.md
        exists: true
      - name: method-in-section-5
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^## 5\. Evaluation method\n(?:(?!^## 6\. )[\s\S])*?^(?:> )?Shortlist ranking \(RICE\):
      - name: all-candidates
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          - id: IDEA-04
      - name: only-the-candidates
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          - id: IDEA-05
      - name: quoted-number-ratings
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          value: "\d+(?:\.\d+)?"[^\n]*\n[ \t]+effort: "\d+(?:\.\d+)?"[^\n]*\n[ \t]+risk: "(?:0|20|50)"[^\n]*\n[ \t]+score: \d+\.\d(?!\d)
      - name: no-word-ratings
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          (?:value|effort|risk):[ \t]*"?(?:high|medium|low)
      - name: uses-given-effort
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          idea: "[^"\n]*(?:[Ss]ingle sign-on|SSO|SAML)[^\n]*\n(?:(?![ \t]*- id:)[^\n]*\n)*?[ \t]+effort: "6"
      - name: uses-given-reach
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^\| Idea \| Reach \| Impact \| Confidence \| Effort \|\n\|(?:-+\|)+\n(?:\|[^\n]*\n)*?\| IDEA-0[1-4] \| 900 \| (?:3|2|1|0\.5|0\.25) \| (?:100|80|50) \| 3 \|
      - name: capacity-line
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^Capacity: 10 person-weeks \(given by the user\)\.$
      - name: cut-table
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^\| Rank \| Idea \| Score \| Effort \| Cumulative effort \| Cut \|\n\|(?:-+\|)+\n\| 1 \| IDEA-0[1-4] \| \d+\.\d \| [\d.]+ \| [\d.]+ \| (?:must|should|could|won't) \|$
      - name: proposals-in-section-6
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^## 6\. Convergence\n(?:(?!^## 7\. )[\s\S])*?^(?:> )?Proposed, awaiting confirmation: promote (?:IDEA-\d\d|none)
      - name: no-decided-disposition
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          disposition:[ \t]*"?(?:promoted|parked|rejected)
      - name: reply-names-framework
        type: llm
        question: >-
          PASS if the reply names shortlist-ranking as the brainstorming framework it used. FAIL if no framework
          is named, or a different framework is named as the one used.
      - name: score-follows-formula
        type: llm
        focus: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        question: >-
          The file is a brainstorm document. In its ideas block every idea has value, effort and risk as quoted
          numbers and a score. Judge only this: for every idea, score equals value × (100 − risk) ÷ 100 ÷ effort,
          rounded to one decimal. PASS if that holds for every idea. FAIL otherwise, and quote the idea ID with
          its four values.
  - id: VER-20
    status: proposed
    covers: [BEH-15, BEH-17, BEH-04]
    level: eval
    obligation: >-
      Named, problem-reframing is used on a symptom: section 5 holds the why chain, the job and the How-Might-We
      line for PRB-01 in their fixed shapes, a why the skill supplied is an assumption, and no disposition is
      written.
    case: uses-problem-reframing
    prompt_frontmatter: |-
      description: "VER-20: problem-reframing, named: why chain, job and How-Might-We lines in section 5; assumed whys are assumptions."
      tags: [brainstorm, ver-20]
      max_turns: 60
      timeout_seconds: 900
      allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
    prompt: |-
      Use the problem-reframing framework: sign-ups for our language-exchange meetup app have been
      flat for six months. Proceed without questions and write the brainstorm document.
    scaffold: none
    graders:
      - name: brn-exists
        type: file_exists
        path: docs/specs/brainstorm/BRN-001.md
        exists: true
      - name: method-in-section-5
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^## 5\. Evaluation method\n(?:(?!^## 6\. )[\s\S])*?^(?:> )?Problem reframing:
      - name: why-chain-line
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^- Why chain for PRB-01: \S[^\n]* → because \S
      - name: job-line
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^- Job for PRB-01: When [^\n]+ wants? to [^\n]+, so that [^\n]+\.$
      - name: hmw-line
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^- HMW-01 \(PRB-01\): How might we [^\n]+\? Ideas: IDEA-\d\d(?:, IDEA-\d\d)*\.$
      - name: assumed-why-marked
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          \(assumed: ASM-\d\d\)
      - name: has-assumptions-block
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          ```yaml items[ \t]*\nassumptions:[ \t]*\n[ \t]*- id: ASM-01
      - name: five-ideas
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          - id: IDEA-05
      - name: word-ratings
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          value: "(?:high|medium|low)"[^\n]*\n[ \t]+effort: "(?:high|medium|low)"[^\n]*\n[ \t]+risk: "(?:high|medium|low)"[^\n]*\n[ \t]+score: -?[0-4]\b
      - name: no-decided-disposition
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          disposition:[ \t]*"?(?:promoted|parked|rejected)
      - name: reply-names-framework
        type: llm
        question: >-
          PASS if the reply names problem-reframing as the brainstorming framework it used. FAIL if no framework
          is named, or a different framework is named as the one used.
      - name: problem-is-a-root-cause
        type: llm
        focus: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        question: >-
          The file is a brainstorm document about a meetup app whose sign-ups are flat. Judge only the statement
          of problem PRB-01. PASS if it names a person, what hurts them, and a cause introduced by "because".
          FAIL if it only restates that sign-ups are flat or names no person, and quote the statement.
  - id: VER-21
    status: proposed
    covers: [BEH-15, BEH-17, BEH-04]
    level: eval
    obligation: >-
      Named, improve-existing is used on a described product: section 5 holds the seven SCAMPER lines in order,
      each with idea IDs or "no idea (reason)", the ideas change what the product does today, and no disposition
      is written.
    case: uses-improve-existing
    prompt_frontmatter: |-
      description: "VER-21: improve-existing, named: seven SCAMPER lines in section 5, ideas grounded in the product described."
      tags: [brainstorm, ver-21]
      max_turns: 60
      timeout_seconds: 900
      allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
    prompt: |-
      Use the improve-existing framework on our product, a web app where a climbing gym's members
      book classes. Today members pick a class from a weekly timetable, pay per class by card and get
      a confirmation email. Staff cancel a class by editing the timetable, and members only find out
      if they look. Proceed without questions and write the brainstorm document.
    scaffold: none
    graders:
      - name: brn-exists
        type: file_exists
        path: docs/specs/brainstorm/BRN-001.md
        exists: true
      - name: method-in-section-5
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^## 5\. Evaluation method\n(?:(?!^## 6\. )[\s\S])*?^(?:> )?Improve existing \(SCAMPER\):
      - name: seven-prompt-lines
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^- Substitute: [^\n]+\n- Combine: [^\n]+\n- Adapt: [^\n]+\n- Modify: [^\n]+\n- Put to another use: [^\n]+\n- Eliminate: [^\n]+\n- Reverse: [^\n]+$
      - name: prompt-lines-well-formed
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        flags: m
        pattern: |-
          ^- (?:Substitute|Combine|Adapt|Modify|Put to another use|Eliminate|Reverse): (?!(?:IDEA-\d\d(?:, IDEA-\d\d)?|no idea \([^\n]+\))$)
      - name: at-most-fourteen-ideas
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          - id: IDEA-15
      - name: word-ratings
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          value: "(?:high|medium|low)"[^\n]*\n[ \t]+effort: "(?:high|medium|low)"[^\n]*\n[ \t]+risk: "(?:high|medium|low)"[^\n]*\n[ \t]+score: -?[0-4]\b
      - name: no-decided-disposition
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          disposition:[ \t]*"?(?:promoted|parked|rejected)
      - name: reply-names-framework
        type: llm
        question: >-
          PASS if the reply names improve-existing as the brainstorming framework it used. FAIL if no framework
          is named, or a different framework is named as the one used.
      - name: ideas-start-from-the-product
        type: llm
        focus: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        question: >-
          The file is a brainstorm document about a climbing gym's class-booking web app. What is known of the
          product: members pick a class from a weekly timetable, pay per class by card and get a confirmation
          email; staff cancel a class by editing the timetable, and members only find out if they look. Judge only
          this: every idea in the ideas block changes, replaces, removes or builds on one of those things. PASS
          if that holds. FAIL if an idea has nothing to do with the product as described, and quote it.
  - id: VER-22
    status: proposed
    covers: [BEH-15, BEH-17, BEH-04]
    level: eval
    obligation: >-
      Named, risk-first-mvp is used: section 5 holds the bet, at least three reasons each tied to one assumption
      or problem, and a tests line for each idea; there are assumptions and at least five ideas, and no
      disposition is written.
    case: uses-risk-first-mvp
    prompt_frontmatter: |-
      description: "VER-22: risk-first-mvp, named: bet, pre-mortem reasons and tests lines in section 5; assumptions recorded."
      tags: [brainstorm, ver-22]
      max_turns: 60
      timeout_seconds: 900
      allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
    prompt: |-
      Use the risk-first-mvp framework: we want to start a subscription box of spare parts for
      vintage bicycles. Proceed without questions and write the brainstorm document.
    scaffold: none
    graders:
      - name: brn-exists
        type: file_exists
        path: docs/specs/brainstorm/BRN-001.md
        exists: true
      - name: method-in-section-5
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^## 5\. Evaluation method\n(?:(?!^## 6\. )[\s\S])*?^(?:> )?Risk-first MVP:
      - name: bet-line
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^- Bet: \S
      - name: three-reasons
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^- Reason 3: [^\n]+ \((?:ASM|PRB)-\d\d\)$
      - name: reasons-well-formed
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        flags: m
        pattern: |-
          ^- Reason \d+: (?![^\n]* \((?:ASM|PRB)-\d\d\)$)
      - name: has-assumptions-block
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          ```yaml items[ \t]*\nassumptions:[ \t]*\n[ \t]*- id: ASM-01
      - name: tests-line
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^- IDEA-01 tests (?:ASM-\d\d(?:, ASM-\d\d)*|no assumption)$
      - name: five-ideas
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          - id: IDEA-05
      - name: word-ratings
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          value: "(?:high|medium|low)"[^\n]*\n[ \t]+effort: "(?:high|medium|low)"[^\n]*\n[ \t]+risk: "(?:high|medium|low)"[^\n]*\n[ \t]+score: -?[0-4]\b
      - name: no-decided-disposition
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          disposition:[ \t]*"?(?:promoted|parked|rejected)
      - name: reply-names-framework
        type: llm
        question: >-
          PASS if the reply names risk-first-mvp as the brainstorming framework it used. FAIL if no framework is
          named, or a different framework is named as the one used.
      - name: value-follows-tests
        type: llm
        focus: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        question: >-
          The file is a brainstorm document. Section 5 has one line per idea of the form "- IDEA-NN tests ASM-NN,
          ASM-NN" or "- IDEA-NN tests no assumption". Judge only this: every idea's value in the ideas block is
          "high" when its line names two or more assumptions, "medium" when it names one, and "low" when it says
          no assumption. PASS if that holds for every idea. FAIL otherwise, and quote the idea ID, its value and
          its line.
  - id: VER-23
    status: proposed
    covers: [BEH-15, BEH-18]
    level: eval
    obligation: >-
      With no framework named, a request that gives four candidates with reach and effort and asks to rank them
      selects shortlist-ranking by rule 2: section 5 opens with its method text and no other framework's, no idea
      is added, the cut table is in section 6, and the reply names the framework.
    case: selects-shortlist-ranking
    prompt_frontmatter: |-
      description: "VER-23: no framework named; candidates and a request to rank select shortlist-ranking (rule 2)."
      tags: [brainstorm, ver-23]
      max_turns: 60
      timeout_seconds: 900
      allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
    prompt: |-
      We run a small online bookshop and can't do everything we have in mind this quarter. Here is
      what we have, with the customers each would reach per quarter: gift wrapping at checkout (300
      customers, 1 person-week); a wishlist customers can share (700 customers, 3 person-weeks);
      pre-orders for upcoming titles (250 customers, 4 person-weeks); a loyalty discount after five
      orders (500 customers, 2 person-weeks). We have 6 person-weeks. Rank them for us. Go ahead
      without asking me anything and write up the brainstorm.
    scaffold: none
    graders:
      - name: brn-exists
        type: file_exists
        path: docs/specs/brainstorm/BRN-001.md
        exists: true
      - name: method-in-section-5
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^## 5\. Evaluation method\n(?:(?!^## 6\. )[\s\S])*?^(?:> )?Shortlist ranking \(RICE\):
      - name: no-other-method
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        flags: m
        pattern: |-
          ^(?:> )?(?:Diverge-converge|Problem reframing|Improve existing \(SCAMPER\)|Risk-first MVP):
      - name: all-candidates
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          - id: IDEA-04
      - name: only-the-candidates
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          - id: IDEA-05
      - name: quoted-number-ratings
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        pattern: |-
          value: "\d+(?:\.\d+)?"[^\n]*\n[ \t]+effort: "\d+(?:\.\d+)?"[^\n]*\n[ \t]+risk: "(?:0|20|50)"[^\n]*\n[ \t]+score: \d+\.\d(?!\d)
      - name: capacity-line
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^Capacity: 6 person-weeks \(given by the user\)\.$
      - name: cut-table
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^\| Rank \| Idea \| Score \| Effort \| Cumulative effort \| Cut \|\n\|(?:-+\|)+\n\| 1 \| IDEA-0[1-4] \| \d+\.\d \| [\d.]+ \| [\d.]+ \| (?:must|should|could|won't) \|$
      - name: no-decided-disposition
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          disposition:[ \t]*"?(?:promoted|parked|rejected)
      - name: reply-names-framework
        type: llm
        question: >-
          PASS if the reply names shortlist-ranking as the brainstorming framework it used. FAIL if no framework
          is named, or a different framework is named as the one used.
  - id: VER-24
    status: proposed
    covers: [BEH-15, BEH-19, ERR-06]
    level: manual
    obligation: >-
      Live, by docs/runbooks/brainstorm-manual-test.md T10 to T15 (§5.3): (a) a request for an MVP selects
      risk-first-mvp with rule 3's sentence word for word; (b) a request to improve a product the user says is
      live selects improve-existing with rule 4's sentence; (c) a topic that is a symptom, with the clarifying
      questions answered "I don't know", selects problem-reframing with rule 5's sentence; (d) a request naming
      SWOT gets ERR-06's sentence word for word, then rule 6's sentence, and the session continues with
      diverge-converge; (e) in that run, "switch to RICE" typed under Other in step 5's form writes no
      disposition, gives the switch sentence, keeps every idea ID and text, replaces the ratings with quoted
      numbers, asks step 5 again with the cut's proposals, and the BRN's section 5 opens with the shortlist
      method text followed by the "Switched from" line; (f) a request to rank a backlog that is named but not
      given gets rule 2's "I can't read" sentence and another framework. Rule 6 is covered by T1.
```

A grader's `target` and `focus` values are the flow maps the case files use, written here as strings. Each grader
becomes one file `graders/<name>.md` with these keys as its frontmatter and the pattern or the question as its
body, as in `evals/brainstorm/uses-named-framework/`. Each `prompt.md` is the `prompt_frontmatter` between `---`
lines, then the prompt.

SPEC-001's VER-05 stays manual and unchanged (runbook T5 and T6 still work: the *Frameworks* table keeps its
four columns, and only one line of the index starts with `| diverge-converge |`). VER-04 and its case
`uses-named-framework` are unchanged. VER-13's list of cases whose prompts say not to ask gains the five cases
above.

### 5.1 `src/tests/brainstorm/test_structure.py`

The whole file. Sibling documents add their own test methods to it and change no assertion here, except that a
document adding a `##` heading to SKILL.md changes `H2`.

````python
"""Structure tests for the brainstorm skill's text (SPEC-001; framework-catalog VER-18).

They check what no eval can: that SKILL.md opens with the task list and keeps its eight checklist lines, that
its headings stand in the agreed order, that every reference file shows its guide at the top, and that the
framework index and the framework files agree with each other.

Run from the repository root:
    python3 -B src/tests/brainstorm/test_structure.py
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "src/claude/DevForgeAI"
SKILL = PLUGIN / "skills/brainstorm"
SKILL_MD = SKILL / "SKILL.md"
REFERENCES = SKILL / "references"
FRAMEWORKS = REFERENCES / "frameworks"
INDEX = FRAMEWORKS / "INDEX.md"
MANIFEST = PLUGIN / "progress/manifests/brainstorm.json"
VALIDATOR = SKILL / "scripts/validate_brn.py"

CHECKLIST = [
    "- [ ] 1. Intake: topic, existing BRNs, clarifying questions",
    "- [ ] 2. Select a framework",
    "- [ ] 3. Diverge: problems, ideas, assumptions",
    "- [ ] 4. Evaluate with the framework",
    "- [ ] 5. Propose dispositions and ask the user to confirm",
    "- [ ] 6. Write the BRN",
    "- [ ] 7. Validate the BRN",
    "- [ ] 8. Report and hand off",
]
CHECKLIST_LINE = re.compile(r"^\s*- \[ \] (\d+)\. (.+?)\s*$")  # progress/evaluate.py's pattern
H2 = [
    "## Workflow",
    "## Decisions that belong to the user",
    "## Inputs",
    "## Working through the steps",
    "## Output contract",
    "## Examples",
    "## References",
]
STEPS = [
    "### 1. Intake",
    "### 2. Select a framework",
    "### 3. Diverge",
    "### 4. Evaluate",
    "### 5. Propose dispositions and confirm",
    "### 6. Write the BRN",
    "### 7. Validate the BRN",
    "### 8. Report and hand off",
]
SECTIONS = [
    "## When to use / When not to use",
    "## Steps",
    "## Questions to ask",
    "## Mapping to the BRN",
    "## Evaluation method text",
    "## Example",
]
FRAMEWORK_HEADER = "| framework | file | use when | avoid when |"
RULES_HEADER = "| # | When | Framework | Tell the user |"
FENCE = re.compile(r"^\s*(`{3,})(.*)$")

BRN = """\
---
id: BRN-001
type: brainstorm
title: "Example"
status: draft
version: 1
created: 2026-11-18
updated: 2026-11-18
owner: "Dana"
authors: ["Dana", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-fable-5-2"
  session: "0f0f0f0f-0000-4000-8000-000000000001"
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: []
sources: []
---

# BRN-001 — Example

## 1. Context

Example.

## 2. Problems

%(problems)s

## 3. Target users

Example.

## 4. Ideas

%(ideas)s

## 5. Evaluation method

Example.

## 6. Convergence

Example.

## 7. Assumptions and open questions

%(assumptions)s

- None.

## 8. Candidate success signals

- None.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-11-18 | claude-code (session 0f0f0f0f-0000-4000-8000-000000000001) | Initial draft |
"""
DEFAULT_PROBLEMS = """\
problems:
  - id: PRB-01
    status: active
    statement: "Example."
    who: "Example"
    evidence: "[NEEDS CLARIFICATION: example]"
    severity: medium"""


def read_lines(path):
    return path.read_text(encoding="utf-8").split("\n")


def fences(lines):
    """[(info string, [content lines])] for each fenced block, and the set of line indexes inside any fence."""
    blocks, inside, marker, info, body = [], set(), None, "", []
    for i, line in enumerate(lines):
        m = FENCE.match(line)
        if marker is None:
            if m:
                marker, info, body = m.group(1), m.group(2).strip(), []
                inside.add(i)
        else:
            inside.add(i)
            if m and len(m.group(1)) >= len(marker) and not m.group(2).strip():
                blocks.append((info, body))
                marker = None
            else:
                body.append(line)
    return blocks, inside


def headings(lines, prefix):
    """The lines outside fences that start with the prefix, with their indexes."""
    _, inside = fences(lines)
    return [(i, line.rstrip()) for i, line in enumerate(lines) if i not in inside and line.startswith(prefix)]


def table(lines, header):
    """The body rows of the table whose header line is given, each a list of its cells."""
    start = lines.index(header)
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def section(lines, heading):
    """The lines under a ## heading, up to the next ## heading outside a fence."""
    marks = headings(lines, "## ")
    for n, (i, text) in enumerate(marks):
        if text == heading:
            end = marks[n + 1][0] if n + 1 < len(marks) else len(lines)
            return lines[i + 1:end]
    raise AssertionError("no heading %r" % heading)


def framework_files():
    return sorted(p for p in FRAMEWORKS.glob("*.md") if p.name != "INDEX.md")


class SkillLayout(unittest.TestCase):
    def setUp(self):
        self.lines = read_lines(SKILL_MD)

    def test_checklist_lines_are_the_pinned_eight(self):
        found = [line.strip() for line in self.lines if CHECKLIST_LINE.match(line)]
        self.assertEqual(found, CHECKLIST)

    def test_checklist_hash_matches_the_progress_manifest(self):
        digest = "sha256:" + hashlib.sha256("\n".join(CHECKLIST).encode("utf-8")).hexdigest()
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(digest, manifest["checklistHash"])

    def test_workflow_section_holds_only_the_checklist(self):
        body = [line for line in section(self.lines, "## Workflow") if line.strip()]
        self.assertEqual(body, ["Work through this checklist:", "```"] + CHECKLIST + ["```"])

    def test_checklist_fence_opens_early_and_before_decisions(self):
        first = next(i for i, line in enumerate(self.lines) if CHECKLIST_LINE.match(line))
        fence = first - 1
        self.assertEqual(self.lines[fence], "```")
        self.assertLessEqual(fence + 1, 25, "the checklist's opening fence must be within the first 25 lines")
        self.assertLess(fence, self.lines.index("## Decisions that belong to the user"))

    def test_h2_headings_in_order(self):
        self.assertEqual([text for _, text in headings(self.lines, "## ")], H2)
        self.assertEqual([text for _, text in headings(self.lines, "# ")], ["# Brainstorm"])

    def test_step_headings_sit_in_working_through_the_steps(self):
        marks = headings(self.lines, "### ")
        self.assertEqual([text for _, text in marks], STEPS)
        start = self.lines.index("## Working through the steps")
        end = self.lines.index("## Output contract")
        for i, text in marks:
            self.assertTrue(start < i < end, text)

    def test_no_reference_to_the_old_heading(self):
        self.assertNotIn("(Workflow", "\n".join(self.lines))

    def test_at_most_400_lines(self):
        self.assertLessEqual(len(SKILL_MD.read_text(encoding="utf-8").splitlines()), 400)

    def test_frameworks_are_reached_through_the_index(self):
        text = "\n".join(self.lines)
        self.assertIn("references/frameworks/INDEX.md", text)
        for path in framework_files():
            if path.stem != "diverge-converge":
                self.assertNotIn(path.name, text)


class ReferenceGuides(unittest.TestCase):
    def test_every_reference_shows_its_guide_within_15_lines(self):
        paths = sorted(REFERENCES.glob("*.md")) + sorted(FRAMEWORKS.glob("*.md"))
        self.assertGreaterEqual(len(paths), 4)
        for path in paths:
            top = read_lines(path)[:15]
            self.assertTrue(any(line == "## Contents" or line.startswith("## When to use") for line in top),
                            "%s: no '## Contents' or '## When to use' line in its first 15 lines" % path.name)


class FrameworkIndex(unittest.TestCase):
    def setUp(self):
        self.lines = read_lines(INDEX)
        self.rows = table(self.lines, FRAMEWORK_HEADER)
        self.names = [row[0] for row in self.rows]

    def test_rows_and_files_match(self):
        self.assertEqual(len(self.names), len(set(self.names)))
        self.assertEqual(sorted(self.names), [p.stem for p in framework_files()])
        for row in self.rows:
            self.assertEqual(len(row), 4, row)
            self.assertEqual(row[1], "[%s.md](%s.md)" % (row[0], row[0]))
            self.assertTrue(row[2] and row[3], row)

    def test_selection_rules(self):
        rules = table(self.lines, RULES_HEADER)
        self.assertEqual([row[0] for row in rules], [str(n) for n in range(1, len(rules) + 1)])
        self.assertEqual(rules[0][2], "the one named")
        self.assertEqual(rules[0][3], "Framework: `<name>`, because you named it.")
        chosen = []
        for row in rules[1:]:
            self.assertEqual(len(row), 4, row)
            name = row[2].strip("`")
            self.assertEqual(row[2], "`%s`" % name)
            self.assertIn(name, self.names)
            self.assertTrue(row[3].startswith("Framework: `%s`, because " % name), row)
            self.assertTrue(row[3].endswith("."), row)
            chosen.append(name)
        self.assertEqual(chosen[-1], "diverge-converge")
        self.assertEqual(chosen, [name for name in self.names if name in chosen])

    def test_index_lists_the_six_required_headings(self):
        body = section(self.lines, "## Required sections")
        listed = [line.split("`")[1] for line in body if re.match(r"^\d\. `## ", line)]
        self.assertEqual(listed, SECTIONS)


class FrameworkFiles(unittest.TestCase):
    def test_six_headings_in_order(self):
        for path in framework_files():
            lines = read_lines(path)
            self.assertTrue(lines[0].startswith("# "), path.name)
            self.assertEqual([text for _, text in headings(lines, "## ")], SECTIONS, path.name)

    def test_method_texts_open_with_distinct_words(self):
        tokens = {}
        for path in framework_files():
            quoted = [line for line in section(read_lines(path), "## Evaluation method text")
                      if line.startswith("> ")]
            self.assertTrue(quoted and ":" in quoted[0], "%s: no quoted method text with a colon" % path.name)
            tokens[path.name] = quoted[0][2:].split(":")[0] + ":"
        values = list(tokens.values())
        for a in values:
            self.assertEqual(sum(1 for b in values if b.startswith(a)), 1, tokens)

    def test_examples_pass_the_validator(self):
        for path in framework_files():
            blocks, _ = fences(section(read_lines(path), "## Example"))
            found = {}
            for info, body in blocks:
                if info == "yaml" and body:
                    found[body[0].rstrip(":")] = "\n".join(body)
            self.assertIn("ideas", found, path.name)
            parts = {
                "problems": found.get("problems", DEFAULT_PROBLEMS),
                "ideas": found["ideas"],
                "assumptions": found.get("assumptions", ""),
            }
            text = BRN % {key: "```yaml items\n%s\n```" % value if value else "" for key, value in parts.items()}
            with tempfile.TemporaryDirectory() as tmp:
                brn = Path(tmp) / "docs/specs/brainstorm/BRN-001.md"
                brn.parent.mkdir(parents=True)
                brn.write_text(text, encoding="utf-8")
                for flags in (["-B"], ["-B", "-S"]):
                    proc = subprocess.run([sys.executable] + flags + [str(VALIDATOR), str(brn)],
                                          capture_output=True, text=True)
                    self.assertEqual(proc.returncode, 0, "%s %s: %s" % (path.name, flags, proc.stdout))
                    self.assertTrue(proc.stdout.startswith("OK: "), proc.stdout)


if __name__ == "__main__":
    unittest.main()
````

### 5.2 Eval cases

Five new hand-written case folders under `src/claude/DevForgeAI/evals/brainstorm/`: `uses-shortlist-ranking`,
`uses-problem-reframing`, `uses-improve-existing`, `uses-risk-first-mvp` and `selects-shortlist-ranking`, as VER-19
to VER-23 give them. Every prompt says to proceed without questions (R5), so each run ends with every disposition
`open` and the proposals in section 6. The framework is graded from the BRN's section 5: `method-in-section-5`
looks for the framework's opening words at the start of a line between the `## 5.` and `## 6.` headings, with or
without a leading `> `.

`selects-shortlist-ranking` holds no name from the index's *Names a user may use*, so rule 1 can't match it. It
gives reach, effort and capacity, so the graded path is the one with the user's figures, not the fallbacks.

Rules 3, 4 and 5 selecting by themselves are not graded by an eval. One case of automatic selection was asked
for, and this document's VER range (README §6) is used up by it; rule 2 has it because its framework differs most
from the default (no idea is generated). Rule 4 needs the project kind, which arrives with the second commit, and
rule 5 follows intake answers that an eval can't give. VER-24 checks all three live.

### 5.3 Manual check: runbook edits

Three edits to `docs/runbooks/brainstorm-manual-test.md`.

**R1.** The opening paragraph names the new tests.

````text old R1
the extend flow, framework selection (VER-05), and stopping mid-session (VER-09).
````

````text new R1
the extend flow, framework selection (VER-05, and VER-24 in T10 to T15), and stopping mid-session
(VER-09).
````

**R2.** The new tests go after T9, before the cleanup.

````text old R2
## 2. Cleanup
````

````text new R2
### T10. An MVP request selects risk-first-mvp (VER-24 a; selection rule 3)

Run T10 to T15 on a fresh copy of the plugin (section 0), without T5's test framework. Restart, then:

> /devforgeai:brainstorm what should the MVP of a meal-planning app for shift workers be?

Answer the clarifying questions briefly; say the app does not exist yet.

**Expect:** a line that reads, word for word, "Framework: `risk-first-mvp`, because you asked what to
build first or what could make this fail." Then it states the bet and asks why the app could have
failed six months after launch. Say "stop here" and decline the draft save.

### T11. Improving a live product selects improve-existing (VER-24 b; selection rule 4)

Restart, then:

> /devforgeai:brainstorm our class-booking web app for a climbing gym is live. How could we improve
> the way cancelled classes are handled?

When asked, say the product is in use.

**Expect:** "Framework: `improve-existing`, because the product exists and you asked to improve,
extend or fix it." Then it asks what to read or how the product works today. Stop and decline the
draft save.

### T12. A symptom selects problem-reframing (VER-24 c; selection rule 5)

Restart, then:

> /devforgeai:brainstorm sign-ups have been flat for six months

Answer every clarifying question with "I don't know". If it asks whether the product exists, say it
does.

**Expect:** "Framework: `problem-reframing`, because the request doesn't yet say who is affected and
what hurts them." Then it asks why sign-ups are flat. Stop and decline the draft save.

### T13. A framework the index lacks (VER-24 d; ERR-06)

Restart, then:

> /devforgeai:brainstorm use the SWOT framework: patients forget appointments booked weeks ahead at
> our dental clinic

**Expect:** first, word for word, "`SWOT` is not a framework in this skill's index, which lists
`shortlist-ranking`, `risk-first-mvp`, `improve-existing`, `problem-reframing` and
`diverge-converge`." Then "Framework: `diverge-converge`, because no other rule in the index
matched." It asks no question about which framework to use. Keep this session for T14.

### T14. Switching at step 5 (VER-24 e; BEH-19)

In T13's session, answer the questions, give two ideas of your own, and go on until the step-5 form
shows the proposed dispositions. Note the idea IDs and their texts. Under Other, type:

> switch to RICE

**Expect:**
- "Framework: `shortlist-ranking`, because you asked to switch from `diverge-converge`."
- No new idea, and every idea keeps its ID and text.
- The step-5 form comes again, with proposals from the cut.

Accept all and say it has converged. **Expect in the BRN:**
- `value`, `effort` and `risk` are quoted numbers and every `score` has one decimal.
- It asked nothing about reach, effort or capacity before the form.
- Section 5 opens with "Shortlist ranking (RICE):", followed by the line "Switched from
  `diverge-converge` after step 3: the problems, ideas and assumptions were kept and only the
  evaluation was redone."
- Section 5 has the line "Reach unit: not known for every candidate, so reach is counted as 1 for all."
- Section 6 has a line of the form `Capacity: 7.5 person-weeks (assumed: half of the candidates' summed
  effort).`, its figure half of the efforts in the table that starts `| Rank | Idea | Score |`.
- The report block says `(framework: shortlist-ranking)`.

Then type "switch to SCAMPER". **Expect:** "The brainstorm is already written as BRN-NNN. To
evaluate it with `improve-existing`, run `/devforgeai:brainstorm` again and choose to extend
BRN-NNN." and no change to the file.

### T15. A backlog that is named but not given (VER-24 f; selection rule 2)

Restart, then:

> /devforgeai:brainstorm rank our Jira backlog for the patient portal

**Expect:** "I can't read `our Jira backlog` as a list of candidates. Paste the list, or give a file
path, and ask me to switch to `shortlist-ranking`." (the quoted words may be "Jira backlog"), then a
"Framework:" line for another framework. Stop and decline the draft save.

## 2. Cleanup
````

**R3.** The results table gains six rows.

````text old R3
| T9 | VER-09, QR-01, QR-02 | | |
````

````text new R3
| T9 | VER-09, QR-01, QR-02 | | |
| T10 | VER-24 a (rule 3) | | |
| T11 | VER-24 b (rule 4) | | |
| T12 | VER-24 c (rule 5) | | |
| T13 | VER-24 d (ERR-06) | | |
| T14 | VER-24 e (BEH-19) | | |
| T15 | VER-24 f (rule 2, unreadable backlog) | | |
````

### 5.4 What the author checked

Run on 2026-11-18 in a scratch copy of the skill, with the staged files copied in and the edits of §2 applied by
a script that reads them from this document:

- Each old text of S1 to S9, D1, O1, W1 to W3 and R1 to R3 was found exactly once in its file at its turn, both
  byte for byte and ignoring line breaks (17 lines `PASS edit …`).
- The edited SKILL.md: 322 lines; `progress/evaluate.py`'s `checklist_hash` of it equals the manifest's
  `checklistHash` (`PASS checklist_hash(SKILL.md) equals the manifest's`).
- `test_structure.py`, taken from §5.1, in a mirror tree (`src/tests/brainstorm/` beside
  `src/claude/DevForgeAI/`): `Ran 16 tests … OK`. On version 11 as it stands the same file fails
  (`FAILED (failures=6, errors=2)`), so it tests the change.
- Each new framework's Example, built into a whole BRN with its section 5 and section 6 text (the method text once
  plain and once quoted): `OK: …/BRN-001.md` under `python3` and under `python3 -S`, 20 runs.
- The `yaml items` blocks of §3, §4 and §5 parse with PyYAML 6.0.3 and hold R4's keys; the IDs are BEH-15 to
  BEH-19, ERR-06 and VER-18 to VER-24.
- The 43 regex graders, read from §5's YAML with their flags, in node v24: each passes its good sample (the BRNs
  above) and fails a sample with the one thing it checks broken (`86 checks over 43 graders, 0 failed`).
- The phrase lists of rules 2, 3 and 4 are the same sets in the staged index and in BEH-15 (18, 25 and 17
  phrases), and each fixed sentence in BEH-15 to BEH-19, ERR-06 and the runbook text occurs in a staged file.
- Rule 1's names, tried on ordinary wording: "How might we cut no-shows at our clinic?", "Ideas for reframing our
  pricing page" and "Ideas for a rice-delivery start-up" name no framework; "Do a RICE on these: …" does.
- `pytest src/tests/brainstorm src/tests/progress` in a scratch copy of `src/` before and after the change:
  `10 failed, 598 passed` before and `10 failed, 614 passed` after. The same ten fail both times, each because the
  scratch copy holds no `docs/` and no `CLAUDE.md`; the 16 more are this document's tests.
- The staged files and this document hold no tab and no trailing space.

Not checked: any eval run (they are paid, and run from the owner's shell), the `llm` graders, and the manual item
VER-24.

## 6. Staged files

Each is complete (R6) and is copied to the same path under `src/claude/DevForgeAI/`.

| Staged under `docs/specs/brainstorming/staged/` | Destination | What it is |
|---|---|---|
| `skills/brainstorm/references/frameworks/INDEX.md` | replaces the index | Selection rules, the frameworks table, names, a name the index lacks, switching, required sections |
| `skills/brainstorm/references/frameworks/shortlist-ranking.md` | new | RICE-style rating on the user's candidates and a must/should/could/won't cut that proposes dispositions |
| `skills/brainstorm/references/frameworks/risk-first-mvp.md` | new | A pre-mortem that gives problems and assumptions, and test ideas for the assumptions |
| `skills/brainstorm/references/frameworks/improve-existing.md` | new | SCAMPER's seven prompts asked of the product as its sources describe it |
| `skills/brainstorm/references/frameworks/problem-reframing.md` | new | Five whys, jobs to be done and How-Might-We questions before any idea |

`diverge-converge.md` is not staged: it changes by edit D1 only.

## 7. Decisions and open questions

**Decisions the author made.**

1. *Rules 2 to 4 match by listed phrases, not by "best fit".* Two builders, and two runs, then choose the same
   framework for the same request. The lists are in the index, so adding a phrase changes one file.
2. *Rule 4's phrase list has no bare "better" or "more".* They appear in most requests; a brownfield request
   without a listed phrase goes on to rules 5 and 6, and the user can switch.
3. *Names in capitals match only in capitals, and no ordinary phrase is a name.* "RICE" and "MoSCoW" are also
   ordinary words ("rice", "Moscow"), and "how might we" or "reframing" in a request names no framework. For the
   same reason rule 3 lists "could go wrong" and "where to start", not "go wrong" and "start with".
4. *No question at step 2.* The choice is told in one fixed sentence and the user can switch; a question would
   stop every eval run (R5) and add a prompt to every session.
5. *A name the index lacks does not stop the run and is not replaced by a guess at the nearest framework.* The
   skill says what the index lists and selects by the other rules.
6. *The RICE inputs map onto today's fields with no new field (R1).* `value` holds reach × impact, `effort` the
   person-weeks, `risk` 100 − confidence, so that the score can be recomputed from the three written values
   alone. Reach, impact and confidence themselves are in a table in section 5.
7. *Reach is never the skill's estimate.* It is a fact about the user's product. When one candidate lacks it, all
   candidates are scored without reach, because a ranking that mixes known and invented reach is worse than one
   that leaves reach out.
8. *Confidence is computed from two grounds, not judged.* It then costs no question and is the same for two
   builders.
9. *The score keeps one decimal and is always written with it.* Whole-number rounding would make ties common in
   short lists.
10. *The cut uses 60, 80 and 100 percent of capacity.* 60 percent for the musts is the usual MoSCoW guidance. With
    no capacity given, half of the summed effort is used and the capacity line says "assumed" (decided by Bryan,
    below). The line carries no NEEDS CLARIFICATION marker: the figure is a stated assumption, not a blank.
11. *Must and should are proposed for promotion; could and won't for parking; nothing for rejection.* "Won't" in
    MoSCoW means "not this time". The user rejects by answering step 5.
12. *The cut's words appear only in section 6 and in a proposed reason.* ADR-003 keeps `priority` the PRD's, so
    the BRN records no priority, and the staged file says the words are not one.
13. *The three other frameworks share `diverge-converge`'s scale and formula*, each with its own definitions of
    the ratings. One formula keeps the PRD's reading of a score the same across four of the five frameworks.
14. *Those three propose by thresholds* (score 2 or more, at most three; score −1 or less). `diverge-converge`'s
    "usually 1 to 3" is left as approved.
15. *In problem-reframing, a why that nobody answered is an assumption*, not a fact and not a blank. The chain
    still reaches a root cause, the BRN shows which links are unproven, and at most two such links are allowed
    in a row.
16. *In improve-existing, a prompt with no honest answer gets no idea*, and the 5-to-15 rule gives way. Seven
    prompts at two ideas each stay under 15.
17. *risk-first-mvp ranks nothing.* It writes one test idea for every assumption, and its `value` counts the
    assumptions an idea tests, which says nothing of how grave or how likely each is. C-07 alone ranks.
18. *A switch after step 3 keeps the items and redoes only the evaluation.* Item IDs are what a continued run and
    the work file hold; regenerating ideas would discard the user's own. The task list is not touched and the
    new framework's questions are not asked, so no step is opened twice and no form is asked under a step other
    than the one in progress; the fallbacks cover what is missing. After the BRN is written, a switch is a new
    run that extends it, which SPEC-001's ERR-01 and BEH-11 already cover.
19. *The index keeps SPEC-001 §4's four-column table* and adds the selection rules as a second table, so the
    runbook's T5 and `.claude/rules/skills.md`'s "a file plus one index row" still hold.
20. *The method text stays a quoted paragraph* in each framework file, as in `diverge-converge.md`; the graders
    accept it in the BRN with or without the quote mark.
21. *SKILL.md's moves are given as four insert-and-remove edits* rather than one large replacement, so each old
    text is short enough to check by eye.
22. *The test file validates each framework's Example* by wrapping its item blocks in a minimal BRN, so a later
    edit to an example can't ship an invalid block.

**Decided by Bryan on 2026-11-19** (session fa59a935-ed2e-4502-b6c4-93bb6d847546, on PR #172's open questions).

1. *What the cut proposes for a "won't"* (`parked` or `rejected`). Bryan: "A "won't" proposes parked." BEH-18
   already said so; nothing changed.
2. *Capacity when the user gives none* (assume half of the summed effort, or make no cut). Bryan: "When capacity
   is missing, use half the summed effort and label it as an assumption." The figure stays; its line changed from
   one with a NEEDS CLARIFICATION marker to the fixed form `Capacity: <C> person-weeks (assumed: half of the
   candidates' summed effort).` (BEH-18, the staged `shortlist-ranking.md`, runbook T14).
3. *A named framework the index lacks* (say so and select, or ask). Bryan: "If I name an unknown framework, tell
   me and select one using the published rules." ERR-06 already said so; nothing changed.
4. *`diverge-converge`'s proposal rule* (leave it, or give it the thresholds of decision 14). Bryan: "Keep
   diverge-converge's existing thresholds." `diverge-converge.md` changes by edit D1 only, as before.

**Open, for Bryan.** Nothing.
