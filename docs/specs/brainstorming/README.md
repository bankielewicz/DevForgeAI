# Brainstorm skill: enhancement specs

**Status:** proposals, written 2026-11-18 by claude-code (session fa59a935-ed2e-4502-b6c4-93bb6d847546) for
Bryan's review. They change no spec, skill or plugin version. The brainstorm skill's approved spec stays
`docs/specs/spec/SPEC-001.md` (version 17); each document here says which SPEC-001 items it adds or changes, and
those changes take effect only in SPEC-001's next version, approved by Bryan, built in a plugin-dev iteration
(`/plugin-dev:create-plugin` and `/plugin-dev:skill-development`; CLAUDE.md, "Rules a change must not break").

This file is the index and the shared contract. Read it before any other file in this folder: the other documents
use its names, shapes and IDs without repeating them.

## The workflow, and where each enhancement lands

The skill's task list is these eight steps. Their lines in SKILL.md don't change (R2); the enhancements add work
inside them. Every document in this folder opens with its own copy of this table, holding only its rows.

| Step (SKILL.md's line, unchanged) | Today | Added by these documents |
|---|---|---|
| 1. Intake: topic, existing BRNs, clarifying questions | Topic; extend or new; up to three questions | Project kind decided (C-01); the question set for that kind; sources gathered (C-09) — intake-and-evidence. Brownfield: the project's documents and earlier BRNs read (C-02) — brownfield-iteration |
| 2. Select a framework | The one named, else `diverge-converge` | Five frameworks and §5's selection rules — framework-catalog |
| 3. Diverge: problems, ideas, assumptions | Problems, 5 to 15 ideas, assumptions | The chosen framework's own steps; `evidence` from the sources; the Target users table (C-03) — intake-and-evidence. Brownfield: covered and previously decided ideas kept out of `ideas` (C-06) — brownfield-iteration |
| 4. Evaluate with the framework | value, effort, risk, score | Each framework's mapping — framework-catalog. The ranking and the cut are not made here: they need step 5's proposals (mvp-and-prototype-path, "Terms and the order of work") |
| 5. Propose dispositions and ask the user to confirm | Two questions: dispositions, convergence | After the proposals: the assumption risk ranking (C-07) and the proposed first release cut (C-05) are made — mvp-and-prototype-path. Up to two more questions in the same form (C-10): the first release cut — mvp-and-prototype-path; assumption updates — brownfield-iteration |
| 6. Write the BRN | Template, frontmatter, Change Log | The fixed shapes of §4 written; success signals (C-08) — intake-and-evidence, mvp-and-prototype-path |
| 7. Validate the BRN | `validate_brn.py`, then the read-back | New validator checks, the IV, BV and MV series of §6, each named in its document; the read-back also covers C-05's status line and assumption states (R3) |
| 8. Report and hand off | Report block; `/devforgeai:prd BRN-NNN` | The report names the project kind and the first-release ideas — prd-handoff-contract |

## 1. Why

`/devforgeai:brainstorm` (SKL-001 v11) ships the plumbing of a brainstorm and one method. What it lacks:

| Gap today | Evidence | Closed by |
|---|---|---|
| One framework, `diverge-converge`, which its own index says to avoid for a shortlist | `skills/brainstorm/references/frameworks/INDEX.md` | [framework-catalog.md](framework-catalog.md) |
| At most three intake questions; no step fills section 3 (Target users) or section 8 (Candidate success signals); `sources` and `evidence` filled only by chance | `SKILL.md` steps 1, 3, 6; the template's sections 3 and 8 are comments | [intake-and-evidence.md](intake-and-evidence.md) |
| Nothing for a product that exists: no reading of the PRD, epics or architecture already written, no revisiting of earlier assumptions | `SKILL.md` step 1 reads other BRNs' titles only | [brownfield-iteration.md](brownfield-iteration.md) |
| No path to a first release or a prototype: assumptions are not ranked, no first-release cut is proposed | no such step or section | [mvp-and-prototype-path.md](mvp-and-prototype-path.md) |
| The PRD skill asks for what a richer brainstorm already holds | `skills/prd/references/interview.md` | [prd-handoff-contract.md](prd-handoff-contract.md) |

[design-prompts.md](design-prompts.md) holds prompts for Claude Design (mock-ups of a brainstorm pane and of the
end-of-run hand-off). It specifies no behaviour.
[design/](design/README.md) holds the mock-ups Claude Design made from them (directions chosen by Bryan on 2026-11-18; the look is not settled).
[staged/prototypes/](staged/prototypes/README.md) holds the scratch prototypes the drafts were tested with.

## 2. Decisions these documents rest on

All by Bryan, 2026-11-18, in session fa59a935-ed2e-4502-b6c4-93bb6d847546:

- "the brainstorming skill is to handle both brownfield and greenfield projects".
- The catalog (PRD-001 §12's open question, "which brainstorming frameworks join the catalog, and in what
  order"): all four offered were chosen: "Shortlist ranking, Problem reframing, Improve an existing product,
  Risk-first and MVP scoping". The order in the index is the order of §5's selection rules.
- The groups: "Intake and evidence, Brownfield iteration, MVP and prototype path, PRD hand-off contract".
- The location, `docs/specs/brainstorming/<slug>.md`, each document feeding SPEC-001's next version: "option 1
  but create a worktree for a PR for you to push".
- Design prompts: "generate an ai prompt for various screens to be generated by claude design ... the look and
  feel of the claude mod for brainstorm (if one is created) along with the 'next steps'/handoff at the end of the
  workflow".

Spec lookup (SPEC-014 BEH-08), run on 2026-11-18 with `find_spec.py`: the framework catalog is deferred in
PRD-001 (non-goal, line 58; FR-002's note; §12) and SPEC-001 §1 (line 44); section 3 and section 8 of a BRN are
read by the PRD skill (SPEC-002#BEH-05, SPEC-002#BEH-19 and its mapping of success signals, line 164); no spec, ADR or
recorded decision covers reading existing documents during a brainstorm, ranking assumptions, or a first-release
cut. ADR-003 (line 92) makes a BRN's `disposition` and a PRD's MoSCoW `priority` part of the document contract
("A different prioritization method needs a mapping to MoSCoW or a schema change, not a setting"), and (line 94)
makes the idea count and the clarifying-question limit interaction defaults. ADR-006 and ADR-010 keep
dispositions the user's. SPEC-001 §12 rejected listing frameworks in SKILL.md and the skill setting dispositions
itself.

## 3. Rules every document here follows

- **R1. No new collection and no new field in a BRN.** A BRN holds `problems`, `ideas` and `assumptions` with the
  fields `references/output-rules.md` lists today, and its frontmatter keys stay the same. New information goes
  into the fixed prose shapes of §4. Reason: a new field would change `src/schemas/brainstorm.schema.json`,
  `validate_brn.py` (which must give the same verdict with and without PyYAML), `output-rules.md`, the template,
  the PRD skill's mapping, the ui skill's `dsn_check.py`, the Codex fork (which Claude sessions don't edit) and
  the BRN fixtures of four skills' evals. A document that needs a field says so under "Open questions" and
  specifies nothing that depends on it.
- **R2. SKILL.md's eight checklist lines don't change**, not by a character. `progress/manifests/brainstorm.json`
  holds their hash and `src/tests/progress/test_evaluate.py` checks it. New work happens inside the existing
  steps; its detail goes into new files under `references/`, each linked from SKILL.md once and from the step that
  needs it. SKILL.md stays at or under 400 lines (the limit is 500; it is 316 today).
- **R3. The user's decisions stay the user's.** A method proposes; only the user's explicit answer writes a
  disposition, `status: converged`, an assumption's `state` other than `open`, or a confirmed first-release cut.
  Whatever was not confirmed is written in its unconfirmed form (§4) and is never worded as decided.
- **R4. Every requirement is an item with an ID** from §6's allocation, written in a `yaml items` block like
  SPEC-001's, with these keys: `id`, `status: proposed`, `rule` (one testable sentence or a numbered list),
  `changes` (the SPEC-001 item it replaces or extends, or `new`), `lands_in` (the destination file and section).
  A verification item has `id`, `status: proposed`, `covers`, `level` (`eval`, `unit` or `manual`), `obligation`,
  and for `eval` the case's folder name, its prompt, its scaffold and each grader with its type (`regex`,
  `file_exists`, `tool_used`, `llm`).
- **R5. An eval can't answer a question** (`.claude/rules/evals.md`; SPEC-001 §9). A behaviour that needs an
  answer is verified `manual`, or its eval prompt says to proceed without questions and grades the unconfirmed
  form.
- **R6. Staged files are complete.** Every file under [staged/](staged/) is the whole file as it should exist at
  its destination, with no placeholder left for the builder. §7 gives each destination.
- **R8. Layout of each document.** In this order: the status line; `## Workflow steps this changes` (the table
  above, its rows only, first in the document, as Bryan asked: "ensure the tasklist or phases of the brainstorm
  skill is at the front of the spec"); `## 1. Scope` (in and out); `## 2. Changes by file`; `## 3. Behaviour`;
  `## 4. Errors and edge cases`; `## 5. Verification`; `## 6. Staged files`; `## 7. Open questions`.
- **R7. Words.** "The skill" is `/devforgeai:brainstorm`. "The project" is the folder the session works in.
  "Earlier BRN" is a `docs/specs/brainstorm/BRN-NNN.md` of the project that exists before the run. "Proposed for
  promotion" means the skill's step-5 proposal for the idea is `promoted`. "The first-release ideas" are the
  ideas whose row in §4's C-05 table says `yes`.

## 4. The shared contract: fixed shapes in a BRN

Every shape below is plain Markdown inside an existing section, valid for today's `validate_brn.py`.
`[NEEDS CLARIFICATION: <question>]` may stand for any cell or value that is unknown.

**C-01. Project kind** (section 1). The first line under `## 1. Context` is exactly one of:

```text
Project kind: greenfield
Project kind: brownfield
Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]
```

followed by a blank line and the context prose. *Brownfield* means the product the topic is about exists (it has
been built, or is in use); *greenfield* means it does not. [intake-and-evidence.md](intake-and-evidence.md) gives the
ordered rules that decide it: the user's words first, then a question. A PRD in the project is only the recommended
answer to that question and the *assumed* kind when the kind can't be decided (the third line above); it never decides
the kind, and the assumed kind is never written as the kind.

**C-02. Existing product** (section 1, brownfield only). After the context prose:

```markdown
### Existing product

| Document | Version | What it already covers |
|---|---|---|
| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006; NFR-001 to NFR-002) |
```

One row per document read; the last cell's form by kind of document is brownfield-iteration.md's BEH-26. The table is
absent in a greenfield BRN.

**C-03. Target users** (section 3). Exactly this table, one row per distinct `who` value of the active problems,
the persona cell equal to that value character for character, rows in the order the values first appear:

```markdown
| Persona | Job to be done | Current workaround | Pain |
|---|---|---|---|
| Returning patient | Keep a check-up booked weeks ahead | A paper card on the fridge | Forgets, then pays a missed-visit fee |
```

**C-04. Convergence prose** (section 6). First the prose SPEC-001 already requires: what was promoted, parked and
rejected and why, or, before confirmation, the paragraph starting `Proposed, awaiting confirmation:`.

**C-05. First release cut** (section 6, after C-04):

```markdown
### First release cut

First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Tests ASM-01 (rank 1); effort low; score 4 |
| IDEA-04 | no | Tests no assumption ranked 1 to 3; effort medium; score 1 |
```

The status line is exactly `First release cut: proposed, not confirmed` or
`First release cut: confirmed by <owner> on YYYY-MM-DD`. The table has one row per idea that is promoted or
proposed for promotion, in ID order; the second column is `yes` or `no`. The `Why` cell is one of the fixed sentences
of mvp-and-prototype-path.md (§3.2) followed by `; effort E; score S`. With no such idea the table is replaced by the
line `No idea is promoted or proposed for promotion.`

**C-06. Already covered and previously decided** (section 6, brownfield only, after C-05):

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

Each table is replaced by the line `None.` when it has no row.

**C-11. Assumption updates** (section 6, brownfield only, after C-06; so section 6's order is C-04, C-05, C-06,
C-11):

```markdown
### Assumption updates

| Earlier assumption | Change | Evidence | Status |
|---|---|---|---|
| BRN-001#ASM-01 | open to validated | 62% of October 2026 bookings were made online (data: ClinicCore booking source report, October 2026) | proposed, not confirmed |
```

`Change` is `open to validated` or `open to invalidated`; `Evidence` is a short claim with one `sources` entry in
parentheses; `Status` is `proposed, not confirmed` or `confirmed by <owner> on YYYY-MM-DD`. The table is replaced by
the line `None.` when it has no row. [brownfield-iteration.md](brownfield-iteration.md) specifies it.

**The gates.** The *kind gate*: a BRN "has the project-kind line" when a line after the frontmatter and outside every
fenced block (a fence opens and closes at a line that starts with three backticks), lowercased and with its spaces
collapsed, starts with `project kind:` (the colon is part of the test: a prose line such as "Project kinds vary" does not
switch the gate on). Every validator check these documents add applies only to a BRN that has it, so
earlier BRNs stay valid, with one exception: intake-and-evidence.md's IV-05 reports a BRN that lacks the line but holds
one of the shape headings (`### Existing product`, `### First release cut`, `### Already covered`,
`### Previously decided`, `### Assumption updates`, `### Assumption risk ranking`), because a BRN that lost its kind line
must not pass unnoticed. The *adoption gate* is mvp-and-prototype-path.md's: its MV checks run only when the BRN also
holds `### First release cut` or `### Assumption risk ranking`, so a BRN written by a build that stops before it stays
valid; a BRN that holds one of the two must hold both. brownfield-iteration.md's BV-02 is gated the same way (by the
four brownfield headings). A BRN with the kind line and none of the later shapes passes; one without the kind line fails
only IV-05, and only when it holds a shape heading.

**C-07. Assumption risk ranking** (section 7, after the `assumptions` block and before the open-question bullets):

```markdown
### Assumption risk ranking

| Rank | Assumption | If wrong | Confidence | Cheapest test |
|---|---|---|---|---|
| 1 | ASM-01 | No idea in the first release works | low | Ask ten patients whether they read texts from the clinic |
```

One row per active assumption whose `state` is `open`, rank 1 the riskiest, in the order of
mvp-and-prototype-path.md §3.1 (level, then confidence, then assumption number). `If wrong` is `Fatal`, `Serious` or
`Minor`, then the first-release ideas that fail with the assumption in parentheses when there are any, a colon and one
clause. `Confidence` is `high`, `medium` or `low`. `Cheapest test` is `Data`, `Prototype` or `Interview`, a colon and
the first sentence of the assumption's `validation`. With no such assumption the table is replaced by the line `None.`

A framework may rank assumptions in its own way: `risk-first-mvp` writes a riskiness table in section 5. The riskiness
table is this framework's own working: it rates the test ideas and nothing else, and it is never copied into the
assumption risk ranking (C-07), which is the only ranking that decides the first release cut (C-05).

**C-08. Candidate success signals** (section 8). One bullet per first-release idea, in ID order, in this shape:

```markdown
- IDEA-01: fewer missed visits among patients who got a reminder; baseline [NEEDS CLARIFICATION: current no-show rate]
```

that is, `- <IDEA-NN>: <observable outcome>; baseline <value with its source, or a NEEDS CLARIFICATION marker>`
(intake-and-evidence.md's BEH-23 gives the words). With no first-release idea the section holds the line `- None.`

**C-09. Sources** (frontmatter `sources`). One quoted string per input the brainstorm used, in the form
`"<kind>: <reference>"`, where `<kind>` is one of `document`, `data`, `ticket`, `interview`, `url`, `note`.
Example: `"document: docs/specs/prd/PRD-001.md v3"`. A problem's `evidence` quotes one entry or is a marker
(intake-and-evidence.md's BEH-22).

**C-10. Step 5's form.** One AskUserQuestion form tagged step 5, its questions in this order, each with
`header: "Step 5"`; a question whose condition fails is left out:

1. "Confirm these dispositions?" (always; unchanged from SPEC-001 BEH-06).
2. "Has the brainstorm converged?" (always; unchanged).
3. "Confirm the first release cut?" (when C-05's table has a row), options `Accept as proposed` (Recommended) and
   `Leave it proposed`, each option's `preview` holding the cut table and the C-07 ranking table; changes come typed
   under Other.
4. "Confirm these assumption updates?" (brownfield, when the skill proposes a new `state` for an assumption of an
   earlier BRN), options `Accept all as proposed` and `Leave them open`, each option's `preview` holding the
   earlier assumption, change and evidence columns of C-11; changes come typed under Other.

A build that has question 4 but not question 3 (README §8, build 3 before build 4) holds it as the third question; build
4 inserts question 3 before it and renumbers it 4.

## 5. Framework selection

`references/frameworks/INDEX.md` lists five frameworks. The skill takes the first rule that matches:

| # | When | Framework |
|---|---|---|
| 1 | The user names a framework that the index lists | that one |
| 2 | The request supplies three or more candidate ideas, or names a backlog or list to use, and asks to rank, prioritise, choose among or cut them | `shortlist-ranking` |
| 3 | The request asks what to build first, for an MVP or a prototype, or what could make the idea fail | `risk-first-mvp` |
| 4 | Project kind is brownfield and the topic is improving, extending or fixing the existing product | `improve-existing` |
| 5 | After intake, no problem can be stated with an affected person and what hurts them (the topic is a symptom, a goal or a solution) | `problem-reframing` |
| 6 | Otherwise | `diverge-converge` |

[framework-catalog.md](framework-catalog.md) specifies each framework and stages its file.

## 6. Item IDs

SPEC-001 version 17 ends at BEH-14, ERR-05, VER-17. Each document takes the next IDs from its own range and
leaves unused ones unallocated. Brainstorm-series IDs (SPEC-001's series: BEH, ERR and VER, as the table below
allots them) are unique in this folder. SPEC-002's IDs are a separate series and are always written with the spec
(`SPEC-002#BEH-27`), never bare.

| Document | BEH | ERR | VER |
|---|---|---|---|
| framework-catalog.md | BEH-15 to BEH-19 | ERR-06 | VER-18 to VER-24 |
| intake-and-evidence.md | BEH-20 to BEH-24 | ERR-07 | VER-25 to VER-29 |
| brownfield-iteration.md | BEH-25 to BEH-29 | ERR-08, ERR-09 | VER-30 to VER-34 |
| mvp-and-prototype-path.md | BEH-30 to BEH-33 | ERR-10 | VER-35 to VER-38 |
| prd-handoff-contract.md (brainstorm's side) | BEH-34 | none | VER-39 |

`prd-handoff-contract.md` also proposes items for SPEC-002 (the PRD skill); it takes them from SPEC-002's own
series: `SPEC-002#BEH-27` to `SPEC-002#BEH-30`, `SPEC-002#ERR-12` and `SPEC-002#VER-50` to `SPEC-002#VER-54`. They are
not the brainstorm items of the same number (brownfield-iteration.md has BEH-27 to BEH-29, mvp-and-prototype-path.md
BEH-30); every citation of a PRD-skill item in this folder carries the `SPEC-002#` prefix, and `prd-handoff-contract.md`
§3.7 says which block belongs to which spec.

Validator check IDs, a second series (message texts are exact in each document):

| Document | Checks |
|---|---|
| framework-catalog.md | none (its checks are the unit test file of VER-23, not validator checks) |
| intake-and-evidence.md | IV-01 to IV-12; the table messages T-1 to T-3, which brownfield-iteration.md shares |
| brownfield-iteration.md | BV-01 to BV-14 |
| mvp-and-prototype-path.md | MV-01 to MV-30 |
| prd-handoff-contract.md | none (the PRD skill has no document validator) |

## 7. Staged files and where they go

| Staged under `docs/specs/brainstorming/staged/` | Destination | Specified in |
|---|---|---|
| `skills/brainstorm/references/frameworks/INDEX.md` | `src/claude/DevForgeAI/skills/brainstorm/references/frameworks/INDEX.md` (replaces) | framework-catalog.md |
| `skills/brainstorm/references/frameworks/shortlist-ranking.md`, `problem-reframing.md`, `improve-existing.md`, `risk-first-mvp.md` | the same folder (new) | framework-catalog.md |
| `skills/brainstorm/references/intake.md` | `src/claude/DevForgeAI/skills/brainstorm/references/intake.md` (new) | intake-and-evidence.md |
| `skills/brainstorm/references/brownfield.md` | `…/references/brownfield.md` (new) | brownfield-iteration.md |
| `skills/brainstorm/references/mvp-path.md` | `…/references/mvp-path.md` (new) | mvp-and-prototype-path.md |
| `skills/brainstorm/assets/brainstorm.md` | `src/claude/DevForgeAI/skills/brainstorm/assets/brainstorm.md` (replaces), and the leftover copy `src/templates/brainstorm.md` | intake-and-evidence.md |
| `examples/brainstorm-greenfield-mvp/` | `src/staging/examples/brainstorm-greenfield-mvp/` (new) | mvp-and-prototype-path.md |
| `examples/brainstorm-brownfield/` | `src/staging/examples/brainstorm-brownfield/` (new) | brownfield-iteration.md |

`diverge-converge.md` is not staged: it changes only where framework-catalog.md says, as an edit.

Two staged files are *end-state* files, written for the point where every build is done; a build that ships alone
must not copy them as they stand:

- `assets/brainstorm.md` (the template) holds the shapes of builds 2 to 4. intake-and-evidence.md §6, "The template per
  build", lists each part to cut for a build that stops early and which document puts it back (brownfield-iteration.md
  §2 puts back the brownfield regions; mvp-and-prototype-path.md §2 the cut and the ranking).
- `references/frameworks/INDEX.md` is complete at build 1 and no later build changes it. Its rows name only the five
  framework files, and its Project kind term works without intake-and-evidence.md (framework-catalog.md §2 and BEH-15).

The staged `intake.md`, `brownfield.md` and `mvp-path.md` need no per-build change: each names a reference that a
later build adds only with "when it exists" (intake.md for brownfield.md, mvp-path.md for the brownfield reference).

## 8. Build order and what a build touches

Build in this order; each is one plugin-dev iteration and may ship alone:

1. framework-catalog.md
2. intake-and-evidence.md (the template and C-01, C-03, C-08, C-09)
3. brownfield-iteration.md (needs 2)
4. mvp-and-prototype-path.md (needs 2)
5. prd-handoff-contract.md (needs 2 and 4; changes the PRD skill)

Every build of 1 to 4:
- edits the shared files (`SKILL.md`, `references/output-rules.md`, `references/work-file.md`) by exact old and new
  text, applied in this order. Each document's old text is the file as the earlier builds left it, read with line
  breaks and runs of spaces as one space; where a document inserts into a passage that an earlier one changed, it says
  so. The checklist numbers in `output-rules.md` are 12 (intake-and-evidence.md), 13 (brownfield-iteration.md) and 14
  (mvp-and-prototype-path.md); the catalog adds none. After all five builds `SKILL.md` is about 370 lines (limit 400,
  R2; simulated on a scratch copy: 362 before the report-block paragraph of prd-handoff-contract.md) and its eight checklist lines are byte for byte as today;
- drafts SPEC-001's next version from the document's items and gets Bryan's approval before any skill edit;
- bumps SKL-001 (`provenance.yaml` `version` and SKILL.md `devforgeai-version`) and the plugin version
  (`plugin.json`, `.claude-plugin/marketplace.json`, the pin in `src/tests/progress/test_adapter_structure.py`);
- writes tests first: `src/tests/brainstorm/test_structure.py` (new, specified in framework-catalog.md) and
  `test_validate_brn.py`;
- keeps `python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py docs/specs/brainstorm/BRN-001.md`
  printing `OK` (an earlier BRN has none of §4's shapes and stays valid: the validator requires a shape only
  where the document that adds the check says so);
- adds the eval cases the document lists. Brainstorm's cases are hand-written; there is no generator.

A new SKL-001 version ends the waiver in SPEC-001 §9 ("until this skill's next version or 2026-12-31"): the
three-run qualification at 0.8 per case is due for every brainstorm case, old and new, including
`saves-work-as-it-goes`, which scored 0.78 on version 10.

Also touched, outside the skill: `docs/specs/adr/ADR-003.md` (intake-and-evidence.md changes the clarifying-question
limit from 3 to 4 on its line 94, so ADR-003 gets version 3 with Bryan's approval and every `upstream` link that cites it
moves to it); `docs/specs/spec/SPEC-002.md` (version 10), the PRD skill and `src/tests/prd/` (prd-handoff-contract.md);
`docs/specs/spec/SPEC-001.md` (a new version per build); `.claude/rules/skills.md` and `CLAUDE.md`'s skills table where
the documents say so.

Not touched by any of these builds: `src/schemas/brainstorm.schema.json` (R1), the progress manifest (R2),
`src/codex/` (Codex sessions keep it).

## 9. Left to Bryan

- Approving each SPEC-001 version at build time, and SPEC-002's for prd-handoff-contract.md.
- The "Open questions" section of each document; each lists what it could not settle, or says `None.`
- Whether a brainstorm pane is built at all (design-prompts.md only prepares its mock-ups).
