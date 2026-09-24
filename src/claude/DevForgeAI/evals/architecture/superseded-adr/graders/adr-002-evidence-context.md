---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
pattern: '- id: EVD-\d\d[ \t]*\n(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*source: [^\n]*ADR-002)(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*classification: context\b)'
---
