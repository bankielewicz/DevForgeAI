---
type: llm
focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
---

The file is a brainstorm document. Under the heading "### First release cut" is a table with the
columns Idea, In first release, Why. Section 8, "Candidate success signals", is a bullet list.
Judge only this claim: section 8 has exactly one bullet starting with the ID of each idea whose
row says "yes", in the same order, and no bullet for any other idea.
PASS if the claim holds. FAIL otherwise, and name the idea ID that is missing or extra.
