---
type: regex
target: {source: file, path: docs/specs/context/source-tree.md}
match: not_contains
---
\bhash:[ \t]*(?!null\b)[^\s,}]
