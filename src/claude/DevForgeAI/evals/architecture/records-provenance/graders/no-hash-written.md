---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
match: not_contains
pattern: 'hash:\s*(?!null\b)\S'
---
