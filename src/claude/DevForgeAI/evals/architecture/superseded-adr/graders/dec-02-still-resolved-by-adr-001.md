---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
pattern: '- id: DEC-02[ \t]*\n(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*state: resolved\b)(?=(?:(?![ \t]*- id: |[ \t]*`{3})[^\n]*\n)*?[ \t]*resolved_by:(?:[^\n]*\bADR-001\b|[ \t]*\n[ \t]*- "?ADR-001\b))'
---
