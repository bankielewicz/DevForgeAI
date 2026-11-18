# Example: a brownfield brainstorm

A small clinic has an online booking product. This example shows the brainstorm that follows its launch: the
brainstorm reads the product's PRD and its earlier brainstorm first, and keeps what is already built or already
decided out of the new ideas.

| File | What it is |
|---|---|
| `BRN-001.md` | The earlier brainstorm, in the shape before `Project kind:` existed: free prose in sections 3 and 8, free-text `sources` and `evidence`. It stays valid and is never edited by a new brainstorm. |
| `PRD-001.md` | The PRD written from BRN-001: version 3, approved, six functional and two non-functional requirements. FR-003 is the day-before text reminder. |
| `BRN-002.md` | The brownfield brainstorm. It follows every shape of the contract (README of `docs/specs/brainstorming/`, section 4, C-01 to C-09), and C-11. |

## What `BRN-002.md` shows

| Shape | Where | What to look at |
|---|---|---|
| C-01 | Section 1, first line | `Project kind: brownfield`, then a blank line |
| C-02 | Section 1, `### Existing product` | A row for PRD-001 (version 3) and one for BRN-001 (version 1); each has an `informed_by` record in `upstream` and a `document:` entry in `sources` |
| C-03 | Section 3 | One row per distinct `who` of the active problems, in order: Returning patient, Front-desk staff; one cell is a `[NEEDS CLARIFICATION: ...]` marker |
| C-04 | Section 6, first paragraph | What was promoted, parked and rejected, and that IDEA-03 takes up BRN-001#IDEA-03 |
| C-05 | Section 6, `### First release cut` | Confirmed by Dana; the three promoted ideas are all in the first release (each tests a top-three assumption, and the cut holds at most three such ideas) |
| C-06 | Section 6, `### Already covered` and `### Previously decided` | The user suggested text reminders: PRD-001#FR-003 already covers them, so they are not an idea. A voice assistant (parked) and a deposit (rejected) were decided in BRN-001 |
| C-07 | Section 7, `### Assumption risk ranking` | Two open assumptions, ranked Serious and low confidence, then by number; each cheapest test starts with its method |
| C-08 | Section 8 | One bullet for each first-release idea (three); one baseline quotes a `sources` entry, the others are markers |
| C-09 | Frontmatter `sources` and each problem's `evidence` | Every `evidence` quotes a `sources` entry or is a marker |
| C-11 | Section 6, `### Assumption updates` | BRN-001#ASM-01 is proposed `open to validated` on a fact the user gave, and the user confirmed it. BRN-001 is not edited |

Two ideas show lineage without a new field: IDEA-03 and ASM-01 each carry an item `upstream` record
(`informed_by`) that names the earlier BRN's item they take up.

## Validate it

The validator checks the folder name, so copy the BRNs into a folder named `docs/specs/brainstorm/` first:

```bash
mkdir -p tmp/ex/docs/specs/brainstorm
cp docs/specs/brainstorming/staged/examples/brainstorm-brownfield/BRN-00[12].md tmp/ex/docs/specs/brainstorm/
python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py tmp/ex/docs/specs/brainstorm/BRN-001.md
python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py tmp/ex/docs/specs/brainstorm/BRN-002.md
```

Both print `OK:`. `BRN-002.md` passes today's validator (which ignores the new shapes) and the validator with the
checks that `intake-and-evidence.md` and `brownfield-iteration.md` specify. Section 5's method text follows `references/frameworks/improve-existing.md`; C-05, C-07 and C-08 follow the
rules of `mvp-and-prototype-path.md` (§3.1 and §3.2) as they stood on 2026-11-18 (E is IDEA-01, IDEA-03, IDEA-04;
both open assumptions are Serious with low confidence; every row of the cut is `yes`, as the rules give). Recheck them
if those files change.

BRN-002 is a new BRN written beside BRN-001. Its topic shares two words with BRN-001's title (`online`,
`patients`), so the skill asked extend or new and the user chose new; nothing in the document shows that choice.

The three documents are fiction: the clinic, the reports and the people do not exist.
