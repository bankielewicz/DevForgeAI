---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
---
^(?=[\s\S]*item: IDEA-01\b)(?=[\s\S]*item: IDEA-03\b)
