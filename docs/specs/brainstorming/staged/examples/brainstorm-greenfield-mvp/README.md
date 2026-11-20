# Example: a greenfield brainstorm with a confirmed first release cut

`BRN-001.md` is a finished brainstorm (BRN) for a product that does not exist yet: a booking service for a
mobile bike repair van. It is a new-shape BRN: it holds every fixed shape a greenfield brainstorm has, and none
of the brownfield ones.

To validate it, copy it to a folder that ends in `docs/specs/brainstorm/` (the validator checks the path):

```bash
mkdir -p tmp/example/docs/specs/brainstorm
cp src/staging/examples/brainstorm-greenfield-mvp/BRN-001.md tmp/example/docs/specs/brainstorm/
python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py tmp/example/docs/specs/brainstorm/BRN-001.md
```

`src/tests/brainstorm/test_validate_brn.py` reads this file: its cases for the first release cut and the
assumption risk ranking are edits of it.

## What it shows

| Shape | Where | In this example |
|---|---|---|
| Project kind | Section 1, first line | `Project kind: greenfield` |
| Sources | Frontmatter `sources` | One `note` entry (the owner's own statements) and one `data` entry; every cited fact ends with one of them in parentheses |
| Target users | Section 3 | One row for each `who` of the problems, in the order they first appear |
| First release cut | Section 6 | Confirmed, with the date and no name; two of four promoted ideas are in |
| Assumption risk ranking | Section 7 | Four open assumptions, one Fatal, three Serious |
| Candidate success signals | Section 8 | One bullet for each idea in the first release, one baseline known, one not |

The request named no framework and did not ask what to build first, so the framework is `diverge-converge`.
Three problems, seven ideas (four promoted, one parked, two rejected), four assumptions. `status: converged`:
the user confirmed the dispositions, the convergence and the cut.

## How the two tables follow from the rule

The cut rows are the four promoted ideas: IDEA-01, IDEA-02, IDEA-03 and IDEA-05.

| Assumption | Cut rows it stops | Class | Support in `sources` | Confidence | Risk points |
|---|---|---|---|---|---|
| ASM-01 commuters book online | IDEA-01, IDEA-02 | Serious (2 of 4) | none | low | 2 × 3 = 6 |
| ASM-02 commuters can reach a stop | IDEA-01, IDEA-03 | Serious (2 of 4) | none | low | 2 × 3 = 6 |
| ASM-03 commuters can name the fault | IDEA-02 | Serious (1 of 4) | the `note` entry | medium | 2 × 2 = 4 |
| ASM-04 commuters pay at the van | all four | Fatal (4 of 4) | the `data` entry | high | 3 × 1 = 3 |

ASM-04 would stop everything, but the job log already shows paid jobs at the van, so it is the least urgent to
test and ranks last. ASM-01 and ASM-02 tie on points, class, confidence and the number of rows they stop; the
lower ID comes first.

The cut then takes one idea for each assumption ranked 1 to 3:

1. ASM-01 stops IDEA-01 (score 3) and IDEA-02 (score 2): IDEA-01 is in, `Tests ASM-01, ranked 1.`
2. ASM-02 stops IDEA-01, which is already in: nothing is added.
3. ASM-03 stops only IDEA-02: it is in, `Tests ASM-03, ranked 3.` IDEA-02 needs IDEA-01, which is already in.
4. IDEA-03 depends on ASM-02, which IDEA-01 already tests: out. IDEA-05 depends only on ASM-04, ranked 4: out,
   `Tests no assumption ranked 1 to 3.`

Each `Cheapest test` cell is the first sentence of the assumption's `validation`, with its kind: "pilot" makes
ASM-01's a `Prototype`, "Ask" makes ASM-03's an `Interview`, and the two that read the job log are `Data`.

The user chose `Accept as proposed` for the cut after accepting every disposition, so the status line reads
`First release cut: confirmed on 2026-11-18`. Had nobody confirmed, the same table would stand
under `First release cut: proposed, not confirmed`, with every idea `disposition: open` and `status: draft`.
