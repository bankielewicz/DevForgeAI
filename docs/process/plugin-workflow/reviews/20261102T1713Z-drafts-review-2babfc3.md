# Drafts review of SPEC-002 v6 at 2babfc3 (EVAL.md V5)

- Reviewer: an independent general-purpose subagent, briefed with the draft, SPEC-002 v5 on main, issues #142 and
  #143, the approved plan (`tmp/plans/2026-11-02-interview-at-scale-and-improve.md`, local), the prd skill's
  `SKILL.md` and `references/interview.md`, ADR-003 A3 to A5, SPEC-011 BEH-13, SPEC-001 BEH-14, REVIEW.md, EVAL.md's V
  rows, the structure test and the new runbook. It edited nothing. Finished 2026-11-02 17:13 UTC.
- Reviewed text: the draft as committed in 2babfc3.
- Its verdict, in its words: "The structure is sound and the mechanics mostly hold, but ten items need a text fix or a
  decision before approval. Three need Bryan's decision, not just an edit: what 'None of these' records, BEH-19's
  source precedence, and the readings missing from section 13. The most serious defect is that the reuse and count
  lines are placed in text that AskUserQuestion hides from the user."
- Passed, in its words: the structure test; `find_spec.py` finds BEH-25 and VER-48 at version 6; no path under
  `src/claude/DevForgeAI` changed and `provenance.yaml` still says version 5; the description line is unchanged; the
  link versions match the files; the approval fields are cleared; the four relinks match the v5 precedent; the SPEC-003
  and SPEC-011 §13 rows are accurate and record-only; the runbook maps onto VER-46 to VER-48; VER-07, VER-35 and
  VER-36 still pass. Not checked by it: PRD-001 NFR-001 to NFR-003 unchanged since version 11 (the author checked it
  with `git show f282281:docs/specs/prd/PRD-001.md`: identical).

## Findings (the reviewer's), with the author's answers

Each answer names what the revision on the same branch changed, or routes the finding to Bryan's approval question.

| # | Finding | Where | Marked | Answer |
|---|---|---|---|---|
| 1 | Reuse and count lines are 'written in the reply before the first call'. Text before an AskUserQuestion call is not shown, so a live user never sees the budget or the reused values | SPEC-002:180-193, 328, 331; runbook:47 | blocks | Fixed: the two lines also go in the first question's text (§4, BEH-19, BEH-20, BEH-21); the reply copy stays for evals and the Change Log row; VER-46 (f) and runbook M1 (a) check the question |
| 2 | BEH-19 reads sources in order, stopping at the first, then asks on a conflict that can never surface | :328 | blocks | Fixed: every source is read; a value is reused only when the sources agree; an answer in the run supersedes the rest; among the request, the PRD and the BRN none outranks another, so a disagreement is asked. Listed as reading (h) for Bryan |
| 3 | BEH-19 drops 'the PRD being extended'; BEH-05's skip clause has the same gap | :286, 328 | blocks | Fixed: both name the PRD being extended or continued; an extension's existing items are never asked again |
| 4 | BEH-25 removes markers by BEH-03's rules though it adds no item; setting operating_context changes the required categories; BEH-10 and BEH-17 R5 are silent for a continue | :346, 280, 174-178, 331 | blocks | Fixed by narrowing: a continue settles the four kinds of open decision only, asks no quality category, adds no item or link, keeps the frontmatter as an extension does, and rewrites or removes the unknown-context markers when it sets the operating context; §4's open decisions are the four kinds (markers are open questions); §12 records the rejected alternative. Reading (e) for Bryan |
| 5 | BEH-26 says a free-text answer ends the menu; BEH-22 shows the table again with options after typed text | :349, 337, 874, 896; runbook:50, 70 | blocks | Fixed: the revised table comes back as plain text, accepted by typing (BEH-22, VER-46 (d), runbook M1 (d)); BEH-26 names it |
| 6 | BEH-24 is unclear on whether the other rounds run before the PRD and the file are written | :343, 334, 1080 | blocks | Fixed: the review file replaces the requirements round only; the other rounds run first (BEH-21, BEH-24); reading (d) |
| 7 | BEH-26 lists 'None of these' as an explicit none, but BEH-22 leaves the group null, indistinguishable from no answer | :349, 337 | blocks | Fixed with the reviewer's second option: the group is recorded as 'Not must now: <IDs>' in the reply and the Change Log row (§4, BEH-22); an answer with no tick decides nothing. Reading (l) for Bryan, who may prefer the first option |
| 8 | Count arithmetic: §4's example prints 12 where 13 is right; the mode question is circular at the boundary; 'modes that fit' is undefined and no cost formula is given | :186, 331, 334, 409, 1075 | blocks | Fixed: the estimate is compared without the mode question and restated with it; the calls available are defined; each mode's cost is given and a mode that doesn't fit is offered with what stays null; §4's example says 12 calls (47 questions) with the mode question joining the restatement |
| 9 | Readings missing from §13 that EVAL.md V1 requires; BEH-01 not in the Change Log's items | :1006-1018, 328-346, 409 | blocks | Fixed: readings (h) to (m) added; BEH-01's text now names continuable PRDs and the second Change Log row lists it |
| 10 | VER-39 says 'proceed without questions', so it can't show that a stage isn't asked again | :808 | blocks | Fixed: VER-49 added, a case with questions whose plain-text questions omit the stage, the context and the release name; VER-39 keeps the file check |
| 11 | Appendix B: 13 ticked of 36 leaves 23 open, not 22; NFR-003 at release current with priority null can't arise | :1085-1094 | note | Fixed: 23 rows, 21 later, NFR-003 at null/null |
| 12 | Appendix A prints '0 NFR' though the ClinicCore constraint is drafted; Appendix B's 'up to 3' counts the constraint twice | :1041, 1075 | note | Fixed: 4 requirements (3 FR, 1 NFR), up to 7; Appendix B up to 2 |
| 13 | §13 (e) cites SPEC-017 BEH-11; the version-raise rule is SPEC-017 BEH-13 | :1011 | note | Fixed |
| 14 | A session raise stays out of the resolution line, but ADR-003 records a local value as '(local)'; name the departure | :331, 1012 | note | Fixed: reading (f) names the A5 form the raise departs from, and BEH-20 says the resolution line never carries a '(local)' entry for it |
| 15 | BEH-13 counts four kinds of open decision; §4 defined five | :322, 169-172, 213 | note | Fixed with finding 4: four kinds |
| 16 | ERR-07 promises a review file that BEH-24 writes only as a mode | :389, 343 | note | Fixed: ERR-07's save offers the file; BEH-24 covers that case |
| 17 | BEH-21 triggers on the whole estimate; a continue with 2 open requirements and 9 quality questions would be offered triage | :334 | note | Fixed: the modes settle the requirements round only, and a continue counts and asks only the open decisions |
| 18 | Builder ambiguities: calls available after gates; ERR-09 and ERR-10 repeats once the budget is spent; two continuable PRDs or one picked from BEH-01's listing; an empty multiSelect; an IDEA-NN entry overlapping an FR entry; staleness undetectable without versions; Codex's 3 per batch against 'twelve a call' | :331, 398-404, 346, 337, 340, 328 | note | Fixed: each is stated (BEH-20, ERR-09, ERR-10, BEH-25, BEH-22, BEH-23, §4's source form with the version, BEH-22's last sentence) |
| 19 | VER-47 (d) and runbook M2 (d) say 'locked at 1', but a local value keeps overridable_by including local | :885; runbook:60 | note | Fixed: the case is the gates using the whole budget, with no raise asked for |
| 20 | VER-43 and VER-44 require 'every other line byte-identical', but version, updated and the Change Log change | :844, 854 | note | Fixed: item blocks, and the earlier Change Log rows kept |
| 21 | A bulk acceptance should name the statements too; the review file has no rule for case, spaces or a '\|' in a statement | :337, 213 | note | Fixed: BEH-22 names the statements; §4 gives the cell rules |
| 22 | §2 relies on ADR-008, and SPEC-011, SPEC-012 and SPEC-017 are cited, none in upstream; the tracker's age sweep over devforgeai/drafts/prd/ is unverified | :18-27, 82, 1014 | note | Fixed: ADR-008 linked; the prose citations are recorded in §13 as not links; SPEC-013's sweep reads manifests' workFiles and prd has no manifest, recorded in §13 as open |
| 23 | BEH-01's text is unchanged though BEH-25 changes its listing | :272, 346, 972 | note | Fixed: BEH-01 names continuable PRDs after the unprocessed BRNs |

## For Bryan at approval

The reviewer marked three findings as decisions, not edits. Each is fixed one way in the revision and listed in
SPEC-002 §13 as a reading: what 'None of these' records (reading (l), finding 7); BEH-19's source rule (reading (h),
finding 2); and the continue's scope (reading (e), finding 4). The approval question shows them.
