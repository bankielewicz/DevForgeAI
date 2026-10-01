---
type: regex
target: {source: file, path: docs/specs/context/rdbms.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?ADR-002\b)(?=[^}\n]*\brelation:[ \t]*["']?constrains\b)[^}\n]*\}|id:[ \t]*["']?ADR-002["']?[ \t]*\n(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+relation:[ \t]*["']?constrains\b)))
