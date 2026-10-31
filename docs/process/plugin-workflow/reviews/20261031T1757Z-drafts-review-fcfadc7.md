# Drafts review of ADR-008 at fcfadc7 (EVAL.md ADR4)

- Reviewer: an independent general-purpose subagent, briefed with the ADR, issue #137, ADR-006, ADR-003 A2 to A4 and
  A8, EVAL.md, REVIEW.md, the mods reference and overview it cites, and the mods proposal §5. It edited nothing.
  Finished 2026-10-31 17:57 UTC.
- Reviewed text: the draft as committed in fcfadc7. The probe results (9f7b8a9) landed while it ran.
- Its verdict, in its words: "well-grounded in the API and honest about what it leaves open, and the citations
  survive checking. It should not be accepted yet". The reasons it gave: close and the commit check don't work in the
  order EVAL.md and REVIEW.md prescribe, and the rules file, the mode and the scope aren't protected or located.

## Findings (the reviewer's), with routing

| # | Finding | Marked | Routing |
|---|---|---|---|
| 1 | D6's close needs reports for HEAD, but the reports, and the ledger line after the close, are committed later, so HEAD moves. EVAL.md's carry-forward covers `reviews/` and §9 rows, not `ledger.jsonl` | blocks | See the author's answers below the table |
| 2 | D8: hashes move on rebase, amend or squash. Appending hashes needs a post-call event. B makes `pytest src/tests` fail through an open iteration. The ledger and reports can be written by hand. A shallow CI checkout breaks `merge-base`, and the job gates nothing unless it is a required check | blocks | |
| 3 | D5(b): an absent `guard.json` makes the guard inert, and the guarded model can edit or delete it. Missing and invalid aren't told apart. Branches older than the file, parent-directory and `--add-dir` sessions are unguarded. "Inside the repository" is undefined without `repoRoots`. The ticket key still holds a machine path | blocks | |
| 4 | D4's mode has no home in D5. It conflicts with ADR-006's one mode key (`progress.mode`) and its `observe` default. Wherever it lives, the model could set it. Recovery from a crashed guard is unspecified | blocks | |
| 5 | D3 defers the amendment to ADR-006 D1, which ADR-006 v2 itself didn't do. The frontmatter says it "answers" ADR-006's out-of-scope line, which asks for policy keys and names A1's rules. (b) is close to ADR-006's rejected option 2 | blocks | |
| 6 | Attribution: D1's "A1 out of scope" is stated as decided while open question 8 recommends it. "No ledger line by hand" and the `<UTC>-<tool>-<hash>` form lack Bryan's words. "Item 4" is cited from a local plan. "Probes before approval" is stricter than #137 | blocks | |
| 7 | "Fails closed" has holes: a `.catch` gets 1 s, and a throwing handler skips the hook. A module that fails to load leaves no guard. Cloud sessions and a project-level `disableAllHooks` are missing from D7 | note | |
| 8 | R2 and R3 are best effort. After a close, R2 would refuse `claude plugin validate` and `test`, the deploy and PR bodies naming the path. R3 misses `commit -a`, `commit <path>`, cherry-pick and merge | note | |
| 9 | Missing questions: ticket lifetime and expiry, carrying `reads` to the next ticket, cleaning `$.store`, minimum Claude Code versions, `$.session.cwd()` after `cd`, ledger merge conflicts, where `scope` (the args) comes from, and the ADR-008 number ADR-007 named | note | |
| 10 | Q7 conflicts with A.2's `reads` (only `docs/research/Claude/`). Q6's SPEC.md overlaps with Q4's SPEC-019. The ADR leans on #137's text. EVAL.md ADR1 says "Change Log row" where ADRs keep a Status history. EVAL P5 assumes A.1. ADR4 names no report location | note | |

## Author's answers

Recorded in ADR-008's revision on the same branch, in its last Status history row:
- **1 and 2:** closing and the commit check bind to the plugin's subtree hash, so rebases and the records commit
  don't move it (checked: `1744e6c` on a docs commit, its parent and main). B is skipped by default and runs in CI with
  `fetch-depth: 0`, and it validates each ledger line. A required check is an Owner's setting.
- **3:** the path anchor (the plugin's own manifest names `devforgeai`) replaces scope-by-file. `guard.json` holds
  only `requiredReads`, is protected, and refuses when missing or invalid.
- **4:** no mode. Recovery from a broken guard is a person's act (`--safe-mode`, or drop the folder from
  `CLAUDE_CODE_PLUGIN_DIRS`).
- **5:** the departure from ADR-006's out-of-scope line is stated. Amending ADR-006 now or at its next change is
  Bryan's question 2: amending now relinks SPEC-012, SPEC-013 and SPEC-016, each a version bump.
- **6:** Bryan's words are quoted for the ledger, the report path, item 4 and the generator rule. A1's scope is moved
  into question 1. The probes ran earlier than #137 asked, as a departure.
- **7 to 9:** settled in D2, D6 and D7 as described.
- **10:** the questions are merged into four. EVAL.md's wording goes to #140.

The revision changed the design (the path anchor, the protected rules file, the subtree hash, a CI-only check). Its
second look was PR #141's close review (`20261031T1841Z-code-review-5dee512.md`), which found three D8 defects that
were fixed before the merge.
