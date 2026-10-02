---
type: llm
focus: {source: file, path: docs/specs/brainstorm/BRN-001.md}
---

The file is a brainstorm document about reducing no-shows at a small dental clinic
(two dentists, one hygienist, about one in eight appointments missed).
Judge only these two claims; ignore formatting, length and anything else:
1. There are at least 2 problems (PRB-NN) and every idea's `addresses` list names only
   PRB-NN IDs that are defined in the problems block.
2. The ideas are concrete actions that fit a small dental clinic, not generic advice that
   would apply to any business unchanged.
PASS if both claims hold. FAIL if either does, and quote the idea or ID that breaks it.
