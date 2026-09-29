---
type: llm
---

The workspace held BRN-001 (volunteer shift sign-up, whose promoted ideas PRD-001 already
cites) and BRN-002 (donation drop-off booking, cited by no PRD).
PASS if the reply offers BRN-002 as the brainstorm to turn into a PRD, does not offer BRN-001
as a candidate (mentioning that it is already covered is fine), and asks the user to confirm
which brainstorm to use before writing anything.
FAIL if it offers BRN-001, picks BRN-002 and writes a PRD without asking, or asks for a file
path.
