---
type: regex
target:
  source: file
  path: docs/specs/prd/PRD-001.md
match: not_contains
pattern: '^-{3}\n(?:(?!\n-{3}\n)[\s\S])*item: SET-01'
---
