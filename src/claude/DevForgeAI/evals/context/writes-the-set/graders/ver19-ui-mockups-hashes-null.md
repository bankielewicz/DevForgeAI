---
type: regex
target: {source: file, path: docs/specs/context/ui-mockups.md}
match: not_contains
---
\bhash:[ \t]*(?!null\b)[^\s,}]
