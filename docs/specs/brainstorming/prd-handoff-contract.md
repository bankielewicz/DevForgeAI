# Brainstorm skill: the hand-off contract with the PRD skill

**Status:** proposal, written 2026-11-18 by claude-code (session fa59a935-ed2e-4502-b6c4-93bb6d847546) for Bryan's
review. It changes no spec, skill or plugin version. Brainstorm's side adds BEH-34 and VER-39 to
`docs/specs/spec/SPEC-001.md` (version 17 today). The PRD skill's side proposes items for
`docs/specs/spec/SPEC-002.md` (version 9 today, approved): SPEC-002#BEH-27 to SPEC-002#BEH-30, SPEC-002#ERR-12 and SPEC-002#VER-50 to SPEC-002#VER-54, which are
the next free IDs there (SPEC-002 ends at SPEC-002#BEH-26, SPEC-002#ERR-11 and SPEC-002#VER-49). Both take effect only in a new version of each
spec, approved by Bryan, built in plugin-dev iterations. This document is built last (README §8): it needs
[intake-and-evidence.md](intake-and-evidence.md) (C-01, C-03, C-08, C-09) and
[mvp-and-prototype-path.md](mvp-and-prototype-path.md) (C-05, C-07) built first. Read [README.md](README.md) first.

## Workflow steps this changes

Brainstorm's steps (SKILL.md's lines unchanged, R2):

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 8. Report and hand off | Report block of four lines; `/devforgeai:prd BRN-NNN` | The block gains two lines, the project kind and the first-release ideas, when the BRN has the `Project kind:` line (§3.1) |

The PRD skill's steps (its checklist lines don't change either):

| PRD step | Today | Added by this document, only for a BRN with the `Project kind:` line |
|---|---|---|
| 3. Read the BRN | Frontmatter, the three collections, the success signals | Also the project kind, the existing-product table, the target users table, the first release cut, the ranking, and the already covered, previously decided and assumption updates tables (§3.2) |
| 6. Draft from the BRN | Problems, requirements, assumptions, metrics | Section 3 from the target users table; assumptions in rank order with a prose list; metrics from the first-release bullets; non-goals and section 9 prose from the brownfield tables (§3.3) |
| 7. Interview only the gaps | Rounds 1 to 5 | Round 1: the stage question carries a suggestion for a brownfield BRN and the primary-users question is skipped; round 3 shows the first release cut as a proposal; round 5 takes baselines from the bullets (§3.3, §3.4) |
| 10. Report and hand off | The report block, `[NEEDS ADR]` pairs, discussion | The discussion gains one line for suggestions that were not written (§3.4) |

## 1. Scope

**In.**

- The two lines of step 8's report block, and when the old four-line block still applies.
- For each BRN shape, what the PRD skill does with it, as exact edits to `skills/prd/references/brn-mapping.md`,
  `skills/prd/references/interview.md` and three places in `skills/prd/SKILL.md`.
- The rule that a BRN without the `Project kind:` line gets exactly today's behaviour.
- The carve-outs from SPEC-002#BEH-19 (reuse before asking) and from "Decisions that belong to the user": a project
  kind and a first release cut are suggestions, never stated values.
- The SPEC-002 items, the eval cases (additions to `src/tests/prd/make_evals.py`), and the manual item.

**Out.**

- Producing any shape: the other documents of this folder.
- The PRD's other steps, its schema, the policy and architecture steps.
- The Codex port of the PRD skill (`src/codex/`, kept by Codex sessions).
- The ui skill, the architecture skill and the epic skill, which read BRNs only through the PRD.

**The predicate.** "A BRN with the `Project kind:` line" means a BRN that has the project-kind line as README §4's
kind gate defines it: a line after the frontmatter and outside every fenced block whose text, lowercased with its spaces
collapsed, starts with `project kind:`. The value is the text after the line's first colon, trimmed and lowercased:
`greenfield`, `brownfield`, or anything else (the marker form), which counts as neither. The PRD skill tests the
predicate by reading the BRN; it runs no script. A BRN without the line is an **earlier-shape BRN**. A BRN with the
line may still lack some shapes (a build that stops before the cut and the ranking): the skill reads the shapes that
are present and treats the others as absent, with no `Ignored:` line, because an absent shape is not an unreadable one.

## 2. Changes by file

### Brainstorm

| File | Change |
|---|---|
| `skills/brainstorm/SKILL.md`, step 8 | The report block, below. About +4 lines (316 today; the other documents add their own; the limit stays 400, R2) |

Replace, in step 8 item 1, the block

```text
BRN-NNN written to docs/specs/brainstorm/BRN-NNN.md (framework: [name])
Problems: N · Ideas: N · Assumptions: N
Promoted: IDEA-NN, … | none confirmed yet (proposals are in section 6)
Open questions: [each NEEDS CLARIFICATION marker and open assumption, briefly]
```

with, and add after the block the paragraph that follows it:

```text
BRN-NNN written to docs/specs/brainstorm/BRN-NNN.md (framework: [name])
Project kind: greenfield | brownfield | not decided
Problems: N · Ideas: N · Assumptions: N
Promoted: IDEA-NN, … | none confirmed yet (proposals are in section 6)
First release: IDEA-NN, … (confirmed) | IDEA-NN, … (proposed, not confirmed) | none proposed
Open questions: [each NEEDS CLARIFICATION marker and open assumption, briefly]
```

```text
Write the two extra lines only when the BRN has the `Project kind:` line; otherwise the block is the four
lines it was. `Project kind` repeats the BRN's value, and says `not decided` for the `[NEEDS CLARIFICATION: …]`
form. `First release` lists the cut's `yes` ideas in ID order, with `(confirmed)` when the cut's status line says
`confirmed by` and `(proposed, not confirmed)` when it says `proposed, not confirmed`; it says `none proposed` when
the cut has no `yes` row or the BRN holds the line `No idea is promoted or proposed for promotion.`
```

The block still opens the reply and the next step is still last (SPEC-001 BEH-10).

### PRD skill

| File | Change |
|---|---|
| `skills/prd/references/brn-mapping.md` | Eight edits, §3.3 |
| `skills/prd/references/interview.md` | Four edits, §3.4 |
| `skills/prd/SKILL.md` | Three edits: "Decisions that belong to the user" (one sentence), step 3 (one bullet), step 10 item 3 (one sentence), about +8 lines (430 today, limit 500), §3.2 |
| `skills/prd/provenance.yaml`, SKILL.md `devforgeai-version`, `plugin.json`, `.claude-plugin/marketplace.json`, `src/tests/progress/test_adapter_structure.py` | Version bumps (SKL-002's next version; plugin version) |
| `docs/specs/spec/SPEC-002.md` | A new version (10), with §3.7's items, §4's mapping table gaining the rows of §3.3, §9's rows, two Change Log rows (the change, authored `claude-code (session <ID>)`, and the owner's approval), and every `upstream` link that cites SPEC-002 moved to it (CLAUDE.md, "Rules a change must not break") |
| `src/tests/prd/test_structure.py` | `SPEC_STATE` moves from `"SPEC-002": (9, "approved")` to the new version once approved |
| `src/tests/prd/make_evals.py`, `check_graders.py` | §5 |
| `CLAUDE.md` | The skills table's prd row, per the repository's rule that it names the current SPEC and SKL versions |

**The sequencing with the interview build.** SPEC-002 versions 6 to 9 (the interview at scale: SPEC-002#BEH-19 to SPEC-002#BEH-26) are
approved and not built. `interview.md` and `brn-mapping.md` on disk today are SKL-002 v6's, which do not hold them.
The edits below are written against today's files, anchored on rows and sentences that SPEC-002#BEH-19 to SPEC-002#BEH-26 do not
rename: the Round 1 table rows, the "Suggest, never assume" bullet, the Round 3 section, the Round 5 section. Where
a rule needs the interview build (the reuse line, the triage table), it says so and applies only then. Whether this
build goes before or after the interview build is open question 1.

## 3. Behaviour

### 3.1 Brainstorm's side

The two lines come from the BRN as written at the end of step 7 (after the read-back), never from the run's
intentions. A confirmed cut is reported `(confirmed)` only when the BRN says so.

### 3.2 The PRD reads the shapes, or does not

1. **Earlier shapes.** A BRN without the `Project kind:` line is read exactly as today. The PRD skill reads none of
   the shapes of this document in it, even when it happens to hold a heading such as `### First release cut`, and
   writes none of the lines of §3.3 and §3.4. Every existing prd case must pass unchanged (SPEC-002#VER-50).
2. **New shapes.** With the line, step 3 also reads, when present: the project kind (`greenfield`, `brownfield`, or
   the marker form, which counts as neither); the `### Existing product` table (C-02); the target users table
   (section 3, C-03); the `### First release cut` status line and table (C-05); the `### Already covered` and
   `### Previously decided` tables (C-06); the `### Assumption updates` table (C-11); the `### Assumption risk ranking` table (C-07); and section 8's bullets
   (C-08).
3. **A shape that does not read.** A table that lacks its header, or has a row of the wrong width, or a status line
   that is neither of C-05's two forms, is **ignored as a whole** (SPEC-002#ERR-12): the PRD skill treats that shape as
   absent, never repairs the BRN, and says in the reply `Ignored: <shape> in BRN-NNN (it does not read as
   specified)`. This is not SPEC-002#ERR-05, which stops the run for an item block that cannot be read.
4. **No new decision.** Nothing in a shape is a value the user supplied for `stage`, `operating_context`,
   `priority` or `release`. The rule of SKILL.md's "Decisions that belong to the user", that a value is written only
   when the user supplied it or confirmed a suggestion, holds unchanged. A suggestion becomes a value only when the
   user picks it.

**SKILL.md edit 1** (prd; "Decisions that belong to the user"): after the paragraph that ends
`…which then builds on a choice nobody made.` add

```text
A BRN's project kind, first release cut and ranking are never a stated value: they can suggest an option
(interview.md), and a value is written only when the user picks it.
```

**SKILL.md edit 2** (prd; step 3 "Read the BRN"): after the bullet list, whose last bullet ends `Continue only on an
explicit yes; with no answer, write nothing.`, and before the paragraph that starts `Use **only** ideas`, add

```text
When the BRN has the line `Project kind:`, also read the shapes brn-mapping.md names, and ignore any that does
not read as specified (SPEC-002#ERR-12). A BRN without that line is read as before.
```

**SKILL.md edit 3** (prd; step 10 item 3, "Any other discussion"): after the end of item 3, which reads
`…(a suspect link to review, never an error; output-rules.md check 9), and that the new revision hasn't been reviewed.`
(the only place where that phrase follows `output-rules.md check 9),`), add

```text
Add one line, `Suggested, not written: …`, for each suggestion a BRN shape made that no answer settled (§3.4), and a
line `Ignored: …` for each shape the skill could not read.
```

### 3.3 `brn-mapping.md`: old text to new text

Every edit applies only to a BRN with the `Project kind:` line, which the new section 2 below says.

**M1. Contents.** After the line `- What the BRN offers` add the line `- A BRN with the Project kind line`.

**M2. Summary table.** After the paragraph that follows the table (the line that starts `` `version` in every BRN link ``) add the
note `Rows for a BRN with the `Project kind:` line:` and a second table with the header below (a row cannot follow a
note inside the first table):

```markdown
| BRN | PRD | Link |
|---|---|---|
| Target users table (section 3) | The table in section 3; the primary-users question is skipped | None |
| Existing product, already covered (sections 1 and 6) | Prose in section 9; never a requirement | None |
| Previously decided, decision `rejected` (section 6) | A non-goal in words, no ID | None |
| Assumption updates, a confirmed row (section 6) | A sentence in section 10, and the carried assumption's `state` as the BRN holds it | None beyond the assumption's `derives` link |
| Assumption updates, a row not confirmed | Nothing | None |
| Project kind | A suggestion on the stage question | None |
| First release cut (section 6) | A suggestion on the release question of round 3, when confirmed | None |
| Assumption risk ranking (section 7) | The order of `assumptions` and a prose list in section 10 | The assumptions' own `derives` links |
| First-release success signals (section 8) | `success_metrics`, one for each bullet whose idea is drafted | `derives` that IDEA |
```

**M3. What the BRN offers.** Replace the bullet
`- Section 1 (context) and section 3 (target users): prose for PRD sections 2 and 3.` with

```text
- Section 1 (context) and section 3 (target users): prose for PRD section 2 and, in a BRN with the `Project kind:`
  line, a table for PRD section 3 (next section).
```

**M4. A new section.** After "What the BRN offers" insert:

```markdown
## A BRN with the Project kind line

Applies only when the BRN has the project-kind line (the predicate in the scope of this document). Without it, skip this section and every row marked
"`Project kind:` line" in this file: read the BRN as before.

- **Project kind.** `greenfield`, `brownfield`, or `[NEEDS CLARIFICATION: …]`, which counts as neither. It
  suggests an answer to the stage question (interview.md) and decides nothing.
- **Target users** (section 3). A table `| Persona | Job to be done | Current workaround | Pain |`. Write PRD section
  3 as the table `| Persona | Goal | Context | Frequency |`, one row for each BRN row, in the BRN's order: Persona the
  same text, Goal the Job to be done, Context `Today: <Current workaround>. Pain: <Pain>`, Frequency
  `[NEEDS CLARIFICATION: how often <Persona> uses it]`. The personas are the primary users, so the
  primary-users question is skipped (interview.md). A BRN whose section 3 holds no table, or a table with no row,
  is read as today.
- **First release cut** (section 6). The status line is `First release cut: confirmed by <NAME> on <DATE>` or
  `First release cut: proposed, not confirmed`; the table lists each idea promoted or proposed for promotion with
  `yes` or `no`. It never sets `release`. A confirmed cut is shown as a suggestion in round 3 (interview.md); a
  proposed one is shown as a proposal only.
- **Assumption risk ranking** (section 7). A table in rank order, riskiest first, of the open assumptions. It sets
  the order of the PRD's assumptions (Assumptions, below).
- **Existing product, already covered, previously decided** (sections 1 and 6, brownfield). Written as follows,
  never as requirements: each `### Existing product` row becomes one sentence in section 9, `Builds on <Document>
  version <Version>, which already covers <What it already covers>.`; each `### Already covered` row one sentence in
  section 9, `Already covered: <Suggestion> (<Covered by>).`; each `### Previously decided` row whose Decision is
  `rejected` one non-goal in section 4, in words and without an ID (Everything else), and a row with any other
  Decision nothing. No FR is drafted from any of these rows, and none carries a link. A table replaced by the line
  `None.` has no rows.
- **Assumption updates** (section 6, brownfield, `### Assumption updates`). A table `| Earlier assumption | Change |
  Evidence | Status |`; `Change` reads `OLD to NEW`; `Status` is `proposed, not confirmed` or `confirmed by NAME on
  DATE`. A row that is `confirmed by` is the user's decision: find the assumption of this BRN whose item-level
  `upstream` link names the `Earlier assumption` (`BRN-001#ASM-01` is `id: BRN-001`, `item: ASM-01`; whatever the
  link's relation). The PRD assumption derived from it takes the `state` that BRN assumption holds, as always
  (Assumptions); when that `state` is not the row's NEW, keep the BRN assumption's `state` and write in the reply
  `Ignored: assumption update ASM-NN in BRN-NNN (the assumption's state differs)`. Add one sentence to section 10:
  `Updated from BRN-NNN#ASM-MM: OLD to NEW (<Evidence>; BRN-NNN vN).` A row that is `proposed, not confirmed`
  writes nothing and gets no sentence, and the carried assumption keeps the `state` the BRN holds. A row whose
  earlier assumption no assumption of this BRN links to writes nothing. This is the only use of an item-level
  `upstream`: the PRD's own `derives` links name this BRN's items, and a link to an earlier BRN is never copied.
```

**M5. Assumptions.** Replace the bullet `- Carry each BRN assumption over as a PRD assumption with the same
statement and validation, and `state` unchanged. Link it with `relation: derives`.` with

```text
- Carry each BRN assumption over as a PRD assumption with the same statement and validation, and `state`
  unchanged. Link it with `relation: derives`.
- When the BRN has the `Project kind:` line and a ranking table: write the carried assumptions in rank order, the
  assumptions the ranking does not list (`validated` or `invalidated` ones) after them in the BRN's order, and
  number them `ASM-01` onward in that order. After the block, in section 10, write the line `Ranked riskiest first
  (BRN-NNN vN):` and one bullet for each ranked assumption, `- ASM-NN: if wrong, <the words after the first colon of
  its If wrong cell>. Confidence <Confidence>. Cheapest test: <its Cheapest test cell> (BRN-NNN#ASM-MM)`, where
  ASM-MM is the BRN's number. Write no idea ID in the bullet. `validation` is never replaced by the cell.
```

**M6. Candidate success signals into metrics.** After the bullet `- If the signal measures a drafted idea's effect, link it:
`derives` that IDEA. Otherwise leave out `upstream`.` add

```text
- In a BRN with the `Project kind:` line, each bullet reads `- IDEA-NN: <outcome>; baseline <value>`. Take the
  idea ID, the outcome up to the last `; baseline `, and the rest as the value. It becomes one metric only when
  that idea is promoted and drafted by this PRD (not left out because a PRD already cites it): `metric` the outcome
  stated as something measurable, `derives` that IDEA, `baseline` the value as written (a
  `[NEEDS CLARIFICATION: …]` value is written as it stands), `target` and `measured_by` markers unless the user
  answers. A bullet for any other idea is dropped, so a `yes` idea that is still `open` gives no metric. `- None.` gives none. Ideas the cut marks `no` have no bullet.
```

**M7. Everything else.** Replace the bullet `- **Users** (section 3): from the BRN's target users and problems' `who`.`
with

```text
- **Users** (section 3): from the BRN's target users and problems' `who`; in a BRN with the `Project kind:` line
  and a target users table, the table (A BRN with the Project kind line).
```

and after the **Non-goals** bullet add `In such a BRN, a `Previously decided` row whose Decision is `rejected` is one more
non-goal in words, without its ID.`

**M8. A worked example.** After the existing worked example add:

```text
BRN-001 (version 1, `Project kind: brownfield`) has the cut IDEA-01 yes and IDEA-03 no, confirmed. The FR for IDEA-01
and the FR for IDEA-03 both keep `release: null`; round 3's question for the first says that the confirmed cut puts
IDEA-01 in the first release, and its `later` option for IDEA-03 reads `later (suggested)`. Section 5 holds one
metric, for IDEA-01's bullet. Nothing is written from the cut.
```

### 3.4 `interview.md`: old text to new text

Every edit applies only to a BRN with the `Project kind:` line.

**I1. Rules for every call.** After the sentence `A suggestion is written only after the user picks it.` in the
"Suggest, never assume" bullet add: `A BRN's project kind and first release cut are suggestions in this sense, however
clearly the BRN states them.`

**I2. Round 1, the Stage row** (the row whose first cell is `Stage?`; the Operating context row has the same `Skip when`
text and is not changed). Replace its `Skip when` cell `The request or BRN states it` with `The request or BRN
states it. A project kind is not a statement of stage`, and add to its `Options` cell the sentence `When the BRN says
Project kind: brownfield, label the evolution option "evolution (suggested)"; with greenfield or the marker form,
suggest nothing. The question is still asked.` The label's wording is exactly `evolution (suggested)`; the description
is as before. Picking any option writes that stage, as always.

**I3. Round 1, the Primary users row.** Replace its `Skip when` cell `The BRN's target users section names them`
with `The BRN's target users section names them, or its section 3 holds the target users table with a row (brn-mapping.md);
say in one line that the personas come from the table`. Under the interview build, the reuse line lists
`primary users=<the Persona cells joined by "; "> (BRN-NNN vN §3)`.

**I4. Round 3: the cut.** After the table of options and the paragraph that follows it (`The user may also edit…`) add:

```markdown
**First release cut.** Only for a requirement whose `upstream` links name an idea that appears in the BRN's cut
table. Start the requirement's question with one line, then the usual question and options:

| The BRN's cut | The line | Options |
|---|---|---|
| Confirmed, the idea is `yes` (or any linked idea is) | `Release cut (BRN-NNN vN, confirmed by <NAME> on <DATE>): IDEA-NN is in the first release.` | Unmarked: the cut proposes `release: current`, and the priority is the user's |
| Confirmed, the idea is `no` (and every linked idea is) | `Release cut (…, confirmed …): IDEA-NN is not in the first release.` | `later` is labelled `later (suggested)` |
| Proposed, not confirmed | `Release cut (BRN-NNN vN, proposed and not confirmed): IDEA-NN is proposed for the first release.` (or `…proposed to be left out of the first release.`) | None marked |

The line is context, not an answer: nothing is written until the user answers (SKILL.md, "Decisions that belong to
the user"). A non-functional requirement has no line. Under the interview build, the table of SPEC-002#BEH-22 labels a row
`later (suggested)` only by its own rule (nobody ticked it) and by no cut; a requirement whose line would read
"in the first release" is shown in the table with `no suggestion` and a blank value, and accepting every row never
writes it.
```

**I5. Round 5.** After the sentence `Options may suggest values from the BRN's evidence.` add: `For a metric that brn-mapping.md
drafted from a section 8 bullet, the baseline is already the BRN's and is not asked again; ask only the target (with its
time frame) and what measures it.`

### 3.5 What the PRD does, as a table

| BRN shape | PRD step | Does | Never |
|---|---|---|---|
| `Project kind: brownfield` | 7, stage question | Labels `evolution (suggested)` | Skips the question, writes `stage` unasked, or treats `release` or `operating_context` as known |
| `Project kind: greenfield`, or the marker | 7, stage question | Nothing | Suggests a stage |
| Target users table (C-03) | 6, 7 | Writes section 3 as a table; skips the primary-users question | Asks who the primary users are |
| First release cut, confirmed (C-05) | 7, round 3 | Shows the cut's line; labels `later (suggested)` for a `no` idea | Writes `release`; marks an option for a `yes` idea |
| First release cut, proposed | 7, round 3 | Shows it as a proposal | Marks any option; calls it confirmed |
| Assumption risk ranking (C-07) | 6, 8 | Orders the `assumptions`; section 10's prose | Replaces `validation`; writes an idea ID |
| Success signals (C-08) | 6, 7 round 5 | One metric for each bullet of a drafted idea, with the baseline | Drafts a metric for an idea that is not drafted |
| Existing product, already covered (C-02, C-06) | 6 | Section 9 prose | A requirement, a link |
| Assumption updates (C-11) | 6 | A confirmed row: one sentence in section 10; the state is the carried assumption's own | Acts on a row that is not confirmed; copies an earlier BRN's link |
| Previously decided, `rejected` (C-06) | 6 | A non-goal in words | An ID, a link |
| An unreadable shape | 3 | Ignores it, says so | Repairs the BRN |

**Under "proceed without questions", or when the budget is spent.** No question is asked, so no suggestion is
answered: `stage` stays `null`, every `release` stays `null` (SPEC-002#BEH-06), and the reply carries the line
`Suggested, not written: stage=evolution (BRN-NNN vN, Project kind brownfield); release current for FR-001, release
later for FR-002 (BRN-NNN vN, confirmed first release cut)`, listing only the suggestions that exist. A proposed cut
adds `release proposals not applied (the cut is proposed, not confirmed)`. The PRD's Change Log row is unchanged.

**The carve-out from SPEC-002#BEH-19 (the interview build).** The reuse before asking does not read a project kind or a
first release cut as a source of `stage` or `release`: they state a suggestion, not a value. The reuse line may list
`primary users` from the BRN's section 3 table. It never lists `stage` or `release` from these shapes.

### 3.6 Brainstorm and PRD together: what a user sees

The brainstorm of a product that does not exist, with the cut confirmed, reports

```text
BRN-001 written to docs/specs/brainstorm/BRN-001.md (framework: diverge-converge)
Project kind: greenfield
Problems: 3 · Ideas: 7 · Assumptions: 4
Promoted: IDEA-01, IDEA-02, IDEA-04, IDEA-06
First release: IDEA-01, IDEA-04, IDEA-06 (confirmed)
Open questions: [NEEDS CLARIFICATION: how many owners have refused a request]; ...
```

(the staged [BRN-001.md](staged/examples/brainstorm-greenfield-mvp/BRN-001.md)). The PRD run on it asks no
primary-users question and writes section 3 as the table of its three personas; asks the stage question with no
suggestion (greenfield); puts `Release cut (BRN-001 v1, confirmed by Sam Okoye on 2026-11-18): IDEA-01 is in the
first release.` above the question for the requirement of IDEA-01, with no option marked, and for the requirement of
IDEA-02 (promoted, cut `no`) `later (suggested)`; writes three metrics, one for each bullet; and orders the four
assumptions ASM-02, ASM-01, ASM-03, ASM-04 of the BRN as ASM-01 to ASM-04 of the PRD, with the ranked prose below.

### 3.7 The items

The next block (BEH-34) is SPEC-001's. Every item after it, with the `SPEC-002#` prefix, is proposed for SPEC-002; the prefix
is the document's own mark and is dropped when the item is written into that spec.

```yaml items
behaviors:
  - id: BEH-34
    status: proposed
    rule: "When the BRN has the line 'Project kind:' (README §4's kind gate: a line after the frontmatter and outside every fenced block whose text, lowercased with spaces collapsed, starts with 'project kind:'), step 8's report block has two more lines, in this order: 'Project kind: greenfield | brownfield | not decided' after the first line, and 'First release: IDEA-NN, … (confirmed) | IDEA-NN, … (proposed, not confirmed) | none proposed' after the 'Promoted:' line. 'Project kind' repeats the BRN's value, 'not decided' for the NEEDS CLARIFICATION form. 'First release' lists the cut's yes ideas in ID order, '(confirmed)' only when the cut's status line says 'confirmed by', and 'none proposed' when the cut has no yes row or holds the line 'No idea is promoted or proposed for promotion.'. The lines are read from the BRN as it stands after step 7. A BRN without the 'Project kind:' line gets the four-line block, unchanged. The block still opens the reply and the next step is still last."
    changes: "extends SPEC-001 BEH-10"
    lands_in: "skills/brainstorm/SKILL.md, step 8 item 1"
```

SPEC-002's proposed items (numbers found: highest SPEC-002#BEH-26, SPEC-002#ERR-11, SPEC-002#VER-49 in version 9; used: SPEC-002#BEH-27 to SPEC-002#BEH-30,
SPEC-002#ERR-12, SPEC-002#VER-50 to SPEC-002#VER-54):

```yaml items
behaviors:
  - id: SPEC-002#BEH-27
    status: proposed
    rule: "Read the shapes of a BRN with the 'Project kind:' line, and only of such a BRN. At step 3, a BRN that has the project-kind line (README §4's kind gate) is also read for its project kind (the value after the first colon: greenfield, brownfield or neither), its '### Existing product', '### Already covered', '### Previously decided' and '### Assumption updates' tables, its section 3 target users table, its '### First release cut' status line and table, its '### Assumption risk ranking' table and its section 8 bullets. A shape that does not read as specified (a missing header or separator, a row of the wrong width, a status line that is neither 'First release cut: proposed, not confirmed' nor 'First release cut: confirmed by NAME on DATE') is ignored as a whole and named in the reply as 'Ignored: SHAPE in BRN-NNN (it does not read as specified)' (SPEC-002#ERR-12). A BRN without that line is read, drafted and interviewed exactly as before, whatever else it contains. No shape is a value for stage, operating_context, priority or release: a suggestion becomes a value only when the user picks it."
    changes: "new; extends SPEC-002#BEH-02 (what is read) and SPEC-002#BEH-04 (the draft)"
    lands_in: "skills/prd/SKILL.md step 3 and 'Decisions that belong to the user'; references/brn-mapping.md, 'A BRN with the Project kind line'"
  - id: SPEC-002#BEH-28
    status: proposed
    rule: "Framing from the shapes (BRN with the 'Project kind:' line). Stage: when the project kind is brownfield, the stage question's evolution option is labelled 'evolution (suggested)' (suggest nothing for greenfield or the NEEDS CLARIFICATION form); the question is never skipped for a kind alone, a project kind is not a statement of stage (SPEC-002#BEH-19), and stage is written only when the user picks an option. Primary users: when section 3 holds the target users table with at least one row, skip the primary-users question and write PRD section 3 as the table '| Persona | Goal | Context | Frequency |' with one row for each BRN row in its order (Persona unchanged, Goal the Job to be done, Context 'Today: <Current workaround>. Pain: <Pain>', Frequency '[NEEDS CLARIFICATION: how often <Persona> uses it]'); under the interview build the reuse line lists 'primary users=<Personas joined by \"; \">' with its BRN source. Non-goals: each previously decided row whose Decision is rejected is one more non-goal, in words and without an ID. Under 'proceed without questions' or an exhausted budget, stage stays null and the reply says so on the 'Suggested, not written:' line (SPEC-002#BEH-29)."
    changes: "extends SPEC-002#BEH-05 (framing) and SPEC-002#BEH-19 (what a source states)"
    lands_in: "references/interview.md I1 to I3; references/brn-mapping.md M4, M7; skills/prd/SKILL.md step 10"
  - id: SPEC-002#BEH-29
    status: proposed
    rule: "Release from the first release cut (BRN with the 'Project kind:' line; round 3 of the interview). The cut never sets a release or a priority. For a functional requirement whose upstream links name an idea in the cut table, the requirement's question starts with one line: for a confirmed cut and a yes idea (or any linked idea yes), 'Release cut (BRN-NNN vN, confirmed by NAME on DATE): IDEA-NN is in the first release.' and no option marked; for a confirmed cut and a no idea (every linked idea no), 'Release cut (BRN-NNN vN, confirmed by NAME on DATE): IDEA-NN is not in the first release.' and the option 'later' labelled 'later (suggested)'; for a proposed cut, 'Release cut (BRN-NNN vN, proposed and not confirmed): IDEA-NN is proposed for the first release.' (or '…proposed to be left out of the first release.') and no option marked. A non-functional requirement has no line. Nothing is written until the user answers. When the interview build has landed (SPEC-002#BEH-22), a row of the table whose requirement is in the first release shows 'no suggestion' with a blank value and is never written by 'Accept every row as listed'; the 'later (suggested)' rule for an unticked requirement is unchanged for the others. Under 'proceed without questions' or an exhausted budget no release is written, and the reply carries 'Suggested, not written: release current for FR-NNN, release later for FR-NNN (BRN-NNN vN, confirmed first release cut)' for a confirmed cut, or 'release proposals not applied (the cut is proposed, not confirmed)' for a proposed one. The reuse before asking (SPEC-002#BEH-19) never reads the cut as a source of release."
    changes: "extends SPEC-002#BEH-05 (the requirements round) and SPEC-002#BEH-22 (the table, once built); carves out SPEC-002#BEH-19"
    lands_in: "references/interview.md I4; skills/prd/SKILL.md step 10"
  - id: SPEC-002#BEH-30
    status: proposed
    rule: "Carry the other shapes into the PRD (BRN with the 'Project kind:' line). Assumptions: the carried assumptions are written in the order of the BRN's ranking table, those the ranking does not list after them in the BRN's order, numbered ASM-01 onward in that order, with the same statement, validation and state, and a derives link; section 10 then holds the line 'Ranked riskiest first (BRN-NNN vN):' and one bullet for each ranked assumption, '- ASM-NN: if wrong, <the words after the first colon of its If wrong cell>. Confidence <value>. Cheapest test: <its Cheapest test cell> (BRN-NNN#ASM-MM)', with no idea ID. Success metrics: each section 8 bullet '- IDEA-NN: <outcome>; baseline <value>' becomes one metric only when that idea is promoted and drafted by this PRD (the outcome stated as something measurable, a derives link to the idea, baseline the value as written, target and measured_by markers unless answered); every other bullet is dropped, so a yes idea that is still open gives no metric. Existing product and already covered rows are section 9 sentences, never requirements, never links. Assumption updates (C-11): only a row that is 'confirmed by' is used, through the BRN assumption whose item-level upstream link names the row's earlier assumption: the PRD assumption takes the state that BRN assumption holds (a disagreement with the row is named as Ignored and the BRN's state kept), and section 10 gets the sentence 'Updated from BRN-NNN#ASM-MM: OLD to NEW (evidence; BRN-NNN vN).'; a row that is proposed, not confirmed, or that no BRN assumption links to, writes nothing."
    changes: "extends SPEC-002#BEH-04 (the draft from the BRN)"
    lands_in: "references/brn-mapping.md M4 to M6; references/interview.md I5"
```

```yaml items
errors:
  - id: SPEC-002#ERR-12
    status: proposed
    condition: "A shape of a BRN with the 'Project kind:' line does not read as specified (SPEC-002#BEH-27): a table with no header or separator, a row of the wrong width, or a first release cut status line of neither form"
    handling: "Ignore that shape as a whole, treat it as absent, repair nothing, and write 'Ignored: SHAPE in BRN-NNN (it does not read as specified)' in the reply's discussion. Continue the run. An item block that cannot be read is still SPEC-002#ERR-05, which stops it"
    user_result: "A PRD drafted without the unreadable shape, and a line saying which shape was left out"
    changes: "new; distinct from SPEC-002#ERR-05"
    lands_in: "skills/prd/SKILL.md step 3; references/brn-mapping.md, 'A BRN with the Project kind line'"
```

## 4. Errors and edge cases

Brainstorm's side has none (README §6 allots no ERR to this document). The PRD side's SPEC-002#ERR-12 is in §3.7. Edge cases:

- **A confirmed cut and a BRN whose version moved on.** The cut's line in a question names the BRN version read
  (`vN`). A PRD that extends a BRN reads the new version's cut; the earlier PRD's FRs are not re-asked.
- **A requirement with two ideas.** Its line uses the first link's idea unless any linked idea is `yes`, in which
  case it reads as `yes` (§3.4, I4).
- **A promoted idea absent from the cut table.** Its requirement has no line.
- **An idea marked `yes` that is not promoted.** The requirement is never drafted (SKILL.md step 3 uses only promoted
  ideas), so no line and no metric.
- **A brownfield BRN and an existing PRD.** The new-versus-extend gate (SKILL.md step 4) is unchanged: the project kind
  is not a choice.

## 5. Verification

Brainstorm's side. One eval case, hand-written under `src/claude/DevForgeAI/evals/brainstorm/`, tagged `brainstorm`
and `ver-39`, no scaffold, with the front matter of `writes-valid-brn`.

```yaml items
verifications:
  - id: VER-39
    status: proposed
    covers:
      - BEH-34
    level: eval
    obligation: |-
      With nobody to confirm, the cut is proposed (the case grades the unconfirmed form, R5); the confirmed form is checked in mvp-and-prototype-path.md's VER-38 (b). The existing case hands-off-to-prd is unchanged and still passes at 0.8.
    case: reports-project-kind-and-first-release
    prompt: |-
      I am starting a new product from scratch and nothing is built or sold yet: an app that helps people in a shared flat split bills and chores. Brainstorm what to build first for an MVP. Skip any questions and write it up.
    scaffold: none
    frontmatter: "as writes-valid-brn: max_turns 60, timeout_seconds 900, allowed_tools Skill, Read, Glob, Grep, Write, Edit, Bash"
    graders:
      - name: report-opens-the-reply
        type: regex
        target: last_message
        match: contains
        pattern: |-
          ^\s*BRN-001 written to docs/specs/brainstorm/BRN-001\.md \(framework: [^)\n]+\)[ \t]*\n
      - name: report-block-lines
        type: regex
        target: last_message
        match: contains
        flags: m
        pattern: |-
          ^BRN-001 written to [^\n]*\n^Project kind: (?:greenfield|brownfield|not decided)[ \t]*\n^Problems: \d+ · Ideas: \d+ · Assumptions: \d+[ \t]*\n^Promoted: [^\n]+\n^First release: (?:IDEA-\d{2}(?:, IDEA-\d{2})* \(proposed, not confirmed\)|none proposed)[ \t]*\n^Open questions:
      - name: first-release-not-confirmed
        type: regex
        target: last_message
        match: not_contains
        flags: m
        pattern: |-
          ^First release: [^\n]*\(confirmed\)
      - name: kind-line-in-brn
        type: regex
        target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
        match: contains
        flags: m
        pattern: |-
          ^Project kind: greenfield[ \t]*$
      - name: next-step-last
        type: regex
        target: last_message
        match: contains
        pattern: |-
          \*\*Next step\*\*[^\n]*/devforgeai:prd BRN-001
      - name: block-and-next-step-order
        type: llm
        question: |-
          PASS if the two lines 'Project kind' and 'First release' appear inside the opening block, the Next step paragraph comes last, and nothing is worded as confirmed by the user; FAIL otherwise, quoting the line.
```

The PRD side, proposed for SPEC-002 version 10. The cases are additions to the generator `src/tests/prd/make_evals.py`
(never to the case files); each case below is one entry of its `CASES` dict, with the helpers it already defines
(`regex`, `exists`, `llm`, `ITEM`, `PRD`, `PRD_EXISTS`, `NO_PRD`). The generator is run from the repository root as
`.claude/rules/evals.md` says.

**Fixtures.** Four BRN fixtures, built from the existing `BRN_FOOD` (the Riverside Food Bank BRN-001, converged,
promoted IDEA-01 and IDEA-03) with `replace()` edits, so the shapes are the only difference:

| Name | Built from `BRN_FOOD` by |
|---|---|
| `BRN_FOOD_NEW_CONFIRMED` | (a) first line of section 1: `Project kind: greenfield` and a blank line, before the context prose; (b) `sources` to `["data: Coordinator call log, August 2026", "data: No-show tally, summer 2026"]`, and the two problems' `evidence` to `"Phone sign-ups only (data: Coordinator call log, August 2026)"` and `"Missed shifts (data: No-show tally, summer 2026)"`, so each holds one `sources` entry character for character; (c) section 3's prose replaced by the table `\| Persona \| Job to be done \| Current workaround \| Pain \|` with the rows `\| Volunteer \| Pick shifts that fit their week \| Phones the coordinator and waits \| Shifts fill before they get through \|` and `\| Shift coordinator \| Keep every shift staffed \| Phone calls and a spreadsheet \| One shift in six starts short-staffed \|`; (d) at the end of section 6: `### First release cut`, `First release cut: confirmed by Priya Nair on 2026-09-12`, and the table with `\| IDEA-01 \| yes \| Tests ASM-01 (rank 1); effort medium; score unrated \|` and `\| IDEA-03 \| no \| Tests no assumption ranked 1 to 3; effort low; score unrated \|`; (e) in section 7, after the assumptions fence, `### Assumption risk ranking` and the row `\| 1 \| ASM-01 \| Serious (IDEA-01): Volunteers keep phoning, so online sign-up is not used \| medium \| Prototype: Share of shifts filled online in the first month \|`; (f) section 8 replaced by the one bullet `- IDEA-01: share of shifts filled online; baseline phone sign-ups only (data: Coordinator call log, August 2026)` |
| `BRN_FOOD_NEW_PROPOSED` | `BRN_FOOD_NEW_CONFIRMED` with the status line `First release cut: proposed, not confirmed` |
| `BRN_FOOD_BROWN_CONFIRMED` | `BRN_FOOD_NEW_CONFIRMED` written as BRN-002 (frontmatter `id`, the `# BRN-002 — …` heading), with `Project kind: brownfield`; IDEA-04's item block removed; after the context prose the table `### Existing product` (`\| Document \| Version \| What it already covers \|`, row `\| BRN-001 \| 1 \| Online sign-up and day-before reminders, promoted last time \|`); and at the end of section 6, after the cut, `### Already covered` with the line `None.`, `### Previously decided` (`\| Idea \| Decision \| Where \|`, row `\| A native mobile app for volunteers \| rejected \| BRN-001#IDEA-04 \|`) and `### Assumption updates` with the line `None.`; the row of `### Existing product` is `\| BRN-001 \| 1 \| Earlier brainstorm: Volunteer shift sign-up for the Riverside Food Bank (IDEA-01 to IDEA-04; ASM-01) \|`; `sources` gains `"document: docs/specs/brainstorm/BRN-001.md v1"` and `upstream` becomes `[{id: BRN-001, relation: informed_by, version: 1, hash: null}]`. Its cases also seed `BRN_FOOD` itself as BRN-001, the earlier BRN, so the references name documents that exist |
| `BRN_FOOD_HEADINGS_NO_KIND` | `BRN_FOOD` with only (d) and (e) of the first fixture added, and no `Project kind:` line |

`main()` gains a check, `check_brn(label, text)`, written like `check_policy_script`: it writes the text to a temporary
`docs/specs/brainstorm/BRN-001.md` and requires `validate_brn.py` to print `OK`; the first three fixtures are checked
with it (and, once the brainstorm MVP build exists, also pass its new checks). The fourth fixture is deliberately not
passed to it: its shape headings without a kind line are what intake-and-evidence.md's IV-05 rejects, so, once that
check exists, `check_brn` expects exactly `'### First release cut' needs a 'Project kind:' line as the first line of
section 1` for it (a BRN that lost its line must not pass the validator); the case is about the PRD skill reading
such a BRN as before. The fixtures are not schema-validated
(a BRN has no schema); `FIXTURES` is unchanged.

**Cases.**

```python
"shapes-ignored-without-project-kind": {   # SPEC-002#VER-50
    "ver": "50", "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD_HEADINGS_NO_KIND},
    "prompt": "Write the PRD for BRN-001. Proceed without questions.\n",
    "description": "SPEC-002#VER-50: a BRN with a first release cut and a ranking but no Project kind line is read as before: two success metrics, no personas table, no ranked prose, no suggestion line.",
    "graders": {
        "prd-exists": PRD_EXISTS,
        "two-metrics-as-before": regex(PRD, "contains", r"- id: SM-02\n"),
        "no-personas-table": regex(PRD, "not_contains", r"\| Persona \|"),
        "no-ranked-prose": regex(PRD, "not_contains", r"Ranked riskiest first"),
        "no-suggestion-line": regex("last_message", "not_contains", r"Suggested, not written"),
    },
},
"brownfield-suggests-evolution": {   # SPEC-002#VER-51
    "ver": "51", "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD, "docs/specs/brainstorm/BRN-002.md": BRN_FOOD_BROWN_CONFIRMED},
    "prompt": "Write the PRD for BRN-002.\n",
    "description": "SPEC-002#VER-51: with a brownfield BRN and a user to ask, the reply's questions label evolution as suggested, still ask the stage, take the primary users from the BRN's table and write no PRD yet.",
    "graders": {
        "no-prd-yet": NO_PRD,
        "evolution-suggested": regex("last_message", "contains", r"\bevolution\b[^\n]{0,80}\(suggested\)|\(suggested\)[^\n]{0,40}\bevolution\b", "i"),
        "stage-still-asked": llm("PASS if the reply asks the user which stage this PRD is (prototype, mvp or evolution) "
                                 "and does not state the stage as decided. FAIL if it skips the stage question or says "
                                 "the stage is evolution as a fact."),
        "users-from-the-table": llm("PASS if the reply does not ask who the primary users are, and says or shows that "
                                    "they come from the brainstorm (Volunteer and Shift coordinator). FAIL if it asks "
                                    "who the primary users are."),
    },
},
"shapes-proceed-without-questions": {   # SPEC-002#VER-52
    "ver": "52", "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD_NEW_CONFIRMED},
    "prompt": "Write the PRD for BRN-001. Proceed without questions.\n",
    "description": "SPEC-002#VER-52: nothing in the shapes is written as a decision: stage and every release stay null; section 3 is the personas table; the assumption is ranked in prose; one metric, for the one drafted idea with a bullet; and the reply lists what was suggested and not written.",
    "graders": {
        "prd-exists": PRD_EXISTS,
        "stage-null": regex(PRD, "contains", r"^stage: null[ \t]*$", "m"),
        "no-release-written": regex(PRD, "not_contains", r"^    release: (?:current|later)[ \t]*$", "m"),
        "personas-table": regex(PRD, "contains", r"## 3\. Users and personas\n(?:(?!## )[^\n]*\n)*?\| Persona \| Goal \| Context \| Frequency \|\n\|---\|---\|---\|---\|\n\| Volunteer \|[^\n]*\n\| Shift coordinator \|"),
        "ranked-prose": regex(PRD, "contains", r"Ranked riskiest first \(BRN-001 v1\):\n(?:\n)?- ASM-01: if wrong, [^\n]+ Confidence (?:high|medium|low)\. Cheapest test: (?:Data|Prototype|Interview): [^\n]+ \(BRN-001#ASM-01\)"),
        "one-metric": regex(PRD, "contains", r"- id: SM-01\n"),
        "no-second-metric": regex(PRD, "not_contains", r"- id: SM-02\n"),
        "metric-derives-idea-01": regex(PRD, "contains", rf"- id: SM-01\n{ITEM}[ \t]+- \{{id: BRN-001, item: IDEA-01, relation: derives"),
        "baseline-as-written": regex(PRD, "contains", r'baseline: "phone sign-ups only \(data: Coordinator call log, August 2026\)"'),
        "no-unpromoted-idea": regex(PRD, "not_contains", r"IDEA-0[24]"),
        "suggestion-line": regex("last_message", "contains", r"Suggested, not written:[^\n]*\brelease\b"),
    },
},
"unconfirmed-cut-is-a-proposal": {   # SPEC-002#VER-53
    "ver": "53", "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD_NEW_PROPOSED},
    "prompt": "Write the PRD for BRN-001.\n",
    "description": "SPEC-002#VER-53: a cut that is proposed, not confirmed is shown, if at all, as a proposal: no option is labelled suggested because of it, and the reply never calls it confirmed.",
    "graders": {
        "no-prd-yet": NO_PRD,
        "no-release-suggestion": regex("last_message", "not_contains", r"\blater\b[^\n]{0,20}\(suggested\)", "i"),
        "never-called-confirmed": llm("PASS if the reply, where it mentions the first release cut, calls it proposed or "
                                      "not confirmed, and nowhere says it is confirmed, agreed or decided. PASS if it "
                                      "does not mention the cut. FAIL otherwise, quoting the sentence."),
    },
},
```

The reuse-line graders of SPEC-002#VER-49 style (`Reused: … primary users=Volunteer; Shift coordinator (BRN-001 v1
§3)`, and no `stage=` or `release` entry from these shapes) are added to SPEC-002#VER-51 and SPEC-002#VER-52 in the build that lands
after the interview build, because the reuse line does not exist before it.

**`check_graders.py`** gains, for each of the four cases, a good result (the PRD and reply a correct run would leave,
written by hand from the fixture) that passes every regex and file grader, and bad results that each break one
obligation: for SPEC-002#VER-50 a PRD with a personas table; for SPEC-002#VER-52 a PRD with `stage: evolution`, a PRD with
`release: current`, a PRD with two metrics, and a reply with no suggestion line; for SPEC-002#VER-51 and SPEC-002#VER-53 a reply that
labels `later (suggested)` or omits the `(suggested)` after evolution. Exactly the graders aimed at each break must
fail. The fixtures' good PRDs are checked with the PRD self-check list of `output-rules.md`.

**`test_structure.py`** pins SPEC-002's version: moved to the new version with SPEC-002's approval. Every new item
(SPEC-002#BEH-27 to SPEC-002#BEH-30, SPEC-002#ERR-12, SPEC-002#VER-50 to SPEC-002#VER-54) is covered by an item that verifies it, which the test checks.

```yaml items
verifications:
  - id: SPEC-002#VER-50
    status: proposed
    covers:
      - SPEC-002#BEH-27
    level: e2e
    obligation: "A BRN without the 'Project kind:' line is read as before. Eval case shapes-ignored-without-project-kind (§5): a BRN holding a confirmed first release cut and a ranking but no 'Project kind:' line gives two success metrics, no personas table, no ranked prose and no suggestion line. Every existing prd case also still passes at 0.8, with its BRN fixture untouched."
    upstream:
      - {id: STORY-002, item: AC-04, relation: verifies, version: 7, hash: null}
  - id: SPEC-002#VER-51
    status: proposed
    covers:
      - SPEC-002#BEH-28
    level: e2e
    obligation: "Eval case brownfield-suggests-evolution (§5): with a brownfield BRN and no waiver, the reply's questions label evolution as suggested, still ask the stage, take the primary users from the table, and write no PRD. Regex on last_message, llm, file_exists false."
    upstream:
      - {id: STORY-002, item: AC-04, relation: verifies, version: 7, hash: null}
  - id: SPEC-002#VER-52
    status: proposed
    covers:
      - SPEC-002#BEH-28
      - SPEC-002#BEH-29
      - SPEC-002#BEH-30
    level: e2e
    obligation: "Eval case shapes-proceed-without-questions (§5): with a confirmed greenfield BRN and the request to proceed without questions, the PRD has stage null and no release, section 3 as the personas table, the ranked prose in section 10, exactly one metric (for the drafted idea with a bullet) with its baseline as written, no unpromoted idea ID, and the reply lists the suggestions it did not write. Regex on the PRD and on last_message."
    upstream:
      - {id: STORY-002, item: AC-04, relation: verifies, version: 7, hash: null}
  - id: SPEC-002#VER-53
    status: proposed
    covers:
      - SPEC-002#BEH-29
    level: e2e
    obligation: "Eval case unconfirmed-cut-is-a-proposal (§5): with a converged BRN whose cut is 'proposed, not confirmed', no option is labelled suggested because of the cut and the reply never calls the cut confirmed. Regex on last_message, llm, file_exists false."
    upstream:
      - {id: STORY-002, item: AC-04, relation: verifies, version: 7, hash: null}
  - id: SPEC-002#VER-54
    status: proposed
    covers:
      - SPEC-002#BEH-28
      - SPEC-002#BEH-29
      - SPEC-002#BEH-30
      - SPEC-002#ERR-12
    level: manual
    obligation: "Manual, interactive, with AskUserQuestion, in a copy of the plugin (docs/runbooks/prd-v6-interview-checks.md style, a new section), on BRN_FOOD_BROWN_CONFIRMED (as BRN-002, with BRN_FOOD as BRN-001) and then on BRN_FOOD_NEW_PROPOSED (as BRN-001). (a) The stage question shows 'evolution (suggested)' for the brownfield BRN and no suggestion for the greenfield one; picking mvp writes mvp; dismissing it writes null. (b) The primary-users question is not asked and section 3 is the table. (c) The question for the requirement of IDEA-01 starts with the line 'Release cut (BRN-002 v1, confirmed by Priya Nair on 2026-09-12): IDEA-01 is in the first release.' (BRN-002 being the brownfield one) with no option marked, and for IDEA-03's requirement 'later' is labelled 'later (suggested)'; picking must writes must/current; the unpicked suggestion writes nothing. (d) For the proposed cut the line reads 'proposed and not confirmed' and nothing is marked. (e) After the interview build: the triage table never writes IDEA-01's requirement from 'Accept every row as listed'. (f) With the request to proceed without questions, the reply has the 'Suggested, not written:' line and stage and release stay null. (g) A BRN whose cut table has a row of two cells is ignored with the 'Ignored:' line (SPEC-002#ERR-12) and the run continues. (h) With a brownfield BRN holding one confirmed and one unconfirmed row of '### Assumption updates': the confirmed row gives its sentence in section 10 and the carried assumption's state; the unconfirmed row gives nothing. (i) The ranked prose, the section 9 sentences for the existing product and the already covered row, and the non-goal for the native mobile app are in the PRD, with no idea ID in any of them. Recorded in SPEC-002 §9."
    upstream:
      - {id: STORY-002, item: AC-04, relation: verifies, version: 7, hash: null}
```

## 6. Staged files

None. This document stages no file: the PRD edits are given as old and new text in §3 and the cases as generator
additions in §5, because the files they change belong to a skill that other work changes first. It uses the staged
example [BRN-001.md](staged/examples/brainstorm-greenfield-mvp/BRN-001.md) of mvp-and-prototype-path.md for §3.6.

## 7. Open questions

1. **Sequencing with the PRD interview build.** SPEC-002 versions 6 to 9 are approved and unbuilt, and they change the
   same Round 1 and Round 3 text (reuse line, triage table). Options: (a) build the interview first, then this, so the
   edits above land on the built text and the reuse-line graders go in at once (my recommendation); (b) build this
   first, against today's files, and have the interview build carry the carve-outs of §3.5 into SPEC-002#BEH-19 and SPEC-002#BEH-22 when
   it lands; (c) put both in one SKL-002 version.
2. **Round 3's `yes` ideas get no marked option.** The cut proposes a release (`current`) and not a priority, and
   every option except `later` writes a priority too, so I mark nothing for a `yes` idea and mark `later` for a `no`
   idea. Options: keep this; or mark `must now` and `should now` both "(suggested release)", which dilutes the marker.
3. **The stage suggestion is only for brownfield.** A greenfield BRN whose first-release ideas are all tested with a
   prototype could suggest `prototype`, but the BRN does not say how the first release is built (R1). Option: none;
   say if you want a rule.
