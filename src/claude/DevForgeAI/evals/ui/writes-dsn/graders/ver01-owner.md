---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?owner:[ \t]*["']?Example Owner["']?[ \t]*(?:#[^\n]*)?\n)
