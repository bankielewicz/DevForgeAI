---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
\n\|[ \t]*3[ \t]*\|[^\n]*PRD-001[^\n]*(?:version[ \t]*|\bv|@)2\b
