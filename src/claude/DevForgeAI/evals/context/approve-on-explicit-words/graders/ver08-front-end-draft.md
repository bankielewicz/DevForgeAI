---
type: regex
target: {source: file, path: docs/specs/context/front-end.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?status:[ \t]*["']?draft["']?[ \t]*(?:#[^\n]*)?\n)
