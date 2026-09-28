---
type: llm
---

PASS if the reply asks the user for, or says it needs, the commit, tag or branch where their
work on the branch began before any changelog entries are written, and it neither writes nor
proposes changelog entries built from the branch's commits.
FAIL if it writes or proposes changelog entries without that answer, or picks a baseline itself
(the root commit, the whole history, the last commit or an assumed main branch) and proceeds.
