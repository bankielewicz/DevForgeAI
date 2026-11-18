# Prototypes

**Status:** scratch prototypes written by the drafting agents on 2026-11-18 to test the specs. They are not the
build, are not specified behaviour, and are not run by any test of this repository. Where a prototype and a
document of this folder disagree, the document is right.

| File | What it is | Checked here |
|---|---|---|
| `validate_brn_iv_bv.py` | Today's `validate_brn.py` plus the checks IV-01 to IV-12 ([intake-and-evidence.md](../../intake-and-evidence.md)) and BV-01 to BV-14 ([brownfield-iteration.md](../../brownfield-iteration.md)). BV-02 is gated by the four brownfield headings and the kind gate needs `project kind:` (with the colon) | Run 2026-11-18 after the review's last edits: prints `OK` for the staged example BRNs (brownfield `BRN-001` and `BRN-002`, greenfield `BRN-001`), under `python3` and `python3 -S` |
| `validate_brn_mv.py` | The checks MV-01 to MV-30 ([mvp-and-prototype-path.md](../../mvp-and-prototype-path.md)) alone. Its fence handling and kind gate now match the README (every fenced block; `project kind:`) | Run 2026-11-18 after the review's last edits: prints `OK` for the greenfield `BRN-001` and brownfield `BRN-002` examples |
| `mutate_brn_002.py` | 57 variants of the brownfield example (the original 54, with the source and evidence variants adapted to the reconciled example, plus the BV-02 gate and the `Project kinds vary` gate cases), run against `validate_brn_iv_bv.py` and the current `BRN-002.md`. It finds both by paths relative to the script and copies each variant to a temp folder ending `docs/specs/brainstorm/` | Run 2026-11-18 after the review's last edits: 57 of 57 give the expected verdict and message, and the same verdict with `python3 -S` |
| `test_structure.py` | A draft of `src/tests/brainstorm/test_structure.py` (framework-catalog.md, VER-23) | Its author ran it; red on today's source, green with the staged files |
| `SKILL.after-all-builds.md` | SKILL.md as it reads after every SKILL.md edit of the five documents is applied in build order (362 lines; the eight checklist lines unchanged) | Made by the review's simulation; a reading aid, not a file to copy |

To validate an example with today's validator, copy it to a path that ends `docs/specs/brainstorm/BRN-NNN.md`
(the validator checks the folder and the file name) and run
`python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py <path>`.
