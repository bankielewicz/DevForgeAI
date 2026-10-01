---
type: llm
---

Context the reply was written in: BRN-001 is at version 2. Its promoted ideas IDEA-01 and IDEA-03 are
already cited by the draft PRD-001 (FR-001, FR-002, SM-01 and SM-02) at BRN-001 version 1, and its new
promoted IDEA-05 isn't cited yet. The user asked to extend PRD-001 from BRN-001 and to proceed without
questions.

Judge only the final reply. PASS if both of these hold:
- It says that IDEA-01 and IDEA-03 were left out, not drafted again, because PRD-001 already cites them.
  Any wording counts, such as "already covered by FR-001 and FR-002".
- It reports that PRD-001's existing links to BRN-001 version 1 now point to an older version (suspect
  links to review), and doesn't present them as validation errors.
FAIL if either is missing, or if the reply says it drafted new requirements from IDEA-01 or IDEA-03.
