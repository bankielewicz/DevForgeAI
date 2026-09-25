---
type: regex
target:
  source: file
  path: docs/specs/epic/EPIC-001.md
match: not_contains
pattern: 'item:\s*(?:FR-012),\s*relation:\s*refines\b'
---
