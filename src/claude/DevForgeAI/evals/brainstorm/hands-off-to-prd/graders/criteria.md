---
type: llm
---

PASS if the reply names writing a PRD (product requirements document) as the next planning step, gives the brainstorm file path as that step's input, and says the PRD workflow or command isn't available or built yet, without telling the user to run a command as if it works now.
FAIL if the reply presents /devforgeai:prd or any other command as ready to run, starts drafting PRD content (requirements, success metrics) itself, or doesn't give the brainstorm file path.
