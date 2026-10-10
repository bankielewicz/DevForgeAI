---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: not_contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?BRN-001\b)(?=[^}\n]*\bitem:[ \t]*["']?IDEA-04\b)(?=[^}\n]*\brelation:[ \t]*["']?derives\b)[^}\n]*\}|id:[ \t]*["']?BRN-001["']?[ \t]*\n(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+item:[ \t]*["']?IDEA-04\b)(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+relation:[ \t]*["']?derives\b)))
