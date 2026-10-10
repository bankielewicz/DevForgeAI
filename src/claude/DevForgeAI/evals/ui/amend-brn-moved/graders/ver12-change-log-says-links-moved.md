---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
\n\|[ \t]*2[ \t]*\|[^\n]*(?:\b[Ll]inks?\b[^\n]*\bmov|\bmov\w*\b[^\n]*\blinks?\b)
