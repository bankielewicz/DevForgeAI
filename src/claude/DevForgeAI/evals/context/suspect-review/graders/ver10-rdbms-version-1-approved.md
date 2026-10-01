---
type: regex
target: {source: file, path: docs/specs/context/rdbms.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?version:[ \t]*1[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?status:[ \t]*["']?approved["']?[ \t]*(?:#[^\n]*)?\n)
