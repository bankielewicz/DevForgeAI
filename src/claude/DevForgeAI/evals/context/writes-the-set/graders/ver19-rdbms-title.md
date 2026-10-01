---
type: regex
target: {source: file, path: docs/specs/context/rdbms.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?title:[ \t]*[\"']shiftlog: relational database[\"'][ \t]*(?:#[^\n]*)?\n)
