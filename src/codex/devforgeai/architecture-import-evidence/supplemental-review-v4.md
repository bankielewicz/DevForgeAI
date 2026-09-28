# Supplemental Architecture Native Review — v4

## Binding and outcome

This independent review covers only
`architecture-import-evidence/supplemental-20260928-v4/`. The frozen plan is
SHA-256 `27cd7a8a88c11f415845b3341a879250c861dfc6bb634edcf655d8034d3d525f`;
the completed summary is
`68447e825601d65e2b7c3507d2a6d253f3ac95d18bb5ed04febc1b14926d530b`.
All four native probes used `codex-cli 0.158.0` and reported model
`gpt-6-astra`.

The helper summary is 4 PASS, 0 FAIL and 0 REVIEW_REQUIRED. Independent
inspection of the raw protocol, final messages and before/after manifests also
finds each probe PASS for its narrowly stated obligation. These are
supplemental results; they do not change the 14-case/84-trial source matrix.

The frozen 11-file candidate digest is
`002672e3f614de13d5268e6d34a71f95d52202f212f06d97de9388f9ceb3da92`.
The plan manifest, aggregate `candidate-after.json`, current candidate and
every per-probe runtime candidate agree byte for byte.

## Probe review

| Probe | Helper | Independent semantic result | Evidence |
|---|---|---|---|
| VER-12(c), draft PRD warning | PASS | PASS for the warning obligation | The compound command at raw protocol line 202 read PRD-001, then exited 2 when it checked absent ARCH/ADR directories. Commentary at line 313 identified `status: draft`, called the architecture a proposal and preceded the first file change at line 321. The final answer at line 656 repeated that PRD-001 and the architecture remained a proposal. The input PRD was unchanged; the only workspace change was a new `docs/specs/arch/ARCH-001.md` with SHA-256 `631d8b29e8b1ab8ec0df0b4c2fbdeb1e5bdf324a6068ccde12a1995a06ec7976`. |
| VER-12(e), invalid policy | PASS | PASS | The final answer at line 162 named `POL-001.md`, `SET-03`, `interview.max_calls`, value 50, the schema range 1–20 and ERR-02. It explicitly said nothing was written. Before and after manifests are identical. |
| VER-12(g), unknown PRD | PASS | PASS | The final answer at line 314 said `PRD-999.md` did not exist, listed available `PRD-001`, and said nothing was written. Before and after manifests are identical. |
| ERR-04, several matching ARCH documents | PASS | PASS | The turn ended `awaiting_input`. Raw protocol line 364 is a real `item/tool/requestUserInput` request with question ID `architecture_baseline`; it names both `ARCH-001` and `ARCH-002` as options. No answer was supplied and the workspace stayed byte-identical. |

The ERR-04 prompt intentionally omitted the source VER-07 instruction to
proceed without questions and explicitly allowed the agent to ask which
existing architecture to use. It therefore tests native question routing for
the several-matches branch. It does not replace or reinterpret the retained
source VER-07 result.

## Coverage and limits

This run directly covers only VER-12(c), VER-12(e), VER-12(g), and one
supplemental ERR-04 scenario. VER-12(a), (b), (d), (f), (h), (i), (j), and (k)
were not exercised by v4. Full manual VER-12 therefore remains NOT_RUN.

The draft-warning run did not establish general Architecture readiness. Its
artifact validation remained blocked because exact host model and session
identities were unavailable; its final answer withheld a validated readiness
handoff. That limitation does not affect the observed ordering and repetition
of the draft proposal warning.

VER-13 remains NOT_RUN: this run used an isolated runtime candidate and did not
install or inspect a deployed plugin. The supplemental PASS results do not
waive failed matrix cases, semantic-grader review, the per-case 0.8 threshold,
or any unrun mandatory/manual obligation.
