---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: not_contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?ADR-009\b)[^}\n]*\}|id:[ \t]*["']?ADR-009["']?[ \t]*\n))
