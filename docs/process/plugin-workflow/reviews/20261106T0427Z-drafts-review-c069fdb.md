# Independent drafts review of SPEC-017 v5 at c069fdb (REVIEW.md; EVAL.md Y1)

A fresh subagent of session 15e49669-ae2d-4c17-badc-913a843f5936, started 2026-11-06 04:27 UTC, given the spec's
diff, issue #153 with its comments, Bryan's scope for version 5 in his words, REVIEW.md, EVAL.md, the skill as it
stands (SKL-013 v4) and the schema, and not the drafting session's reasoning. It changed no file; `pytest src/tests/ui`
passed. Five blocks and seven notes. The findings are the reviewer's, shortened; each answer is the drafting session's,
applied in the commit that adds this report.

Sound, per the reviewer: the frontmatter and the Change Log row, the approval row left for Bryan; SPEC-009's link,
CLAUDE.md's row and the test pins (`SPEC_VERSION` 5 in review, `IMPLEMENTS` 4); no mid-run warning, "once in the run" or
"reply text" requirement left; items 3, 7, 20, 21 and 29 fixed as #153 asks; the design for item 1 and the High item;
VER-50 (a), (c) and (f) checkable from a trace and a report; (bn) flagged as new behaviour for Bryan.

| # | Finding | Answer |
|---|---|---|
| B1 | BEH-27 still says BEH-23 confirms "with the same question", which would bring back "Create the canvas" | **Fixed:** "with its question for an addition" |
| B2 | BEH-23's addition question has no title, and only its first option is named | **Fixed:** "Add the boards made from these briefs to the canvas <URL>?" with 'Add to the canvas' (Recommended), 'Change a brief', 'Change the grouping' and 'Not now', the last three as for a new canvas (ERR-22), asked again after a redraft |
| B3 | QR-06 and §2 still say every send is "a private artifact" on the user's account | **Fixed:** both split a new canvas (private, the user's account) from an addition (the canvas it is added to, whose owner and sharing the question states) |
| B4 | Read (d) has no failure handling; a canvas changed since BEH-27's read of canvas.json could lose boards on the update | **Fixed:** read (d) finding no canvas, failing or returning a summary is ERR-23, nothing published. **Not changed:** the stale canvas.json is version 2's behaviour, outside Bryan's scope ("Defects, not redesigns" named #153's items); filed on #153 and listed in §13 as not in version 5 |
| B5 | VER-50 (b) ("says nothing about sharing") conflicts with (g) on a private canvas; BEH-29 omits the user's private canvas from what the question says | **Fixed:** (b) covers the replies and the report, not the question; BEH-29 gives the question's four cases (the user's private canvas, the user's canvas not private, sharing not read, another person's canvas) |
| N1 | BEH-29's reads, VER-50's items and §13's readings all use letters; EVAL.md Y4 requires VER-50 (d), which VER-50 lets be "not reachable" | **Fixed:** Y4 requires (a), (b), (c) and (g), and lets (d), (e) and (f) be recorded as not reachable. **Not changed:** the letters of BEH-29's reads, which version 4 used and the skill cites |
| N2 | Read (d) is made each time the question is asked; item 1's gap between the read and the answer remains | **Fixed:** reading (bn) says "each time the question is asked", that a change after the read isn't shown, and that a refused publish's retry doesn't ask again |
| N3 | ERR-25's "no earlier text is a warning" is untrue after an addition question; "says it too"; does the question name the Share menu? | **Fixed:** ERR-25 says never claim a warning at a read, lets the finding say the question stated the sharing, and drops "too"; BEH-29 says the question doesn't name the Share menu, which the report does |
| N4 | BEH-28's canvas report doesn't say where the sharing findings go | **Fixed:** after the briefs, before the Next step paragraph |
| N5 | Item 5's live defect was the version check's read with paths; VER-50 (c) checks only plain reads | **Fixed:** (c) also checks that read |
| N6 | Items 19, 21, 25 to 27 aren't named; ERR-25's "the report the run ends with" is another term; §11 and §13 half-claim item 24 | **Fixed:** reading (br) names them as build wording (26 needs nothing); ERR-25 uses BEH-17's "findings of the final reply"; §11 no longer claims item 24, which stays on #153 |
| N7 | The report isn't committed; §9's next-version row reads as all undecided; `generated_by.session`; "The canvas stays private" | **Fixed:** this report; the row names version 5; the session is this one, and `approved_by` and `approved_on` are removed while the version is in review, as the version 3 draft did; "A new canvas stays private" |
