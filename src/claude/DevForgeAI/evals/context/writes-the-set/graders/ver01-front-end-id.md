---
type: regex
target: {source: file, path: docs/specs/context/front-end.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?id:[ \t]*["']?CTX-011["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?document:[ \t]*["']?front-end["']?[ \t]*(?:#[^\n]*)?\n)
