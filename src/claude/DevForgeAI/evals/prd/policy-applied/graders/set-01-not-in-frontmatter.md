---
type: regex
target:
  source: file
  path: docs/specs/prd/PRD-001.md
match: not_contains
pattern: '^---\n(?:(?!\n---\n)[\s\S])*item: SET-01'
---
