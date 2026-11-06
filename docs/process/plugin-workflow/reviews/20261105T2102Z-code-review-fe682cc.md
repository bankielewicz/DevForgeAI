commit: fe682cc (PR #152's head; last plugin commit 1a14f85)

# Close review of PR #152 at fe682cc (`/code-review 152`, xhigh)

Run 2026-11-05 21:02 UTC by a forked `code-review` agent of session 15e49669-ae2d-4c17-badc-913a843f5936, with
REVIEW.md and EVAL.md. `src/tests/ui` and `test_adapter_structure.py` passed (389), the full `src/tests` exited 0,
`git diff --check` was clean, and Codex had no findings. 15 findings; 11 were already on #153 or decided by Bryan,
and the records ones are fixed in the commit after fe682cc.

1. `canvas.md:170`: ERR-25's warning isn't given as reply text, and a report can claim one (check 1). Waived by
   Bryan ("One more round, then waive (Recommended)"; "One more small edit (Recommended)"); on #153.
2. `canvas.md:85`: the recommended option on an addition is "Create the canvas" (check 1; SPEC-017 BEH-23's
   wording since v2). Bryan: "#153, marked high (Recommended)".
3. `canvas.md:171`: the warning counts once per run, not per canvas. #153, item 3.
4. `canvas.md:78`: the question's sharing isn't refreshed, and a canvas another person owns gets "private artifact"
   on the user's account. #153, items 1 and 2.
5. `canvas.md:62`: a create run that ends after publishing says "private" and then "could not be read". Bryan's
   "Follow the spec (Recommended)"; the effect is noted on #153.
6. `canvas.md:258`: ERR-20 for "artifact not found" doesn't give the "signed in to the account that owns it" advice
   this PR added to ERR-23 (check 1). A note: filed in #153 under the PR's stopping rule.
7. `SPEC-017.md:830`: the Build row said both reviewers passed every commit with no block; skill-reviewer blocked
   4a67876 and 8f63b26 (check 6). Fixed: the row names both blocks and says each was answered in the next round.
8. `20261105T1536Z-plugin-validator-3489054.md:7`: the invocation times were approximate and came after their
   commits (check 3). Fixed: both validator reports give each round's `/plugin-dev:create-plugin` time from the
   session transcript (22:29 to 20:13 UTC, each 1 to 3 minutes before its first commit), and so does #152's G5 table.
9. `SPEC-017.md:836`: the Version 3 row still said "Behavioural: NOT_RUN" (check 6). Fixed: it points to SKL-013
   v4's rows.
10. `canvas.md:39`: up to four plain reads in an amend run (efficiency). #153, item 4.
11. `SKILL.md:110`: ERR-25's rule restated in about ten places (simplification). On #153.
12. `canvas.md:183`: "start over once" and step 0. Bryan: "File in #153 and merge (Recommended)".
13. `boards.md:110`: "step 1's read". Bryan: "File in #153 and merge (Recommended)".
14. `CHANGELOG.md:12`: a second "### Changed" under Unreleased (Keep a Changelog). Fixed: the entry joins the
    existing "### Changed". The second "### Fixed" at the top comes from #150 (#135's entry), not this PR.
15. `test_structure.py:272`: repeated flatten-and-find code, heading-only checks, guards that could ban later
    wording (check 7). On #153.
