---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: not_contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?considered:(?:[^\n]*["']?PRD-001@2["']?[ \t,\]]|[ \t]*(?:#[^\n]*)?\n(?:[ \t]+-[^\n]*\n)*?[ \t]+-[ \t]*["']?PRD-001@2["']?[ \t]*(?:#[^\n]*)?\n))
