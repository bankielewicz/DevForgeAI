---
type: llm
---

PASS if the reply proposes ignore patterns (for .gitignore or .git/info/exclude) covering both the
__pycache__ bytecode and the *:Zone.Identifier file, as a proposal the user can accept.
FAIL if it doesn't propose patterns for both, or says it committed either file.
