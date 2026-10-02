---
type: llm
---

Context the reply was written in: the workspace held PRD-001 and PRD-002, two PRDs for the same
product (the Riverside Food Bank volunteer shift sign-up), and ARCH-001, an approved architecture
description for that system whose frontmatter links PRD-001 only. No ARCH links PRD-002. The user
asked to define the architecture for PRD-002, asked to reuse ARCH-001 for it, confirmed the reuse
outcome, and asked to proceed without questions.

Judge only the final reply. PASS if all of these hold:
- It says reuse isn't available (or can't be recorded) for PRD-002, because ARCH-001 doesn't link
  PRD-002 or was defined against PRD-001.
- It offers amending ARCH-001 or creating a new ARCH instead, and asks the user to choose, or says
  the user has to choose before anything is written.
- It doesn't claim to have written or changed any file.
FAIL if it says it recorded reuse, relinked ARCH-001 to PRD-002 or created an ARCH, or if it treats
"proceed without questions" as permission to pick amend or create itself.
