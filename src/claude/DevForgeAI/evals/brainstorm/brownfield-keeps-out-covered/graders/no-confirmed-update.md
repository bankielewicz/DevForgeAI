---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: not_contains
---
\| confirmed [^|\n]*\d{4}-\d{2}-\d{2} \|
