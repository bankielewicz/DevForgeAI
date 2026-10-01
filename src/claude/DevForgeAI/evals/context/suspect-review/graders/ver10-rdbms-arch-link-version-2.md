---
type: regex
target: {source: file, path: docs/specs/context/rdbms.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?ARCH-001\b)(?=[^}\n]*\brelation:[ \t]*["']?constrains\b)(?=[^}\n]*\bversion:[ \t]*["']?2\b)[^}\n]*\}|id:[ \t]*["']?ARCH-001["']?[ \t]*\n(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+relation:[ \t]*["']?constrains\b)(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+version:[ \t]*["']?2\b)))
