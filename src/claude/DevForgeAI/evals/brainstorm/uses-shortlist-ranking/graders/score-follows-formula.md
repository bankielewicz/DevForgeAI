---
type: llm
focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
---

The file is a brainstorm document. In its ideas block every idea has value, effort and risk as quoted
numbers and a score. Judge only this: for every idea, score equals value × (100 − risk) ÷ 100 ÷ effort,
rounded to one decimal. PASS if that holds for every idea. FAIL otherwise, and quote the idea ID with
its four values.
