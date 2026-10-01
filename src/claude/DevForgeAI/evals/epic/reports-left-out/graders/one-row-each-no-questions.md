---
type: llm
---

The workspace held PRD-001 with FR-005 (release later and priority null, which is how the PRD skill
writes every later requirement; its architectural question DEC-06 is open), FR-006 (priority wont),
FR-007 (priority null with release current, meaning undecided) and NFR-002 (priority and release both
null, meaning undecided). The user asked for one epic covering every eligible requirement and said to
proceed without questions.

Judge only the final reply.
PASS if all of these hold:
- FR-005, FR-006, FR-007 and NFR-002 each appear in a list of requirements left out of the epics,
  each once, with its reason and one next action: FR-005 is later, with no action for the current
  release; FR-006 is won't have, with none for this release; FR-007 and NFR-002 are undecided, and
  the PRD owner decides.
- FR-005's row does not call it undecided and doesn't ask the PRD owner to decide its priority: a
  later requirement's null priority is normal.
- The reply asks the user no question about any of the four and doesn't ask them to decide a
  priority or release.
FAIL if any of the four is missing, has no next action, appears in more than one row, is put in an
epic, if FR-005 is called undecided, or if the reply asks a question about any of them.
