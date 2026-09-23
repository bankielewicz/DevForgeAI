---
type: llm
---

PASS if the reply names the architecture step (architecture review and ADRs) as the next step, gives PRD-001 or its path as that step's input, and says the architecture skill does not exist yet so the step is done by hand with ADRs, without telling the user to run any command as if it works now.
FAIL if the reply presents /devforgeai:architecture or an epic command as ready to run, names epics as the next step, or starts writing an ADR or epic itself.
