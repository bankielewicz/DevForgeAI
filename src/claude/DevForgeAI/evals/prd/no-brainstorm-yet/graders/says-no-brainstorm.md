---
type: llm
---

Context the reply was written in: the workspace has no docs/specs/ folder, so no brainstorm (BRN)
document exists. The user asked to write a PRD and named no brainstorm.

Judge only the final reply. PASS if all of these hold:
- It says that no brainstorm exists yet, or that there is no BRN to turn into a PRD.
- It tells the user to start with /devforgeai:brainstorm.
- It doesn't present a PRD as written.
FAIL if any of these fails, or if it says that promoted ideas are already cited by a PRD.
