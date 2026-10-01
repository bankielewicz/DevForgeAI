---
type: regex
target: {source: file, path: docs/specs/context/ui-mockups.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?version:[ \t]*2[ \t]*(?:#[^\n]*)?\n)
