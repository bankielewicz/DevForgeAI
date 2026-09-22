---
type: llm
---

PASS if the final reply reports that a brainstorm document was written at a path of the form docs/specs/brainstorms/BRN-001-<slug>.md, where the slug is lowercase, hyphenated and at most five words; gives counts of problems, ideas and assumptions; and names a next step.
FAIL if no file path is given, the reply claims the document is a PRD or a plan rather than a brainstorm, or the reply says the work could not be saved.
