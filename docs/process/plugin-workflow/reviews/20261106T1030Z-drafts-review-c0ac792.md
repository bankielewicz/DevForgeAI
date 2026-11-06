# Independent drafts review of SPEC-017 v5 at c0ac792, the refusal of shared canvases (REVIEW.md; EVAL.md Y1)

A fresh subagent of session 15e49669-ae2d-4c17-badc-913a843f5936, started 2026-11-06 10:30 UTC, given the change since
6ce238e, version 5 against version 4, Bryan's decisions of 2026-11-06 in his words, issue #153, REVIEW.md, EVAL.md,
the schema and the skill as built (SKL-013 v4), and not the drafting session's reasoning. It changed no file;
`pytest src/tests/ui` passed. Five blocks and six notes, shortened; each answer is the drafting session's, applied in
the commit that adds this report, with Bryan's answers of 2026-11-06 where the finding needed a decision.

Sound, per the reviewer: each decision implemented as Bryan worded it (the refusal of the user's canvas, unstated
sharing refused, the copy's question and title, a declined or unanswered copy refused, the stop at the last read, the
whole amend run refused, the live items recorded as not run); BEH-17, BEH-19, BEH-23, BEH-26, BEH-28 and BEH-29 free
of the report-only finding; no path left for a canvas that isn't private to receive or give boards apart from the
decided copy; QR-06 and §2 matching BEH-30; the test pins.

| # | Finding | Answer |
|---|---|---|
| B1 | §5's action list allows a publish only after briefs, `out_dir` only the DSN's folder or none, and omits the plain read; BEH-19's scratchpad clause omits the copy's files | **Fixed:** §5 lists the copy's publish (no briefs, on the user's yes), the plain read, and the scratchpad `out_dir` for the copy; BEH-19 lists the files BEH-30's reads save |
| B2 | A copy in an amend run with no board changed ends at ERR-17, writes nothing, and the next run copies again | **Fixed:** replacing the DSN's canvas with a copy counts as a change (BEH-10, ERR-17, BEH-30), so the DSN is amended |
| B3 | BEH-30 offers the copy for unstated sharing, where Bryan said "Refuse it too", and its question would claim "others can open it" | **Fixed:** the copy only when a read states the canvas isn't private; unstated sharing is ERR-25 |
| B4 | After a stop at read (c), a later create run without a URL records the placed copy as it is | **Decided by Bryan:** "Name it; may be recorded (Recommended)": ERR-25 names the folder, says a later import replaces it once the canvas is private and that a later create run without a URL would record it only as an unchecked copy (null canvas, a marker, no approval until an import); the amend case is stated |
| B5 | §12 still rejects "stop the run"; readings (bd), (bh), (bk) unmarked; §9's next-version row still lists VER-50 (a) as open; a dangling report path | **Fixed:** §12's row is the replaced alternative; (bd) and (bk) marked superseded and (bh) kept for an unreachable canvas, (bs); the next-version row says version 5 settles it; this report's path |
| N1 | A view-only canvas would get the copy offer and fail after the yes | **Fixed:** BEH-30 reads `canvas.json` before asking; a summary (view only) or a failed read is ERR-20 before any question |
| N2 | The copy isn't checked against the source; ERR-12 and ERR-06 apply only after publishing | **Fixed:** ERR-12 and ERR-06 checked before the question; the import's digests must equal the source's (ERR-21 otherwise) |
| N3 | ERR-23's "show the briefs" and "never publish to a new URL"; a copy that reads not private; BEH-25's read after the copy | **Fixed:** briefs "when the run has any"; the copy is not a canvas published to a new URL; a copy found not private is ERR-25 and stays (the skill deletes nothing); the copy's read (e) counts as the import's read (a) |
| N4 | VER-50's waiver has no end; the whole offer, not only the copy, needs another account | **Decided by Bryan:** "Next version or 2026-12-31 (Recommended)"; VER-50 says what is checked only by the structure tests; (f)'s whole offer is not run |
| N5 | A new canvas is never read for sharing | **Decided by Bryan:** "Yes, read it (Recommended)": read (e) just after a publish makes a canvas; one not private stops the run; the canvas report states it (closes #153 item 23); VER-50 (h) |
| N6 | Two change rows for version 5 plus Bryan's approval row will make three | **Not changed:** the second row records the redesign separately from the first draft, which is clearer than rewriting it; G4 needs the change rows and the approval row, both present then |
