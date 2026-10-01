---
type: regex
target: {source: file, path: docs/specs/context/testing.md}
match: contains
---
\n\|[ \t]*`?testing\.coverage_exclusions`?[ \t]*\|[^|\n]*\|[ \t]*`?\(default\)`?[ \t]*\|
