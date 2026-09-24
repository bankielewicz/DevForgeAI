---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
match: not_contains
pattern: 'resolved_by:[^\n]*ADR-|resolved_by:[ \t]*\n[ \t]*- "?ADR-'
---
