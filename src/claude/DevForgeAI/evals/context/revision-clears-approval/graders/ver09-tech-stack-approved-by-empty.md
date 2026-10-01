---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?approved_by:[ \t]*(?:\"\"|'')[ \t]*(?:#[^\n]*)?\n)
