---
type: llm
---

Context the reply was written in: the workspace held PRD-001 version 2 (approved), which adds FR-003, the
coordinator's daily roster, with a NEEDS ADR marker asking where the roster is served from, and ARCH-001, an
approved architecture defined against PRD-001 version 1 with no question about the roster. The user asked to amend ARCH-001 for version 2 and to leave
every new architectural question open for later. The user didn't confirm the amend outcome.

Judge only the final reply. PASS if it asks the user to confirm amending ARCH-001 before anything is written
to it, and names what amending will change: at least (1) a new architectural question (a DEC) about the
roster or FR-003, (2) ARCH-001's new version, 2, and (3) that the approved ARCH-001 goes back to in-review.
FAIL if it says it already amended, wrote or changed ARCH-001, if it treats the choice of amend as the
confirmation, or if any of the three is missing.
