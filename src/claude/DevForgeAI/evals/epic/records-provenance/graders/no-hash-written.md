---
type: regex
target:
  source: file
  path: docs/specs/epic/EPIC-001.md
match: not_contains
pattern: 'hash:\s*(?!null\b)\S'
---
