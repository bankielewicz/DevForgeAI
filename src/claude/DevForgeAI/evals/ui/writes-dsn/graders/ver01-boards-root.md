---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?boards_root:[ \t]*["']?docs/specs/design/DSN-001/boards/["']?[ \t]*(?:#[^\n]*)?\n)
