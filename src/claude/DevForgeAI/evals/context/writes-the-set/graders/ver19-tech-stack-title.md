---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?title:[ \t]*[\"']shiftlog: tech stack[\"'][ \t]*(?:#[^\n]*)?\n)
