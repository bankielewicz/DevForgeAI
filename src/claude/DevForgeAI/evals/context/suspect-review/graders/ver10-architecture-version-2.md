---
type: regex
target: {source: file, path: docs/specs/context/architecture.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?version:[ \t]*2[ \t]*(?:#[^\n]*)?\n)
