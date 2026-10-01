---
type: regex
target: {source: file, path: docs/specs/context/architecture.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?id:[ \t]*["']?CTX-002["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?document:[ \t]*["']?architecture["']?[ \t]*(?:#[^\n]*)?\n)
