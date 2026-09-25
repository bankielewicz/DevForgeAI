---
type: regex
target:
  source: file
  path: docs/specs/epic/EPIC-001.md
match: not_contains
pattern: 'item:\s*(?:FR-001|FR-008|FR-009|FR-010|FR-011),\s*relation:\s*refines\b'
---
