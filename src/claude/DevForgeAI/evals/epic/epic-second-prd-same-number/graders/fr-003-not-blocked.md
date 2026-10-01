---
type: llm
---

The workspace held PRD-001 and PRD-002, two PRDs for the same system, and ARCH-001 version 2, which
covers both. ARCH-001's open question DEC-08 cites only PRD-002's FR-003 (a monthly report export).
PRD-001 also has an FR-003 (the coordinator's daily roster), which no open question cites. A
question blocks only the requirements of the PRD its links name, so PRD-001's FR-003 is ready and
eligible.

Judge only the final reply, which is about PRD-001.
PASS if PRD-001's FR-003 is presented as included in the epic and is not reported as blocked by
DEC-08, blocked at all, or left out.
FAIL if the reply says FR-003 is blocked by DEC-08 (or by any open question), leaves it out, or puts
PRD-002's requirements in the epic.
