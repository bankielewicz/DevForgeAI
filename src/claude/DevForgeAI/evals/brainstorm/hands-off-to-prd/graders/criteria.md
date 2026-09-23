---
type: llm
---

PASS if the reply names writing a PRD (product requirements document) as the next planning step, tells the user to run /devforgeai:prd with the brainstorm's ID (BRN-001), and gives the brainstorm file path as that step's input.
FAIL if the reply passes a file path to /devforgeai:prd as its argument, starts drafting PRD content (requirements, success metrics) itself, or doesn't give the brainstorm file path.
