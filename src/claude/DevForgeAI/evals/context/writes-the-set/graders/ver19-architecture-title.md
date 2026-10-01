---
type: regex
target: {source: file, path: docs/specs/context/architecture.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?title:[ \t]*[\"']shiftlog: architecture overview[\"'][ \t]*(?:#[^\n]*)?\n)
