---
type: regex
target:
  source: file
  path: docs/specs/prd/PRD-001.md
pattern: 'category: constraint\s*\n\s*statement: "[^"]*Org A Identity Platform[^\n]*\n(\s+(priority|release|superseded_by): [^\n]*\n)*\s+upstream:\s*\n(\s+- \{[^\n]*\n)*?\s+- \{id: POL-001, item: SET-01, relation: constrains, version: 3\b'
---
