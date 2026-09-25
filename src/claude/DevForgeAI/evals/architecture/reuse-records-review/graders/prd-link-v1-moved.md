---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
match: not_contains
pattern: '^-{3}\n(?:(?!\n-{3}\n)[\s\S])*?- \{id: PRD-001, relation: informed_by, version: 1\b'
---
