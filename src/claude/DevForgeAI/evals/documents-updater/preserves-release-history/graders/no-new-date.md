---
type: regex
target: {source: file, path: CHANGELOG.md}
match: not_contains
---
\b(?!2026-06-02\b|2026-04-15\b)20\d\d-\d\d-\d\d\b
