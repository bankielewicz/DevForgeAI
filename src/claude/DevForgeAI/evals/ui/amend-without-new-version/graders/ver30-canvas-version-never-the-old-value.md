---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: not_contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?canvas_version:[ \t]*["']?17-example["']?[ \t]*(?:#[^\n]*)?\n)
