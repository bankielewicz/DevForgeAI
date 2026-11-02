# Drafts review of SPEC-019 v1 at df1e844 (EVAL.md W5)

- Reviewer: an independent general-purpose subagent, briefed with the draft, ADR-008 v2, issue #137 and its two
  comments, the two #141 review reports whose notes the spec settles, Bryan's four answers of 2026-11-02, the mods
  reference lines §2 cites, ADR-006 D1, EVAL.md, REVIEW.md, mod-builder's SPEC template and UI-states checklist, and
  SPEC-017's boards convention. It edited nothing. Finished 2026-11-02 19:57 UTC.
- Reviewed text: the draft as committed in df1e844.
- Its verdict, in its words: "not yet. Fix seven blocking findings, then go to Bryan. The draft is well sourced. Every
  BEH traces to an ADR-008 decision, a review note or Bryan's words. The validator is clean, upstream versions match,
  EVAL.md's M, N, W and B4 rows match their VER items, and `dev-guard/` does not collide with the ui skill's `DSN-NNN`
  scan. Seven findings are real defects or contradictions with ADR-008."
- Passed, in its words: BEH-06 matches DM-01's key text; BEH-09, BEH-10 and DM-03 agree; BEH-16 and BEH-17 agree with
  M1 and M2; the `docs/specs/design/dev-guard/` folder is safe; `devforgeai/dev-guard/.gitignore` follows a real
  pattern; the lookup finds BEH-09; the diff lists only EVAL.md and SPEC-019.md; every API line §2 cites matches the
  reference.

## Findings (the reviewer's), with the author's answers

| # | Finding | Marked | Answer (the revision on the same branch) |
|---|---|---|---|
| 1 | The records commit is impossible, and ledger.jsonl and guard.json are writable under a ticket: BEH-02 let a permitting ticket write them, against ADR-008 D2 and Bryan's "no hand-written ledger.jsonl lines"; after close, R2 and R3 refused staging and committing the line | blocks | Fixed: the two files are refused whatever the ticket (BEH-01, BEH-02, BEH-03); `git add`, `git rm --cached` and `git commit` naming them or a report run without a ticket, and staged records never refuse a commit (BEH-03, BEH-04); `guard.json` is edited by a person outside Claude Code (VER-18). Reading (c) for Bryan |
| 2 | `agentId` has no source: ADR-008 P2 saw none on the Agent call | blocks | Fixed: `agentId` is optional in DM-01 and DM-03; where `subagent_type` and the spawned agent's id can be read is a build probe (§13; BEH-08) |
| 3 | B's re-derivation broke after a rebase, amend or squash, against ADR-008 D8 | blocks | Fixed: reports carry `commit:` and `tree:` lines; close and B match by `tree`; the line's `commit` is informational and resolved only when it exists; VER-10 and VER-16 add the rewrite case (DM-05, BEH-10, BEH-14) |
| 4 | R2's detection mode was undefined and the incident's heredoc class untested | blocks | Fixed: R2 searches the whole command text, heredoc bodies and quoted strings included, in every spelling of the path, with word normalisation as an extra (BEH-03); VER-05 and VER-15 add heredoc, quoted-path and variable cases |
| 5 | NotebookEdit's field is `notebook_path`, not `file_path` | blocks | Fixed (BEH-02, VER-01) |
| 6 | The allowlist grammar rejected CLAUDE.md's own commands and the spec-lookup agent's invocation; composite elements and backtracking were undefined | blocks | Fixed: entries are anchored regular expressions with four named expansions (DM-02); VER-15 runs every CLAUDE.md command and the agent's invocation through the matcher. The pytest entry stays as ADR-008 D2 lists it, though it names no protected path |
| 7 | The detached-HEAD key couldn't be looked up once HEAD moved | blocks | Fixed: the key uses the word `detached`, one ticket per detached checkout whatever its HEAD (DM-01, BEH-06); reading (a) restated |
| 8 | Platform facts stated beyond the reference: `$.fs` has no realpath or append; the `$.process.run` timeout option's name; `tool.check` for `Read` unprobed and recording an attempt; a `.catch` on the Read recorder denying reads; `cwd` and the scope's source unprobed | note | Accepted: realpath goes through `git rev-parse --show-toplevel` and `$.process.run` (BEH-03); appends are whole-file writes, the ledger under a close lock, the refusal log per session (BEH-05, BEH-10, DM-04); reads are recorded on `tool.call` after success; recording hooks never refuse (BEH-11); the timeout option's name, the Read event, the scope and the parallel reads are probes (§13) |
| 9 | `$.store` read-modify-write loses updates under parallel reads | note | Accepted: the ticket is several keys, one per read and per reviewer (DM-01, reading (i)); VER-15 tests three parallel reads |
| 10 | ERR-06 and VER-16 were stricter than ADR-008 D8: one bad historical line would fail every later PR | note | Accepted: B checks only the line whose `tree` is HEAD's; other lines are ignored (BEH-14, ERR-05, VER-16) |
| 11 | BEH-10's time ordering was invented; `minItems` didn't force one reviewer of each type or every required read; B never read guard.json | note | Accepted: every time lies between `openedAt` and `closedAt`, no order between the load and the reads (BEH-07, BEH-10); reviewers are exactly one of each type, reads cover every `requiredReads` path, B reads guard.json and ledger.schema.json (DM-03, BEH-14) |
| 12 | Clauses with no source: QR-03's numbers, IF-04's seven days, ERR-04, ERR-05, the widened R3 | note | Accepted: each is now a reading ((c), (l), (o), (p)); R3 is back to staged plugin files only (BEH-04) |
| 13 | Builder ambiguities: "the checkout" for each rule; the key lookup's cost; the allowlist's scope; "names the file"; which report counts; where B gets DM-03; the requirements wording; the marker's deselection; panes or text; the medium width; the marketplace entry | note | Accepted, each stated: the checkout is the one containing the path's real path, a ticket permits its own checkout only (BEH-01); the lookup is cached per working directory (BEH-06); the allowlist applies only to commands R2 would refuse (BEH-03); a read names the file by a resolving path (BEH-07); the newest report per tool (BEH-09); `ledger.schema.json` equal to DM-03 (BEH-14); the job installs the packages itself (IF-07, reading (m)); `addopts` deselects the marker (BEH-14); `/dev-guard` and `log` are panes, close not immediate (reading (k)); the medium width is drawn (BEH-16); no marketplace entry (BEH-13, reading (f)) |
| 14 | The origin allow-list can't tell a person from the model typing into a sibling pane | note | Accepted: the limit is stated (BEH-09, reading (n)) |
| 15 | EVAL.md A1 still cited A.7's `repoRoots` test; §9 and ERR-09 rested on a local handoff; Appendix A had one row per surface | note | Accepted: A1 reworded in EVAL.md; §9 and §11 say the account check is step 1 without citing the handoff; Appendix A has one row per board, twelve |
| 16 | Length: §2 restated D1 to D8, DM-03 repeated DM-01's sub-schemas, §3 duplicated BEH-13, §12 restated Bryan's answers | note | Accepted in part: §2 is one line per decision, §3's tree is a comment block, DM-01 is the store keys only, §12 folds the three answers into one row. The spec is 591 lines, since the twelve notes and the mockups each needed text of their own |

## For Bryan at approval

The readings (a) to (p) and the probes are in §13. The reviewer marked finding 1 as his call (the records-commit path,
reading (c)); the side agent's note of 2026-11-02 marks reading (b) (a `cat` of a guide counts as a read) the same way.
