---
type: llm
---

Context the reply was written in: BRN-001 is at version 2. Its promoted ideas IDEA-01 and IDEA-03 are
already cited by the draft PRD-001 (IDEA-01 by FR-001 and SM-01, IDEA-03 by FR-002 and SM-02) at BRN-001
version 1, and its new promoted IDEA-05 isn't cited yet. The user asked to extend PRD-001 from BRN-001 and
to proceed without questions. A correct run adds requirements for IDEA-05 only and passes validation.

Judge only the final reply. PASS if it names both IDEA-01 and IDEA-03, by ID, as left out (not drafted
again) because PRD-001 already cites them, and names for each a PRD-001 item that cites it (FR-001 or SM-01
for IDEA-01; FR-002 or SM-02 for IDEA-03). Any wording counts, such as "IDEA-01 left out: PRD-001#FR-001
cites it" or "IDEA-01 and IDEA-03 are already covered by FR-001 and FR-002".
FAIL if either ID or its citing item is missing, or if the reply says it drafted new requirements from
IDEA-01 or IDEA-03.
