---
type: regex
target: {source: file, path: docs/specs/context/testing.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?title:[ \t]*[\"']shiftlog: testing[\"'][ \t]*(?:#[^\n]*)?\n)
