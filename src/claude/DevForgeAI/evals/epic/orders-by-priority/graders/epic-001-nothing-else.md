---
type: regex
target:
  source: file
  path: docs/specs/epic/EPIC-001.md
match: not_contains
pattern: 'item:\s*(?:FR-00[13-9]|FR-01[01]),\s*relation:\s*refines\b'
---
