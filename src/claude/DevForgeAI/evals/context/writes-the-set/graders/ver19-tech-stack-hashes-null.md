---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: not_contains
---
\bhash:[ \t]*(?!null\b)[^\s,}]
