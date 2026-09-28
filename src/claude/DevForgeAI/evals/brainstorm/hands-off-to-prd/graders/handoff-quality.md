---
type: llm
---

PASS if the final reply names the PRD workflow as the next step, tells the user to run
/devforgeai:prd BRN-001 (the BRN ID, not a path), and gives the brainstorm at
docs/specs/brainstorm/BRN-001.md as its input.
FAIL if it says the PRD workflow is not built yet or unavailable, passes a file path as the
command's argument, or starts drafting PRD content (requirements, success metrics).
