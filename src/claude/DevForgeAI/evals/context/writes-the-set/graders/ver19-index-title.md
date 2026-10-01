---
type: regex
target: {source: file, path: docs/specs/context/index.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?title:[ \t]*[\"']shiftlog: project context index[\"'][ \t]*(?:#[^\n]*)?\n)
