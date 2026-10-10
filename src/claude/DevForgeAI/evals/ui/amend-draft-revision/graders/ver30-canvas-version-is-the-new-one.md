---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?canvas_version:[ \t]*["']?1791580000-c3d4["']?[ \t]*(?:#[^\n]*)?\n)
