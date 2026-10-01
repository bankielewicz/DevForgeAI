---
type: regex
target: {source: file, path: docs/specs/context/ui-mockups.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?id:[ \t]*["']?CTX-017["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?document:[ \t]*["']?ui-mockups["']?[ \t]*(?:#[^\n]*)?\n)
