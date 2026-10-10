---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?canvas:[ \t]*["']?https://claude\.ai/artifact/EXAMPLE["']?[ \t]*(?:#[^\n]*)?\n)
