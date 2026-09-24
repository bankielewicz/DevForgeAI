---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
flags: i
pattern: '- id: DEC-\d\d[ \t]*\n(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*question: (?![^\n]*revo)[^\n]*(provider|provides|idp\b|identity platform|identity service))(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*state: open\b)(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*resolved_by: \[\][ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*- \{id: PRD-001, item: FR-001,)'
---
