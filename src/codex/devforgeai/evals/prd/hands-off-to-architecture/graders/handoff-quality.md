---
type: llm
---

Look at the final paragraph of the reply, the one that starts with "Next step".
PASS if it tells the user to run $devforgeai:architecture PRD-001, naming the PRD by its ID.
FAIL if it says the architecture skill does not exist yet or is unavailable, says the
architecture step must be done by hand, passes a file path instead of the ID, or if the reply
starts architecture work (proposing components or writing ADRs).
