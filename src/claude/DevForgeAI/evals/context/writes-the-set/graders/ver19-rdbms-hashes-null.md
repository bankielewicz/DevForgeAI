---
type: regex
target: {source: file, path: docs/specs/context/rdbms.md}
match: not_contains
---
\bhash:[ \t]*(?!null\b)[^\s,}]
