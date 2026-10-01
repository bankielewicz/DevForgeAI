---
type: regex
target: {source: file, path: docs/specs/context/architecture.md}
match: not_contains
---
\bhash:[ \t]*(?!null\b)[^\s,}]
