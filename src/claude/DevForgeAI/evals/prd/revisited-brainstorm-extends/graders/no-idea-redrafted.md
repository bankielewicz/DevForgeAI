---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: not_contains
---
(?:item: IDEA-01,[\s\S]*){3}|(?:item: IDEA-03,[\s\S]*){3}|IDEA-0[24]\b
