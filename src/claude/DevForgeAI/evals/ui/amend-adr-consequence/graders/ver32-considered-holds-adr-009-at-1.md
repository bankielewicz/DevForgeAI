---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?considered:(?:[^\n]*["']?ADR-009@1["']?[ \t,\]]|[ \t]*(?:#[^\n]*)?\n(?:[ \t]+-[^\n]*\n)*?[ \t]+-[ \t]*["']?ADR-009@1["']?[ \t]*(?:#[^\n]*)?\n))
