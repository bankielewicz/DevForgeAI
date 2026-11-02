# Close review of PR #145 at 6d1ecdb, round 1 (REVIEW.md; EVAL.md G9)

- Review: `/code-review medium 145`, run from the branch's worktree on 6d1ecdb (SPEC-019 version 1, approved by Bryan on
  2026-11-02, "Approve as drafted (Recommended)"), finished 2026-11-02 20:20 UTC.
- Its verdict: ten findings, eight of them design defects a builder would hit, two record items. None is on REVIEW.md's
  "What blocks the merge" list as such, but two are defects the build would ship (the `-c` flag bypass under the pytest
  allow entry; a permit that can't open when the guides are read before the load), so the author took them to Bryan
  through the advisor (Bryan, 2026-11-02: "prior to modifying it, run it by /advisor for guidance"), and Bryan chose
  "Version 2 in this PR (Recommended)". The advisor revised two of the proposed fixes before he saw them (findings 1
  and 4 below).
- What blocks the merge: nothing after version 2. The stop rule from here (SPEC-019 §13): a further design finding
  becomes version 3 at the build, after the probes run.

## Findings (the reviewer's), with routing

| # | Finding | Where | Routing |
|---|---|---|---|
| 1 | BEH-07 said no order between the create-plugin load and the reads, but a read is recorded in a ticket's keys and a ticket opens only at the load, so reads made first never count | SPEC-019.md:244 | Fixed in v2 as the advisor revised: a read counts only while the ticket is open (ADR-008 D6, "in this iteration"); a read made before the load is repeated, and the refusal's remedy says so; the free order is between skill-development's load and the reads only. The author's first proposal, "reads since the previous close count", would have departed from D6 and was dropped |
| 2 | QR-03 promised no process call for R1 and R2, while BEH-03 resolved symlinks through `$.process.run` and a new file has no realpath | :342 | Fixed in v2: lexical normalisation on the hot path, one cached realpath per directory on a miss, the nearest existing parent for a new file, the anchor check cached per folder; QR-03 reworded |
| 3 | A worktree under the main checkout is contained by both top levels; the ticket keyed on the session's working directory | :225 | Fixed in v2: the innermost top level wins; a ticket permits its own checkout only; an iteration on a worktree is loaded from a session whose working directory is the worktree, and a session in the main checkout editing it by absolute path is refused with that remedy (reading (r); VER-07). A change to how sessions have worked, shown to Bryan |
| 4 | BEH-10's close lock needed an atomic primitive `$.store` doesn't have, and no stale-lock expiry | :252 | Fixed in v2 as the advisor revised: no lock; read, append, write, re-read, retry when the line isn't present; the residual race stated (reading (s)). The author's first proposal, a lock with a 60 s takeover, was dropped |
| 5 | VER-15's "every command in CLAUDE.md's Commands section" couldn't pass: `diff -rq … src/claude/DevForgeAI …` had no entry, and some commands name no plugin path | :460 | Fixed in v2: VER-15 lists the exact commands; a "deploy diff" allow entry added (DM-02) |
| 6 | The `F` wildcard let `python3 -c <code> -m pytest src/tests` run under the pytest entry | :154 | Fixed in v2: `F` expands only to each entry's listed flag forms, each value holding no protected-path form; `V` is `PYTHONDONTWRITEBYTECODE=1` only (reading (t)); VER-15 adds the `-c` case |
| 7 | The records-commit exception could be satisfied by a compound or multi-path command | :233 | Fixed in v2: one git invocation, no shell operator, every path one of ledger.jsonl, guard.json or a reviews/ report (BEH-03); VER-15 adds a `git add` naming the ledger and a plugin file |
| 8 | Store keys joined the path and the branch with `/`, so slashed branch names could collide or break prefix deletes | :242 | Fixed in v2: the key is a 16-hex digest of the top level and the branch, the plain values inside the ticket (DM-01, DM-03, BEH-06; reading (q)) |
| 9 | Change Log row 1 cited ERR-01 to ERR-09 while the spec has eight; three rows at version 1 | :590 | Fixed: row 1 says "as drafted, merged to eight in the revision"; the three version-1 rows are the draft, the review fixes before approval and the approval, which is this repository's pattern |
| 10 | EVAL.md W2 cited an uncommitted script and a coverage claim no check enforced | EVAL.md:99 | Fixed: `src/tests/process/test_spec_019_structure.py`, self-contained, pins SPEC-019's version and status, checks the schema, the coverage and the JSON blocks; seen failing on the version-1 pin before the v2 edits; W2 cites it |

## Summary

Version 2 carries the ten fixes with Bryan's approval row. Round 2 of the close review runs on the final commit; its
report is committed next to this one. Codex's pass is requested on that commit.
