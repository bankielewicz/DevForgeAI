---
type: regex
target: {source: file, path: docs/specs/context/architecture.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?ARCH-001\b)(?=[^}\n]*\bitem:[ \t]*["']?CMP-02\b)(?=[^}\n]*\brelation:[ \t]*["']?constrains\b)[^}\n]*\}|id:[ \t]*["']?ARCH-001["']?[ \t]*\n(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+item:[ \t]*["']?CMP-02\b)(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+relation:[ \t]*["']?constrains\b)))
