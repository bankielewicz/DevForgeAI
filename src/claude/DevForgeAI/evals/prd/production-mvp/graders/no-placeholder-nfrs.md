---
type: regex
target:
  source: file
  path: docs/specs/prd/PRD-001.md
match: not_contains
pattern: 'category: (reliability|observability|compliance|performance|accessibility)\b'
---
