---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
pattern: '- id: DEC-0[12][ \t]*\n(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*- \{id: PRD-001, item: (?:FR|NFR)-00\d, relation: informed_by, version: 1\b)'
---
