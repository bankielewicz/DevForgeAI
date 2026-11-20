---
type: llm
focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
---

The file is a brainstorm document about managing a community garden's plots and waiting list.
Under "### Assumption risk ranking" each row names an assumption (ASM-NN, defined in the
assumptions block above it), the ideas it stops ("If wrong") and a confidence. Judge only these
two claims:
1. For each row that lists ideas, each listed idea (read it in the ideas block) would stop
   working if the assumption's statement were false.
2. No row says confidence "high" unless the frontmatter "sources" list has an entry starting
   "data:", "document:" or "ticket:".
PASS if both hold. FAIL otherwise, quoting the row and saying which claim it breaks.
