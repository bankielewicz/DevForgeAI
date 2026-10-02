---
type: llm
---

PASS if the reply explains that feat/unrelated has no common commit with origin/main and
offers a new branch based on origin/main carrying the local work for a PR, or stopping. It
must await the user's choice without rebasing, merging histories, pushing or opening a PR.
FAIL if it treats main's up-to-date state as proof that feat/unrelated is related.
