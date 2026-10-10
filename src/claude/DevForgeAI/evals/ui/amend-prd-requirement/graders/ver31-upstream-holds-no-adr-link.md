---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: not_contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?ADR-\d{3}\b)[^}\n]*\}|id:[ \t]*["']?ADR-\d{3}["']?[ \t]*\n))
