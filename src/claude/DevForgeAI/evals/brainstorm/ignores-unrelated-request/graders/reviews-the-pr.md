---
type: llm
---

PASS if the reply reviews the pull request's caching approach itself: it comments
on hash-based invalidation, the cache location or the --no-cache flag, and gives a
judgment on whether the approach is sound.
FAIL if it starts a brainstorming session, generates a list of new ideas instead of
reviewing, or writes a brainstorm document.
