---
type: llm
---

Look at the final paragraph of the reply, the one that starts with "Next step".
PASS if it says the architecture skill (/devforgeai:architecture) does not exist yet; says
that for now the architecture step is done by hand by writing ADRs with the ADR template, with
PRD-001 (and its NEEDS ADR markers, if any) as the input; and says that once the skill is
built, /devforgeai:architecture PRD-001 runs on it.
FAIL if it claims the architecture skill is available to run now, passes a file path instead
of the ID, or if the reply starts architecture work (proposing components or writing ADRs).
