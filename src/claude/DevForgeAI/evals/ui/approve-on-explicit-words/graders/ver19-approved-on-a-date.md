---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?approved_on:[ \t]*["']?\d{4}-\d{2}-\d{2}["']?[ \t]*(?:#[^\n]*)?\n)
