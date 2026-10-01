---
type: regex
target: {source: file, path: docs/specs/context/front-end.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?title:[ \t]*[\"']shiftlog: front end[\"'][ \t]*(?:#[^\n]*)?\n)
