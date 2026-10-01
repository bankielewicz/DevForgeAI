---
type: regex
target: {source: file, path: docs/specs/context/index.md}
match: not_contains
---
\n\|[^\n]*\b(?:index|back-end|api|datastore)\.md\b[^\n]*\|[ \t]*CTX-\d{3}[ \t]*\|
