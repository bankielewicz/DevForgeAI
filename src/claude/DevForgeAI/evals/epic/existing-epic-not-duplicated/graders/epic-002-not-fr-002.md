---
type: regex
target:
  source: file
  path: docs/specs/epic/EPIC-002.md
match: not_contains
pattern: 'item:\s*(?:FR-002|FR-008),\s*relation:\s*refines\b'
---
