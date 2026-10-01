---
type: regex
target: {source: file, path: docs/specs/context/index.md}
match: not_contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?freshness_days:)
