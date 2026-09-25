---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
flags: i
match: not_contains
pattern: 'Reviewed against PRD-001[\s\S]*Reviewed against PRD-001'
---
