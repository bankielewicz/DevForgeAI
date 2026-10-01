---
type: regex
target: {source: file, path: docs/specs/context/rdbms.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?id:[ \t]*["']?CTX-015["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?document:[ \t]*["']?rdbms["']?[ \t]*(?:#[^\n]*)?\n)
