---
type: regex
target: {source: file, path: docs/specs/context/middle-tier.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?title:[ \t]*[\"']shiftlog: middle tier[\"'][ \t]*(?:#[^\n]*)?\n)
