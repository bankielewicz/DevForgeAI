---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?approved_by:[ \t]*(?:\"\"|'')[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?approved_on:[ \t]*(?:null|~)[ \t]*(?:#[^\n]*)?\n)
