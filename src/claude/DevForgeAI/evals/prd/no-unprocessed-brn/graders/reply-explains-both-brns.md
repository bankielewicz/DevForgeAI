---
type: llm
---

Context the reply was written in: BRN-001's promoted ideas (IDEA-01 and IDEA-03) are all cited by PRD-001.
BRN-002 is a draft brainstorm whose ideas are all open, so it has no promoted idea. The user asked to write
the next PRD and named no brainstorm, so no BRN can be processed.

Judge only the final reply. PASS if all of these hold:
- It says that BRN-002 has no promoted idea yet (a draft, not converged) and points to /devforgeai:brainstorm
  to converge it.
- It says that BRN-001's promoted ideas are already cited by PRD-001.
- It doesn't present a PRD as written.
FAIL if any of these fails, or if it offers BRN-001 or BRN-002 as ready to turn into a PRD.
