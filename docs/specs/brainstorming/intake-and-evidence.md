# Brainstorm skill: intake and evidence

**Status:** proposal, written 2026-11-18 by claude-code (session fa59a935-ed2e-4502-b6c4-93bb6d847546) for Bryan's
review. It changes no spec, skill or plugin version. It adds BEH-20 to BEH-24, ERR-07 and VER-25 to VER-29 to
`docs/specs/spec/SPEC-001.md` (version 17 today), changes its BEH-01 and BEH-08, and edits one cell of
`docs/specs/adr/ADR-003.md`; all of it takes effect only in SPEC-001's next version, approved by Bryan and built in a
plugin-dev iteration (`/plugin-dev:create-plugin`, `/plugin-dev:skill-development`). Read [README.md](README.md)
first: its rules R1 to R8, shapes C-01 to C-11 and ID ranges apply here unchanged.

## Workflow steps this changes

The skill's task list is these eight steps. Their lines in SKILL.md don't change (R2). This document adds work
inside steps 1, 3, 6 and 7 only.

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 1. Intake: topic, existing BRNs, clarifying questions | Topic; extend or new; up to three questions in one message | The project kind decided by an ordered rule (C-01), asked in its own form only when the rule can't decide; up to four questions in one form, from a set for that kind; every input recorded as a source (C-09) |
| 3. Diverge: problems, ideas, assumptions | Problems, 5 to 15 ideas, assumptions | Each problem's `evidence` from a source or a marker; the Target users facts gathered (C-03); success-signal baselines noted (C-08) |
| 6. Write the BRN | Template, frontmatter, Change Log | The kind line, the Target users table and the success-signal bullets written in their fixed shapes; `sources` in the C-09 form |
| 7. Validate the BRN | `validate_brn.py`, then the read-back | Validator checks IV-01 to IV-12, each only for a BRN with a `Project kind:` line; the read-back checks that line exists |

## 1. Scope

**In.** C-01 (project kind), C-03 (Target users), C-08 (Candidate success signals: how each cell is gathered and
written; which ideas get a bullet is README R7's rule, with the transition rule of BEH-23), and C-09 (`sources` and
the `evidence` that cites them). The intake question sets and their limit. The validator checks for these shapes.
What the work file must hold so a continued run keeps them. The template.

**Out.** Reading the project's documents, C-02, C-06 and assumption updates: [brownfield-iteration.md](
brownfield-iteration.md). The first release cut (C-05), the ranking (C-07) and step 5's question 3:
[mvp-and-prototype-path.md](mvp-and-prototype-path.md). The report block and the PRD's reading of these shapes:
[prd-handoff-contract.md](prd-handoff-contract.md). The frameworks: [framework-catalog.md](framework-catalog.md).
No new field, collection or frontmatter key (R1); no change to SKILL.md's eight checklist lines (R2).

**Terms.** *Gate*: the test of IV-01 that switches this document's validator checks on. *Request*, *can ask*, *can't
ask*: as in the staged [intake.md](staged/skills/brainstorm/references/intake.md), "The words in this file".
*Earlier BRN*: README R7.

## 2. Changes by file

Paths are under `src/claude/DevForgeAI/skills/brainstorm/` unless they start with `src/tests`, `docs` or `.claude`.

| File | Change |
|---|---|
| `SKILL.md` | Edits 1 to 7 below. Its length stays under 400 lines (R2) |
| `references/intake.md` | New; staged |
| `assets/brainstorm.md` | Replaced; staged (also `src/templates/brainstorm.md`, the leftover copy) |
| `references/output-rules.md` | Edits 8 to 11 below |
| `references/work-file.md` | Edits 12 to 14 below |
| `scripts/validate_brn.py` | The checks of §2.2, in one new function `check_kind_shapes`, called once at the end of `check()` before the optional YAML check |
| `src/tests/brainstorm/test_validate_brn.py` | The tests of §2.3 |
| `src/tests/brainstorm/test_structure.py` | One assertion added (framework-catalog.md, VER-23): the greenfield and brownfield phrase lists of `references/intake.md`, K1, equal the two lists of the term `Project kind` in `references/frameworks/INDEX.md`, item for item |
| `docs/specs/spec/SPEC-001.md` | §2.4 |
| `docs/specs/adr/ADR-003.md` | §2.4 |

### 2.1 Text edits

**SKILL.md edit 1.** Step 1, item 3 (found by its text, `**Clarifying questions.**`: the catalog's build moves the
Workflow section, so line numbers differ). Replace it by:

```text
3. **Project kind and clarifying questions.** Decide whether the product the topic is about already exists
   (greenfield or brownfield), by the ordered rules in [references/intake.md](references/intake.md). Then ask at most
   four clarifying questions, in one form: the set for that kind, leaving out any the request already answers. Ask
   none when the request says to proceed without questions and the waiver was answered *Proceed without questions*
   or couldn't be asked; then the kind is written as unresolved, as intake.md says. Record anything still unknown as
   `[NEEDS CLARIFICATION: question]` in the document; never fill a gap with a guess.
```

**SKILL.md edit 2.** Step 3, first bullet. After `- Frame **problems** first (`PRB-NN`), stated from the affected
user's side.` add: ` Fill each problem's `evidence`, and gather the facts for the Target users table and the success
signals, as [references/intake.md](references/intake.md) says.`

**SKILL.md edit 3.** Step 6, item 2. Replace `Replace the example items with the real ones. Delete every HTML
comment.` by:

```text
Replace the example items with the real ones. Delete every HTML comment. A region between the template's
BROWNFIELD START and BROWNFIELD END marker comments is kept, without the two marker lines, when the project kind is
brownfield (or unresolved and assumed brownfield), and deleted with them otherwise (the template's first comment
says so).
```

**SKILL.md edit 4.** Step 6, item 3, last bullet. Replace `- `upstream`, `participants` and `sources`: fill from
the conversation, or leave them empty.` by:

```text
   - `upstream`, `participants` and `sources`: fill from the conversation, or leave them empty. Write each `sources`
     entry, each problem's `evidence`, section 3 and section 8 as [references/intake.md](references/intake.md) says.
```

**SKILL.md edit 5.** Step 7, item 2. After the sentence ending `or to `status: draft`.` add: ` Check too that the first
line of section 1 is a `Project kind:` line, unless the run extended a BRN that had none: the validator applies the
new shapes only to a BRN with that line.`

**SKILL.md edit 6.** "Examples", the first example, item 1. Replace `The skill asks up to three questions (trigger,
who is affected, constraints) and picks` by `The skill decides the project kind, asks up to four questions (trigger,
who is affected, constraints, evidence) and picks`.

**SKILL.md edit 7.** "References". After the `output-rules.md` bullet add:

```text
- [references/intake.md](references/intake.md): read at step 1, and at steps 3 and 6 for the evidence, the Target
  users table and the success signals.
```

**output-rules.md edit 8.** Frontmatter table, the `sources` row. Replace its value cell by: `` `[]`, or a list of quoted
strings. In a BRN with the `Project kind:` line each is `"<kind>: <reference>"` with the kind `document`, `data`,
`ticket`, `interview`, `url` or `note` ([intake.md](intake.md)); an earlier BRN's free-text entries stay valid ``.

**output-rules.md edit 9.** "Collections and fields", the `problems` table, the `evidence` row. Replace its value
cell by: `` Quoted source or data, or `"[NEEDS CLARIFICATION: …]"`. In a BRN with the `Project kind:` line: a short claim
followed by one `sources` entry in parentheses, one `sources` entry alone, or the marker ``.

**output-rules.md edit 10.** New section after "Unknowns" and before "Change Log", with the contents entry
`- Project kind and fixed shapes` added to the list at the top in the same place:

```text
## Project kind and fixed shapes

The first line of section 1 is `Project kind: greenfield`, `Project kind: brownfield` or
`Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]`, then a blank line. A BRN with that line also has the
Target users table in section 3, bullets of the form `- IDEA-NN: outcome; baseline value` (or `- None.`) in section
8, and `sources` and `evidence` as [intake.md](intake.md) says. A BRN without the line is an earlier BRN: none of
these shapes applies to it, and the validator checks none of them.
```

**output-rules.md edit 11.** "Validation checklist", after item 11 add:

```text
12. In a BRN with the `Project kind:` line: that line is the first line of section 1, followed by a blank line;
    every `sources` entry reads `<kind>: <reference>`; every active problem's `evidence` is a marker or quotes one
    `sources` entry; section 3 holds only the Target users table with one row per distinct `who` of the active
    problems; section 8 holds `- None.` or one bullet per first-release idea, each with a baseline that is a marker
    or quotes one `sources` entry.
```

**work-file.md edit 12.** "Its shape", after the bullet `- Every idea `disposition: open`, `reason: null`. A
proposal is never a disposition value.` add:

```text
- Section 1's first line is the `Project kind:` line step 1 decided ([intake.md](intake.md)): the exact line of the
  BRN, the unresolved form included. Every save from the first one holds it.
- Frontmatter `sources` holds every source recorded so far, each save writing the whole list.
- Section 3 holds the Target users table from the first save, with one row per distinct `who` of the problems
  captured so far.
- Section 8 holds, in the third save (step 5's proposals), the bullets for the ideas proposed for promotion, with the
  baselines noted so far; in the first two saves it holds `[NEEDS CLARIFICATION: not reached]`.
```

**work-file.md edit 13.** "Continuing a run", after item 2 add:

```text
3. Read the kind from section 1's first line. Don't decide it again and don't ask the kind or clarifying questions
   again. When the line holds the unresolved marker, recompute the assumed kind as intake.md's K2 and K4 say.
```

and renumber the old item 3 as 4.

**work-file.md edit 14.** Intro paragraph unchanged. In "Its shape", the first bullet (`id`) gains at its end: `A
run that extends a BRN without a `Project kind:` line keeps that BRN's shape and writes none of the lines above.`

### 2.2 Validator checks

All checks of this section run inside one function `check_kind_shapes(lines, fm_end, fm, fv, list_of, items, err)` and
use only the script's own line parsing (`list_of`, the item-block parser, the table split below), never PyYAML, so
the verdict is the same with and without it (SPEC-001 BEH-09). Messages print as `line N: message`; `N` is the line
of the offending entry, row or heading, `0` when no line applies.

**Definitions.**

- *Prose lines*: the lines after the frontmatter's closing `---` outside every fenced block. A fence opens and closes
  at a line that starts with three backticks.
- *Gate*: a prose line, lower-cased, with every run of white space replaced by one space and the ends trimmed, that
  starts with `project kind:`. The gate is on when at least one prose line passes. When it is off, no check below
  runs except IV-05.
- *plain(value)*: for a double-quoted value, the text between the quotes with `\"` read as `"` and `\\` as `\`;
  otherwise the value.
- *A table*: the consecutive non-blank prose lines of a section or subsection. Cells are
  `[c.strip() for c in line.strip().strip("|").split("|")]`. The header and the separator must equal the stated
  text after `strip()`. These three messages are shared with [brownfield-iteration.md](brownfield-iteration.md);
  `NAME` is the table's name as stated at each use.
  - T-1: `NAME: the table must start with the header HEADER and the separator SEPARATOR`
  - T-2: `NAME: a table row must have N cells: ROW`
  - T-3: `NAME: a table cell is empty; write [NEEDS CLARIFICATION: ...] for an unknown value`
- *Cites*: a text cites when it starts with `[NEEDS CLARIFICATION:` or contains, character for character, one of the
  BRN's `sources` entries as *plain(value)*.

| ID | Runs when | Check | Error message (exact) |
|---|---|---|---|
| IV-01 | always | Compute the gate | none |
| IV-02 | gate on | The first non-blank prose line after the `## 1. Context` heading, `rstrip()`ed, equals one of the three lines of C-01 and is the first line that passes the gate. When the heading is missing, report at the first gate line (the existing section check reports the heading) | `the first line of section 1 must be 'Project kind: greenfield', 'Project kind: brownfield' or 'Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]'` |
| IV-03 | IV-02 passed | The line after it is blank | `the Project kind line must be followed by a blank line` |
| IV-04 | gate on | Every gate line after the first | `more than one 'Project kind' line` |
| IV-05 | gate off | No prose line, `rstrip()`ed, equals `### Existing product`, `### First release cut`, `### Already covered`, `### Previously decided`, `### Assumption updates` or `### Assumption risk ranking` | `'HEADING' needs a 'Project kind:' line as the first line of section 1` (HEADING repeated in single quotes) |
| IV-06 | gate on | Every entry of `sources` that is a double-quoted string has *plain* text matching `^(document\|data\|ticket\|interview\|url\|note): \S` | `sources entry N must read "<kind>: <reference>", kind being one of document, data, ticket, interview, url, note` (N counts from 1; the literal `<kind>` and `<reference>` stay) |
| IV-07 | gate on | No *plain* text of two entries is equal | `sources entry N repeats entry M` (N the later) |
| IV-08 | gate on | In a `sources` entry, and in the `evidence` of every active problem, the quoted text has no backslash that is not followed by `"` or `\` | for a source: `sources entry N: a backslash may only be followed by " or \`; for evidence: `PRB-NN: evidence: a backslash may only be followed by " or \` |
| IV-09 | gate on | Every active problem's `evidence`, when quoted, cites | `PRB-NN: evidence must be a [NEEDS CLARIFICATION: ...] marker or quote one entry of sources` |
| IV-10 | gate on | No active problem's `who`, when quoted, contains `\|` after *plain* | `PRB-NN: who must not contain '\|' (it becomes a table cell in section 3)` |
| IV-11 | gate on | See below | See below |
| IV-12 | gate on | See below | See below |

**IV-11, section 3.** The prose lines between `## 3. Target users` and `## 4. Ideas` (when either heading is missing,
skip; the existing check reports it).

1. A non-blank line that doesn't start with `|` → `section 3 holds only the Target users table`, at that line.
2. No line starts with `|` → `section 3 must hold the Target users table with the header | Persona | Job to be done |
   Current workaround | Pain |`, at the first line of the section.
3. Otherwise parse the table with the header `| Persona | Job to be done | Current workaround | Pain |`, the
   separator `|---|---|---|---|`, four cells (T-1 to T-3 with `NAME` = `section 3`).
4. When the table parsed, its first-column values, in order, must equal the distinct *plain* `who` values of the
   problems whose `status` is `active`, in order of first appearance, with a `who` that is not a quoted string left
   out (the existing check reports it) → `section 3 must have one row per distinct who of the active problems, in
   order of first appearance: A; B (found: A)`, the two lists joined by `; ` and `(none)` for an empty list, at
   the table's first line.

**IV-12, section 8.** The non-blank prose lines between `## 8. Candidate success signals` and `## Change Log` (skip
when either heading is missing). The lines are valid when they are exactly the one line `- None.`, or when every
line matches `^- (IDEA-\d{2}): ([^;]+); baseline (\S.*)$` and, for the matches in order:

- `section 8 must be the line '- None.' or one bullet per first-release idea: '- IDEA-NN: outcome; baseline value'`
  when a line doesn't match, when no line exists, or when `- None.` is mixed with other lines;
- `section 8: IDEA-NN is not a defined idea` when the ID is not among the document's `ideas`;
- `section 8: bullets must be in ID order, once each (IDEA-NN after IDEA-MM)` when the ID is not greater than the
  one before;
- `section 8: baseline of IDEA-NN must be a [NEEDS CLARIFICATION: ...] marker or quote one entry of sources` when the
  baseline (group 3) doesn't cite.

IV-12 doesn't check which ideas have a bullet: the first-release ideas are fixed by the first release cut
([mvp-and-prototype-path.md](mvp-and-prototype-path.md), which may add its own check against the cut's `yes` rows).

A reference prototype of IV-01 to IV-12 and of brownfield-iteration.md's BV-01 to BV-14 was run on 2026-11-18
against the staged example BRN and 54 variants of it (9 that must print OK, 45 that must fail): each rule above
produced its message, and the verdict (pass or fail) was the same under `python3` and `python3 -S`. The variants that
concern this document are the tests of §2.3.

### 2.3 Tests

`test_validate_brn.py` gains the tests below inside `Base`, so each runs the three ways the file already runs every
test. Fixtures: `BRK = (ROOT / "src/staging/examples/brainstorm-brownfield/BRN-002.md").read_text()`, run with
`name="BRN-002.md"` (the file name must equal the id), and the file's own `VALID` text and the repository's
`docs/specs/brainstorm/BRN-001.md` for earlier BRNs. `edit(text, old, new)` is the file's helper. Every test of
the second table asserts exit code 1, a message line matching the pattern, and the same result in all three runs.
Tests are written before the checks and fail until they exist (VER-25).

| Test | Result |
|---|---|
| `test_kind_shapes_example_passes` | `BRK` prints OK |
| `test_earlier_brn_without_kind_line_passes` | `VALID` and the real BRN-001 still print OK, and `VALID` with its free-text sources still prints OK |
| `test_kind_needs_clarification_form_passes` | the kind line changed to the marker form prints OK and switches the checks on (the same file with `sources` entry 1 changed to `"the user"` fails with IV-06) |
| `test_greenfield_without_brownfield_regions_passes` | `BRK` with kind `greenfield` and the spans from `### Existing product` to `## 2. Problems` and from `### Already covered` to `## 7.` removed prints OK |
| `test_section_8_none_passes` | section 8 replaced by `- None.` prints OK |
| `test_deprecated_problem_is_not_a_row` | PRB-02 `deprecated` and its Target users row removed prints OK |
| `test_proposed_assumption_update_passes` | the update row's status `proposed, not confirmed` prints OK |

| Test | Change to `BRK` | Pattern |
|---|---|---|
| `test_kind_value_is_rejected` | `Project kind: both` | `the first line of section 1 must be` |
| `test_kind_line_not_first_is_rejected` | a prose line before it | `the first line of section 1 must be` |
| `test_kind_line_wrong_case_is_rejected` | `Project Kind: brownfield` | `the first line of section 1 must be` |
| `test_kind_line_needs_blank_line` | the blank line after it removed | `must be followed by a blank line` |
| `test_second_kind_line_is_rejected` | a second `Project kind: brownfield` line before `### Existing product` | `more than one 'Project kind' line` |
| `test_shape_heading_without_kind_line_is_rejected` | the kind line and its blank line removed | `'### Existing product' needs a 'Project kind:' line` |
| `test_prose_line_project_kinds_is_not_the_gate` | the kind line and its blank line replaced by the prose line `Project kinds vary.` and a blank line | `'### Existing product' needs a 'Project kind:' line` |
| `test_source_without_kind_is_rejected` | entry 5 loses `note: ` | `sources entry 5 must read` |
| `test_source_with_unknown_kind_is_rejected` | entry 5 starts `email: ` | `sources entry 5 must read` |
| `test_duplicate_source_is_rejected` | entry 3 repeated as entry 6 | `sources entry 6 repeats entry 3` |
| `test_source_bad_escape_is_rejected` | `\q` inside entry 5 | `sources entry 5: a backslash may only be followed by` |
| `test_evidence_without_source_is_rejected` | PRB-02's evidence `"Staff say it happens a lot"` | `PRB-02: evidence must be a [NEEDS CLARIFICATION` |
| `test_evidence_with_partial_source_is_rejected` | PRB-01's two entries cut to `(data: ClinicCore attendance report)` and `(note: a chat)` | `PRB-01: evidence must be` |
| `test_who_with_pipe_is_rejected` | PRB-02's `who` `"Front desk \| staff"` (a real pipe) | `PRB-02: who must not contain '\|'` |
| `test_section_3_missing_table_is_rejected` | the table replaced by a prose line | `section 3 holds only the Target users table` and `section 3 must hold the Target users table` |
| `test_section_3_wrong_header_is_rejected` | header `\| Persona \| Job \| Workaround \| Pain \|` | `section 3: the table must start with the header` |
| `test_section_3_missing_persona_is_rejected` | the Front-desk staff row removed | `section 3 must have one row per distinct who of the active problems, in order of first appearance: Returning patient; Front-desk staff (found: Returning patient)` |
| `test_section_3_extra_persona_is_rejected` | a `Dentist` row inserted | `section 3 must have one row per distinct who` |
| `test_section_3_empty_cell_is_rejected` | cell 2 of row 1 emptied | `section 3: a table cell is empty` |
| `test_section_3_short_row_is_rejected` | row 1 cut to three cells | `section 3: a table row must have 4 cells` |
| `test_section_8_free_bullet_is_rejected` | the IDEA-03 bullet replaced by `- Fewer missed visits.` | `section 8 must be the line '- None.' or one bullet` |
| `test_section_8_unknown_idea_is_rejected` | `IDEA-03` becomes `IDEA-09` | `section 8: IDEA-09 is not a defined idea` |
| `test_section_8_order_is_rejected` | the second bullet's ID becomes `IDEA-01` | `section 8: bullets must be in ID order, once each (IDEA-01 after IDEA-01)` |
| `test_section_8_baseline_without_source_is_rejected` | IDEA-01's baseline `12% of visits missed` | `section 8: baseline of IDEA-01 must be` |
| `test_section_8_missing_baseline_is_rejected` | `; baseline ...` cut from the IDEA-03 bullet | `section 8 must be the line '- None.' or one bullet` |
| `test_section_8_none_mixed_is_rejected` | `- None.` added above the bullets | `section 8 must be the line '- None.' or one bullet` |

Missing headings or sections must never raise: a test removes each of `## 1. Context`, `## 3. Target users`,
`## 6. Convergence` and `## 8. Candidate success signals` from `BRK` in turn and asserts exit code 1 with no
`Traceback` on stderr (`run_file` already asserts empty stderr).

### 2.4 SPEC-001 and ADR-003

**SPEC-001, next version.** Item changes (R4 keys are in §3):

| Item | Change |
|---|---|
| BEH-01 | Replaced by the text below |
| BEH-08 | At its end add: `Keep the template's fixed shapes; delete the template's brownfield regions unless the project kind is brownfield (BEH-20).` |
| BEH-09 | Add to its list of what the validator applies: `the project-kind shapes of a BRN with a Project kind line (BEH-24)`, and to the read-back: `that the first line of section 1 is a Project kind line, unless the BRN extended had none` |
| BEH-14 | Add: `The work file also holds the kind line, the sources and the Target users table, as references/work-file.md says (BEH-24).` |
| BEH-20 to BEH-24, ERR-07, VER-25 to VER-29 | New, from §3 to §5 |
| §4 Data model | The frontmatter `sources` description gains the C-09 form; section 1 gains the kind line; section 3 and section 8 gain their shapes |

BEH-01, replacement:

```text
Take the topic from the arguments or the conversation. If there is none, ask for it and write nothing until it is
given. Decide the project kind by BEH-20, then ask at most four clarifying questions, in one form, from the set for
that kind (BEH-21), skipping any question the request already answers. When the request says to proceed without
questions, ask none, once the waiver question (BEH-13) has been answered Proceed without questions or couldn't be
asked, except the topic question when no topic is given (BEH-13, version 15). Record anything still unknown as
[NEEDS CLARIFICATION] markers, not guesses.
```

**ADR-003, line 94.** The Interaction default row (class table A2) lists `clarifying-question limit (3)`; it becomes
`clarifying-question limit (4)`. ADR-003 is accepted (version 2), so the edit is a new version (3) with a `updated`
date, two Change Log rows (the change, authored `claude-code (session <ID>)`, and Bryan's approval), and every
`upstream` link that cites ADR-003 moved to version 3 (CLAUDE.md, "Rules a change must not break"). The limit is
not configurable (only `interview.max_calls` is exposed), and 4 is the platform limit of the same table (at most 4
questions per call): it can't grow further.

## 3. Behaviour

The staged [intake.md](staged/skills/brainstorm/references/intake.md) holds the full wording of each rule; where an
item below says "the phrase lists" or "the options of intake.md", it means the ones in that file. Every list, table,
question text and option label that appears both here and there is identical in the two (the build diffs them).

```yaml items
behaviors:
  - id: BEH-20
    status: proposed
    rule: |-
      Decide the project kind once, in step 1, after the topic and after the extend-or-new answer, by the first of
      these rules that decides, and write it as the first line of section 1 (C-01), followed by a blank line.
      1. K0. When the run extends a BRN whose first line of section 1 is `Project kind: greenfield` or
         `Project kind: brownfield`, that kind stands. When that BRN has no `Project kind:` line, decide no kind and
         write none of the shapes of this document or of brownfield-iteration.md. When its line is the unresolved
         marker, go on.
      2. K1. Search the request, case-insensitively and on whole words, for the greenfield phrases and the brownfield
         phrases of intake.md (word for word the two lists of INDEX.md's term `Project kind`, framework-catalog.md).
         Phrases of exactly one list: that kind. Phrases of both lists, or of neither: go on. The folder never
         overrides the words.
      3. K2. `has_prd` is true when `docs/specs/prd/PRD-*.md` matches at least one file (a Glob of that path, never a
         listing of the project root).
      4. K3. When the skill can ask, ask the kind question alone in its own form (BEH-21); the answer is the kind;
         an answer typed under Other is read by K1; a dismissal or an answer K1 doesn't decide goes on.
      5. K4. Otherwise write `Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]`, add
         `- [NEEDS CLARIFICATION: greenfield or brownfield]` to section 7's bullets, and assume brownfield when
         `has_prd` is true, otherwise greenfield. The assumed kind chooses the question set, whether brownfield.md
         is followed, and the framework rule that names brownfield; it is never written as the kind.
    changes: >-
      new (SPEC-001 BEH-01 loses its fixed 'three questions' wording; BEH-03's framework rules read the kind)
    lands_in: "references/intake.md, 'Decide the project kind'; SKILL.md edit 1; assets/brainstorm.md, section 1"
  - id: BEH-21
    status: proposed
    rule: |-
      Ask the kind question and the clarifying questions with AskUserQuestion, each form tagged
      metadata source devforgeai_step:1 and each question headed 'Step 1'.
      1. The kind question is alone in its own form, takes none of the four slots, and is asked only when BEH-20's K3
         is reached. Its text is 'Does the product this brainstorm is about already exist?'; its options are
         'Yes, it exists' and 'No, it is new', with ' (Recommended)' added to the first when has_prd is true and to
         the second otherwise. Without AskUserQuestion it is asked in plain text, alone in one message.
      2. The clarifying questions are one form of at most four questions, the set for the decided or assumed kind,
         in the order of intake.md (greenfield: trigger, who is affected, constraints, evidence; brownfield: trigger,
         affected users, what must stay as it is, what shows how the product is used), each with the options of
         intake.md. Without AskUserQuestion the same questions are asked in plain text, numbered, in one message.
      3. A question is skipped only when a clause of the request can be quoted that states what the question asks,
         with enough detail to write the cell or sentence it feeds; that clause's content is recorded where the answer
         would go.
      4. Under the waiver answered Proceed without questions, or with no user to ask, no question of this item is
         asked (the waiver's wording is unchanged), and BEH-20's K4 applies when K1 didn't decide.
      5. The limit is four: SPEC-001 BEH-01's 'at most three' and ADR-003's interaction default become four.
    changes: "SPEC-001 BEH-01 (limit 3 becomes 4; one message becomes one form); ADR-003 line 94; BEH-13 unchanged"
    lands_in: "references/intake.md, 'Ask the kind question' and 'Ask the clarifying questions'; SKILL.md edit 1"
  - id: BEH-22
    status: proposed
    rule: |-
      Record inputs as sources and tie each problem's evidence to them (C-09).
      1. An input is a number, date, quotation, file, link, ticket or interview the user states or supplies and the
         BRN relies on. The skill's own knowledge, generated ideas and proposals are not inputs. The skill adds no
         source for something it was not given or did not read in the run, and fetches no URL.
      2. Each input is one `sources` entry, `"<kind>: <reference>"`, in the forms of intake.md's table: `document`
         (a project file read: path, and ' v' and its version when it has one), `data` (a named report or dataset
         and its period), `ticket`, `interview`, `url` (as given), `note` (`the user's request, <today>` or
         `the user's answers to the intake questions, <today>`). One entry per input, no repeats, no double quote
         inside, no backslash except before a double quote or a backslash. A stated number is carried in the
         evidence text, not in the entry. With no input, `sources` is `[]`.
      3. Each active problem's `evidence` is a short claim and one entry in parentheses, one entry alone, or a
         `[NEEDS CLARIFICATION: ...]` marker, and nothing else; a problem described without a fact, file or number
         gets the marker.
    changes: "new (SPEC-001 BEH-08 leaves `sources` and `evidence` to the model)"
    lands_in: "references/intake.md, 'Record sources' and 'Write each problem's evidence'; SKILL.md edits 2 and 4"
  - id: BEH-23
    status: proposed
    rule: |-
      Gather the Target users and success-signal facts in steps 1, 3 and 5; write both at step 6 in their fixed shapes.
      1. Section 3 holds only C-03's table: one row per distinct `who` value of the active problems in order of first
         appearance, the Persona cell equal to the value. Job to be done: at most 15 words starting with a verb, from
         the user's words else from the persona's problem statements, else `[NEEDS CLARIFICATION: job of PERSONA]`;
         with the `problem-reframing` framework the cell is that framework's own form, `When [situation], I want to
         [motivation], so I can [outcome].`, with no word limit.
         Current workaround: at most 15 words from the user's answer; `Nothing; the user said so` when the user said
         there is none; else `[NEEDS CLARIFICATION: current workaround of PERSONA]`. Pain: at most 15 words from the
         user's words, else the `statement` of the persona's active problem with the highest severity (ties: lower
         ID), restated. No cell is empty or holds a pipe (a slash replaces it).
      2. Section 8 holds one bullet per first-release idea in ID order, `- IDEA-NN: outcome; baseline value`, or the
         line `- None.` when there is none. The first-release ideas are the ideas whose row in `### First release
         cut` says yes; while a BRN has no such table (before mvp-and-prototype-path.md is built), they are the ideas
         promoted or proposed for promotion. The outcome starts with one of `fewer`, `more`, `less`, `faster`,
         `shorter`, `longer`, `higher`, `lower`, `share of`, `number of`, `time to`, `rate of`, contains no `;` and
         states no target number. The baseline is the value from the evidence of the problem the idea addresses
         with its `sources` entry in parentheses, or a `[NEEDS CLARIFICATION: ...]` marker; `unknown` and `none` are
         not baselines.
    changes: "new (SPEC-001 BEH-08 leaves sections 3 and 8 as free prose)"
    lands_in: "references/intake.md, 'Section 3' and 'Section 8'; assets/brainstorm.md, sections 3 and 8"
  - id: BEH-24
    status: proposed
    rule: |-
      Keep the shapes consistent across the run and check them.
      1. Extending: a BRN that has the `Project kind:` line keeps it and keeps every source, and new or changed
         problems, rows and bullets follow BEH-22 and BEH-23. A BRN without the line stays as it is: no kind line,
         no table, no new-form source, and the skill tells the user in one sentence that the BRN kept its earlier
         shape and that a new BRN would use the new shapes.
      2. The work file holds the kind line (the unresolved form included), every source recorded so far, the Target
         users table from the first save, and, in the third save, the section 8 bullets for the ideas proposed for
         promotion; a continued run reads the kind from the work file and doesn't ask the kind or clarifying questions
         again (the assumed kind is recomputed by K2 and K4).
      3. validate_brn.py checks IV-02 to IV-12 only for a BRN whose prose has a gate line (IV-01), and IV-05 only for
         one that has none; the earlier BRN docs/specs/brainstorm/BRN-001.md still prints OK.
      4. Step 7's read-back checks that the first line of section 1 is a `Project kind:` line, unless the run
         extended a BRN that had none, because the validator can't tell a BRN that lost the line from an earlier BRN.
    changes: "SPEC-001 BEH-09, BEH-11, BEH-14 extended"
    lands_in: >-
      scripts/validate_brn.py (check_kind_shapes); references/work-file.md edits 12 to 14; SKILL.md edit 5;
      references/intake.md, 'Extending a BRN' and 'Before step 7'
```

## 4. Errors and edge cases

```yaml items
errors:
  - id: ERR-07
    status: proposed
    condition: >-
      The project kind is unresolved at the end of step 1: the request has no deciding phrase (BEH-20, K1) and
      the question couldn't be asked (waiver answered Proceed without questions, no user, or a dismissal)
    handling: >-
      Write the first line of section 1 as the unresolved marker, add the marker to section 7's bullets, assume
      brownfield when docs/specs/prd/PRD-*.md matches a file and greenfield otherwise, and use the assumed kind
      for the question set (none is asked when the question can't be asked), brownfield.md and framework
      selection. Never write the assumed kind as the kind
    user_result: >-
      A BRN whose first line says the kind is unresolved, an open question in the report, and nothing worded as
      decided
    changes: "new; extends SPEC-001 BEH-01 (what is recorded when something is unknown)"
    lands_in: "references/intake.md, 'Decide the project kind' (K4); assets/brainstorm.md, section 1"
```

Edge cases, each decided by the rules above:

| Case | Result |
|---|---|
| The request says "brand new" but the project holds PRD-001 | K1 decides: `Project kind: greenfield`. The folder never overrides the words |
| The request says "brand new app" and "our existing website" | Both lists match: K2, then K3 when it can ask, else K4 |
| "Our existing customers want it" | `existing customers` is in neither list: neither list matches |
| The user dismisses the kind question | K4 |
| The user types "it's live, but a rewrite" under Other | K1 on that text: `it's live` matches no phrase, so K4 |
| The request is `Proceed without questions` and the kind is unresolved with a PRD in the project | The unresolved line, assumed brownfield; brownfield.md is followed (brownfield-iteration.md) |
| A continued run whose work file has the unresolved line | The assumed kind is recomputed (K2, K4); no question |
| Extending BRN-001 (no kind line) | Nothing new is written; one sentence tells the user |
| A problem the user described with no fact | `evidence` is a marker |
| The user states a number in the request | A `note: the user's request, <today>` entry, and the evidence claims it with the entry in parentheses |
| A persona's pain isn't in the user's words | The restated statement of that persona's highest-severity active problem |
| No first-release idea | Section 8 is `- None.` |

## 5. Verification

Brainstorm's cases are hand-written; there is no generator (README §8). Each eval prompt says to proceed without
questions and grades the unconfirmed form (R5). Every eval case has the front matter of `writes-valid-brn`
(`max_turns: 60`, `timeout_seconds: 900`, `allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]`) and the tags
`[brainstorm, ver-NN]`. Graders are the files under §5.1; `file_exists` counts only files the run created, so seeded
files are graded by regex on their content.

```yaml items
verifications:
  - id: VER-25
    status: proposed
    covers: [BEH-20, BEH-22, BEH-23, BEH-24]
    level: unit
    obligation: >-
      src/tests/brainstorm/test_validate_brn.py gains the tests of §2.3 of this document, inside Base, written
      before the checks. Each runs the three ways the file runs every test (this interpreter's packages, a
      throwaway HOME, python3 -S), and the verdict is the same in all three. The unchanged staged example prints
      OK; the earlier BRNs (the file's VALID and docs/specs/brainstorm/BRN-001.md) print OK; each other test
      changes only what its row says and asserts the exact message of IV-02 to IV-12; no test ends in a
      traceback.
  - id: VER-26
    status: proposed
    covers: [BEH-20, BEH-22, BEH-23, BEH-24]
    level: eval
    case: intake-greenfield-full-shape
    scaffold: none (an empty workspace)
    prompt: |-
      I want to start a lending library of tools for the 48 households on my street. It's a brand new idea and I'm
      starting from scratch. Neighbours buy tools they use once, and the street group chat has about a dozen failed
      loan requests from October 2026. Brainstorm ways to get the first loans happening. Don't ask me any questions,
      just work through it and write it up.
    graders:
      - {name: skill-fired, type: tool_used}
      - {name: brn-exists, type: file_exists}
      - {name: kind-first-line, type: regex}
      - {name: no-brownfield-parts, type: regex}
      - {name: sources-in-form, type: regex}
      - {name: evidence-cites-a-source, type: regex}
      - {name: target-users-table, type: regex}
      - {name: success-signals-shape, type: regex}
      - {name: no-leftovers, type: regex}
      - {name: no-dispositions, type: regex}
      - {name: not-converged, type: regex}
      - {name: ran-validator-alone, type: tool_used}
    obligation: >-
      The prompt holds the phrases 'brand new' and 'from scratch' and none of the brownfield list, so K1 decides
      greenfield with no question. The BRN's first line of section 1 is Project kind: greenfield with a blank
      line after it; it has no brownfield region; sources holds an entry in the C-09 form and a problem's
      evidence cites a note entry; section 3 is the C-03 table and section 8 is - None. or well-formed bullets;
      no leftovers; nothing confirmed; the validator ran as a command of its own.
  - id: VER-27
    status: proposed
    covers: [BEH-20, ERR-07]
    level: eval
    case: intake-kind-unresolved
    scaffold: >-
      scaffold.sh writes docs/specs/prd/PRD-001.md byte for byte from
      src/staging/examples/brainstorm-brownfield/PRD-001.md (a heredoc with a quoted delimiter)
    prompt: |-
      Brainstorm ways to cut missed visits at our clinic. The booking pages are up and a text goes out the day before.
      Don't ask me any questions, just work through it and write it up.
    graders:
      - {name: skill-fired, type: tool_used}
      - {name: brn-exists, type: file_exists}
      - {name: kind-needs-line, type: regex}
      - {name: kind-not-written-as-fact, type: regex}
      - {name: kind-in-open-questions, type: regex}
      - {name: existing-product-table, type: regex}
      - {name: prd-001-unchanged, type: regex}
      - {name: no-new-prd, type: file_exists}
      - {name: ran-validator-alone, type: tool_used}
      - {name: reply-names-the-open-kind, type: llm}
    obligation: >-
      The prompt holds no phrase of either list, a PRD is in the project, and nothing can be asked: K4. The
      first line of section 1 is the unresolved marker; no line says greenfield or brownfield; section 7 holds
      the marker bullet; the assumed kind was brownfield, so, from build 3 on, the Existing product table has
      the PRD-001 row (the table's own checks are brownfield-iteration.md's); the seeded PRD is unchanged and no
      PRD was written; the validator ran alone; the reply lists the unresolved kind.
  - id: VER-28
    status: proposed
    covers: [BEH-20, BEH-22, BEH-23]
    level: eval
    case: intake-sources-never-invented
    scaffold: none (an empty workspace)
    prompt: |-
      Brainstorm ways for neighbours on one street to share tools. Don't ask me any questions, just work through it and
      write it up.
    graders:
      - {name: skill-fired, type: tool_used}
      - {name: brn-exists, type: file_exists}
      - {name: kind-needs-line, type: regex}
      - {name: sources-empty, type: regex}
      - {name: evidence-all-markers, type: regex}
      - {name: no-url, type: regex}
      - {name: no-brownfield-parts, type: regex}
      - {name: baselines-are-markers, type: regex}
      - {name: ran-validator-alone, type: tool_used}
      - {name: reply-invents-nothing, type: llm}
    obligation: >-
      The prompt gives the topic and nothing else: no number, document or link, and no kind phrase; the
      workspace is empty, so the assumed kind is greenfield and no brownfield region is written. sources is [];
      every problem's evidence is a marker; every baseline is a marker; no URL appears; neither the reply nor
      the BRN states a number or source the user didn't give.
  - id: VER-29
    status: proposed
    covers: [BEH-20, BEH-21, BEH-24]
    level: manual
    obligation: >-
      Live, in the brainstorm runbook's way (docs/runbooks/brainstorm-manual-test.md: the plugin copied and
      loaded with claude --plugin-dir), in a session with the task tools and AskUserQuestion. (a) A request with
      no kind phrase in an empty project: a form with one question, 'Does the product this brainstorm is about
      already exist?', options 'Yes, it exists' and 'No, it is new' with ' (Recommended)' on the second, tagged
      step 1, header 'Step 1'; answering 'No, it is new' gives a second form of four questions in the greenfield
      order ('What triggered this brainstorm?', 'Who is affected, and how do they cope today?', 'What
      constraints apply?', 'What evidence do you already have?'), each headed 'Step 1', with the options of
      intake.md; the BRN's first line of section 1 is Project kind: greenfield. (b) The same with
      docs/specs/prd/PRD-001.md present: the first option carries ' (Recommended)'; 'Yes, it exists' gives the
      four brownfield questions. (c) A request holding 'our existing booking app': no kind question. (d) A
      request that answers the trigger with a number ('about one in eight appointments is a no-show'): the form
      holds three questions, without the trigger question. (e) A dismissal of the kind question: the BRN's first
      line is the unresolved marker. (f) The waiver answered Proceed without questions: no kind or clarifying
      question; the unresolved marker (or the phrase's kind) is written. (g) Without AskUserQuestion (a session
      started with it denied) and no waiver: the kind question in plain text alone, then, after the answer, the
      numbered questions in one message. (h) A run stopped after step 5 and continued: no kind or clarifying
      question, the work file's first line of section 1 kept. (i) Extending BRN-001 of the repository (no kind
      line): the reply says the BRN kept its earlier shape; the file gains no kind line, and the validator
      prints OK. Recorded in SPEC-001 §9.
```

### 5.1 Graders

Each file is `evals/brainstorm/<case>/graders/<name>.md`, shown as it must be written (front matter, then the pattern
on its own line). The regexes were each run with `node` against example BRNs built to match and to miss them
(2026-11-18); `ran-validator-alone` and `skill-fired` are `writes-valid-brn`'s, unchanged. The three `no-*` and
`not-converged` graders are `no-unconfirmed-dispositions`' patterns, with the path of the case.

**Case `intake-greenfield-full-shape`** (BRN at `docs/specs/brainstorm/BRN-001.md`):

`graders/brn-exists.md`

```text
---
type: file_exists
path: docs/specs/brainstorm/BRN-001.md
exists: true
---
```

`graders/skill-fired.md`

```text
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?brainstorm"'
---
```

`graders/ran-validator-alone.md`

```text
---
type: tool_used
tool: Bash
input_match: '"command"\s*:\s*"(?:[^"\\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*validate_brn\.py(?:[^"\\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*"'
---
```

`graders/kind-first-line.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
## 1\. Context\n\nProject kind: greenfield\n\n[^\n#]
```

`graders/no-brownfield-parts.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
### Existing product|### Already covered|### Previously decided|### Assumption updates|BROWNFIELD
```

`graders/sources-in-form.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
\nsources:(?:\n  - |\s*\[\s*)"(?:document|data|ticket|interview|url|note): [^"\n]+"
```

`graders/evidence-cites-a-source.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
\n\s+evidence: "(?:[^"\n]*\()?(?:document|data|ticket|interview|url|note): [^"\n]+
```

`graders/target-users-table.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
\n## 3\. Target users\n\n\| Persona \| Job to be done \| Current workaround \| Pain \|\n\|---\|---\|---\|---\|\n\| [^\n]+\|\n
```

`graders/success-signals-shape.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
\n## 8\. Candidate success signals\n\n(?:- None\.\n|(?:- IDEA-\d{2}: [^;\n]+; baseline [^\n]+\n)+)\n## Change Log
```

`graders/no-leftovers.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
<!--|BRN-000|YYYY-MM-DD|<[a-z][^<>\n]*>|title: ""
```

`graders/no-dispositions.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
disposition:[ \t]*"?(?:promoted|parked|rejected)
```

`graders/not-converged.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
flags: m
---
^status:[ \t]*"?converged
```

**Case `intake-kind-unresolved`** (new BRN at `docs/specs/brainstorm/BRN-001.md`; seeded PRD at
`docs/specs/prd/PRD-001.md`). `brn-exists`, `skill-fired` and `ran-validator-alone` as above.

`graders/kind-needs-line.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
## 1\. Context\n\nProject kind: \[NEEDS CLARIFICATION: greenfield or brownfield\]\n\n
```

`graders/kind-not-written-as-fact.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
flags: m
---
^Project kind: (?:greenfield|brownfield)[ \t]*$
```

`graders/kind-in-open-questions.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
\n- \[NEEDS CLARIFICATION: greenfield or brownfield\]
```

`graders/existing-product-table.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
### Existing product\n\n\| Document \| Version \| What it already covers \|\n\|---\|---\|---\|\n\| PRD-001 \| 3 \|[ ]
```

`graders/prd-001-unchanged.md`

```text
---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
---
^---\nid: PRD-001\n[\s\S]*\nversion: 3\n[\s\S]*\| 3 \| 2026-10-20 \| Dana \| Approved for launch \| all \|\s*$
```

`graders/no-new-prd.md`

```text
---
type: file_exists
path: docs/specs/prd/PRD-002.md
exists: false
---
```

`graders/reply-names-the-open-kind.md`

```text
---
type: llm
---

The workspace held a PRD but the request did not say whether the product exists, and the user asked for
no questions.
PASS if the final reply lists, among the open questions, that the project kind (greenfield or brownfield) is
unresolved.
FAIL if it states a kind as settled, or never mentions it.
```

**Case `intake-sources-never-invented`** (BRN at `docs/specs/brainstorm/BRN-001.md`). `brn-exists`, `skill-fired`,
`ran-validator-alone` and `kind-needs-line` as above.

`graders/sources-empty.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
flags: m
---
^sources: \[\][ \t]*$
```

`graders/evidence-all-markers.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
\n\s+evidence: "(?!\[NEEDS CLARIFICATION: )
```

`graders/no-url.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
https?://
```

`graders/no-brownfield-parts.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
### Existing product|BROWNFIELD
```

`graders/baselines-are-markers.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
\n## 8\. Candidate success signals\n\n(?:- None\.\n|(?:- IDEA-\d{2}: [^;\n]+; baseline \[NEEDS CLARIFICATION: [^\]\n]+\]\n)+)\n## Change Log
```

`graders/reply-invents-nothing.md`

```text
---
type: llm
---

The user gave no numbers, documents or links, only a topic.
PASS if neither the final reply nor the written BRN states a number, a rate, a date or a source as a fact that the
user did not give.
FAIL if either does; quote the invented fact.
```

## 6. Staged files

| Staged | Destination |
|---|---|
| [staged/skills/brainstorm/references/intake.md](staged/skills/brainstorm/references/intake.md) | `src/claude/DevForgeAI/skills/brainstorm/references/intake.md` (new) |
| [staged/skills/brainstorm/assets/brainstorm.md](staged/skills/brainstorm/assets/brainstorm.md) | `src/claude/DevForgeAI/skills/brainstorm/assets/brainstorm.md` (replaces), and `src/templates/brainstorm.md` |

The template keeps every heading and frontmatter key `validate_brn.py` requires, and adds C-01 (a placeholder line
that leaves a leftover error if it is not replaced), C-03, C-05, C-07 and C-08 as live shapes, and C-02, C-06 and
C-11 between `BROWNFIELD START` and `BROWNFIELD END` marker comments. The marker comments are why step 6's "delete
every HTML comment" needs SKILL.md edit 3. A leftover marker is a "leftover HTML comment" error, so a marker that
survives is caught. C-05 and C-07 belong to mvp-and-prototype-path.md; the template carries their shapes only. The
work file is built from this template, so it has the same regions.

**The template per build.** The staged template is the whole template after builds 2, 3 and 4 (README §8). Build 2
(this document alone) uses it with the parts of the later builds cut out, and the build that owns a part puts it
back. Nothing else in it differs between builds.

| Part of the staged template | At build 2 | Put back by |
|---|---|---|
| In the first comment, the sentence that starts `Brownfield parts:` and ends `both marker lines included.` | cut | brownfield-iteration.md |
| Each region from a `BROWNFIELD START` marker line to its `BROWNFIELD END` marker line, both lines included (C-02, C-06, C-11) | cut | brownfield-iteration.md |
| `### First release cut`, its comment, its status line and its table, up to the line before the next heading | cut | mvp-and-prototype-path.md |
| `### Assumption risk ranking`, its comment and its table, up to the line before the section 7 bullet | cut | mvp-and-prototype-path.md |
| In the first comment, the words `and, for a brownfield BRN, references/brownfield.md` | cut | brownfield-iteration.md |
| In the `upstream:` line's trailing comment, the words `and, in a brownfield BRN, each document read` | cut | brownfield-iteration.md |

SKILL.md edit 3 (the marker comments) is applied at build 3, not at build 2. The staged `intake.md` needs no
per-build change: it mentions `brownfield.md` only as "when that file exists" and defines the first-release ideas
with the transition rule that holds until build 4. VER-27's grader `existing-product-table` is added at build 3;
before that the case has the others, and a run with an assumed brownfield kind writes no Existing product table.

The examples of the same iteration are in [brownfield-iteration.md](brownfield-iteration.md), §6.

## 7. Open questions

1. README §8 says each build "may ship alone" and builds this document before mvp-and-prototype-path.md. Section 8's
   bullets depend on the first release cut (README R7), which this build doesn't have, so BEH-23 uses a transition
   rule (the ideas promoted or proposed for promotion are the first-release ideas while a BRN has no cut table), and
   §6's per-build template cut keeps the cut and the ranking out of a build 2 template. Bryan: which do you want?
   - **A (as written):** each build ships alone; keep the transition rule and the template cuts; delete the
     transition rule when mvp-and-prototype-path.md is built.
   - **B:** build this document and mvp-and-prototype-path.md as one iteration: no transition rule, no template cut
     for C-05 and C-07 (the brownfield cut stays, since brownfield-iteration.md may follow separately).
