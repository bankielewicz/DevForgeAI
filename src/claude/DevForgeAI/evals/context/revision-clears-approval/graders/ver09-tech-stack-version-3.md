---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?version:[ \t]*3[ \t]*(?:#[^\n]*)?\n)
