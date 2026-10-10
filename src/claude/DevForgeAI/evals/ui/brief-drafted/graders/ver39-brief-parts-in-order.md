---
type: llm
---

The agent was asked to design the UI for a brainstorm (BRN-001, Shiftlog: record shifts) in a session with no Artifact tool, so it
could only propose flows and draft briefs for Claude Design. Judge the briefs in its output. A pass needs all of these:
- It shows one brief for each flow it proposes (one flow for the whole release gives one brief, two flows give two).
- Each brief starts with a lead line that names the flow and the product, Shiftlog.
- After its lead line each brief has, in this order, a Context, a Content, Must-haves and a Style, and each ends with a line that
  asks for 3 distinctly different directions of the key screen first.
- Labels may be bold, plain or followed by a colon, and a brief may sit in a code block.
Anything else is not a pass.
