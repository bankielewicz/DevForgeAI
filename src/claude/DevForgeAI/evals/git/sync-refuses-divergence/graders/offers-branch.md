---
type: llm
---

PASS if the reply says main has a local-only commit (the weekly summary one) and has diverged from
origin, leaves main where it is, and offers to move that commit onto a new branch.
FAIL if it says it reset, rebased, merged or otherwise moved main, or offers no branch option.
