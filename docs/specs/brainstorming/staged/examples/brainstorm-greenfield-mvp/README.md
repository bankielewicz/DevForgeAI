# Example: a greenfield brainstorm on the MVP path

`BRN-001.md` is a complete, converged brainstorm of a product that does not exist yet: a lending service for the
tools of one street. It shows every shape the MVP path adds to a greenfield BRN, written the way the skill would
write them after the user confirmed everything. The names, numbers and quotes in it are invented for this
example. Copy it to `docs/specs/brainstorm/BRN-001.md` in a scratch project to validate it.

| Shape | Where in `BRN-001.md` |
|---|---|
| C-01, project kind | First line of section 1: `Project kind: greenfield` |
| C-03, target users | Section 3: one row for each distinct `who` of the three problems, in the order they first appear |
| C-04, convergence prose | Section 6, first paragraph: what was promoted, parked and rejected |
| C-05, first release cut | Section 6, `### First release cut`: confirmed, four rows, three `yes` |
| C-07, assumption risk ranking | Section 7, `### Assumption risk ranking`: four open assumptions, riskiest first |
| C-08, candidate success signals | Section 8: one bullet for each `yes` idea (IDEA-01, IDEA-04, IDEA-06) |
| C-09, sources | The `sources` frontmatter key: a note and an interview |

It shows no C-02 or C-06 table, because those belong to brownfield BRNs.

## What to look at

- **The ranking order.** ASM-02 is Fatal (all four ideas of the cut are in its list), so it is rank 1. ASM-01 and
  ASM-03 are both Serious with low confidence, so the lower number goes first. ASM-04 is Serious but its
  confidence is medium, so it is last.
- **The cut.** All four rows test ASM-02, rank 1. The cut holds at most three such ideas, sorted by score and
  then by ID: IDEA-01 (score 4), IDEA-04 and IDEA-06 (score 2, the lower ID first) are `yes`; IDEA-02 (score 1)
  is `no`, though it is promoted. The user confirmed the table as proposed, so the status line names them and the
  date.
- **The cheapest tests.** Each cell is a method word plus the first sentence of the assumption's `validation`:
  an interview for what owners and neighbours would say, a prototype (the spreadsheet) for what owners would do,
  and data (the group chat) for what the street's own notes already show.
- **Decisions.** Every disposition and `status: converged` are there because the user confirmed them. The
  skill would write the same BRN with `disposition: open` on every idea, `status: draft` and the line
  `First release cut: proposed, not confirmed` when nobody could confirm.

The framework is `diverge-converge`, so scores follow its formula: 2 × value − effort − risk with high = 3,
medium = 2 and low = 1. The other shapes do not depend on the framework.

The file passes `python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py` as it is today and
passes the checks added in `mvp-and-prototype-path.md` (BEH-33).
