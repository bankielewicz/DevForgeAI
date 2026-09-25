---
type: regex
target:
  source: file
  path: docs/specs/epic/EPIC-003.md
match: not_contains
pattern: 'item:\s*(?:FR-00[1-35-9]|FR-01\d|NFR-\d{3}),\s*relation:\s*refines\b'
---
