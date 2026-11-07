commit: c26a0f868965f98b7ddb95e7da0967f3ed8c6761
tree: 1e15dcfc58464c94945cb8572cdcc4ce2a72dcfc

# skill-reviewer on the #153 refusal build (ui, SKL-013 v5)

The same rounds as the plugin-validator report of this commit. Each pass checked the skill against SPEC-017 v5 and
Anthropic's skill-authoring guidance; the first draft's rounds are in `20261106T0501Z-skill-reviewer-02593b2.md`.

- **160c916, the refusal: FAIL, 3 blocks.** No wording let a shared canvas through; the failures ran the other way.
  (1) The copy could be stopped by its own reads of the source (fixed in the spec, 78ef2bf, and in 780e20a). (2) An
  amend run after a copy could record the copy's URL with the source's version and digests (78ef2bf, 780e20a: the
  yes to the copy also answers the import question). (3) VER-50 (h) wanted a new canvas's report to say it is
  private, against (b) (78ef2bf). ERR-25's message gave no command to run again (780e20a). SKILL.md 366 lines,
  references one level deep, each over 100 lines with a Contents list.
- **780e20a: FAIL, 2 blocks, both gaps in the spec that the skill copied.** (B1) After a stop at read (e), ERR-25's
  rerun line named the empty canvas just made, and the briefs were lost (ac876d8, ec421ba). (B2) A copy followed by
  "Draw it now" always ended at ERR-21 (Bryan, 2026-11-06: "Check only right after (Recommended)"; ac876d8,
  ec421ba).
- **ec421ba: PASS, no blocks, 7 notes,** on #153 (items 38 to 44); item 38, ERR-25's amend rerun line, was fixed in
  d13db23 after Codex flagged it too.
- **a97a928: PASS, no blocks.** The copy's version check is correct and complete against BEH-30, BEH-25 and ERR-21:
  no path publishes two source versions, asks twice or stops a valid run. Notes: which digests the import's match
  check uses after a re-read; the re-read's board list and order; ERR-21's wording for a copy; output-rules.md's
  scratchpad list; step 2's heading.
- **d13db23: PASS, no blocks.** ERR-25's lines walked to each rerun. Note: BEH-28's resume line had the same gap
  after "Iterate later" on a canvas the request named (Bryan, 2026-11-06: "Fix it now, one rule (Recommended)";
  fixed in d9cc7cc).
- **d9cc7cc: FAIL, 1 block.** ERR-22 said only "run the skill again", so an amend run that copied a canvas and then
  declined the addition reran on the source and offered a second copy; ERR-13's line didn't say which canvas (the
  line defined once in e71a9d0 and b095314).
- **b095314: PASS, no blocks.** Every case walked to its rerun. Notes: "copied" readable as the source; a copy of
  the DSN's own canvas got its URL, which a rerun counts as a change; restatements beside the pointers; the stray
  blank line in Contents (all fixed in c26a0f8).
- **c26a0f8, the last plugin commit: PASS, no blocks.** Checked by walking each case to its rerun (a create run that
  made or copied a canvas; an amend run on the DSN's canvas, on a canvas the request named, agreed or declined, and
  after a copy, the DSN's own canvas included, through ERR-13, ERR-21, ERR-22 and ERR-25; a stop at read (e); a run
  with no canvas; "proceed without questions"): every line is right, and a model reading a pointer and the section
  can build it. Notes, on #153 under the stopping rule: "The DSN holds its canvas until an import" should say until
  an amend run writes it (the spec's words too); which canvas stopped the run when ERR-21 comes from the copy's
  match check; "didn't decline" names no question; ERR-25's message after a stop at read (e) tells the user to make
  private a canvas the rerun won't use; the canvas report under "proceed without questions" can't be reached; ERR-19
  gives no line.

`SKILL.md` has 367 lines at c26a0f8, within the 500-line limit.
