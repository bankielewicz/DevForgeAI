---
type: llm
---

The workspace held PRD-001 with NFR-001 (must, current release) and NFR-003 (release later, no priority
yet), an ARCH-001 whose open question DEC-08 cites both, and an existing approved EPIC-001 that refines
FR-003, NFR-001 and NFR-003. A blocked NFR that an existing epic refines is reported as "refined by"
that epic, with the next action to review that epic's work before continuing; it is never "covered". A
later NFR's first reason is "later", so its action is the later one (nothing for the current release),
but its row still names the epic and the block.

Judge only the final reply.
PASS if all of these hold:
- NFR-001 is reported as left out, refined by EPIC-001 and blocked by DEC-08, with a next action to
  review EPIC-001's work (any wording).
- NFR-001 is not called covered.
- NFR-003 is reported as left out because it is for a later release, also naming EPIC-001 and DEC-08,
  with no action asked for the current release.
FAIL if any of these doesn't hold, if NFR-003 is called covered or its row asks for an action for the
current release (such as reviewing EPIC-001's work), or if the reply says EPIC-001 was changed.
