---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: not_contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?PRD-001\b)[^}\n]*\}|id:[ \t]*["']?PRD-001["']?[ \t]*\n))
