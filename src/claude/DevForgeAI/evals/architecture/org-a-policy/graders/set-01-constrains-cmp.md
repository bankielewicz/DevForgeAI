---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
pattern: '- id: CMP-\d\d[ \t]*\n(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*- \{id: POL-001, item: SET-01, relation: constrains, version: 3\b)'
---
