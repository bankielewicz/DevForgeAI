---
type: llm
focus:
  source: file
  path: docs/specs/prd/PRD-001.md
---

The input is the PRD Claude wrote. Check only how it treats microservices.
PASS if microservices appear nowhere in the functional or non-functional requirements (the `yaml items` blocks), and if they are mentioned at all, it is only as an open question or design preference for a future ADR, not as a decision or requirement.
FAIL if any requirement, constraint or prose section states that the system uses, shall use or is built as microservices, or otherwise records microservices as decided.
