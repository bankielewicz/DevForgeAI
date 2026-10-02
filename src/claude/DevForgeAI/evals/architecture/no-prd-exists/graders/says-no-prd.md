---
type: llm
---

Context the reply was written in: the project's docs/specs/prd/ folder exists but holds no PRD, and
no other planning documents exist. The user asked to define the architecture for "this project",
named no PRD, and asked to proceed without questions.

Judge only the final reply. PASS if it says that no PRD exists yet (so there is nothing to define the
architecture for), says that nothing was written, and points the user to /devforgeai:prd as the next
step. Mentioning /devforgeai:brainstorm as an earlier step as well is fine.
FAIL if it invents a PRD, writes or proposes architecture content as if a PRD existed, or doesn't
point to /devforgeai:prd.
