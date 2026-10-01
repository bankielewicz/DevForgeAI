---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?id:[ \t]*["']?CTX-003["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?document:[ \t]*["']?tech-stack["']?[ \t]*(?:#[^\n]*)?\n)
