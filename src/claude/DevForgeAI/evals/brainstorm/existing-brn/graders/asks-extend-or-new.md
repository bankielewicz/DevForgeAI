---
type: llm
---

The workspace already held docs/specs/brainstorm/BRN-001.md, a brainstorm on
reducing dental appointment no-shows.
PASS if the reply points the user to that existing BRN-001 (by ID, title or path)
and asks whether to extend it or create a new brainstorm, without having written
either yet.
FAIL if it silently extends or overwrites BRN-001, creates a new BRN without asking,
or never mentions the existing document.
