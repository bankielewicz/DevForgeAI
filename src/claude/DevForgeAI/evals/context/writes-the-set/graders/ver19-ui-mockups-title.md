---
type: regex
target: {source: file, path: docs/specs/context/ui-mockups.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?title:[ \t]*[\"']shiftlog: ui mockups[\"'][ \t]*(?:#[^\n]*)?\n)
