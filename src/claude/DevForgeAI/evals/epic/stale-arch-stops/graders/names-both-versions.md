---
type: llm
---

The workspace held PRD-001 at version 2 and ARCH-001, whose frontmatter link to PRD-001 is at version 1:
the architecture was last reviewed against PRD-001 version 1. The epic skill must stop without
writing an epic.

Judge only the final reply.
PASS if it says the architecture (ARCH-001) was defined or reviewed against PRD-001 version 1 while
PRD-001 is now at version 2, and tells the user to review the architecture against the current PRD
version, without writing or proposing epics as if the architecture were current.
FAIL if either version is missing or attributed to the wrong document, if it says the ARCH must be
rewritten or amended before anything else (a review that confirms reuse is enough), or if it says it
wrote an epic.
