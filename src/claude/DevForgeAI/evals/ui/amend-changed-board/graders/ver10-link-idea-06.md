---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?BRN-001\b)(?=[^}\n]*\bitem:[ \t]*["']?IDEA-06\b)(?=[^}\n]*\brelation:[ \t]*["']?derives\b)(?=[^}\n]*\bversion:[ \t]*["']?1\b)[^}\n]*\}|id:[ \t]*["']?BRN-001["']?[ \t]*\n(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+item:[ \t]*["']?IDEA-06\b)(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+relation:[ \t]*["']?derives\b)(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+version:[ \t]*["']?1\b)))
