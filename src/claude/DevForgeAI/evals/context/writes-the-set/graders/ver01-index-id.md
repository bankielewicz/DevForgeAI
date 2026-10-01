---
type: regex
target: {source: file, path: docs/specs/context/index.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?id:[ \t]*["']?CTX-001["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?document:[ \t]*["']?index["']?[ \t]*(?:#[^\n]*)?\n)
