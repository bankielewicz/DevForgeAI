---
type: regex
target: {source: file, path: docs/specs/context/testing.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?POL-001\b)(?=[^}\n]*\bitem:[ \t]*["']?SET-01\b)(?=[^}\n]*\brelation:[ \t]*["']?constrains\b)[^}\n]*\}|id:[ \t]*["']?POL-001["']?[ \t]*\n(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+item:[ \t]*["']?SET-01\b)(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+relation:[ \t]*["']?constrains\b)))
