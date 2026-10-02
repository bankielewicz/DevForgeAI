---
type: llm
---

Context the reply was written in: the user asked for a PRD from BRN-001 and named ADR-002 (accepted:
ClinicCore is the calendar of record) and ADR-003 (proposed: synchronous booking writes vs a scheduled
import). A proposed ADR resolves nothing, so a correct PRD records the booking decision as a [NEEDS ADR]
marker naming the booking requirements. An open decision is resolved in the architecture step, by an
accepted ADR or by an approved mandated platform (a policy setting) that answers exactly that question.

Judge only the final reply. PASS if all of these hold:
- It lists the open booking decision (the [NEEDS ADR] marker) with the requirements it names.
- It says that epics for those requirements must wait until the architecture step resolves that decision.
- It names both ways the decision can be resolved: an accepted ADR, or an approved mandated platform (or
  policy setting) that answers it. Any wording counts.
FAIL if any of these fails, or if it says or implies that only an accepted ADR can resolve the decision,
such as "epics must wait until an accepted ADR resolves it" with no other way named.
