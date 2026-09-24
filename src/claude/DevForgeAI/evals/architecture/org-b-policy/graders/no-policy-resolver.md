---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
match: not_contains
pattern: 'resolved_by:[^\n]*POL-|resolved_by:[ \t]*\n[ \t]*- "?POL-'
---
