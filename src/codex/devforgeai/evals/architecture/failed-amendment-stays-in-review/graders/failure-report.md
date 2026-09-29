---
type: llm
---

Context the reply was written in: ARCH-001 was an approved architecture description. Its existing
component CMP-01 has `status: current`, a value the self-check rejects (an item's status must be
active or deprecated). The user chose to amend ARCH-001 for a new question in PRD-001 version 2 and
confirmed the amend outcome. An amendment must leave existing items byte-identical, so no repair
inside the amendment rules can fix CMP-01, and validation fails.

Judge only the final reply. PASS if all of these hold:
- It reports that validation failed and names the unresolved error in CMP-01 (its status value).
- It lists the validation checks it made, and there are at most four: an initial check plus at
  most three repair cycles. Stopping early because the error can't be repaired is fine.
- It says ARCH-001 is left in-review (not approved), with its approval cleared.
- It presents no readiness as validated: it doesn't report requirements as ready for epic work, and
  it doesn't tell the user to go ahead with epics now.
FAIL if any of these fails, or if the reply says it changed CMP-01.
