---
type: llm
focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
---

The file is a brainstorm document. Under "### Assumption risk ranking" each row names an
assumption (ASM-NN), its rank and, in "If wrong", the ideas it stops. Under "### First release
cut" each row names an idea, yes or no, and a reason. Judge only these two claims:
1. Every row whose reason reads "Tests ASM-NN, ranked R." names an assumption that has rank R
   in the ranking table and lists that idea in its "If wrong" cell.
2. For each such row, the idea would in fact stop working if that assumption (read its
   statement in the assumptions block) were false.
PASS if both hold for every such row, or if no row has that reason. FAIL otherwise, quoting the
row and saying which claim it breaks.
