---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
flags: i
pattern: '- id: DEC-\d\d[ \t]*\n(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*question: (?![^\n]*revo)[^\n]*(provider|provides|idp\b|identity platform|identity service))(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*state: resolved\b)(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*resolved_by:(?:[^\n]*POL-001#SET-01|[ \t]*\n[ \t]*- "?POL-001#SET-01))'
---
