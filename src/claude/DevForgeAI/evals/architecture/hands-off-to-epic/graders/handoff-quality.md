---
type: llm
---

Look at the final paragraph of the reply, the one that starts with "Next step".
PASS if it tells the user to run /devforgeai:epic PRD-001, naming the PRD by its ID, as the epic step:
either now for the requirements that are ready, or once open architectural questions are settled
(for example after answering them in another /devforgeai:architecture run).
FAIL if it says the epic skill does not exist yet, isn't built or is unavailable, says epics must be
written by hand, passes a file path instead of the ID, or if the reply starts epic work (proposing
epics or writing an epic).
