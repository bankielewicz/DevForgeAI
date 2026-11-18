# Framework catalog: four more brainstorming frameworks and how the skill chooses

**Status:** proposal, written 2026-11-18 by claude-code (session fa59a935-ed2e-4502-b6c4-93bb6d847546) for
Bryan's review. It changes no spec, skill or plugin version. Its changes to SPEC-001 take effect only in
SPEC-001's next version, approved by Bryan and built in a plugin-dev iteration (`/plugin-dev:create-plugin` and
`/plugin-dev:skill-development`; CLAUDE.md, "Rules a change must not break"). Read
[README.md](README.md) first: this document uses its rules (R1 to R8), shapes (C-01 to C-11) and §5.

## Workflow steps this changes

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 2. Select a framework | The one named, else `diverge-converge` | Five frameworks and README §5's selection rules, kept in `INDEX.md`; one sentence on which framework and why |
| 3. Diverge: problems, ideas, assumptions | Problems, 5 to 15 ideas, assumptions | The chosen framework's own steps. Two frameworks relax the 5-to-15 rule: `shortlist-ranking` takes the user's list and adds no idea, `improve-existing` may give fewer than five |
| 4. Evaluate with the framework | value, effort, risk, score | Each framework's mapping: RICE-style numbers for `shortlist-ranking`, the default ratings for the others, the blocks each writes into section 5 and the cut it proposes in section 6 |

## 1. Scope

**In.**

- `references/frameworks/INDEX.md` with five rows and the selection rules (BEH-15).
- Four new framework files, each with SPEC-001 §4's six sections: `shortlist-ranking`,
  `problem-reframing`, `improve-existing` and `risk-first-mvp` (BEH-18, which includes their proposals).
- The order of SKILL.md, the task list first, and the opening of every reference file (BEH-19).
- Two text edits in SKILL.md, in step 2 and in step 3, and one edit in `diverge-converge.md` (§2).
- The sentence that tells the user which framework was chosen and why (BEH-16), the change to BEH-05's idea count
  (BEH-17) and the error for a framework name the index lacks (ERR-06).
- Verification: five eval cases, one unit test file, one manual item (VER-18 to VER-24).

**Out.**

- Project kind, sources, the Target users table and the success signals (C-01, C-03, C-08, C-09): intake-and-evidence.md.
  This document works without them (BEH-15 item 5, `improve-existing`) and agrees with their shapes.
- Reading earlier BRNs and the project's documents, "Already covered" and "Previously decided" (C-02, C-06):
  brownfield-iteration.md.
- The first release cut and the written assumption risk ranking (C-05, C-07): mvp-and-prototype-path.md.
  `risk-first-mvp` supplies their inputs (BEH-18 item 4) and writes neither shape.
- A new BRN field or collection (R1), any change to `src/schemas/brainstorm.schema.json`, `validate_brn.py`,
  `output-rules.md`, the BRN template, the progress manifest or `src/codex/`.
- Any priority, MoSCoW or release assignment. The cut of `shortlist-ranking` is a proposal in prose; priority stays
  with the PRD (ADR-003, line 92).
- A user setting that picks or orders frameworks (SPEC-001 §12 rejected listing frameworks in SKILL.md).

## 2. Changes by file

Paths are under `src/claude/DevForgeAI/skills/brainstorm/` unless they start with `src/tests/`, `docs/` or
`.claude/`. Staged files are in [staged/](staged/) (§6).

| Destination | What changes |
|---|---|
| `references/frameworks/INDEX.md` | Replaced by the staged file: the selection rules and their terms, a table of five rows in the order shortlist-ranking, risk-first-mvp, improve-existing, problem-reframing, diverge-converge, the "Required sections" text unchanged, and a last line that now also names the selection rules. |
| `references/frameworks/shortlist-ranking.md`, `problem-reframing.md`, `improve-existing.md`, `risk-first-mvp.md` | New, from the staged files. |
| `references/frameworks/diverge-converge.md` | One edit, in "When to use / When not to use" (exact text below). Nothing else changes. |
| `SKILL.md`, step 2 | One paragraph replaced (exact text below). The paragraph after it, which holds ERR-04's fallback, is untouched. |
| `SKILL.md`, step 3 | One sentence of the second bullet extended (exact text below). |
| `SKILL.md`, order (BEH-19) | The `## Workflow` section moves, whole, to directly after the opening paragraph under `# Brainstorm` and before `## Inputs`. Resulting order of the `## ` headings: Workflow, Inputs, Decisions that belong to the user, Output contract, Examples, References. Inside Workflow the order is unchanged: the heading, "Work through this checklist:", the fenced checklist (opening fence on line 21), the task-list rules, "Save the work as it goes", "Continuing an earlier run", then `### 1.` to `### 8.`. |
| `SKILL.md`, everything else | Unchanged, the eight checklist lines byte-identical (R2); apart from the two edits above, the new file holds the lines of the old file in another order (checked on a scratch copy: the sorted lines are equal). After the edits and the move the file is 318 lines (316 today; the limit is 400). |
| `provenance.yaml`, `SKILL.md` metadata, plugin version files | Bumped as README §8 says, in the build's plugin-dev iteration. |
| `src/tests/brainstorm/test_structure.py` | New (VER-23). Written first. |
| `evals/brainstorm/uses-shortlist-ranking/`, `uses-problem-reframing/`, `uses-improve-existing/`, `uses-risk-first-mvp/`, `selects-shortlist-ranking/` | Five new case folders (VER-18 to VER-22). |
| `docs/runbooks/brainstorm-manual-test.md` | A new section for VER-24's steps. |
| `docs/specs/spec/SPEC-001.md`, next version | BEH-03's text replaced by the pointer below (it stays active, so VER-04, VER-05, §3's diagram and §11 step 5, which cite it, stay valid); BEH-05's text replaced (below); BEH-15 to BEH-19, ERR-06 and VER-18 to VER-24 added as written here; §4's INDEX paragraph says the index also holds the selection rules; §1's "The catalog is chosen later (PRD-001 §12)" says the catalog was chosen on 2026-11-18. PRD-001's non-goal (line 58), FR-002's note and §12's open question get their own version bump; that edit is not specified here. |
| `.claude/rules/skills.md`, last sentence of the "Anatomy" section about frameworks | Says that a framework chosen without being named also needs one selection rule in the index. |

**`diverge-converge.md`, exact edit.**

Old (two lines, lines 8 and 9):

```text
**Avoid when** the user already has a fixed shortlist and only wants it ranked. Then diverging
adds noise.
```

New:

```text
**Avoid when** the user already has a fixed shortlist and only wants it ranked: use
`shortlist-ranking`. Then diverging adds noise.
```

**`SKILL.md` step 2, exact edit.**

Old:

```text
Read `${CLAUDE_SKILL_DIR}/references/frameworks/INDEX.md`. Pick the framework the user named, or
the one whose *use when* criteria best fit the topic; use `diverge-converge` when nothing fits
better. Read the chosen framework file and follow it from here on. Tell the user in one
sentence which framework you chose and why, and switch if they ask.
```

New:

```text
Read `${CLAUDE_SKILL_DIR}/references/frameworks/INDEX.md`. Choose by its selection rules: the first
rule that matches the request decides, and the last rule picks `diverge-converge`. Read the chosen
framework file and follow it from here on. Tell the user in one sentence which framework you chose
and which condition of the rule it met, and switch if they ask. When the user names a framework the
index does not list, say so, name the ones it lists, and choose by the other rules.
```

**`SKILL.md` step 3, exact edit.**

Old (second bullet, last two lines):

```text
  ideas you generate. Generate between 5 and 15 ideas unless the user asks for another number.
  Every idea addresses at least one problem and starts with `disposition: open`.
```

New:

```text
  ideas you generate. Generate between 5 and 15 ideas unless the user asks for another number or
  the framework's *Steps* say otherwise. Every idea addresses at least one problem and starts with
  `disposition: open`.
```

**SPEC-001 BEH-03, new text** (replaces the old `rule`): "Read references/frameworks/INDEX.md and choose the framework by
its selection rules (BEH-15); use diverge-converge when no other rule matches. Tell the user which framework was
chosen and why, and switch if they ask (BEH-16)."

**SPEC-001 BEH-05, new text** (replaces the old `rule`): "During divergence, record the user's ideas in their own
words alongside generated ones. Generate between 5 and 15 ideas unless the user asks otherwise or the chosen
framework's Steps say otherwise (BEH-17). Every idea starts with disposition open."

## 3. Behaviour

```yaml items
behaviors:
  - id: BEH-15
    status: proposed
    rule: |-
      The skill chooses the framework by the selection rules in INDEX.md, as a numbered list:
      1. When: after step 1 (Intake) is done and before step 3 (Diverge) starts, the skill reads INDEX.md and takes
         the first rule, in the order of item 6 below, whose condition the request meets.
      2. It decides from the arguments, the conversation, the answers to the intake questions, and the BRNs and
         project documents that step 1 already read. It reads no other file to decide.
      3. The terms. "Names a framework": the request uses a name from the index's Frameworks table, written with a
         hyphen or a space, in any case; a phrase that only resembles a name does not count. "Candidate ideas":
         separate options the user lists in the request, or in a file or issue list the request names. "Project
         kind": the term of that name in INDEX.md, which is intake-and-evidence.md's BEH-20 (K0 to K4) without the
         question: the kind step 1 wrote, else the request's words, else brownfield when `docs/specs/prd/PRD-*.md`
         matches a file and greenfield when it does not; its two phrase lists are word for word the lists of
         intake.md's K1 (a unit test of intake-and-evidence.md's build compares them). "A problem can be stated": the request or the user's
         answers give both a kind of person and a difficulty, cost or harm that person suffers; a drop in a number,
         a target or a feature does not.
      4. Project kind comes from the first line under section 1 of the BRN (C-01) when the run's intake wrote one
         (its `[NEEDS CLARIFICATION: ...]` form counts as the assumed kind of item 3, as intake.md's K4 says);
         otherwise the skill decides it by item 3's rule from the request alone, so the catalog works before
         intake-and-evidence is built and for a BRN extended without a kind line. The two definitions never give
         different answers: with intake built, the only difference is that intake asks the kind question (K3) where
         the catalog's rule would assume.
      5. A framework named by the user wins (rule 1) even when its "use when" does not fit. One exception: when the
         user names shortlist-ranking and neither the request nor the conversation holds any candidate idea, the
         skill asks for the list when it may ask (the question belongs to step 2, tagged as SPEC-001 BEH-12 says); when
         it may not ask (BEH-13), it uses diverge-converge and says in BEH-16's sentence that no list was given.
      6. The rules, in this order (the same text as INDEX.md): (1) The user names a framework that the index
         lists: that one. (2) The request supplies three or more candidate ideas, or names a backlog or list to
         use, and asks to rank, prioritise, choose among or cut them: shortlist-ranking. (3) The request asks what
         to build first, for an MVP or a prototype, or what could make the idea fail: risk-first-mvp. (4) Project
         kind is brownfield and the topic is improving, extending or fixing the existing product: improve-existing.
         (5) After intake, no problem can be stated with an affected person and what hurts them (the topic is a
         symptom, a goal or a solution): problem-reframing. (6) Otherwise: diverge-converge.
      7. Rules 1 to 5 are checked in order and the first match wins; rule 6 applies when none match.
      8. ERR-04 is unchanged: an index that is missing, or a chosen file that is missing or lacks a required
         section, falls back to diverge-converge.
    changes: "BEH-03, extended: BEH-03 stays active and its text becomes the pointer given in §2; BEH-15 holds the selection rules"
    lands_in: "references/frameworks/INDEX.md (the selection rules, their terms, the unknown name and the no-list exception); SKILL.md step 2 (the edit in §2)"
  - id: BEH-16
    status: proposed
    rule: |-
      After choosing, and before step 3 starts, the skill tells the user in one sentence which framework it chose
      and why, in the form "I'm using `<name>`, because <clause>." where <name> is the framework's name in the
      index's first column and <clause> is the clause of the rule that matched, word for word:
      rule 1, "you named it"; rule 2, "you gave candidate ideas to rank or choose among"; rule 3, "you asked what
      to build first or what could make it fail"; rule 4, "the product exists and the topic is improving it";
      rule 5, "no problem with an affected person and a hurt could be stated yet"; rule 6, "no more specific rule
      matched". When BEH-15 item 5's exception applies, the clause is "you named shortlist-ranking but gave no
      list, so I'm using diverge-converge instead" and <name> is diverge-converge. The skill switches framework
      when the user asks for another one the index lists. The name written after "framework:" in step 8's report
      line is the index name of the framework the run ended with, and section 5 of the BRN holds that framework's
      Evaluation method text (BEH-18 item 5).
    changes: "BEH-03, its last sentence (tell the user which framework was chosen and why, and switch if they ask), made exact"
    lands_in: "references/frameworks/INDEX.md (the 'Telling the user' section); SKILL.md step 2 (the edit in §2); each framework file's Evaluation method text"
  - id: BEH-17
    status: proposed
    rule: |-
      The idea count of BEH-05 becomes: between 5 and 15 ideas unless the user asks for another number or the
      chosen framework's Steps say otherwise. Two frameworks say otherwise:
      1. shortlist-ranking: the ideas are exactly the user's candidates, in the order given, from 1 to 30. The skill
         generates no idea. When the list holds more than 30, it takes the first 30 and says in section 5 how many
         were left out and which was the first.
      2. improve-existing: between 5 and 15 ideas, except that when fewer than five of SCAMPER's seven prompts give an
         idea, it writes the ideas that exist (at least one), adds no others, and says in section 5 that the
         existing product left fewer than five improvements. When no prompt gives an idea it writes one idea: the
         smallest change that addresses the most severe problem.
      BEH-05's other rules stand: the user's own ideas are recorded in their own words, and every idea starts with
      disposition open. SKILL.md step 3's rule that every idea addresses at least one problem stands for all five
      frameworks.
    changes: "BEH-05, second sentence extended (new text in §2)"
    lands_in: "SKILL.md step 3 (the edit in §2); shortlist-ranking.md and improve-existing.md"
  - id: BEH-18
    status: proposed
    rule: |-
      Each framework fills the BRN only through the problems, ideas and assumptions collections and their defined
      fields (BEH-04, R1) and through the prose blocks named here. As a numbered list:
      1. shortlist-ranking. `value` = reach × impact; `effort` = person-weeks; `risk` = 100 − confidence; `score` =
         value × (100 − risk) ÷ 100 ÷ effort rounded half up to one decimal. Reach is the people reached in one
         quarter; impact is 3, 2, 1, 0.5 or 0.25; confidence is 100, 80 or 50 by the evidence rule of the file.
         `value`, `effort` and `risk` are quoted strings holding a number, `score` an unquoted number with one
         decimal; all four are null for an idea whose reach or effort the user did not give, and section 5 says
         which. Reach and effort are never estimated. Section 5 holds the line "Capacity: N person-weeks" or
         "Capacity: not given" and a rating table with the header
         "| Idea | Reach | Impact | Confidence | Effort | Value | Risk | Score |", one row per idea in ID order, so
         every score can be worked out again from the BRN. Worked example: reach 900, impact 2, confidence 80,
         effort 2 give value "1800", risk "20", effort "2" and score 1800 × 0.8 ÷ 2 = 720.0.
      2. problem-reframing. Root causes and jobs to be done become `problems` (a root cause: "[Who] [suffers what]
         because [the root cause]."; a job: "[Who] wants to [outcome] but [the obstacle]."). Jobs are written in
         section 3's table, in the form "When [situation], I want to [motivation], so I can [outcome]." Section 5,
         after the method text, holds a "### Five whys" block (a line "Chain N, starting point: ..." then bullets
         "- Why K: ..." for K up to 5, then "- Root cause: PRB-NN", with " (not confirmed)" after the ID when the
         chain stopped on an unknown) and a "### How-might-we questions" block with one bullet for each problem, in
         the shape "- PRB-NN: How might we ... ?". Ratings and score are the default framework's: high, medium and
         low as quoted strings, score = 2 × value − effort − risk with high = 3, medium = 2, low = 1, an integer
         from −4 to 4.
      3. improve-existing. Each problem's `evidence` is the text of one `sources` entry (form "<kind>: <reference>",
         kind one of document, data, ticket, interview, url, note) or a NEEDS CLARIFICATION marker; each source used
         is added to `sources`. Section 5, after the method text, holds a "### SCAMPER prompts" table with the
         header "| Prompt | Ideas | Note |" and seven rows in the order Substitute, Combine, Adapt, Modify, Put to
         another use, Eliminate, Reverse; the Ideas cell lists idea IDs or "none", the Note cell is one sentence and
         never empty. Every prompt is attempted; a prompt that gives nothing is recorded as none with its reason, and
         no idea is written only to fill a prompt. Ratings and score are the default framework's, with effort and
         risk counted on top of the existing product.
      4. risk-first-mvp. A reason from the pre-mortem that names a kind of person and a hurt they suffer today is a
         problem; every other reason becomes an assumption ("We believe that ..."). Section 5, after the method text,
         holds a "### Pre-mortem" block (one bullet for each reason, ending with the ID of the problem or assumption
         it became in parentheses) and a "### Assumption riskiness" table with the header
         "| Rank | Assumption | If wrong | Severity | Confidence | Riskiness |". Riskiness = severity points (high 3,
         medium 2, low 1) × uncertainty points (confidence low 3, medium 2, high 1), 1 to 9; rank by riskiness, ties
         by the lower ASM number. Confidence is high when the user gave data or a direct observation of the very
         thing, medium for indirect evidence or the user's own statement from experience, low when there is none
         (always, for an assumption the skill added): the definitions that C-07 shares. Each assumption's
         `validation` is its cheapest test in two sentences, the test and then the pass line. Each idea is a test that
         starts "Test ASM-NN: " and tests one assumption; `value` is high when the assumption is ranked 1, medium
         when ranked 2 or 3, low otherwise or when it tests none; `effort` is low at most 5 working days, medium 6 to
         20, high above 20; score as in item 2. The riskiness table is this framework's own working: it rates the
         test ideas and nothing else, and it is never copied into the assumption risk ranking (C-07), which is the
         only ranking that decides the first release cut (C-05). mvp-and-prototype-path.md orders C-07 by its own
         rule (its §3.1); this framework writes neither C-07 nor the first release cut.
      5. All four. Section 5 contains the framework's Evaluation method text, which starts with its fixed name token:
         "Shortlist ranking:", "Problem reframing:", "Improve existing:" or "Risk-first MVP:". That text names no
         other framework. The default framework's token is "Diverge-converge:". Severity of a problem is `high`
         when the user said it stops people doing what they came to do, costs money or harms someone, `low` when they
         called it an annoyance, otherwise `medium` with a line in section 5 that the severity was not given.
      6. Proposals. Every framework only proposes dispositions; the skill writes a disposition, `status: converged`
         or a confirmed value only on the user's explicit answer in step 5 (R3; SPEC-001 BEH-06). The proposals are:
         (a) shortlist-ranking. Rank the rated ideas by score, highest first, ties by the lower effort then the lower idea
            number. With a capacity, each idea has a running total of the efforts down the ranking including its own:
            must when the total is at most 0.6 × capacity, should when above that and at most 0.8 × capacity, could when
            above that and at most the capacity, won't above the capacity. Without a capacity, k is the number of rated
            ideas divided by 4, rounded up: ranks 1 to k are musts, k + 1 to 2k shoulds, 2k + 1 to 3k coulds, the rest
            won'ts. A must or a should is proposed promoted; a could parked; a won't rejected when its score is below one
            tenth of the highest score and parked otherwise; a not-rated idea parked, its reason the missing figure.
            The cut is written only in section 6 prose, as a "### Priority cut" block after any other shape section 6
            holds: the line "Priority cut: a proposal; priority stays with the PRD", then a table with the header
            "| Rank | Idea | Cut | Proposed disposition | Why |", one row per idea in rank order (not-rated ideas last, rank
            "-", cut "Not rated"), the Cut cell one of Must, Should, Could, Won't, Not rated. It is never a field, never
            a PRD `priority` and its status line never changes.
         (b) problem-reframing and improve-existing. Promoted: the up to three ideas with the highest scores, each only when
            its score is 3 or more. Parked: every other idea with a score of 1 or more. Rejected: every idea with a score of
            0 or less. Ties: the lower effort (low before medium before high), then the lower idea number. A not-rated
            idea is parked.
         (c) risk-first-mvp. For each of the three highest-ranked assumptions, the idea that tests it with the highest score
            (ties as in (b)) is promoted. Every other idea with a score of 1 or more is parked; every idea with a score
            of 0 or less is rejected; a not-rated idea is parked.
         (d) Every proposal has a one-line reason. Before the user confirms, the proposals are written in section 6 prose
            as the paragraph "Proposed, awaiting confirmation: ...", as SPEC-001 and C-04 already require.
    changes: "new; extends BEH-04 (no new keys) with each framework's mapping, and BEH-06 with what the proposals are for each framework (item 6; BEH-06's confirmation rules stand)"
    lands_in: "each framework file's Mapping to the BRN and Evaluation method text sections (the proposals of item 6 are in the Mapping section)"
  - id: BEH-19
    status: proposed
    rule: |-
      The skill's task list is the first thing in SKILL.md, and every reference file opens with what guides its use
      (Bryan, 2026-11-18: "ensure the tasklist or phases of the brainstorm skill is at the front of the spec for the
      skill"). The reason: the whole SKILL.md body loads when the skill triggers, but a reference file may be read in
      part, and the instructions placed first are the ones most reliably followed. As a numbered list:
      1. In SKILL.md the `## Workflow` section moves, whole and unchanged, to directly after the opening paragraph
         under `# Brainstorm` and before `## Inputs`. Its heading comes first, then the line "Work through this
         checklist:", then the fenced eight-line checklist, then the rest of the section in its present order (the
         task-list rules, "Save the work as it goes", "Continuing an earlier run", and the steps `### 1.` to `### 8.`).
      2. The resulting `## ` headings, in order: `## Workflow`, `## Inputs`, `## Decisions that belong to the user`,
         `## Output contract`, `## Examples`, `## References`. `## Inputs` and `## Decisions that belong to the user`
         keep their text and now follow the whole Workflow section.
      3. The move is the only change it makes: the eight checklist lines stay byte-identical (R2), and apart from the
         edits of §2 (step 2 and step 3) the lines of the new file are the lines of the old file in another order. The
         progress tracker's hash comes from the checklist lines wherever they sit in the text
         (`progress/evaluate.py`, `checklist_steps` and `checklist_hash` read every checklist line of the text), so
         no manifest changes.
      4. The opening fence of the checklist is within the first 25 lines of SKILL.md and before `## Inputs`.
      5. Every file in `references/` and `references/frameworks/` shows its guide within its first 15 lines: a
         framework file its `## When to use / When not to use` section; INDEX.md its `## Selection rules` section;
         every other reference a `## Contents` list.
    changes: "new; R2's text moves only (README R2 keeps the eight checklist lines)"
    lands_in: "SKILL.md (the move of §2); the five staged files (they open as item 5 says); the unit test of VER-23"
```

## 4. Errors and edge cases

```yaml items
errors:
  - id: ERR-06
    status: proposed
    condition: "The request asks for a framework by name, in words such as 'use X' or 'with the X framework', and X is not a name in INDEX.md's Frameworks table"
    handling: |-
      Rule 1 does not match. The skill says so in one sentence, names the five frameworks the index lists, reads no
      file for the name it does not know, does not improvise its method, and chooses by rules 2 to 6 of BEH-15. Its
      BEH-16 sentence then gives the clause of the rule that matched. SKILL.md step 2's last sentence says this
      (§2).
    user_result: "The session continues with a listed framework, and the user knows that the name was not available and which ones are"
    changes: "new; distinct from ERR-04, which covers a missing index or a missing or malformed file"
    lands_in: "SKILL.md step 2 (the edit in §2); INDEX.md (the paragraph after the terms)"
```

ERR-04 is unchanged and covers every new file: an index that is missing, or a chosen file that is missing or lacks
one of the six sections, falls back to `diverge-converge` and names the file. The unit test (VER-23) is what keeps
the five files from being malformed.

ERR keys: R4 names none for errors. This document uses SPEC-001's `condition`, `handling` and `user_result`, plus
`changes` and `lands_in` as R4 asks of every item.

## 5. Verification

SPEC-001's VER-05 (a framework added or removed with SKILL.md unchanged) stays manual. VER-24 re-runs it against
the five-row index and adds the selection rules, ERR-06 and the switch.

Eval runs are non-interactive: no user answers (R5). Every prompt below says to proceed without questions, and
the graders check the unconfirmed form: every disposition `open`, `status: draft`. Eval runs have no
AskUserQuestion, so BEH-13's waiver question is not asked. "Which framework" is graded on the BRN's section 5
text, with the reply as a second, llm-judged witness (`.claude/rules/evals.md`: regex graders for exact file
content, llm graders for the reply). Each case is a folder under `evals/brainstorm/` with `prompt.md` (frontmatter
`description`, `tags`, `max_turns: 60`, `timeout_seconds: 900`, `allowed_tools: [Skill, Read, Glob, Grep, Write,
Edit, Bash]`; the body is the prompt) and `graders/<name>.md` (frontmatter `type`, and for regex `target`,
`match` and `flags`; the body is the regex or the question), as the existing cases do. None of the five has a
scaffold: the workspace starts empty. The hand-written cases have no generator.

All five cases are tagged `brainstorm` and `ver-NN`. They join the three-run qualification that README §8 says the
new SKL-001 version owes (0.8 per case).

### 5.1 Common graders

Every eval case below carries these ten graders, copied from the existing cases (`uses-named-framework`,
`no-unconfirmed-dispositions`, `writes-valid-brn`), plus the four graders of §5.2 and its own
specific graders. The path is `docs/specs/brainstorm/BRN-001.md` throughout.

```yaml items
common_graders:
  - name: brn-exists
    type: file_exists
    path: docs/specs/brainstorm/BRN-001.md
    exists: true
  - name: skill-fired
    type: tool_used
    tool: Skill
    input_match: '"skill"\s*:\s*"(?:[\w-]+:)?brainstorm"'
  - name: ran-validator-alone
    type: tool_used
    tool: Bash
    input_match: '"command"\s*:\s*"(?:[^"\\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*validate_brn\.py(?:[^"\\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*"'
  - name: no-leftovers
    type: regex
    target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    match: not_contains
    pattern: |-
      <!--|BRN-000|YYYY-MM-DD|<topic>|<idea>|<persona>|<signal>|<question>|<one sentence|<we believe|title: ""
  - name: only-allowed-collections
    type: regex
    target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    match: not_contains
    pattern: |-
      ```yaml items[ \t]*\n(?!(?:problems|ideas|assumptions):)
  - name: only-allowed-fields
    type: regex
    target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    match: not_contains
    pattern: |-
      ```yaml items[ \t]*\n(?:(?!```).*\n)*?[ \t]+(?:- )?(?!(?:id|status|superseded_by|upstream|statement|who|evidence|severity|idea|addresses|value|effort|risk|score|disposition|reason|validation|state):)[a-z_]+:
  - name: one-key-per-block
    type: regex
    target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    match: not_contains
    pattern: |-
      ```yaml items[ \t]*\n[a-z_]+:.*\n(?:(?!```).*\n)*?[a-z_]+:
  - name: no-decided-disposition
    type: regex
    target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    match: not_contains
    pattern: |-
      disposition:[ \t]*\"?(?:promoted|parked|rejected)
  - name: has-open-ideas
    type: regex
    target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    match: contains
    pattern: |-
      disposition:[ \t]*open
  - name: not-converged
    type: regex
    target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    match: not_contains
    flags: m
    pattern: |-
      ^status:[ \t]*\"?converged
```

### 5.2 The four framework graders

For each case, with the token and the other tokens of its row (each regex tested with `node` against a scratch BRN
built from the framework's own Example, which `validate_brn.py` passes):

| Case | Own token | The other four tokens |
|---|---|---|
| uses-shortlist-ranking, selects-shortlist-ranking | `Shortlist ranking` | `Diverge-converge\|Problem reframing\|Improve existing\|Risk-first MVP` |
| uses-problem-reframing | `Problem reframing` | `Diverge-converge\|Shortlist ranking\|Improve existing\|Risk-first MVP` |
| uses-improve-existing | `Improve existing` | `Diverge-converge\|Shortlist ranking\|Problem reframing\|Risk-first MVP` |
| uses-risk-first-mvp | `Risk-first MVP` | `Diverge-converge\|Shortlist ranking\|Problem reframing\|Improve existing` |

In the table, `\|` is Markdown's escape for the regex's `|`. The graders, with `OWN` and `OTHERS` taken from the row
(the pattern text has no other variable part):

```yaml items
framework_graders:
  - name: method-in-section-5
    type: regex
    target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    match: contains
    pattern: |-
      ## 5\. Evaluation method\n(?:(?!\n## 6\.)[\s\S])*?OWN:
  - name: no-other-method-in-section-5
    type: regex
    target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    match: not_contains
    pattern: |-
      ## 5\. Evaluation method\n(?:(?!\n## 6\.)[\s\S])*?(?:OTHERS):
  - name: reply-names-framework
    type: llm
    question: |-
      PASS if the reply names the framework called OWN as the framework used, in the line "(framework: ...)" or in a
      sentence saying which framework it used, in either its index name (hyphenated) or its plain name. FAIL if no
      framework is named, or a different one is named as the one used.
  - name: file-conforms
    type: llm
    focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
    question: |-
      The file is a brainstorm (BRN) document. Its item blocks are the fenced blocks whose info string is "yaml
      items". The allowed fields per collection are:
      - problems: id, status, superseded_by, upstream, statement, who, evidence, severity
      - ideas: id, status, superseded_by, upstream, idea, addresses, value, effort, risk, score, disposition, reason
      - assumptions: id, status, superseded_by, upstream, statement, validation, state
      No other collections are allowed.
      PASS if every item block uses only its own collection's fields, and section 5 (Evaluation method) contains the
      OWN method text and explains how value, effort, risk and score were assigned.
      FAIL otherwise. When failing, quote the offending passage or field and name the requirement it violates.
```

In the two regexes, `OWN` is the own-token column ("Shortlist ranking" and so on) and `OTHERS` is the last column. In the
two llm questions, `OWN` is the same plain name. For `uses-shortlist-ranking` the first pattern is therefore
`## 5\. Evaluation method\n(?:(?!\n## 6\.)[\s\S])*?Shortlist ranking:`.

### 5.3 Items

```yaml items
verifications:
  - id: VER-18
    status: proposed
    covers: [BEH-16, BEH-17, BEH-18]
    level: eval
    obligation: |-
      The user names shortlist-ranking and gives five candidate ideas with figures and a capacity. The skill records
      exactly those five ideas, rates them with the RICE-style numbers (value, effort and risk quoted numbers, score one
      decimal), writes the rating table, the capacity line and the priority cut in section 6, adds no sixth idea, and
      leaves every disposition open.
    case: uses-shortlist-ranking
    prompt: |-
      Our neighbourhood public library has a backlog of five ideas to get more teenagers through the door, and I want
      them ranked with the shortlist-ranking framework. Reach is how many teenagers each would bring in per quarter,
      and effort is in person-weeks:
      1. A Saturday gaming night: reach 150, effort 3.
      2. A homework help desk after school: reach 300, effort 6.
      3. A teen advisory board that picks new books: reach 40, effort 2.
      4. Free printing for school projects: reach 500, effort 1.
      5. Extended Sunday opening: reach 200, effort 10.
      These figures are our own estimates. We have 12 person-weeks this quarter. Proceed without questions and write
      the brainstorm document.
    scaffold: none
    graders:
      common: [brn-exists, skill-fired, ran-validator-alone, no-leftovers, only-allowed-collections, only-allowed-fields,
        one-key-per-block, no-decided-disposition, has-open-ideas, not-converged]
      framework: [method-in-section-5, no-other-method-in-section-5, reply-names-framework, file-conforms]
      specific:
        - name: five-ideas
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            id: IDEA-05
        - name: no-sixth-idea
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            id: IDEA-06
        - name: numbers-are-quoted-numbers
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+(?:value|effort|risk):[ \t]*(?![ \t])(?!"\d+(?:\.\d+)?"|null\b)\S
        - name: risk-is-0-20-or-50
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+risk:[ \t]*"(?!(?:0|20|50)")
        - name: score-has-one-decimal
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+score:[ \t]*(?![ \t])(?!\d+\.\d[ \t]*\n)(?!null[ \t]*\n)
        - name: rating-table
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \| Idea \| Reach \| Impact \| Confidence \| Effort \| Value \| Risk \| Score \|\n\|---\|---\|---\|---\|---\|---\|---\|---\|\n\| IDEA-01 \|
        - name: capacity-line
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            Capacity: 12 person-weeks
        - name: priority-cut-block
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \n## 6\. Convergence\n[\s\S]*?\n### Priority cut\n\nPriority cut: a proposal; priority stays with the PRD\n\n\| Rank \| Idea \| Cut \| Proposed disposition \| Why \|\n\|---\|---\|---\|---\|---\|\n
        - name: cut-and-proposal-words
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n\| (?:[0-9]+|-) \| IDEA-\d{2} \| (?!(?:Must|Should|Could|Won't|Not rated) \| (?:promoted|parked|rejected) \|)
        - name: proposals-in-prose
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            Proposed, awaiting confirmation:
        - name: figures-and-arithmetic
          type: llm
          focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          question: |-
            The user gave five ideas and these figures: 1 Saturday gaming night reach 150, effort 3; 2 homework help desk
            reach 300, effort 6; 3 teen advisory board reach 40, effort 2; 4 free printing reach 500, effort 1; 5
            extended Sunday opening reach 200, effort 10; capacity 12 person-weeks. Check section 5's rating table and
            the ideas block, one idea at a time, working each number out again yourself. PASS only if all of these
            hold for every idea: (a) its Reach and Effort cells equal the user's figures; (b) Impact is one of 3, 2, 1,
            0.5, 0.25 and Confidence one of 100, 80, 50; (c) Value = Reach x Impact; (d) Risk = 100 - Confidence; (e)
            Score = Value x (100 - Risk) / 100 / Effort, rounded half up to one decimal; (f) the idea's `value`,
            `effort`, `risk` and `score` fields equal the table's Value, Effort, Risk and Score; (g) the Priority cut
            table lists the ideas in descending score order, and the Cut column follows the capacity rule (running
            total of efforts down the ranking: Must up to 7.2, Should up to 9.6, Could up to 12, Won't above 12), and
            the proposed dispositions follow (Must and Should promoted, Could parked, Won't rejected only when its
            score is below a tenth of the highest score, else parked). FAIL otherwise, and quote the first row that
            breaks a rule and the rule.
        - name: ideas-are-the-users
          type: llm
          focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          question: |-
            The user's five ideas were: a Saturday gaming night; a homework help desk after school; a teen advisory
            board that picks new books; free printing for school projects; extended Sunday opening. PASS if the ideas
            block holds exactly these five, each in words close to the user's own, and no other idea. FAIL if one is
            missing, merged, split or added, and name it.
  - id: VER-19
    status: proposed
    covers: [BEH-16, BEH-18]
    level: eval
    obligation: |-
      The user names problem-reframing for a symptom with facts. The skill writes the five-whys block and the
      how-might-we block in section 5 in their fixed shapes, writes the jobs in section 3's table, takes its problems
      from root causes and jobs, rates with the default high, medium and low scores, and leaves every disposition open.
    case: uses-problem-reframing
    prompt: |-
      Our online shop's sales are down 20% since spring. Analytics show that visits are flat, but fewer visitors finish
      checkout. In April we began to make customers create an account before paying, and customers who emailed support
      said they did not want another password. Use the problem-reframing framework on this. Proceed without questions
      and write the brainstorm document.
    scaffold: none
    graders:
      common: [brn-exists, skill-fired, ran-validator-alone, no-leftovers, only-allowed-collections, only-allowed-fields,
        one-key-per-block, no-decided-disposition, has-open-ideas, not-converged]
      framework: [method-in-section-5, no-other-method-in-section-5, reply-names-framework, file-conforms]
      specific:
        - name: five-whys-block
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \n### Five whys\n\nChain 1, starting point: [^\n]+\n\n(?:- Why [1-5]: [^\n]+\n)+- Root cause: PRB-\d{2}(?: \(not confirmed\))?\n
        - name: how-might-we-block
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \n### How-might-we questions\n\n(?:- PRB-\d{2}: How might we [^\n]+\?\n)+
        - name: jobs-in-section-3
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            ## 3\. Target users\n\n\| Persona \| Job to be done \| Current workaround \| Pain \|\n\|---\|---\|---\|---\|\n(?:\|[^\n]*\n)*?\| [^|\n]+ \| When [^|\n]*, I want to [^|\n]*, so I can [^|\n]* \|
        - name: ratings-are-words
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+(?:value|effort|risk):[ \t]*(?![ \t])(?!"(?:high|medium|low)"|null\b)\S
        - name: score-is-an-integer
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+score:[ \t]*(?![ \t])(?!-?\d[ \t]*\n)(?!null[ \t]*\n)
        - name: reframing-quality
          type: llm
          focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          question: |-
            The user's facts were: sales down 20% since spring; visits flat; fewer visitors finish checkout; since April
            customers must create an account before paying; customers who emailed support did not want another password.
            PASS only if all hold: (a) no problem in the problems block merely restates "sales are down" (each is a root
            cause or an unmet job); (b) each answer in the five-whys block rests on one of those facts or is a
            NEEDS CLARIFICATION marker, and none invents a number or a cause; (c) the how-might-we block has exactly one
            bullet for each problem, each starting "How might we", naming a kind of person and an outcome, and naming no
            solution; (d) every idea addresses a problem that exists. FAIL otherwise and name the failing item.
  - id: VER-20
    status: proposed
    covers: [BEH-16, BEH-17, BEH-18]
    level: eval
    obligation: |-
      The user names improve-existing for a product that exists, with evidence in the request. The skill cites the
      evidence as sources in the frontmatter and in each problem's evidence, writes the SCAMPER table in its fixed
      shape with seven rows and a reason in every Note, adds no idea only to fill a prompt, and leaves every
      disposition open.
    case: uses-improve-existing
    prompt: |-
      Our clinic's online booking site is live. Patients pick a time and book, but about one in eight booked
      appointments is still a no-show. Last month's analytics show that 40% of the people who start the booking form
      never finish it, the form asks for 14 fields, and a patient cannot reschedule without phoning us. Use the
      improve-existing framework to find improvements to the existing booking site. Proceed without questions and
      write the brainstorm document.
    scaffold: none
    graders:
      common: [brn-exists, skill-fired, ran-validator-alone, no-leftovers, only-allowed-collections, only-allowed-fields,
        one-key-per-block, no-decided-disposition, has-open-ideas, not-converged]
      framework: [method-in-section-5, no-other-method-in-section-5, reply-names-framework, file-conforms]
      specific:
        - name: scamper-table
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \n### SCAMPER prompts\n\n\| Prompt \| Ideas \| Note \|\n\|---\|---\|---\|\n\| Substitute \| (?:none|IDEA-\d{2}(?:, IDEA-\d{2})*) \| [^|\n]*[^|\n ] \|\n\| Combine \| (?:none|IDEA-\d{2}(?:, IDEA-\d{2})*) \| [^|\n]*[^|\n ] \|\n\| Adapt \| (?:none|IDEA-\d{2}(?:, IDEA-\d{2})*) \| [^|\n]*[^|\n ] \|\n\| Modify \| (?:none|IDEA-\d{2}(?:, IDEA-\d{2})*) \| [^|\n]*[^|\n ] \|\n\| Put to another use \| (?:none|IDEA-\d{2}(?:, IDEA-\d{2})*) \| [^|\n]*[^|\n ] \|\n\| Eliminate \| (?:none|IDEA-\d{2}(?:, IDEA-\d{2})*) \| [^|\n]*[^|\n ] \|\n\| Reverse \| (?:none|IDEA-\d{2}(?:, IDEA-\d{2})*) \| [^|\n]*[^|\n ] \|\n
        - name: sources-recorded
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          flags: m
          pattern: |-
            \nsources:(?:[ \t]*\[|[ \t]*\n[ \t]+-)[ \t]*"(?:document|data|ticket|interview|url|note):[ ]
        - name: evidence-cites-a-source
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            evidence:[ \t]*"(?:document|data|ticket|interview|url|note):[ ]
        - name: ratings-are-words
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+(?:value|effort|risk):[ \t]*(?![ \t])(?!"(?:high|medium|low)"|null\b)\S
        - name: score-is-an-integer
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+score:[ \t]*(?![ \t])(?!-?\d[ \t]*\n)(?!null[ \t]*\n)
        - name: grounded-in-the-evidence
          type: llm
          focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          question: |-
            The user's evidence was: one in eight booked appointments is a no-show; 40% of people who start the booking
            form never finish it (last month's analytics); the form has 14 fields; a patient cannot reschedule without
            phoning. PASS only if all hold: (a) the problems rest on that evidence and no problem or evidence field
            invents a statistic; (b) every idea names the part of the product it changes; (c) every ID listed in the
            SCAMPER table's Ideas column exists in the ideas block, and every idea appears in at least one row; (d) a
            prompt recorded as "none" has a Note that gives a reason, and no idea reads as filler written to fill a
            prompt; (e) when fewer than five ideas exist, section 5 holds a sentence beginning "The existing product left fewer than
            five improvements". FAIL otherwise and name the failing item.
  - id: VER-21
    status: proposed
    covers: [BEH-16, BEH-18]
    level: eval
    obligation: |-
      The user names risk-first-mvp. The skill writes the pre-mortem block and the assumption riskiness table in their
      fixed shapes, makes test ideas that start "Test ASM-NN: ", rates them as the file says, and leaves every
      disposition open.
    case: uses-risk-first-mvp
    prompt: |-
      We are thinking of a mobile app where neighbours lend each other tools. Use the risk-first-mvp framework: what
      could make it fail, and what is the smallest thing we should test first? Proceed without questions and write the
      brainstorm document.
    scaffold: none
    graders:
      common: [brn-exists, skill-fired, ran-validator-alone, no-leftovers, only-allowed-collections, only-allowed-fields,
        one-key-per-block, no-decided-disposition, has-open-ideas, not-converged]
      framework: [method-in-section-5, no-other-method-in-section-5, reply-names-framework, file-conforms]
      specific:
        - name: pre-mortem-block
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \n### Pre-mortem\n\n(?:- [^\n]+ \((?:PRB|ASM)-\d{2}\)\n){5,10}\n
        - name: riskiness-table
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \n### Assumption riskiness\n\n\| Rank \| Assumption \| If wrong \| Severity \| Confidence \| Riskiness \|\n\|---\|---\|---\|---\|---\|---\|\n\| 1 \| ASM-\d{2} \| [^|\n]+ \| (?:high|medium|low) \| (?:high|medium|low) \| [1-9] \|\n
        - name: three-test-ideas
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            (?:idea:[ \t]*"Test ASM-\d{2}: [\s\S]*?){3}
        - name: ratings-are-words
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+(?:value|effort|risk):[ \t]*(?![ \t])(?!"(?:high|medium|low)"|null\b)\S
        - name: score-is-an-integer
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+score:[ \t]*(?![ \t])(?!-?\d[ \t]*\n)(?!null[ \t]*\n)
        - name: ranking-and-tests
          type: llm
          focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          question: |-
            PASS only if all hold: (a) in the riskiness table each Riskiness equals severity points (high 3, medium 2,
            low 1) times uncertainty points (confidence low 3, medium 2, high 1); (b) the rows are in descending
            Riskiness order, a tie ranked by the lower ASM number; (c) each of the three highest-ranked assumptions
            has at least one idea that starts "Test ASM-NN:" naming it; (d) an idea testing the assumption ranked 1 has
            value "high", one testing a rank 2 or 3 assumption has "medium", and one testing a lower-ranked assumption
            or none has "low"; (e) each idea's score equals 2 x value - effort - risk with high 3, medium 2, low 1;
            (f) each assumption's `validation` is a cheap test, not a build. FAIL otherwise and quote the first item
            that breaks a rule and the rule.
  - id: VER-22
    status: proposed
    covers: [BEH-15, BEH-16, BEH-17, BEH-18]
    level: eval
    obligation: |-
      The user names no framework and gives five candidate ideas to choose among, with no figures. The skill selects
      shortlist-ranking by itself (rule 2): section 5 holds its method text and no other framework's, the reply says
      why, the five ideas are the user's and no sixth exists, no reach or effort is guessed (all four fields null,
      reach marked NEEDS CLARIFICATION), and the cut is "Not rated" for every idea.
    case: selects-shortlist-ranking
    prompt: |-
      We have five feature ideas for our household budgeting app and we can only build two this quarter: CSV export,
      dark mode, shared household budgets, bill reminders, and receipt scanning. Which two should we pick? Proceed
      without questions and write the brainstorm document.
    scaffold: none
    graders:
      common: [brn-exists, skill-fired, ran-validator-alone, no-leftovers, only-allowed-collections, only-allowed-fields,
        one-key-per-block, no-decided-disposition, has-open-ideas, not-converged]
      framework: [method-in-section-5, no-other-method-in-section-5, reply-names-framework, file-conforms]
      specific:
        - name: five-ideas
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            id: IDEA-05
        - name: no-sixth-idea
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            id: IDEA-06
        - name: no-guessed-score
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n[ \t]+score:[ \t]*-?\d
        - name: score-is-null
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \n[ \t]+score:[ \t]*null
        - name: reach-marked-unknown
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \[NEEDS CLARIFICATION: reach\]
        - name: nothing-is-cut
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: not_contains
          pattern: |-
            \n\| [0-9]+ \| IDEA-\d{2} \| (?:Must|Should|Could|Won't) \|
        - name: every-idea-not-rated
          type: regex
          target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          match: contains
          pattern: |-
            \n### Priority cut\n\nPriority cut: a proposal; priority stays with the PRD\n\n\| Rank \| Idea \| Cut \| Proposed disposition \| Why \|\n\|---\|---\|---\|---\|---\|\n(?:\| - \| IDEA-\d{2} \| Not rated \| parked \| [^\n]+ \|\n){5}
        - name: selection-explained
          type: llm
          question: |-
            PASS if the reply names shortlist-ranking as the framework used AND gives, anywhere in the reply, the reason
            that the user gave candidate ideas to rank or choose among, in the words "you gave candidate ideas to rank
            or choose among" or words of the same meaning. FAIL if it names another framework, names none, or gives no
            reason.
        - name: ideas-are-the-users
          type: llm
          focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
          question: |-
            The user's five ideas were: CSV export; dark mode; shared household budgets; bill reminders; receipt
            scanning. PASS if the ideas block holds exactly these five, in this order, in words close to the user's, and
            no other idea. FAIL if one is missing, merged, split, reordered or added, and name it.
  - id: VER-23
    status: proposed
    covers: [BEH-15, BEH-16, BEH-17, BEH-18, BEH-19, ERR-06]
    level: unit
    obligation: |-
      A new test file keeps the framework catalog well formed and SKILL.md within its limits. It is written first, so
      that it fails before the build (every assertion below except the checklist and the length) and passes after.
      Run from the repository root, as test_validate_brn.py is:
      `PYTHONDONTWRITEBYTECODE=1 python3 -B src/tests/brainstorm/test_structure.py`. It uses the standard library
      only, and `unittest`, so pytest collects it with the repository's `--import-mode=importlib`. This version
      asserts the catalog only. Each later build of README §8 (intake-and-evidence, brownfield-iteration,
      mvp-and-prototype-path) adds the assertions for its own reference file to this file in its own iteration.
    file: src/tests/brainstorm/test_structure.py
    asserts:
      - "SKILL.md's checklist opening fence (the first line that is exactly three backticks) is on line 25 or earlier
        and before the line `## Inputs`. The `## ` headings outside fenced blocks are, in order: `## Workflow`,
        `## Inputs`, `## Decisions that belong to the user`, `## Output contract`, `## Examples`, `## References`. The
        lines `### 1.` to `### 8.` (each starting with the number, a full stop and a space) appear in order between
        `## Workflow` and `## Inputs`."
      - "Each file in `references/*.md` and `references/frameworks/*.md` shows its guide within its first 15 lines: a
        framework file the line `## When to use / When not to use`; INDEX.md the line `## Selection rules`; every
        other file the line `## Contents`."
      - "Every row of the Frameworks table in INDEX.md (the table under `## Frameworks`) names a framework in this
        order: shortlist-ranking, risk-first-mvp, improve-existing, problem-reframing, diverge-converge. Its file cell
        is `[NAME.md](NAME.md)` and the file exists in `references/frameworks/`."
      - "Every `*.md` file in `references/frameworks/` other than INDEX.md is the file of a row (no file is missing from
        the index)."
      - "Each of the five framework files has exactly these `## ` headings, in this order and no others, ignoring every
        line inside a fenced code block (a line starting with three backticks opens or closes a fence): When to use /
        When not to use; Steps; Questions to ask; Mapping to the BRN; Evaluation method text; Example."
      - "The table under `## Selection rules` has six rows numbered 1 to 6; their second cells equal the six strings
        pinned below; their third cells equal `that one`, `shortlist-ranking`, `risk-first-mvp`, `improve-existing`,
        `problem-reframing` and `diverge-converge` (the last five in backticks)."
      - "The table under `## Telling the user` has six rows numbered 1 to 6 whose second cells equal the six clauses
        pinned below, and INDEX.md contains the sentence `I'm using `name`, because clause.` and the no-list clause
        pinned below."
      - "SKILL.md's checklist, the lines between the first two lines that are exactly three backticks after the line
        `Work through this checklist:`, equals the eight lines pinned below."
      - "SKILL.md has at most 400 lines."
      - "SKILL.md's step 2 section (from `### 2. Select a framework` to `### 3. Diverge`) contains `selection rules`,
        `the first` followed by a line break and `rule that matches the request decides`, and `does not list` (with
        line breaks read as spaces), and does not contain `best fit the topic`. Its step 3 section contains `or` followed
        by a line break, two spaces and `the framework's *Steps* say otherwise`."
      - "In each framework file, the first line of the Evaluation method text section that starts `> ` starts with
        `> ` and that framework's token (pinned below), and no `> ` line of that section contains another framework's
        token."
      - "In each of the five files, the Mapping to the BRN section contains `value`, `effort`, `risk` and `score`, each
        in backticks."
      - "No framework file or INDEX.md contains `<!--`, `docs/specs/brainstorming`, `README.md`, `TODO` or
        `PLACEHOLDER` (shipped files cite no proposal document)."
      - "diverge-converge.md's section `When to use / When not to use` contains the text `ranked: use`, a line break and
        `` `shortlist-ranking` `` (the edit of §2)."
    pinned: |-
      Checklist (SKILL.md, the eight lines, byte for byte):
      - [ ] 1. Intake: topic, existing BRNs, clarifying questions
      - [ ] 2. Select a framework
      - [ ] 3. Diverge: problems, ideas, assumptions
      - [ ] 4. Evaluate with the framework
      - [ ] 5. Propose dispositions and ask the user to confirm
      - [ ] 6. Write the BRN
      - [ ] 7. Validate the BRN
      - [ ] 8. Report and hand off
      Selection rules, second cells, rows 1 to 6 (README §5's text, one line each):
      The user names a framework that the index lists
      The request supplies three or more candidate ideas, or names a backlog or list to use, and asks to rank, prioritise, choose among or cut them
      The request asks what to build first, for an MVP or a prototype, or what could make the idea fail
      Project kind is brownfield and the topic is improving, extending or fixing the existing product
      After intake, no problem can be stated with an affected person and what hurts them (the topic is a symptom, a goal or a solution)
      Otherwise
      Clauses, rows 1 to 6 of the table under "Telling the user":
      you named it
      you gave candidate ideas to rank or choose among
      you asked what to build first or what could make it fail
      the product exists and the topic is improving it
      no problem with an affected person and a hurt could be stated yet
      no more specific rule matched
      No-list clause: you named shortlist-ranking but gave no list, so I'm using diverge-converge instead
      Tokens (after `> `): Shortlist ranking: | Risk-first MVP: | Improve existing: | Problem reframing: | Diverge-converge:
  - id: VER-24
    status: proposed
    covers: [BEH-15, BEH-16, ERR-06]
    level: manual
    obligation: |-
      Live, in a session with the question tools, following `docs/runbooks/brainstorm-manual-test.md` (a new section),
      with a copy of the built plugin loaded by `claude --plugin-dir`, never `src/`. Each step starts a fresh session.
      (a) Rule 3: "Brainstorm a mobile app where neighbours lend tools. What should we build first?" The skill says it
      is using risk-first-mvp, because you asked what to build first or what could make it fail, and its BRN section 5
      starts with "Risk-first MVP:". (b) Rule 4: in a project holding PRD-001 for a booking site, "Brainstorm
      improvements to our booking site, which is already live." improve-existing, because the product exists and the
      topic is improving it. (c) Rule 5: "Brainstorm: we want 10,000 users by Christmas." (any intake question answered "not
      sure" or "don't know") problem-reframing, because no problem with an affected person and a hurt could be
      stated yet. (d) Rule 6: "Brainstorm ways to cut no-shows at our dental clinic." with the intake questions answered
      "patients who forget, and the clinic loses the hour" diverge-converge, because no more specific rule matched. (e) ERR-06: "Brainstorm
      with the SWOT framework: ways to cut no-shows at our dental clinic." The skill says SWOT is not listed, names
      the five frameworks, and then uses one by rules 2 to 6 (here diverge-converge) and says why. (f) The exception
      of BEH-15 item 5: "Use shortlist-ranking to brainstorm ways to cut no-shows." with no list: the skill asks for
      the list; answered "no list", or run with questions waived, it says it is using diverge-converge instead. (g)
      The switch: after (d), "Use problem-reframing instead." The skill switches, reads that file and says so; the
      final report names problem-reframing. (h) SPEC-001 VER-05: add a sixth row and file to the copy's index with
      SKILL.md untouched, and name the sixth framework: the skill uses it; delete its file: the skill falls back to
      diverge-converge and names the file. Record each step's result and the Claude Code version in SPEC-001's §9.
    runbook: docs/runbooks/brainstorm-manual-test.md
```

## 6. Staged files

All five are complete files as they should exist at the destination (R6). They are the framework text a builder
copies; the unit test of VER-23 and the evals of VER-18 to VER-22 test them. Each framework's Example was built into
a scratch BRN with filler that the Example does not show, and `validate_brn.py` printed `OK` for all four; the
regexes of §5 were run with `node` against those four BRNs.

| Staged file | Destination |
|---|---|
| [staged/skills/brainstorm/references/frameworks/INDEX.md](staged/skills/brainstorm/references/frameworks/INDEX.md) | `src/claude/DevForgeAI/skills/brainstorm/references/frameworks/INDEX.md` (replaces) |
| [staged/skills/brainstorm/references/frameworks/shortlist-ranking.md](staged/skills/brainstorm/references/frameworks/shortlist-ranking.md) | the same folder (new) |
| [staged/skills/brainstorm/references/frameworks/problem-reframing.md](staged/skills/brainstorm/references/frameworks/problem-reframing.md) | the same folder (new) |
| [staged/skills/brainstorm/references/frameworks/improve-existing.md](staged/skills/brainstorm/references/frameworks/improve-existing.md) | the same folder (new) |
| [staged/skills/brainstorm/references/frameworks/risk-first-mvp.md](staged/skills/brainstorm/references/frameworks/risk-first-mvp.md) | the same folder (new) |

The framework files cite `references/brownfield.md` and `references/mvp-path.md` only with "when it exists", so the
catalog can ship before intake-and-evidence, brownfield-iteration and mvp-and-prototype-path (README §8, build
order 1). They cite no file of this folder.

## 7. Open questions

1. **What a switch keeps.** SKILL.md says "switch if they ask" and BEH-16 keeps that, but nothing says what happens
   to what the first framework already wrote when the user switches after step 3. Options: (a) restart at the new
   framework's first step, keeping only the user's own ideas, in their words; (b) keep every problem and idea and
   re-rate them with the new framework. This document does not decide it; VER-24 (g) checks only that the framework
   changes and is named.
2. **Two assumption rankings in one BRN.** With `risk-first-mvp`, section 5 holds this framework's riskiness table
   (severity × uncertainty) and, when mvp-and-prototype-path.md is built, section 7 holds C-07's ranking, which that
   document orders by level, confidence and number (its §3.1, "the framework's working"). The two can order the
   assumptions differently. Options: (a) keep both, as that document accepts (the default here); (b) drop the
   riskiness table and let the test ideas' `value` follow C-07's ranks, which makes `risk-first-mvp` depend on
   mvp-and-prototype-path.md being built. Settled in review (option a): every document now says, in the same words,
   that the riskiness table rates the test ideas and nothing else and that C-07 alone decides the first release cut.
   Bryan: confirm.
3. **Numbers in `value`, `effort` and `risk`.** `references/output-rules.md` and `validate_brn.py` accept a number
   there, but `src/schemas/brainstorm.schema.json` types the three fields as string or null (only `score` may be a
   number), and R1 forbids a schema change. This document writes quoted numbers, which satisfy all three. Options:
   (a) keep the quoted numbers (default); (b) fix `output-rules.md` to say "a quoted string" for these fields, so the
   rule matches the schema; (c) allow numbers in the schema, which R1 rules out for now.
4. **Where "Decisions that belong to the user" sits.** Moving the whole Workflow section first (the only move that
   keeps the `### 1.` to `### 8.` steps under their `## Workflow` heading, with no heading renamed) puts `## Decisions
   that belong to the user` after the steps. Options: (a) accept that order (this document); (b) keep Decisions
   directly after the checklist by giving the steps their own `## Steps` heading under Workflow's rules, which renames
   a heading and moves the task-list rules; (c) restate the two decisions in one line inside the opening paragraph.
5. **The constants of the RICE-style method and of the proposals.** The impact scale (3, 2, 1, 0.5, 0.25), the
   confidence values (100, 80, 50), the capacity limits (0.6, 0.8 and 1.0 of the capacity), the won't threshold
   (below a tenth of the top score) and the promotion rule of the other three frameworks (up to three ideas with a
   score of 3 or more; park at 1 or more; reject at 0 or less) are defaults chosen here; no spec, ADR or recorded
   decision sets them. Options: (a) accept them; (b) change named values before the build, in the staged files and in
   VER-18's llm question, which repeats the limits.
