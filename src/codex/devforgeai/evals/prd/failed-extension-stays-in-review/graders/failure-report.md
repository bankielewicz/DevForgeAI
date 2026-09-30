---
type: llm
---

Context the reply was written in: PRD-001 was an approved PRD. Its existing requirement FR-001 has
`priority: high`, a value the self-check rejects (priority must be must, should, could, wont or null).
The user asked to extend PRD-001 from BRN-002, a brainstorm of the same initiative, and to proceed
without questions. An extension must leave existing items byte-identical, so no repair within the
extension rules can fix FR-001, and validation fails.

Judge only the final reply. PASS if all of these hold:
- It reports that validation failed and names the unresolved error in FR-001 (its priority value).
- It lists the validation checks it made and any repairs, and there are at most four checks: an
  initial check plus at most three repair cycles. Stopping early because the error can't be
  repaired is fine.
- It says PRD-001 is left in-review (not approved), with its approval cleared.
- It doesn't present the PRD as ready for the architecture step: it doesn't tell the user to run
  $devforgeai:architecture now, and doesn't call the PRD valid or complete.
FAIL if any of these fails, or if the reply says it changed FR-001.
