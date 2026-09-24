---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
pattern: '- id: EVD-\d\d[ \t]*\n(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*kind: prd\b)(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*classification: context\b)'
---
