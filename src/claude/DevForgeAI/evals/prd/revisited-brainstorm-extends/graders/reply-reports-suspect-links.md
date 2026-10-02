---
type: llm
---

Context the reply was written in: BRN-001 is at version 2. Its promoted ideas IDEA-01 and IDEA-03 are
already cited by the draft PRD-001 (IDEA-01 by FR-001 and SM-01, IDEA-03 by FR-002 and SM-02) at BRN-001
version 1, and its new promoted IDEA-05 isn't cited yet. The user asked to extend PRD-001 from BRN-001 and
to proceed without questions. A correct run adds requirements for IDEA-05 only and passes validation.

Judge only the final reply. PASS if it tells the user that PRD-001's existing links to BRN-001 cite
version 1 while BRN-001 is now at version 2, so they point to an older version and need review. Any wording
counts; the word "suspect" isn't required, and the reply needn't list every such link.
FAIL if the reply doesn't mention them, or if it counts them as validation errors, as repairs, or as a
reason a check failed.
