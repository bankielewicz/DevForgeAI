---
type: llm
focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
---

The file is a brainstorm document. Section 5 has one line per idea of the form "- IDEA-NN tests ASM-NN,
ASM-NN" or "- IDEA-NN tests no assumption". Judge only this: every idea's value in the ideas block is
"high" when its line names two or more assumptions, "medium" when it names one, and "low" when it says
no assumption. PASS if that holds for every idea. FAIL otherwise, and quote the idea ID, its value and
its line.
