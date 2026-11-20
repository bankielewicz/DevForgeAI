# Brainstorm skill: enhancement specs

**Status:** approved as enhancement specs by Bryan on 2026-11-19 ("I approve the enhancement specs in PR #172 at
7deb4d4, including both readings"); written 2026-11-18 and 2026-11-19 by claude-code on the model Fable 5.2
(session fa59a935-ed2e-4502-b6c4-93bb6d847546). They change no spec, skill or plugin version by themselves. The
brainstorm skill's spec is `docs/specs/spec/SPEC-001.md` (version 17 on `main` when these were written,
version 18 since pull request #173; the build works from version 19: §8). Each document here says which
SPEC-001 items it adds or changes; those changes take effect only in SPEC-001's next version, approved by Bryan and
built in a plugin-dev iteration (`/plugin-dev:create-plugin` and `/plugin-dev:skill-development`; CLAUDE.md, "Rules
a change must not break").

This file is the index and the shared contract. Read it before any other file in this folder: the other documents
use its names, shapes and IDs without repeating them. Every document in this folder is written by the Fable model,
the project's architect model (Bryan, 2026-11-18: "specs must be made by fable 5.2 model not sonnet as it is the
architect model for this project").

## The workflow, and where each enhancement lands

The skill's task list is these eight steps. Their lines in SKILL.md don't change (R2); the enhancements add work
inside them. Every document in this folder opens with its own copy of this table, holding only its rows.

| Step (SKILL.md's line, unchanged) | Today | Added by these documents |
|---|---|---|
| 1. Intake: topic, existing BRNs, clarifying questions | Topic; extend or new; up to three questions | The project kind decided (C-01); the question set for that kind; sources gathered (C-09): intake-and-evidence. Brownfield: the project's documents and earlier BRNs read (C-02): brownfield-iteration |
| 2. Select a framework | The one named, else `diverge-converge` | Five frameworks and §5's selection rules: framework-catalog |
| 3. Diverge: problems, ideas, assumptions | Problems, 5 to 15 ideas, assumptions | The chosen framework's own steps; `evidence` taken from the sources: intake-and-evidence. Brownfield: covered and previously decided ideas kept out of `ideas` (C-06); parked ideas offered: brownfield-iteration |
| 4. Evaluate with the framework | value, effort, risk, score | Each framework's mapping: framework-catalog |
| 5. Propose dispositions and ask the user to confirm | Two questions: dispositions, convergence | Before the questions: the assumption risk ranking (C-07) and the proposed first release cut (C-05): mvp-and-prototype-path. Proposed assumption updates (C-11): brownfield-iteration. Up to two more questions in the same form (C-10) |
| 6. Write the BRN | Template, frontmatter, Change Log | The fixed shapes of §4 written, among them Target users (C-03) and success signals (C-08): intake-and-evidence |
| 7. Validate the BRN | `validate_brn.py`, then the read-back | New validator checks (series IV, BV, MV; §6); the read-back also covers C-05's status line, C-11's status cells and assumption states (R3) |
| 8. Report and hand off | Report block; `/devforgeai:prd BRN-NNN` | The report names the project kind and the first-release ideas: prd-handoff-contract |

## 1. Why

`/devforgeai:brainstorm` (SKL-001 v12) ships the plumbing of a brainstorm and one method. What it lacks:

| Gap today | Evidence | Closed by |
|---|---|---|
| One framework, `diverge-converge`, which its own index says to avoid for a shortlist | `skills/brainstorm/references/frameworks/INDEX.md` | [framework-catalog.md](framework-catalog.md) |
| At most three intake questions; no step fills section 3 (Target users) or section 8 (Candidate success signals); `sources` and `evidence` are filled only by chance | `SKILL.md` steps 1, 3 and 6; the template's sections 3 and 8 are comments | [intake-and-evidence.md](intake-and-evidence.md) |
| Nothing for a product that exists: no reading of the PRD, epics or architecture already written, no revisiting of earlier assumptions | `SKILL.md` step 1 reads other BRNs' titles only | [brownfield-iteration.md](brownfield-iteration.md) |
| No path to a first release or a prototype: assumptions are not ranked and no first-release cut is proposed | no such step or section | [mvp-and-prototype-path.md](mvp-and-prototype-path.md) |
| The PRD skill asks for what a richer brainstorm already holds | `skills/prd/references/interview.md` | [prd-handoff-contract.md](prd-handoff-contract.md) |

[design-prompts.md](design-prompts.md) holds prompts for Claude Design. It specifies no behaviour.

## 2. Decisions these documents rest on

All by Bryan, in session fa59a935-ed2e-4502-b6c4-93bb6d847546, on 2026-11-18:

- "the brainstorming skill is to handle both brownfield and greenfield projects".
- The catalog (PRD-001 §12's open question, "which brainstorming frameworks join the catalog, and in what
  order"): "Shortlist ranking, Problem reframing, Improve an existing product, Risk-first and MVP scoping". The
  order in the index is the order of §5's selection rules.
- The groups: "Intake and evidence, Brownfield iteration, MVP and prototype path, PRD hand-off contract".
- The location, `docs/specs/brainstorming/<slug>.md`, each document feeding SPEC-001's next version.
- The task list first: "ensure the tasklist or phases of the brainstorm skill is at the front of the spec for the
  skill".
- What is built first: "Brainstorm's four (Recommended)": the four brainstorm documents are built together as one
  skill version, SKL-001 version 13, one commit for each; the PRD hand-off is built later.
- Design prompts: "generate an ai prompt for various screens to be generated by claude design ... the look and
  feel of the claude mod for brainstorm (if one is created) along with the 'next steps'/handoff at the end of the
  workflow". His chosen directions for the mock-ups: "brainstorm pane = A / confirm decisions = A / Hand off = A /
  Brainstorm band - step 4 = B / Intake-brownfield session = B".

Spec lookup (SPEC-014 BEH-08), run on 2026-11-18 with `find_spec.py`: the framework catalog was deferred in
PRD-001 version 15 (non-goal, line 58; FR-002's note; §12), whose version 16 records the catalog as chosen on the
answer above, and is still deferred in SPEC-001 §1 (line 44); section 3 and section 8 of a BRN are
read by the PRD skill (SPEC-002 BEH-05, BEH-19 and its mapping of success signals, line 164); no spec, ADR or
recorded decision covers reading existing documents during a brainstorm, ranking assumptions, or a first-release
cut. ADR-003 (line 92) makes a BRN's `disposition` and a PRD's MoSCoW `priority` part of the document contract
("A different prioritization method needs a mapping to MoSCoW or a schema change, not a setting"), and (line 94)
makes the idea count and the clarifying-question limit interaction defaults. ADR-006 and ADR-010 keep
dispositions the user's. SPEC-001 §12 rejected listing frameworks in SKILL.md and the skill setting dispositions
itself.

On 2026-11-19 Bryan answered the open questions of pull request #172 ("Use PR #172 as the source for these
decisions"). Each document's section 7 quotes his answer where it decides something. In short: the catalog's
defaults stand, with a missing capacity labelled as an assumption; the limit of four questions is fixed; an
undecided kind works as brownfield only when a PRD exists and is recorded as still undecided; a project file the
user names may be read as a source; the reading caps stand, and no story or spec is read automatically; a covered
suggestion is reported with its requirement ID and the user may say "add it anyway" without being asked; a
confirmed assumption update lives in the new BRN only; the cut uses the top three assumptions, keeps the user's
explicit choices when a BRN is extended, and recomputes or flags a row whose reason no longer holds, the two user
sentences being reserved for choices the user made; the report block ships with the fourth commit and the PRD
side under SPEC-002 version 10, before the PRD interview-at-scale build; the five chosen layouts are kept and
their look waits for a design system ([design/README.md](design/README.md)).

On 2026-11-20 Bryan decided four more points; section 7 of each document they touch quotes him. A confirmation
names no owner: asked about the skill's ask for the owner's name when a BRN's `owner` is a NEEDS CLARIFICATION
marker, he answered "the owner isn't necessary", and of four readings of that answer he chose "No owner in the
line at all" (the option's text: "The line is always "confirmed on <date>", never naming anyone."). So C-05's
status line and C-11's status cell hold a date and no name; a line or cell that names someone is not valid
(nothing shipped with the earlier forms, so no rule reads them); and the skill never asks for the owner's name
in order to confirm. The frontmatter key `owner` is untouched (R1), and so is SPEC-001 BEH-07's rule for filling
it. The sentence for a kept-out suggestion the user adds anyway always says "the user": ""at the user's request"
(Recommended)" (brownfield-iteration.md, BEH-26). A change typed in answer to the cut question, when it is asked
once more, makes only the rows it names the user's: "Only the rows I name (Recommended)"
(mvp-and-prototype-path.md, BEH-32 item 10). The build's plugin version is 0.36.0: "0.36.0 (Recommended)" (§8).

## 3. Rules every document here follows

- **R1. No new collection and no new field in a BRN.** A BRN holds `problems`, `ideas` and `assumptions` with the
  fields `references/output-rules.md` lists today, and its frontmatter keys stay the same. New information goes
  into the fixed prose shapes of §4. Reason: a new field would change `src/schemas/brainstorm.schema.json`,
  `validate_brn.py` (which must give the same verdict with and without PyYAML), `output-rules.md`, the template,
  the PRD skill's mapping, the ui skill's `dsn_check.py`, the Codex fork (which Claude sessions don't edit) and
  the BRN fixtures of four skills' evals. The schema types `value`, `effort` and `risk` as strings: a framework
  that rates with numbers writes them quoted.
- **R2. SKILL.md's eight checklist lines don't change**, not by a character. `progress/manifests/brainstorm.json`
  holds their hash, computed from the lines wherever they stand in the file (`progress/evaluate.py`,
  `checklist_hash`), and `src/tests/progress/test_evaluate.py` checks it. New work happens inside the existing
  steps; its detail goes into new files under `references/`, each linked from SKILL.md once and from the step that
  needs it. SKILL.md stays at or under 400 lines (the limit is 500; it is 325 today). The `tasks:` list in
  SKILL.md's frontmatter (SPEC-001 version 18, for the Taskmaster mod) holds the same eight lines without their
  boxes and numbers. It doesn't change either: a title changes only with its checklist line (SPEC-001 §5).
- **R3. The user's decisions stay the user's.** A method proposes; only the user's explicit answer writes a
  disposition, `status: converged`, an assumption's `state` other than `open`, a confirmed first release cut or a
  confirmed assumption update. Whatever was not confirmed is written in its unconfirmed form (§4) and is never
  worded as decided.
- **R4. Every requirement is an item with an ID** from §6's allocation, in a `yaml items` block with these keys:
  `id`, `status: proposed`, `rule` (one testable sentence, or a numbered list of them), `changes` (the SPEC-001
  item it replaces or extends, or `new`), `lands_in` (the destination file and section). A verification item has
  `id`, `status: proposed`, `covers`, `level` (`eval`, `unit` or `manual`), `obligation`, and for `eval`: `case`
  (the folder name), `prompt` (the full text), `scaffold` (what it seeds, or `none`) and `graders` (a list; each
  with `name`, `type`, one of `regex`, `file_exists`, `tool_used`, `llm`, and the exact pattern or judge
  question). An error item uses SPEC-001's keys `condition`, `handling`, `user_result`, plus `changes` and
  `lands_in`.
- **R5. An eval can't answer a question** (`.claude/rules/evals.md`; SPEC-001 §9). A behaviour that needs an
  answer is verified `manual`, or its eval prompt says to proceed without questions and grades the unconfirmed
  form. A regex grader runs in JavaScript: no inline flags such as `(?i)`.
- **R6. Staged files are complete.** Every file under [staged/](staged/) is the whole file as it should exist at
  its destination after the build of §8, with no placeholder left for the builder. §7 gives each destination.
- **R7. Edits to existing files are exact.** A change to a file that is not replaced whole is given as
  "old text" and "new text", the old text found exactly once in the file as it stands when that document is
  built (§8's order), ignoring line breaks. Where two documents change the same passage, the later one's old text
  is the earlier one's new text.
- **R8. Layout of each document.** In this order: the status line; `## Workflow steps this changes` (the table
  above, its rows only); `## 1. Scope` (in and out); `## 2. Changes by file`; `## 3. Behaviour`; `## 4. Errors and
  edge cases`; `## 5. Verification`; `## 6. Staged files`; `## 7. Decisions and open questions`. Section 7 states
  each design choice the author made with its reason, and lists as open only what Bryan must decide, each with
  its options and the default the document specifies meanwhile.
- **R9. No judgment left to the builder.** A rule names its inputs, its order and its tie-break. Where a rule
  can't be made mechanical (whether two sentences say the same thing), the document says so, gives the test the
  model applies with an example on each side, and verifies it `manual` or with an `llm` grader.
- **R10. Words.** "The skill" is `/devforgeai:brainstorm`. "The project" is the folder the session works in.
  "Earlier BRN" is a `docs/specs/brainstorm/BRN-NNN.md` of the project that exists before the run. "Proposed for
  promotion" means the skill's step-5 proposal for the idea is `promoted`. "The first-release ideas" are the ideas
  whose row in C-05's table says `yes`. "A new-shape BRN" is one that has the project-kind line (§4, the gate).

## 4. The shared contract: fixed shapes in a BRN

Every shape is plain Markdown inside an existing section and valid for today's `validate_brn.py`.
`[NEEDS CLARIFICATION: <question>]` may stand for a cell or value that is unknown, with these exceptions, which
the owners' documents fix: no cell of C-05 holds one, no cell of C-07 other than `Cheapest test` does, and a C-11
`Evidence` cell never does. The document named with a shape owns its rules; this section fixes only the form.

**C-01. Project kind** (section 1; intake-and-evidence). The first line under `## 1. Context` is exactly one of:

```text
Project kind: greenfield
Project kind: brownfield
Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]
```

followed by a blank line and the context prose. *Brownfield*: the product the topic is about exists (it is built
or in use). *Greenfield*: it does not. The user's words decide; what the project folder holds only suggests.

With the third line, and only then, section 7 holds exactly one bullet that says which kind the run worked as
(Bryan, 2026-11-19: "Record that the kind is still undecided."):
`- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as greenfield]`, or the same with
`worked as brownfield`. Check IV-07 requires it while the kind is undecided and rejects it once the kind line
says `greenfield` or `brownfield`. A BRN whose bullet says `worked as brownfield` holds the brownfield shapes.

**C-02. Existing product** (section 1, brownfield only, after the context prose; brownfield-iteration):

```markdown
### Existing product

| Document | Version | What it already covers |
|---|---|---|
| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006) |
```

One row per document read; `Document` is a document ID. With no document read, the table is replaced by the line
`No document was found in the project.` After the table or that line, one line `Skipped: <path> (<reason>)` for
each document that could not be used.

**C-03. Target users** (section 3; intake-and-evidence). Exactly this table, one row per distinct `who` value of
the active problems, the persona cell equal to that value character for character, rows in the order the values
first appear:

```markdown
| Persona | Job to be done | Current workaround | Pain |
|---|---|---|---|
| Returning patient | Keep a check-up booked weeks ahead | A paper card on the fridge | Forgets, then pays a missed-visit fee |
```

**C-04. Convergence prose** (section 6; unchanged from SPEC-001). What was promoted, parked and rejected and why;
before confirmation, the paragraph starting `Proposed, awaiting confirmation:`.

**C-05. First release cut** (section 6, after C-04; mvp-and-prototype-path):

```markdown
### First release cut

First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Tests ASM-01, ranked 1. |
| IDEA-02 | no | Tests no assumption ranked 1 to 3. |
```

The status line is exactly `First release cut: proposed, not confirmed` or
`First release cut: confirmed on YYYY-MM-DD`, naming nobody. One row per idea that is promoted or proposed for
promotion, in ID order; the second column is `yes` or `no`; the `Why` cell is one of the eight fixed sentences
mvp-and-prototype-path defines: five that the rule writes, `Included by the user.` and `Left out by the user.`,
which are written only on a row whose value the user stated, and the review flag
`Needs review: no rule supports this value.`, which stands with either value and only under the proposed status
line. With no such idea the table is replaced by the line `No idea is promoted or proposed for promotion.`

**C-06. Already covered and previously decided** (section 6, brownfield only, after C-05; brownfield-iteration):

```markdown
### Already covered

| Suggestion | Covered by |
|---|---|
| Text reminders before a visit | PRD-001#FR-003 |

### Previously decided

| Idea | Decision | Where |
|---|---|---|
| Charge a deposit at booking | rejected | BRN-001#IDEA-06 |
```

`Covered by` is `<document ID>#<item ID>`; `Decision` is `rejected` or `parked`; `Where` is `BRN-NNN#IDEA-NN`.
Each table is replaced by the line `None.` when it has no row. When the user says to add a candidate anyway, its
row is removed and section 6's prose says so: the tables list only what is still kept out.

**C-11. Assumption updates** (section 6, brownfield only, after C-06; brownfield-iteration). Section 6's order is
therefore C-04, C-05, C-06, C-11.

```markdown
### Assumption updates

| Earlier assumption | Change | Evidence | Status |
|---|---|---|---|
| BRN-001#ASM-01 | open to validated | 8 of 10 reminder texts were opened (data: reminder pilot export, October 2026) | proposed, not confirmed |
```

`Change` is `open to validated` or `open to invalidated`; `Status` is `proposed, not confirmed` or
`confirmed on YYYY-MM-DD`, naming nobody. The table is replaced by the line `None.` when it has no row. In a run
that extends a brownfield BRN, the first cell may name that BRN's own assumption.

**C-07. Assumption risk ranking** (section 7, after the `assumptions` block and before the open-question bullets;
mvp-and-prototype-path):

```markdown
### Assumption risk ranking

| Rank | Assumption | If wrong | Confidence | Cheapest test |
|---|---|---|---|---|
| 1 | ASM-01 | Serious: stops IDEA-01 (1 of 2 in the cut table). | low | Interview: Ask ten patients whether they read texts from the clinic. |
```

One row per active assumption whose `state` is `open`, ranks 1 to n with no gap. `If wrong` starts with `Fatal`,
`Serious` or `Minor` and names the cut-table ideas the assumption stops; `Confidence` is `high`, `medium` or
`low`; `Cheapest test` starts with `Data`, `Prototype` or `Interview`, or is the marker
`[NEEDS CLARIFICATION: how to test ASM-NN]`. With no such assumption the table is replaced by the line `None.`
This ranking, and no other table, decides the first release cut.

**C-08. Candidate success signals** (section 8; intake-and-evidence). One bullet per first-release idea, in ID
order:

```markdown
- IDEA-01: fewer missed visits among patients who got a reminder; baseline [NEEDS CLARIFICATION: current no-show rate]
```

that is, `- <IDEA-NN>: <observable outcome>; baseline <value with its source, or a NEEDS CLARIFICATION marker>`.
With no first-release idea the section holds the line `- None.`

**C-09. Sources** (frontmatter `sources`; intake-and-evidence). One quoted string per input the brainstorm used,
`"<kind>: <reference>"`, `<kind>` one of `document`, `data`, `ticket`, `interview`, `url`, `note`. Example:
`"document: docs/specs/prd/PRD-001.md v3"`. A fact cited in a problem's `evidence` or a C-08 baseline is either
one NEEDS CLARIFICATION marker and nothing else, or text that ends with one `sources` entry, without its quotes,
in parentheses after a space. A C-11 `Evidence` cell always ends with such an entry and is never a marker: with
no fact there is no row (brownfield-iteration.md). In a BRN a brownfield run creates, the entries of the
documents it read stand first; a run that extends a BRN appends its new entries and never reorders the others.

**C-10. Step 5's form.** One AskUserQuestion form tagged step 5, its questions in this order, each with
`header: "Step 5"`; a question whose condition fails is left out:

1. "Confirm these dispositions?" (always; unchanged from SPEC-001 BEH-06).
2. "Has the brainstorm converged?" (always; unchanged).
3. "Confirm the first release cut?" (when C-05's table has a row), options `Accept as proposed` and
   `Leave it proposed`; changes come typed under Other.
4. "Confirm these assumption updates?" (when C-11's table has a row), options `Accept all as proposed` and
   `Leave them proposed`; changes come typed under Other.

Built in §8's order, SKILL.md's list passes through one intermediate state. The third commit
(brownfield-iteration.md, edit B-S5) adds question 4's item after question 2 and numbers it 3, because no cut
question exists yet. The fourth commit (mvp-and-prototype-path.md, edit S7) inserts question 3 and renumbers
that item 4. Only the fourth commit's state ships.

**The gate.** A BRN is a *new-shape BRN* when a line after the frontmatter and outside every fenced block,
lowercased and with its runs of spaces collapsed, starts with `project kind:`. Every validator check these
documents add applies only to a new-shape BRN, and a new-shape BRN must hold every shape its kind requires
(C-01, C-03, C-05, C-07, C-08, C-09 always; C-02, C-06 and C-11 when the kind is brownfield). The test is loose
on purpose and C-01 is exact: a line that passes the test but is not one of C-01's three lines
(`project  kind: Brownfield`) makes the BRN new-shape, switches every check on, and is then rejected by IV-01,
which requires C-01's exact line, first under `## 1. Context` and followed by a blank line.

A BRN without the line is an earlier-shape BRN: it is checked exactly as today and stays valid. When it is
extended it keeps its earlier shape: no shape of this section is added to it, nothing of brownfield-iteration.md
or mvp-and-prototype-path.md applies to it, its run asks the greenfield question set (intake-and-evidence.md,
BEH-20), and step 8's report block is today's (prd-handoff-contract.md, BEH-34). Framework selection applies to
it as to any run, except rule 4, which needs a kind.

When a new-shape BRN is extended, its kind line changes only towards brownfield (the NEEDS CLARIFICATION line
may be decided; `greenfield` may become `brownfield`; `brownfield` stays) and nothing is removed from it except
the bullet of C-01 that says which kind an undecided run worked as. A run that turns the line to `brownfield`
adds C-02, C-06 and C-11 (intake-and-evidence.md, BEH-20; brownfield-iteration.md, BEH-29).

## 5. Framework selection

`references/frameworks/INDEX.md` lists five frameworks. The skill takes the first rule that matches:

| # | When | Framework |
|---|---|---|
| 1 | The user names a framework that the index lists | that one |
| 2 | The request supplies three or more candidate ideas, or names a backlog or list to use, and asks to rank, prioritise, choose among or cut them | `shortlist-ranking` |
| 3 | The request asks what to build first, for an MVP or a prototype, or what could make the idea fail | `risk-first-mvp` |
| 4 | The project kind is brownfield and the topic is improving, extending or fixing the existing product | `improve-existing` |
| 5 | After intake, no problem can be stated with an affected person and what hurts them (the topic is a symptom, a goal or a solution) | `problem-reframing` |
| 6 | Otherwise | `diverge-converge` |

[framework-catalog.md](framework-catalog.md) specifies each framework, the phrases that make rules 2 to 4 match,
and stages each file. Rule 4's project kind is the kind step 1 decided or, when it is undecided, the kind the
run works with (intake-and-evidence.md, BEH-20).

## 6. Item IDs

SPEC-001 version 18 ends at BEH-14, ERR-05, VER-17, as version 17 did. Each document takes the next IDs from
its own range and leaves unused ones unallocated. No brainstorm-series ID is used twice in this folder.

| Document | BEH | ERR | VER | Validator checks |
|---|---|---|---|---|
| framework-catalog.md | BEH-15 to BEH-19 | ERR-06 | VER-18 to VER-24 | none |
| intake-and-evidence.md | BEH-20 to BEH-24 | ERR-07 | VER-25 to VER-29 | IV-01 to IV-07 |
| brownfield-iteration.md | BEH-25 to BEH-29 | ERR-08, ERR-09 | VER-30 to VER-34 | BV-01 to BV-05 |
| mvp-and-prototype-path.md | BEH-30 to BEH-33 | ERR-10 | VER-35 to VER-38 | MV-01 to MV-12 |
| prd-handoff-contract.md (brainstorm's side) | BEH-34 | none | VER-39 | none |

`prd-handoff-contract.md` also proposes items for SPEC-002, the PRD skill's spec. They come from SPEC-002's own
series and are always written with the prefix, `SPEC-002#BEH-27`, so they can't be read as brainstorm items.

## 7. Staged files and where they go

| Staged under `docs/specs/brainstorming/staged/` | Destination | Specified in |
|---|---|---|
| `skills/brainstorm/references/frameworks/INDEX.md` | `src/claude/DevForgeAI/skills/brainstorm/references/frameworks/INDEX.md` (replaces) | framework-catalog.md |
| `skills/brainstorm/references/frameworks/shortlist-ranking.md`, `problem-reframing.md`, `improve-existing.md`, `risk-first-mvp.md` | the same folder (new) | framework-catalog.md |
| `skills/brainstorm/references/intake.md` | `src/claude/DevForgeAI/skills/brainstorm/references/intake.md` (new) | intake-and-evidence.md |
| `skills/brainstorm/references/brownfield.md` | `…/references/brownfield.md` (new) | brownfield-iteration.md |
| `skills/brainstorm/references/mvp-path.md` | `…/references/mvp-path.md` (new) | mvp-and-prototype-path.md |
| `skills/brainstorm/assets/brainstorm.md` | `src/claude/DevForgeAI/skills/brainstorm/assets/brainstorm.md` (replaces) and its identical copy `src/templates/brainstorm.md` | intake-and-evidence.md (the one template, holding every shape) |
| `examples/brainstorm-greenfield-mvp/` | `src/staging/examples/brainstorm-greenfield-mvp/` (new) | mvp-and-prototype-path.md |
| `examples/brainstorm-brownfield/` | `src/staging/examples/brainstorm-brownfield/` (new) | brownfield-iteration.md |

`diverge-converge.md`, `SKILL.md`, `output-rules.md`, `work-file.md` and `validate_brn.py` are not staged: they
change by the exact edits (R7) and the checks the documents give.

## 8. The build

**Coordination with pull request #173** (Bryan, 2026-11-19: "Coordinate the build with #173, which already has
approval for SPEC-001 v18 and SKL-001 v12. Let #173 land first, then draft the enhancement spec on Fable 5.2
against updated main, preserving Taskmaster's eight checklist titles. Use the next available versions, expected to
be SPEC-001 v19 and SKL-001 v13. Bring me that spec for approval before editing the skill. Then build on Opus 5.5
at xhigh using both plugin-dev skills, one commit per brainstorm enhancement. Keep the PRD-side hand-off
separate."). #173 merged on 2026-11-20 (`8769dd8`): `main` holds SPEC-001 version 18, SKL-001 version 12 and
plugin 0.35.0, so this build is SPEC-001 version 19 and SKL-001 version 13. #173 added a `tasks:` list to
SKILL.md's frontmatter whose eight titles are the checklist lines without their numbers: R2 keeps those lines
unchanged, and the build keeps the `tasks:` list equal to them.

The documents were checked again on 2026-11-20 against `main` at `ff78d44`. Every exact edit (R7) of the five
documents still applies: #173 changed only the frontmatter of SKILL.md, which no document quotes. What changed
here: the build's version numbers; SKILL.md's line counts, 9 higher at every stage (325 today; 331, 348 and 368
after the first three commits; 386 after the fourth, 380 before BEH-34's six lines); the hash
framework-catalog.md gives; and BEH-16's bound on where the checklist opens, now counted from the end of the
frontmatter (Bryan, 2026-11-20: "17 lines after frontmatter (Recommended)"). Where a document's record of its
author's checks names version 11, that record stands as written and a dated line gives the re-check. The
review of SPEC-001 version 19, the same day, added one sentence to BEH-32's item 5, the ask for the owner's
name, which mvp-and-prototype-path.md's §4 and the staged `mvp-path.md` already gave.

Later on 2026-11-20 Bryan decided that a confirmation names no owner (§2). That took the ask for the owner's
name out again, from BEH-32's item 5, BEH-28, both documents' §4 and both staged references, and changed C-05's
status line, C-11's status cell, the override sentence of BEH-26, the validator's checks MV-08, MV-12 and BV-05
with their tests, the template's two comments and both staged examples. Checked the same way afterwards: every
exact edit applies; SKILL.md's line counts are the same at every stage; the tests are as many as before (16 in
`test_structure.py`; 96, 183, 279 and 354 in `test_validate_brn.py` after the four commits), `OK` with and
without site-packages; the staged examples print `OK`.

SPEC-001 version 19 and ADR-003 version 3 are drafted before the build and approved by Bryan. They make the
five edits the documents give for those two files (A-P1, A-D1, B-P1, B-P2, B-P3), so no commit of the build
repeats them.

The four brainstorm documents are built together as SKL-001 version 13, in this order, one commit for each:

1. framework-catalog.md
2. intake-and-evidence.md
3. brownfield-iteration.md
4. mvp-and-prototype-path.md

Because they ship as one version, no document carries a rule for shipping alone: the template is staged once, in
its final form, and is copied by the second commit; a shape owned by a later document is written by the skill only
from that document's commit on, and the validator's check for it arrives with that commit. Each commit leaves
every test passing.

prd-handoff-contract.md's one brainstorm item (BEH-34, the report block of step 8) is built with the fourth
commit, so the skill needs no further version for it. Its PRD side is built afterwards, alone: it changes the
PRD skill and needs a version of SPEC-002.

The build:
- works from SPEC-001 version 19, which takes in the documents' items, and from ADR-003 version 3 (the
  clarifying-question limit, as intake-and-evidence.md says): Bryan approves both before any skill edit;
- bumps SKL-001 once, to 13 (`provenance.yaml` `version` and SKILL.md `devforgeai-version`), and the plugin
  version to 0.36.0 (Bryan, 2026-11-20: "0.36.0 (Recommended)"; `plugin.json`,
  `.claude-plugin/marketplace.json`, the pin in `src/tests/progress/test_adapter_structure.py`);
- writes tests first: `src/tests/brainstorm/test_structure.py` (new; framework-catalog.md) and
  `src/tests/brainstorm/test_validate_brn.py`;
- keeps `python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py docs/specs/brainstorm/BRN-001.md`
  printing `OK`;
- adds the eval cases the documents list. Brainstorm's cases are hand-written; there is no generator.

A new SKL-001 version ends the waivers in SPEC-001 §9 (version 11's, "until this skill's next version or
2026-12-31", and version 12's, "until the next brainstorm skill version or 2026-12-31, whichever comes first"):
the three-run qualification at 0.8 per case is due for every brainstorm case, old and new, including
`saves-work-as-it-goes`, which scored 0.78 on version 10.

Not touched by the build: `src/schemas/brainstorm.schema.json` (R1), the progress manifest (R2), `src/codex/`
(Codex sessions keep it).

## 9. Left to Bryan

- Approving SPEC-001 version 19 and ADR-003 version 3 before the build, and SPEC-002's next version for
  prd-handoff-contract.md.
- The entries each document lists as open in its section 7.
- Whether a brainstorm pane is built at all (design-prompts.md only prepares its mock-ups).
