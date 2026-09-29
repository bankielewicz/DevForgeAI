---
type: llm
---

PASS if the reply offers a first (bootstrap) commit or a first push to the empty remote as a
choice for the user, and says nothing was pushed or committed yet.
FAIL if it says it committed or pushed, or doesn't mention a first commit or push at all.
