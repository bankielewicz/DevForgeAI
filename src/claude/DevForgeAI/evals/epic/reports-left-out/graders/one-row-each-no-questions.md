---
type: llm
---

The workspace held PRD-001 with FR-005 (priority must, release later; its architectural question
DEC-06 is open), FR-006 (priority wont) and FR-007 (priority null, meaning undecided). The user asked
for one epic covering every eligible requirement and said to proceed without questions.

Judge only the final reply.
PASS if all of these hold:
- FR-005, FR-006 and FR-007 each appear in a list of requirements left out of the epics, each once,
  with its reason (later, won't have, undecided) and one next action: no action for the current
  release (FR-005), none for this release (FR-006), the PRD owner decides (FR-007).
- The reply asks the user no question about any of the three and doesn't ask them to decide a
  priority or release.
FAIL if any of the three is missing, has no next action, appears in more than one row, is put in an
epic, or if the reply asks a question about any of them.
