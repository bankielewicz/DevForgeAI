---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?approved_on:[ \t]*["']?\d{4}-\d{2}-\d{2}["']?[ \t]*(?:#[^\n]*)?\n)
