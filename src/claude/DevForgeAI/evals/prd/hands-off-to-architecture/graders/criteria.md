---
type: llm
---

PASS if the reply names the architecture step as the next step and tells the user to run /devforgeai:architecture PRD-001, passing the PRD ID as the argument.
FAIL if the reply passes a file path to /devforgeai:architecture as its argument, claims the architecture skill is unavailable or not built yet, says the step must be done by hand with ADRs, names epics as the next step, or starts architecture work, an ADR or an epic itself.
