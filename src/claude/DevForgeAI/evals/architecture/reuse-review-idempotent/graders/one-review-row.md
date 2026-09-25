---
type: regex
target:
  source: file
  path: docs/specs/arch/ARCH-001.md
flags: i
pattern: '\n\|[^\n]*\|[^\n|]*Reviewed against PRD-001 v2\b[^\n|]*reuse confirmed[^\n]*\|[ \t]*(?=\n|$)'
---
