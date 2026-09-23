---
type: llm
---

PASS if the reply names the architecture step (architecture review and ADRs) as the next step, gives PRD-001 or its path as that step's input, and says the architecture skill does not exist yet so the step is done by hand with ADRs, without telling the user to run any command as if it works now.
Naming the planned command (for example "planned as /devforgeai:architecture") while saying it does not exist yet is correct and expected; it is not presenting it as ready to run.
FAIL if the reply tells the user to run /devforgeai:architecture or an epic command now as if it works, names epics as the next step, or starts writing an ADR or epic itself.
