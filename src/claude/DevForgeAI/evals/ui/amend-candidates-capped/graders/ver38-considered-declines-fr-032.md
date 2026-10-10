---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?considered:(?:[^\n]*["']?declined:PRD-001#FR-032["']?[ \t,\]]|[ \t]*(?:#[^\n]*)?\n(?:[ \t]+-[^\n]*\n)*?[ \t]+-[ \t]*["']?declined:PRD-001#FR-032["']?[ \t]*(?:#[^\n]*)?\n))
