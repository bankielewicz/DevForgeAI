---
type: regex
target: {source: file, path: docs/specs/context/ui-mockups.md}
match: not_contains
---
^---[ \t]*\n(?:(?!---[ \t]*\n)[^\n]*\n)*?[^\n]*\bSTORY-\d{3}
