---
type: regex
target: {source: file, path: docs/specs/context/source-tree.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?id:[ \t]*["']?CTX-004["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?document:[ \t]*["']?source-tree["']?[ \t]*(?:#[^\n]*)?\n)
