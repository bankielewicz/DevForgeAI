# Brainstorm skill: brownfield iteration

**Status:** proposal, written 2026-11-18 by claude-code (session fa59a935-ed2e-4502-b6c4-93bb6d847546) for Bryan's
review. It changes no spec, skill or plugin version. It adds BEH-25 to BEH-29, ERR-08, ERR-09 and VER-30 to VER-34 to
`docs/specs/spec/SPEC-001.md` (version 17 today), and changes its BEH-05, BEH-06, BEH-11 and ERR-01; all of it takes
effect only in SPEC-001's next version, approved by Bryan and built in a plugin-dev iteration
(`/plugin-dev:create-plugin`, `/plugin-dev:skill-development`). Read [README.md](README.md) first: its rules R1 to
R8, shapes C-01 to C-11 and ID ranges apply here unchanged. It needs [intake-and-evidence.md](
intake-and-evidence.md) built first (README §8): the kind line, the gate, `sources` and the table helper are its.

## Workflow steps this changes

The skill's task list is these eight steps. Their lines in SKILL.md don't change (R2). This document adds work
inside steps 1, 3, 5, 6 and 7 only, and only for a brownfield run: a run whose project kind is brownfield, or
unresolved and assumed brownfield (intake-and-evidence.md, BEH-20).

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 1. Intake: topic, existing BRNs, clarifying questions | Topic; extend or new when a BRN on a similar topic exists; up to three questions | The test for "on the topic" made exact; the project's PRDs, earlier BRNs, ARCH, epics and ADRs read, read-only, with a limit and an order (C-02); the brownfield question set is intake-and-evidence.md's |
| 3. Diverge: problems, ideas, assumptions | Problems, 5 to 15 ideas, assumptions | Ideas that an active requirement already covers, or an earlier BRN rejected or parked, kept out of `ideas` and listed (C-06); the earlier BRNs' parked ideas offered again; earlier open assumptions revisited |
| 5. Propose dispositions and ask the user to confirm | Two questions: dispositions, convergence | Question 4 of C-10 in the same form: the proposed assumption updates |
| 6. Write the BRN | Template, frontmatter, Change Log | `### Existing product`, `### Already covered`, `### Previously decided` and `### Assumption updates` written; `upstream` and `sources` for each document read |
| 7. Validate the BRN | `validate_brn.py`, then the read-back | Validator checks BV-01 to BV-14, each only for a BRN with a `Project kind:` line; the read-back resets a confirmed assumption update the user did not confirm (R3) |

## 1. Scope

**In.** What a brownfield run reads and how; C-02; the `upstream` and `sources` records for each document read; the
test for "already covered" and for "previously decided"; offering parked ideas again; revisiting the assumptions of
earlier BRNs and where a confirmed change is written; extend versus new; unreadable and missing documents. C-11 (README §4;
specified in §3, BEH-28).

**Out.** The kind line, the gate, `sources`, `evidence`, Target users and success signals:
[intake-and-evidence.md](intake-and-evidence.md). The first release cut, the ranking and question 3:
[mvp-and-prototype-path.md](mvp-and-prototype-path.md). How the PRD skill reads C-02 and C-06:
[prd-handoff-contract.md](prd-handoff-contract.md). Never in scope: editing any document the run reads.

**Decision that fixes this document's shape (R3, R1).** The earlier BRN is never edited by a run that creates a new
BRN. A change to an earlier assumption that the user confirmed is written in the new BRN, as a row of C-11
(`### Assumption updates`, section 6). Only when the user chose *extend it* at step 1 is the BRN edited, and then it is
the extended BRN's own assumptions that change, in place, by SPEC-001 BEH-11's rules. A new field would break R1, so
C-11 is a table in prose.

**Terms.** *Brownfield run*, *can ask*, *can't ask*, *has_prd*: intake-and-evidence.md. *Document read*: a document
that [references/brownfield.md](staged/skills/brainstorm/references/brownfield.md) (staged) says to read and that
could be read. *Active*: an item whose `status` is `active`. *Restates*: the test of BEH-27.

## 2. Changes by file

Paths are under `src/claude/DevForgeAI/skills/brainstorm/` unless they start with `src/tests`, `src/staging`, `docs`
or `.claude`.

| File | Change |
|---|---|
| `SKILL.md` | Edits 1 to 8 below |
| `references/brownfield.md` | New; staged |
| `assets/brainstorm.md` | Staged by intake-and-evidence.md; it holds the brownfield regions C-02, C-06 and C-11, which this build puts back (intake-and-evidence.md, §6, "The template per build") |
| `references/output-rules.md` | Edits 9 and 10 below |
| `references/work-file.md` | Edit 11 below |
| `scripts/validate_brn.py` | The checks of §2.2, in one new function `check_brownfield_shapes`, called right after `check_kind_shapes` |
| `src/tests/brainstorm/test_validate_brn.py` | The tests of §2.3 |
| `src/staging/examples/brainstorm-brownfield/` | New; staged (§6) |
| `docs/specs/spec/SPEC-001.md` | §2.4 |

### 2.1 Text edits

This build applies on top of intake-and-evidence.md's. SKILL.md edit 3 of that document (the marker comments in step 6)
is applied with it.

**SKILL.md edit 1.** Step 1, item 2 (found by its text, `**Existing BRNs.**`: the catalog's build moves the Workflow
section, so line numbers differ). Replace it by:

```text
2. **Existing BRNs.** Glob `docs/specs/brainstorm/BRN-*.md` and read each file's `title`. If one is on the topic by
   the test in [references/brownfield.md](references/brownfield.md) (its title shares at least two of the topic's
   words), show its ID, title and path and ask: *extend it* (version + 1, with a Change Log entry) or *create a new
   BRN*. Wait for the answer and write nothing before it. When the session has no AskUserQuestion and the request
   said not to ask, create a new BRN. Never overwrite an existing BRN silently.
```

**SKILL.md edit 2.** Step 1, item 3. Old text: the item exactly as intake-and-evidence.md's edit 1 leaves it. Replace it by
(intake's edit 1 and this one make one item):

```text
3. **Project kind and clarifying questions.** Decide whether the product the topic is about already exists
   (greenfield or brownfield), by the ordered rules in [references/intake.md](references/intake.md). For a
   brownfield kind, then read the project's documents as [references/brownfield.md](references/brownfield.md) says.
   Then ask at most four clarifying questions, in one form: the set for that kind, leaving out any the request
   already answers. Ask none when the request says to proceed without questions and the waiver was answered
   *Proceed without questions* or couldn't be asked; then the kind is written as unresolved, as intake.md says.
   Record anything still unknown as `[NEEDS CLARIFICATION: question]` in the document; never fill a gap with a
   guess.
```

**SKILL.md edit 3.** Step 3, after the three bullets (`Frame problems`, `Capture ideas`, `Capture assumptions`) add:

```text
- In a brownfield run, keep out of `ideas` what the project's documents already cover or earlier BRNs already
  decided, offer the earlier BRNs' parked ideas again, and propose new states for their open assumptions, as
  [references/brownfield.md](references/brownfield.md) says.
```

**SKILL.md edit 4.** Step 5, the list of the form's questions. After question 2 (`2. "Has the brainstorm
converged?", options `Converged` and `Not yet`.`) add:

```text
3. In a brownfield run that proposes a new state for an assumption of an earlier BRN: "Confirm these assumption
   updates?", options `Accept all as proposed` and `Leave them open`, each option's `preview` holding the table of
   earlier assumption, change and evidence ([references/brownfield.md](references/brownfield.md)).
```

In the sentence before the list, replace `both questions with` by `each question with`. The item is numbered 3 here;
mvp-and-prototype-path.md's edit 2 inserts its own question as item 3 and renumbers this one 4.

In the same step, after `Changes come typed under Other.` add: ` In a brownfield run, "add it anyway" typed there for a
suggestion listed as already covered adds it as an idea.`

**SKILL.md edit 5.** Step 6, item 3, the `upstream`, `participants` and `sources` bullet. It replaces
intake-and-evidence.md's edit 4:

```text
   - `upstream`, `participants` and `sources`: fill from the conversation, or leave them empty. In a brownfield
     BRN write `upstream` and the document `sources` as [references/brownfield.md](references/brownfield.md) says.
     Write each `sources` entry, each problem's `evidence`, section 3 and section 8 as
     [references/intake.md](references/intake.md) says.
```

**SKILL.md edit 6.** Step 6, the paragraph "Extending an existing BRN". At its end add: ` When the BRN extended is a
brownfield BRN, [references/brownfield.md](references/brownfield.md), "Extend or new", adds rules.`

**SKILL.md edit 7.** Step 7, item 2. After intake-and-evidence.md's addition (the sentence ending `…with that line.`)
add: ` A row of `### Assumption updates` that says `confirmed by` stands only when the user confirmed it in step
5; reset any other to `proposed, not confirmed`.`

**SKILL.md edit 8.** "References", after the `intake.md` bullet add:

```text
- [references/brownfield.md](references/brownfield.md): read at step 1 and step 3 in a brownfield run, and when
  extending a brownfield BRN.
```

and, in "Examples", the third example (`**A BRN on the topic already exists.**`): replace `A BRN on the topic already
exists.` by `A BRN on the topic already exists (by the test in references/brownfield.md).`

**output-rules.md edit 9.** Frontmatter table, the `upstream` row. Replace its value cell by: `` `[]`, or link records
(usually `relation: informed_by`). A brownfield BRN has one `informed_by` record, without `item`, for each document it
read ([brownfield.md](brownfield.md)) ``.

**output-rules.md edit 10.** "Validation checklist", after the item that intake-and-evidence.md's edit 11 adds (item
12) add:

```text
13. In a BRN with `### Existing product`: its table (or the line `No document was found in the project.`) has one
    row for each document read; each row has a `document:` entry in `sources`, and, in a new BRN, an `informed_by`
    record in `upstream`; `### Already covered`, `### Previously decided` and `### Assumption updates` follow it in
    section 6, each a table or the line `None.`; every status of an assumption update says `confirmed by` only
    where the user confirmed it. In a greenfield BRN none of these four headings appears.
```

(The number follows intake-and-evidence.md's 12. mvp-and-prototype-path.md's item is numbered 14 when it is built.)

**work-file.md edit 11.** "Its shape", after the bullets that intake-and-evidence.md's edits 12 add:

```text
- In a brownfield run: `### Existing product` ends section 1 from the first save, and section 6 holds `### Already
  covered`, `### Previously decided` and `### Assumption updates` from the first save, after whatever else section 6
  holds (the `[NEEDS CLARIFICATION: not reached]` line, or step 5's proposals table). Every status in
  `### Assumption updates` is `proposed, not confirmed` in a work file, never `confirmed by`. Item `upstream`
  records of ideas taken up and assumptions carried are kept.
```

and, in "Continuing a run", at the end of intake's item 3 (the same item, after its last sentence) add: `A continued brownfield run reads those tables and the
frontmatter `upstream` and `sources` from the work file and doesn't read the project's documents again, unless the
`### Existing product` table is missing.`

### 2.2 Validator checks

All checks run inside `check_brownfield_shapes`, only when intake-and-evidence.md's gate (IV-01) is on, with the
same *prose lines*, *plain*, *Cites* and table helper (messages T-1 to T-3, `NAME` stated at each use). A *section*
of a heading `### X` is the non-blank prose lines after it up to the next prose line that starts `### ` or `## `.
`kind` is `greenfield`, `brownfield` or unresolved from the first line of section 1 (IV-02). *Rows* are the parsed
rows of `### Existing product`; `FOLDER` maps `PRD` to `prd`, `BRN` to `brainstorm`, `ARCH` to `arch`, `EPIC` to
`epic`, `ADR` to `adr`. The checks use the same parsing as intake's and never PyYAML.

| ID | Runs when | Check | Error message (exact) |
|---|---|---|---|
| BV-01 | kind greenfield | None of `### Existing product`, `### Already covered`, `### Previously decided`, `### Assumption updates` is a prose line | `'HEADING' is for a brownfield BRN; this one says greenfield` (once per heading present, at its line) |
| BV-02 | kind brownfield, and at least one of the four headings of BV-01 is a prose line | `### Existing product` is a prose line | `a brownfield BRN needs '### Existing product' in section 1` (at the kind line) |
| BV-03 | `### Existing product` is present | `### Already covered`, `### Previously decided` and `### Assumption updates` are present | `a BRN with '### Existing product' also needs 'HEADING' in section 6` (once per missing heading, at `### Existing product`) |
| BV-04 | `### Existing product` is present | Its section is exactly the one line `No document was found in the project.`, or a table with the header `\| Document \| Version \| What it already covers \|`, the separator `\|---\|---\|---\|` and three cells per row | T-1 to T-3 with `NAME` = `'### Existing product'` |
| BV-05 | a row parsed | The `Document` cell matches `^(PRD\|EPIC\|ARCH\|ADR\|BRN)-\d{3}$` and isn't this BRN's `id` | `Document 'X' must be a PRD, EPIC, ARCH, ADR or earlier BRN id, not this BRN` |
| BV-06 | BV-05 passed | `Version` matches `^[1-9]\d*$` | `X: Version must be a positive integer` |
| BV-07 | rows | The rows are ordered by kind (PRD, BRN, ARCH, EPIC, ADR) and, within a kind, by number, highest first; no document twice | `C-02 rows go PRD, BRN, ARCH, EPIC, ADR, highest number first within a kind, once each` |
| BV-08 | rows | `sources` holds, as a *plain* text, `document: docs/specs/FOLDER/X.md vN` for each row (X the Document, N the Version) | `X: sources must hold the entry "document: docs/specs/FOLDER/X.md vN"` |
| BV-09 | rows, and this BRN's `version` is `1` | `upstream` holds a record without `item` whose `id` is X, `relation` is `informed_by` and `version` is N | `X: upstream must hold {id: X, relation: informed_by, version: N, hash: null}` |
| BV-10 | `### Existing product` is present | Every `upstream` record without `item` and with relation `informed_by` whose `id` starts `PRD-`, `EPIC-`, `ARCH-`, `ADR-` or `BRN-` is a row | `upstream links X, which has no row in '### Existing product'` |
| BV-11 | all three later headings are present | They appear in the order `### Already covered`, `### Previously decided`, `### Assumption updates` | `section 6 order is Already covered, Previously decided, Assumption updates` (at the first) |
| BV-12 | `### Already covered` is present | Its section is exactly `None.` or a table `\| Suggestion \| Covered by \|`, `\|---\|---\|`, two cells; each comma-separated item of `Covered by` matches `^PRD-\d{3}#(FR\|NFR)-\d{3}$` and its PRD is a row | T-1 to T-3 with `NAME` = `'### Already covered'`; `Covered by 'X' must be PRD-NNN#FR-NNN or PRD-NNN#NFR-NNN of a PRD in '### Existing product'` |
| BV-13 | `### Previously decided` is present | Exactly `None.` or a table `\| Idea \| Decision \| Where \|`, `\|---\|---\|---\|`, three cells; `Decision` is `rejected` or `parked`; `Where` matches `^BRN-\d{3}#IDEA-\d{2}$` and its BRN is a row; rows ascend by `Where` (string order), none twice | T-1 to T-3 with `NAME` = `'### Previously decided'`; `Previously decided rows need Decision rejected or parked and Where BRN-NNN#IDEA-NN of a BRN in '### Existing product'`; `Previously decided rows go in the order of Where, once each` |
| BV-14 | `### Assumption updates` is present | Exactly `None.` or a table `\| Earlier assumption \| Change \| Evidence \| Status \|`, `\|---\|---\|---\|---\|`, four cells; `Earlier assumption` matches `^BRN-\d{3}#ASM-\d{2}$` and its BRN is a row; `Change` is `open to validated` or `open to invalidated`; `Evidence` contains a `sources` entry; `Status` is `proposed, not confirmed` or matches `^confirmed by \S.* on \d{4}-\d{2}-\d{2}$`; rows ascend by `Earlier assumption`, none twice | T-1 to T-3 with `NAME` = `'### Assumption updates'`; `Earlier assumption 'X' must be BRN-NNN#ASM-NN of a BRN in '### Existing product'`; `Change must be 'open to validated' or 'open to invalidated'`; `Evidence must quote one entry of sources`; `Status must be 'proposed, not confirmed' or 'confirmed by NAME on YYYY-MM-DD'`; `Assumption updates rows go in the order of Earlier assumption, once each` |

A BRN of version 2 or later (an extension) may omit the `informed_by` records (BV-09 doesn't run): extending would
otherwise link a document that cites the extended BRN to it, a cycle. BV-10 still runs on the records it has. In
the line `No document was found in the project.` case, BV-12 to BV-14 accept only `None.`, because no PRD or BRN is a
row.

The validator never checks that a row is true (that the PRD really holds FR-003, that the earlier idea really was
rejected): it can read one file only. The read-back and the evals check that.

Reference prototype: see intake-and-evidence.md, §2.2. Its BV-01 to BV-14 produced each message above on the staged
example's variants; the example BRN-002 prints OK under `python3` and `python3 -S`.

### 2.3 Tests

`test_validate_brn.py` gains these tests inside `Base` (three runs each). The fixture is `BRK` of
intake-and-evidence.md §2.3 (`BRN-002.md`, read from `src/staging/examples/brainstorm-brownfield/`). Each failing
test asserts exit code 1, a line matching the pattern, and the same verdict in all three runs.

| Test | Change to `BRK` | Result or pattern |
|---|---|---|
| `test_brownfield_example_passes` | none | OK |
| `test_unresolved_kind_with_existing_product_passes` | the kind line becomes the unresolved marker | OK |
| `test_no_document_line_with_none_tables_passes` | `### Existing product`'s table replaced by `No document was found in the project.`; `upstream` set to `[]`; the three later tables replaced by `None.` | OK |
| `test_extension_may_omit_informed_by_records` | `version: 2`, the BRN-001 record removed, a second Change Log row | OK |
| `test_proposed_update_status_passes` | the update's status `proposed, not confirmed` | OK |
| `test_greenfield_with_existing_product_is_rejected` | kind `greenfield` | `'### Existing product' is for a brownfield BRN; this one says greenfield` |
| `test_brownfield_without_existing_product_is_rejected` | the heading and its table removed | `a brownfield BRN needs '### Existing product' in section 1` |
| `test_existing_product_without_section_6_tables_is_rejected` | `### Already covered` and its table removed | `a BRN with '### Existing product' also needs '### Already covered' in section 6` |
| `test_row_for_this_brn_is_rejected` | the BRN-001 row's Document `BRN-002` | `Document 'BRN-002' must be` |
| `test_row_version_is_rejected` | `\| PRD-001 \| v3 \|` | `PRD-001: Version must be a positive integer` |
| `test_row_order_is_rejected` | the two rows swapped | `C-02 rows go PRD, BRN, ARCH, EPIC, ADR` |
| `test_row_without_source_is_rejected` | the PRD-001 `document:` entry removed | `PRD-001: sources must hold the entry "document: docs/specs/prd/PRD-001.md v3"` |
| `test_row_without_upstream_record_is_rejected` | the BRN-001 record removed | `BRN-001: upstream must hold {id: BRN-001, relation: informed_by, version: 1, hash: null}` |
| `test_row_with_wrong_upstream_version_is_rejected` | the PRD-001 record's version `2` | `PRD-001: upstream must hold` |
| `test_upstream_record_without_row_is_rejected` | the table replaced by the `No document was found` line | `upstream links PRD-001, which has no row in '### Existing product'` |
| `test_section_6_order_is_rejected` | `### Already covered` and `### Previously decided` swapped | `section 6 order is Already covered, Previously decided, Assumption updates` |
| `test_covered_by_unknown_prd_is_rejected` | `PRD-009#FR-003` | `Covered by 'PRD-009#FR-003' must be` |
| `test_previously_decided_bad_decision_is_rejected` | `deferred` | `Previously decided rows need Decision rejected or parked` |
| `test_previously_decided_unknown_brn_is_rejected` | `BRN-007#IDEA-06` | `Previously decided rows need` |
| `test_previously_decided_order_is_rejected` | `BRN-001#IDEA-04` becomes `BRN-001#IDEA-07` | `Previously decided rows go in the order of Where, once each` |
| `test_update_change_is_rejected` | `open to confirmed` | `Change must be 'open to validated' or 'open to invalidated'` |
| `test_update_evidence_without_source_is_rejected` | the evidence `62% of bookings were made online` | `Evidence must quote one entry of sources` |
| `test_update_status_is_rejected` | the status `confirmed` | `Status must be 'proposed, not confirmed' or 'confirmed by NAME on YYYY-MM-DD'` |
| `test_update_unknown_brn_is_rejected` | `BRN-005#ASM-01` | `Earlier assumption 'BRN-005#ASM-01' must be` |

Earlier BRNs (the file's `VALID`, the real `docs/specs/brainstorm/BRN-001.md`) still print OK (VER-30).

### 2.4 SPEC-001, next version

| Item | Change |
|---|---|
| BEH-05 | Add at its end: `In a brownfield run, a candidate idea, the user's own included, that restates an active requirement of a PRD read is not added to ideas but listed (BEH-27); the user can ask for it to be added.` |
| BEH-06 | Add: `In a brownfield run that proposes a new state for an assumption of an earlier BRN, the form also holds the question 'Confirm these assumption updates?' (BEH-28).` |
| BEH-11 | Add: `The brownfield rules for extending are in BEH-29.` |
| ERR-01 | Replace `closely similar topic` by `a topic the test of BEH-29 calls the same: the BRN's title shares at least two of the topic's words`, and add to `handling`: `when the question can't be asked (no AskUserQuestion and the request said not to ask), create a new BRN` |
| BEH-25 to BEH-29, ERR-08, ERR-09, VER-30 to VER-34 | New, from §3 to §5 |

BEH-05, ERR-01 and the tests of BEH-29 are the only edits to behaviour that exists today.

## 3. Behaviour

The staged [brownfield.md](staged/skills/brainstorm/references/brownfield.md) holds the full wording. Every list,
table, question text and sentence that appears both here and there is identical in the two (the build diffs them).
Shape C-11, which README §4 repeats:

```markdown
### Assumption updates

| Earlier assumption | Change | Evidence | Status |
|---|---|---|---|
| BRN-001#ASM-01 | open to validated | 62% of October 2026 bookings were made online (data: ClinicCore booking source report, October 2026) | confirmed by Dana on 2026-11-18 |
```

C-11 is section 6, after C-06's `### Previously decided`, in a new brownfield BRN only. `Change` is `open to validated`
or `open to invalidated`. `Evidence` holds one `sources` entry. `Status` is `proposed, not confirmed` or
`confirmed by <owner> on YYYY-MM-DD`, written like C-05's status. With no row the table is the line `None.`. (Section 7 is not used because it already holds C-07 at a fixed position.)

```yaml items
behaviors:
  - id: BEH-25
    status: proposed
    rule: |-
      In a brownfield run, read these documents in step 1, after the kind is decided and before the clarifying
      questions, by their paths (never a listing of the project root), read-only: never write, edit or repair one.
      1. The kinds, their paths, the statuses to skip and the limit of each: PRD `docs/specs/prd/PRD-NNN.md` (skip
         superseded, deprecated; 4); earlier BRN `docs/specs/brainstorm/BRN-NNN.md` (skip archived; 4); ARCH
         `docs/specs/arch/ARCH-NNN.md` (skip superseded, deprecated; 1); epic `docs/specs/epic/EPIC-NNN.md` (skip
         superseded, deprecated; 4); ADR `docs/specs/adr/ADR-NNN.md` (skip rejected, superseded, deprecated; 3). The
         BRN being extended is not an earlier BRN. `docs/specs/story/` and `docs/specs/context/` are not read.
      2. Read in the order PRDs, BRNs, ARCH, epics, ADRs. Within a kind, first the documents the request names by ID,
         then the others, highest number first; a named document counts toward the limit; read the first 40 lines of
         a candidate for its status; stop at the limit.
      3. End section 1's prose with one sentence `Not read:` naming each document skipped for its status or the limit,
         with `(retired)` or `(over the limit)`; leave it out when none was.
      4. From each document read keep only active items: PRD title, version, requirement IDs and statements, metric
         IDs and names, the non-goals; BRN title, version, ideas (ID, text, disposition, reason) and assumptions (ID,
         statement, validation, state); ARCH title, version, outcome; epic title, version and the PRD items its
         refines links name; ADR title, version, status.
    changes: "new (SPEC-001 step 1 reads other BRNs' titles only)"
    lands_in: "references/brownfield.md, 'Read the project's documents'; SKILL.md edit 2"
  - id: BEH-26
    status: proposed
    rule: |-
      Write C-02 and link each document read.
      1. In section 1, after the context prose, write `### Existing product` and a table with the header
         `| Document | Version | What it already covers |`, one row per document read, in the order of BEH-25's
         item 2 with the highest number first within a kind. Version is the document's version. The last cell is,
         by kind: PRD `title (FR ranges; NFR ranges)`; BRN `Earlier brainstorm: title (IDEA ranges; ASM ranges)`;
         ARCH `title (architecture; outcome VALUE)` or `outcome not set`; epic `title (covers ranges)` or `(covers no
         requirement)`; ADR `title (status)`. A range is consecutive IDs as `FR-001 to FR-003`; a gap starts a new
         range; ranges are separated by `, `; only active IDs count; no cell holds a pipe.
      2. In a new BRN add to `upstream` one record `{id: X, relation: informed_by, version: N, hash: null}` per row,
         and to `sources` one entry `"document: docs/specs/FOLDER/X.md vN"` per row. When the run extends a BRN, add
         the `sources` entries and no `upstream` record (a document citing the extended BRN would make a cycle).
      3. When the run extends a BRN, that BRN is not a row, and the table is replaced by this run's.
    changes: "new"
    lands_in: "references/brownfield.md, 'Write the Existing product table'; SKILL.md edit 5; assets/brainstorm.md"
  - id: BEH-27
    status: proposed
    rule: |-
      Keep covered and decided ideas out of `ideas`, in step 3, for every candidate idea, the skill's and the user's.
      1. A candidate restates a requirement (or an earlier idea) when the requirement, built exactly as written,
         would already make the candidate's sentence true. Compare who is served, what the product does, when it
         happens, and the channel or limit: it restates only when every attribute the candidate states is stated,
         equal or more general, in the requirement; an attribute the candidate states and the requirement doesn't is
         an addition. In doubt, it is not a restatement.
      2. In this order, stopping at the first that applies. Already covered: the candidate restates an active
         functional or non-functional requirement of a PRD read: do not add it to `ideas`; add a row to
         `### Already covered` (the candidate in at most 12 words, the user's own words when the user raised it;
         `PRD-NNN#FR-NNN`, several joined by `, `); tell the user, and a typed 'add it anyway' under step 5's question 1
         adds it as the next idea and removes the row. Rejected earlier: the candidate restates an active idea of an
         earlier BRN read whose disposition is rejected: when the user raised it in this run, add it as an idea in
         the user's own words, write no row, and add to the convergence prose `The user raised it again:
         BRN-NNN#IDEA-NN rejected it.`; otherwise do not add it, and add a row to `### Previously decided` (the idea
         in at most 12 words, `rejected`, `BRN-NNN#IDEA-NN`). Parked earlier: handle as item 3.
      3. After the problems are framed and before ideas are generated, collect the parked ideas of the earlier BRNs
         read (active, disposition parked, not restating an active requirement), ordered by BRN number highest first
         then idea number lowest first. When the skill can ask and there is one, ask one multi-select question in a
         form tagged devforgeai_step:3, header 'Step 3': 'Take up any of these parked ideas again?', with one option
         for each of the first three (label `BRN-NNN#IDEA-NN`, description the idea, then ' Parked: ' and its reason)
         and the option 'None of these'; name the others in the reply under 'Not offered:'. A question with several
         selectable options is a multiSelect question, as SPEC-002#BEH-22's triage already uses; an answer with no
         selection decides nothing (none is taken up), as SPEC-002#BEH-26 treats an unticked answer. A selected idea is added
         as the next idea of the new BRN: its text the earlier idea's (reworded to fit), addressing the problems it
         fits, disposition open, with the item `upstream` record `{id: BRN-NNN, item: IDEA-NN, relation: informed_by,
         version: N, hash: null}`, and no row; taking it up promotes nothing. Every offered idea not selected, and
         every parked idea a candidate restated, gets a row in `### Previously decided` (`parked`), in the order of
         the Where cell. When the skill can't ask, none is taken up.
    changes: "SPEC-001 BEH-05 (a user's own idea that restates an active requirement is not recorded as an idea)"
    lands_in: >-
      references/brownfield.md, 'Keep covered and decided ideas out' and 'Offer the parked ideas'; SKILL.md edit
      3; assets/brainstorm.md, section 6
  - id: BEH-28
    status: proposed
    rule: |-
      Revisit the assumptions of earlier BRNs, in step 3 after the problems are framed, and record any change in C-11.
      1. The assumptions considered are the active assumptions of the earlier BRNs read whose effective state is
         open; the effective state is the Change of the last confirmed row for the assumption in the
         `### Assumption updates` tables of the BRNs read (highest BRN number first), else its own `state`.
      2. Propose a new state only when a fact the user gave in this run, or a document read, states that the
         assumption holds (validated) or doesn't (invalidated), compared with its statement and validation; a partial
         fact proposes nothing; never from the skill's own belief. Each proposal is a row of C-11 whose Evidence holds
         the fact and its `sources` entry (added to `sources` if missing), Status `proposed, not confirmed`.
      3. The earlier BRN is never edited by a new BRN's run. A new assumption stating the same belief as an open
         earlier one gets the item `upstream` record `{id: BRN-NNN, item: ASM-NN, relation: informed_by, version: N,
         hash: null}`.
      4. With at least one row and the skill able to ask, step 5's form gains, as its last question, 'Confirm these
         assumption updates?', options 'Accept all as proposed' and 'Leave them open', each preview holding the table
         of earlier assumption, change and evidence, changes typed under Other. Accept all writes 'confirmed by OWNER
         on TODAY' on every row (OWNER the frontmatter owner, or 'the user' when it is a marker); Leave them open
         writes nothing; typed changes confirm only the rows named. When the skill can't ask, every row stays
         proposed and the reply says the user can confirm later (SKILL.md, 'Decisions that belong to the user').
      5. Step 7's read-back resets a status that says 'confirmed by' the user did not confirm to 'proposed, not
         confirmed'.
    changes: "new; SPEC-001 BEH-06 (a fourth question in step 5's form, README C-10)"
    lands_in: >-
      references/brownfield.md, 'Revisit earlier assumptions'; SKILL.md edits 4 and 7; assets/brainstorm.md,
      section 6
  - id: BEH-29
    status: proposed
    rule: |-
      Decide extend or new by an exact test, and apply the extension rules.
      1. The topic is the arguments when not empty, else the user's answer to the topic question when it was asked,
         else the user's first message of the conversation. A BRN is on the topic when its title shares at least two
         of the topic's words: words of at least four letters, lower-cased, split on every character that is not a
         letter, without the stop list of brownfield.md. When none is, ask no question and create a new BRN. When one or more is, show the one that
         shares the most words (ties: the higher number) and ask extend or new, also under the waiver's Proceed
         without questions; when the skill can't ask (no AskUserQuestion and the request said not to ask), create a
         new BRN. The test applies to every project kind.
      2. New: the earlier BRN is read like any other document and never edited.
      3. Extend: SKILL.md step 6's rules for extending apply; the extended BRN is not a row of its own C-02 and the
         table is replaced by this run's; rows of C-06 are kept, new ones are added, a row repeating a kept one is left
         out; C-11 is left as it is; only the extended BRN's own open assumptions are revisited, and on Accept all or a
         typed confirmation their `state` is edited in place and the Change Log row names it, while on Leave them
         open or when the skill can't ask no `state` changes and the convergence prose gets `Proposed, not confirmed:
         BRN-NNN#ASM-NN open to validated (FACT, ENTRY).`; no `informed_by` record is added.
      4. A BRN without a `Project kind:` line is extended as today and none of this document applies.
    changes: "SPEC-001 ERR-01 (the test), BEH-11 (the extension rules)"
    lands_in: "references/brownfield.md, 'Extend or new'; SKILL.md edits 1 and 6"
```

## 4. Errors and edge cases

```yaml items
errors:
  - id: ERR-08
    status: proposed
    condition: >-
      A document of BEH-25's list is unreadable (Read fails, it is not UTF-8 text, or the request named it and
      it doesn't exist) or malformed (its first line is not '---' or its frontmatter has no closing '---'; its
      id differs from its file name; its type is not prd, brainstorm, arch, epic or adr for its folder; its
      version is not a positive integer; a yaml items fence in it is not closed)
    handling: >-
      Skip it completely: no row, no upstream record, no source, nothing extracted, never repaired, and it
      doesn't count toward its kind's limit. Add the bullet '- [NEEDS CLARIFICATION: ID could not be read:
      REASON]' to section 7 (REASON is unreadable, or the first failed condition in the words used here) and
      mention it in the final reply
    user_result: "A BRN that doesn't cite the document, an open question naming it, and the document untouched"
    changes: "new"
    lands_in: "references/brownfield.md, 'Documents you cannot read'"
  - id: ERR-09
    status: proposed
    condition: >-
      The project kind is brownfield (decided or assumed) and every document of BEH-25's list is missing,
      unreadable or skipped
    handling: >-
      Replace C-02's table by the line 'No document was found in the project.', add '- [NEEDS CLARIFICATION:
      where the existing product is documented]' to section 7, write 'None.' for C-06's two tables and C-11, add
      no upstream record, and tell the user in the reply. Go on with the brownfield question set
    user_result: >-
      A brownfield BRN built from the user's answers alone, with an open question about where the product is
      documented
    changes: "new"
    lands_in: "references/brownfield.md, 'Documents you cannot read' (No document at all)"
```

Edge cases, each decided by the rules above:

| Case | Result |
|---|---|
| The request names `PRD-007` and the project has no such file | Unreadable (ERR-08): the bullet; the other documents are read |
| Five PRDs, none superseded | The four highest numbers are read; section 1's prose ends `Not read: PRD-001 (over the limit).` |
| `PRD-004` is `superseded` | Skipped, `Not read: PRD-004 (retired).`; the next lower PRD takes its place in the limit |
| The user suggests "text reminders before a visit"; PRD-001 holds FR-003 "send a text reminder the day before each appointment" | Covered: a row in `### Already covered`, no idea |
| The user suggests "a second reminder two days before, with a link to move the visit" | The timing and the link are additions: an idea |
| The user suggests "email reminders" | The channel is an addition: an idea |
| The user raises "charge a deposit" and BRN-001 rejected it | Added as an idea in the user's words; the convergence prose says the user raised it again; no row |
| A generated candidate restates a rejected idea | Not added; a row in `### Previously decided` |
| Parked idea BRN-001#IDEA-03 selected in the offer | A new idea with an `informed_by` record to `BRN-001#IDEA-03`; disposition open; no row |
| Five parked ideas | Three offered with 'None of these'; two named under 'Not offered:' and given no row |
| An earlier assumption has a confirmed update in BRN-002; BRN-003 is written | Its effective state is the update's; it is not revisited |
| The user gives a fact that doesn't settle an assumption | No proposal |
| Extend the earlier BRN, with a confirmed update to its own `ASM-01` | The `state` is edited in place; the Change Log row names it |
| The topic and BRN-001's title share one word | Not on the topic: no question, a new BRN |
| The unresolved kind with a PRD in the project | Assumed brownfield: the documents are read; the kind line stays the marker |
| A run extends a BRN with no `Project kind:` line | None of this document applies |

## 5. Verification

Brainstorm's cases are hand-written. Each eval prompt says to proceed without questions and grades the unconfirmed
form (R5). Every case has the front matter of `writes-valid-brn` (`max_turns: 60`, `timeout_seconds: 900`,
`allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]`) and the tags `[brainstorm, ver-NN]`. `file_exists`
counts only files the run created, so each seeded document is graded by a regex on its content (every seeded document
has an "unchanged" grader). The scaffolds write their files byte for byte from the staged example, with quoted heredoc
delimiters; the eval prompts hold phrases of the brownfield list of intake-and-evidence.md (`already live`) and none of
the greenfield list, so the kind is decided with no question. In VER-31 to VER-33 the topic is whatever the skill is
given as its arguments, and the new BRN is BRN-002 either way: when the arguments are "ways to cut missed visits" the
topic shares no word of four letters with BRN-001's title ("Online appointment booking for returning patients"), so no
question arises; when they are the whole prompt it shares `online` and `booking`, the extend-or-new question is
due, can't be asked (no AskUserQuestion, and the prompt says not to ask), and BEH-29 creates a new BRN.

```yaml items
verifications:
  - id: VER-30
    status: proposed
    covers: [BEH-26, BEH-27, BEH-28, ERR-09]
    level: unit
    obligation: >-
      src/tests/brainstorm/test_validate_brn.py gains the tests of §2.3 of this document, inside Base, written
      before the checks, each run the three ways the file runs every test with the same verdict. The unchanged
      staged example prints OK; the no-document form and the unresolved kind with C-02 print OK; each other test
      changes only what its row says and asserts the exact message of BV-01 to BV-14; the earlier BRNs still
      print OK; no test ends in a traceback.
  - id: VER-31
    status: proposed
    covers: [BEH-25, BEH-26, ERR-08]
    level: eval
    case: brownfield-reads-and-records
    scaffold: >-
      scaffold.sh writes docs/specs/prd/PRD-001.md and docs/specs/brainstorm/BRN-001.md byte for byte from
      src/staging/examples/brainstorm-brownfield/PRD-001.md and BRN-001.md, and docs/specs/prd/PRD-002.md as the
      malformed stub of this item
    prompt: |-
      Our clinic's online booking is already live. Brainstorm ways to cut missed visits. Don't ask me any questions,
      just work through it and write it up.
    graders:
      - {name: skill-fired, type: tool_used}
      - {name: brn-exists, type: file_exists}
      - {name: no-brn-003, type: file_exists}
      - {name: no-prd-003, type: file_exists}
      - {name: kind-brownfield, type: regex}
      - {name: existing-product-rows, type: regex}
      - {name: no-row-for-the-malformed-prd, type: regex}
      - {name: malformed-prd-is-named, type: regex}
      - {name: upstream-prd, type: regex}
      - {name: upstream-brn, type: regex}
      - {name: sources-prd, type: regex}
      - {name: sources-brn, type: regex}
      - {name: prd-001-unchanged, type: regex}
      - {name: brn-001-unchanged, type: regex}
      - {name: prd-002-unchanged, type: regex}
      - {name: ran-validator-alone, type: tool_used}
    obligation: >-
      The seeded project holds PRD-001 (version 3), the earlier BRN-001 and a malformed PRD-002 (its id says
      PRD-003). The new BRN-002 says Project kind: brownfield; its Existing product table has the rows PRD-001
      version 3 and BRN-001 version 1 and none for PRD-002 or PRD-003; section 7 names PRD-002 as not read; the
      frontmatter has the two informed_by records and the two document sources; the three seeded documents are
      unchanged, no BRN-003 or PRD-003 exists, and the validator ran alone.
  - id: VER-32
    status: proposed
    covers: [BEH-27]
    level: eval
    case: brownfield-covered-and-rejected-again
    scaffold: >-
      scaffold.sh writes docs/specs/prd/PRD-001.md and docs/specs/brainstorm/BRN-001.md byte for byte from the
      staged example
    prompt: |-
      Our clinic's online booking is already live. Brainstorm ways to cut missed visits. I want to consider texting
      patients a reminder before each visit, and also charging a deposit when they book. Don't ask me any questions,
      just work through it and write it up.
    graders:
      - {name: skill-fired, type: tool_used}
      - {name: brn-exists, type: file_exists}
      - {name: kind-brownfield, type: regex}
      - {name: covered-row, type: regex}
      - {name: deposit-is-an-idea, type: regex}
      - {name: raised-again-sentence, type: regex}
      - {name: no-deposit-row, type: regex}
      - {name: reminder-is-not-an-idea, type: llm}
      - {name: prd-001-unchanged, type: regex}
      - {name: brn-001-unchanged, type: regex}
      - {name: ran-validator-alone, type: tool_used}
    obligation: >-
      The user's reminder suggestion restates PRD-001#FR-003, so it is a row of Already covered and not an idea;
      the user's deposit suggestion restates the idea BRN-001 rejected, but the user raised it, so it is an idea
      in the user's words, the convergence prose says so, and there is no Previously decided row for it; the
      seeded documents are unchanged and the validator ran alone.
  - id: VER-33
    status: proposed
    covers: [BEH-28]
    level: eval
    case: brownfield-unattended-assumption-update
    scaffold: "as VER-32"
    prompt: |-
      Our clinic's online booking is already live, and the ClinicCore booking source report for October 2026 shows that
      62% of bookings were made online. Brainstorm ways to cut missed visits. Don't ask me any questions, just work
      through it and write it up.
    graders:
      - {name: skill-fired, type: tool_used}
      - {name: brn-exists, type: file_exists}
      - {name: kind-brownfield, type: regex}
      - {name: update-row, type: regex}
      - {name: nothing-confirmed, type: regex}
      - {name: status-draft, type: regex}
      - {name: no-dispositions, type: regex}
      - {name: nothing-taken-up, type: regex}
      - {name: prd-001-unchanged, type: regex}
      - {name: brn-001-unchanged, type: regex}
      - {name: ran-validator-alone, type: tool_used}
    obligation: >-
      The 62% fact settles BRN-001#ASM-01 ('most patients will book online'): the BRN holds the update row open
      to validated with a data entry in its evidence and the status proposed, not confirmed; nothing says
      confirmed by; status is draft and no disposition is set; no parked idea was taken up (no item upstream
      record to a BRN-001 idea); BRN-001 and PRD-001 are unchanged (BRN-001's ASM-01 is still open); the
      validator ran alone.
  - id: VER-34
    status: proposed
    covers: [BEH-27, BEH-28, BEH-29, ERR-08, ERR-09]
    level: manual
    obligation: >-
      Live, in the brainstorm runbook's way (docs/runbooks/brainstorm-manual-test.md), in a session with the
      task tools and AskUserQuestion, in a project seeded as VER-31's scaffold but without PRD-002. (a) A
      request with 'already live' and a topic sharing no word with BRN-001's title: no kind question; the
      clarifying form holds the four brownfield questions ('What triggered this brainstorm about the existing
      product?', 'Which users of the product are affected, and how do they cope today?', 'What must stay as it
      is?', 'What shows how the product is used today?'), each headed 'Step 1'. (b) After the problems are
      framed: a step-3 form 'Take up any of these parked ideas again?' with multiple selection, the options
      BRN-001#IDEA-03 and BRN-001#IDEA-04 with their idea and ' Parked: ' reason, and 'None of these'; selecting
      IDEA-03 gives a new idea with an informed_by record to BRN-001#IDEA-03; IDEA-04 gets a Previously decided
      row. (c) With a fact that validates BRN-001#ASM-01 given in the request: step 5's form holds, last,
      'Confirm these assumption updates?' with 'Accept all as proposed' and 'Leave them open', each preview
      showing the table; Accept all writes 'confirmed by' the owner and today on the row; Leave them open leaves
      'proposed, not confirmed'; in both BRN-001 is unchanged. (d) A topic sharing two words with BRN-001's
      title (for example 'Cut missed visits among patients who book online': `patients`, `online`): the
      extend-or-new question is asked, also after the waiver's Proceed without questions; choosing extend leaves
      no informed_by record, replaces the Existing product table and, on Accept all, edits BRN-001's own ASM-01
      state in place with a Change Log row naming it; choosing new leaves BRN-001 unchanged. (e) A project with
      no PRD, ARCH, epic, ADR or BRN and 'brownfield' in the request: the Existing product section is the line
      'No document was found in the project.' and section 7 has the marker bullet. (f) A malformed PRD-002 (its
      id differs from its file name): named in section 7 and in the reply, not repaired. (g) A PRD whose status
      is superseded and five PRDs in all: 'Not read:' names the skipped ones. Recorded in SPEC-001 §9.
```

### 5.1 Graders

Each file is `evals/brainstorm/<case>/graders/<name>.md`, shown as it must be written. The regexes were each run with
`node` against example BRNs built to match and to miss them (2026-11-18). `skill-fired` and `ran-validator-alone`
are `writes-valid-brn`'s (shown in [intake-and-evidence.md](intake-and-evidence.md), §5.1). A grader with the same
name and text as one of an earlier case is not repeated. The scaffold's `PRD-002.md`:

```text
---
id: PRD-003
type: prd
title: "Stub"
status: draft
version: 1
---

# PRD-002 broken

MALFORMED-FIXTURE
```

**Case `brownfield-reads-and-records`**

`graders/brn-001-unchanged.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
^---\nid: BRN-001\n[\s\S]*\nupdated: 2026-09-03\n[\s\S]*ASM-01\n    status: active\n    statement: "We believe that most patients will book online if it is available\."\n    validation: "Share of bookings made online in the first month after launch\."\n    state: open\n[\s\S]*\| 1 \| 2026-09-03 \| claude-code \(session example-session\) \| Converged \|\s*$
```

`graders/brn-exists.md`

```text
---
type: file_exists
path: docs/specs/brainstorm/BRN-002.md
exists: true
---
```

`graders/existing-product-rows.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
### Existing product\n\n\| Document \| Version \| What it already covers \|\n\|---\|---\|---\|\n\| PRD-001 \| 3 \| [^\n]+\|\n\| BRN-001 \| 1 \| [^\n]+\|\n
```

`graders/kind-brownfield.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
## 1\. Context\n\nProject kind: brownfield\n\n
```

`graders/malformed-prd-is-named.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
\n- \[NEEDS CLARIFICATION: PRD-002 could not be read: [^\]\n]+\]
```

`graders/no-brn-003.md`

```text
---
type: file_exists
path: docs/specs/brainstorm/BRN-003.md
exists: false
---
```

`graders/no-prd-003.md`

```text
---
type: file_exists
path: docs/specs/prd/PRD-003.md
exists: false
---
```

`graders/no-row-for-the-malformed-prd.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: not_contains
---
\| PRD-00[23] \|
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

`graders/prd-002-unchanged.md`

```text
---
type: regex
target: {source: file, path: docs/specs/prd/PRD-002.md}
match: contains
---
^---\nid: PRD-003\n[\s\S]*MALFORMED-FIXTURE\s*$
```

`graders/sources-brn.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
"document: docs/specs/brainstorm/BRN-001\.md v1"
```

`graders/sources-prd.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
"document: docs/specs/prd/PRD-001\.md v3"
```

`graders/upstream-brn.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
\{id: BRN-001, relation: informed_by, version: 1, hash: null\}
```

`graders/upstream-prd.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
\{id: PRD-001, relation: informed_by, version: 3, hash: null\}
```

**Case `brownfield-covered-and-rejected-again`**

`graders/covered-row.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
### Already covered\n\n\| Suggestion \| Covered by \|\n\|---\|---\|\n\| [^\n|]*[Rr]eminder[^\n|]* \| PRD-001#FR-003 \|
```

`graders/deposit-is-an-idea.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
\n    idea: "[^"\n]*[Dd]eposit[^"\n]*"
```

`graders/no-deposit-row.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: not_contains
---
\| [^|\n]*[Dd]eposit[^|\n]* \| rejected \| BRN-001#IDEA-06 \|
```

`graders/raised-again-sentence.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
The user raised it again: BRN-001#IDEA-06 rejected it\.
```

`graders/reminder-is-not-an-idea.md`

```text
---
type: llm
---

The seeded PRD-001 already requires a text reminder the day before each appointment (FR-003).
PASS if no idea in section 4 of docs/specs/brainstorm/BRN-002.md is only a text reminder before or the day
before a visit. An idea that adds something, such as a second reminder, another channel or a way to move the
visit, is fine.
FAIL if an idea merely restates the day-before text reminder; quote it.
```

Same file and text as in an earlier case: `brn-001-unchanged`, `brn-exists`, `kind-brownfield`, `prd-001-unchanged`.

**Case `brownfield-unattended-assumption-update`**

`graders/no-dispositions.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: not_contains
---
disposition:[ \t]*"?(?:promoted|parked|rejected)
```

`graders/nothing-confirmed.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: not_contains
---
confirmed by \S[^\n]* on \d{4}-\d{2}-\d{2}
```

`graders/nothing-taken-up.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: not_contains
---
\{id: BRN-001, item: IDEA-\d{2}, relation: informed_by
```

`graders/status-draft.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
flags: m
---
^status: draft[ \t]*$
```

`graders/update-row.md`

```text
---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
### Assumption updates\n\n\| Earlier assumption \| Change \| Evidence \| Status \|\n\|---\|---\|---\|---\|\n\| BRN-001#ASM-01 \| open to validated \| [^|\n]*\((?:document|data|ticket|interview|url|note): [^)\n]+\)[^|\n]* \| proposed, not confirmed \|
```

Same file and text as in an earlier case: `brn-001-unchanged`, `brn-exists`, `kind-brownfield`, `prd-001-unchanged`.


## 6. Staged files

| Staged | Destination |
|---|---|
| [staged/skills/brainstorm/references/brownfield.md](staged/skills/brainstorm/references/brownfield.md) | `src/claude/DevForgeAI/skills/brainstorm/references/brownfield.md` (new) |
| [staged/examples/brainstorm-brownfield/](staged/examples/brainstorm-brownfield/) (`BRN-001.md`, `PRD-001.md`, `BRN-002.md`, `README.md`) | `src/staging/examples/brainstorm-brownfield/` (new) |

`BRN-002.md` follows every shape C-01 to C-09 and C-11, and `BRN-001.md` is an earlier BRN in the old shape. Both
print `OK` under `validate_brn.py` (run from a path ending `docs/specs/brainstorm/`, since the validator checks the
folder). The scaffolds of VER-31 to VER-33 and the tests of §2.3 read them; the PRD is the scaffolds' seed.

## 7. Open questions

1. **The "on the topic" test applies to every kind (BEH-29).** SPEC-001's ERR-01 leaves "closely similar topic" to
   judgment. An exact test is needed in a brownfield project, where almost every earlier BRN concerns the same product,
   and a rule that applies to one kind only would be two rules for one question. Bryan: which do you want?
   - **A (as written):** the word test decides for every project kind; greenfield behaviour changes slightly.
   - **B:** the word test only when the kind is brownfield or assumed brownfield; greenfield keeps judgment.
2. **A confirmed update lives only in the new BRN (BEH-28).** The earlier BRN stays `open`, so the PRD skill, which
   reads a BRN's own `assumptions`, sees the old state unless it also reads C-11 (prd-handoff-contract.md would have to
   say so), and a later brownfield run uses the effective-state rule instead. Bryan: which do you want?
   - **A (as written):** earlier BRNs are never edited by a new BRN's run; the effective-state rule carries the
     update.
   - **B:** also write the confirmed `state` into the earlier BRN, as an edit of a converged document (version plus
     one, a Change Log row) that the user chose not to extend (SPEC-001 ERR-01 offers extend or new), and one that a
     PRD may already cite.
3. **BV-02 and a BRN written between builds (added in review).** A BRN written by build 2 (intake-and-evidence.md)
   can say `Project kind: brownfield` without the brownfield blocks, because the template of that build has none.
   BV-02 would reject it once this build's validator ships, against README §8 ("earlier BRNs stay valid"). BV-02 now
   runs only when the BRN holds at least one of the four brownfield headings, as mvp-and-prototype-path.md's adoption
   gate does. The cost: a brownfield BRN that lost all four headings passes the validator, and only step 7's read-back
   (output-rules item 13) can catch it. Bryan: which do you want?
   - **A (as written now):** BV-02 gated by the headings.
   - **B:** BV-02 always runs for kind brownfield; a build-2 BRN with that kind must be edited after build 3.
