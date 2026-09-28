---
type: llm
---

The workspace held PRD-001 and three ADRs, but no architecture description (ARCH) citing PRD-001.
The epic skill must write no epic, because which requirements are ready for epic work is computed
from the ARCH.

Judge only the final reply.
PASS if it says, in any wording, that no ARCH exists for PRD-001 and that epics (or which
requirements are ready for them) depend on it, and tells the user to run /devforgeai:architecture
PRD-001 first.
FAIL if it treats the missing ARCH as meaning nothing blocks, proposes or writes epics, or gives no
reason for handing back to the architecture step.
