# Example: a brownfield brainstorm

A dental clinic's online booking site is live. Its owner, Dana, brainstorms what to improve next. The
three documents show what `/devforgeai:brainstorm` reads and writes when the product already exists.

| File | In a project it is | What it shows |
|---|---|---|
| `BRN-001.md` | `docs/specs/brainstorm/BRN-001.md` | The earlier brainstorm, in the earlier shape (no `Project kind:` line). Converged: two ideas promoted, two parked, two rejected; two assumptions open |
| `PRD-001.md` | `docs/specs/prd/PRD-001.md` | The PRD of the product in use, version 3, with FR-001 to FR-006 |
| `BRN-002.md` | `docs/specs/brainstorm/BRN-002.md` | The brownfield brainstorm, in the new shape, after Dana confirmed everything |

## What to look at in BRN-002

| Where | What |
|---|---|
| Frontmatter `upstream` | One `informed_by` record for each document read: BRN-001 version 1 and PRD-001 version 3 |
| Frontmatter `sources` | The two documents first, then the two datasets Dana named and her own statements, each as `"<kind>: <reference>"` |
| Section 1 | `Project kind: brownfield` as the first line, then *Existing product* with one row per document read |
| Section 2 | PRB-01 and PRB-03 cite a source at the end of `evidence`; PRB-02 has none and holds the marker |
| Section 3 | One row per `who` value, in the order the values first appear; unknown cells hold markers |
| Section 4 | IDEA-03 takes up BRN-001#IDEA-04, which BRN-001 had parked: a new idea with an item-level `upstream` link |
| Section 6, *Already covered* | Dana's suggestion of text reminders is not an idea: PRD-001#FR-003 covers it |
| Section 6, *Previously decided* | The deposit, rejected in BRN-001, was not proposed again; the waitlist, parked there, was offered and not taken up |
| Section 6, *Assumption updates* | BRN-001#ASM-01 moved from open to validated on the pilot's numbers, confirmed by Dana. BRN-001 itself is unchanged |
| Section 8 | One bullet for IDEA-01, the only idea in the first release, with a cited baseline |

BRN-001 and PRD-001 are byte for byte what the eval cases `brownfield-reads-documents` and
`brownfield-keeps-out-covered` seed.

## Checks

Each BRN prints `OK` under the skill's validator, from the repository root:

```bash
python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py docs/specs/brainstorm/BRN-002.md
```

The validator needs the path `docs/specs/brainstorm/BRN-NNN.md`, so copy the two BRNs into a scratch
project folder first. `src/tests/brainstorm/test_validate_brn.py` reads `BRN-002.md` from this folder as
its brownfield fixture.

The rows of *First release cut* and *Assumption risk ranking* follow the forms of
`docs/specs/brainstorming/README.md`, section 4 (C-05 and C-07). The build checks them against the
sentences `references/mvp-path.md` fixes, in the commit that adds it.
