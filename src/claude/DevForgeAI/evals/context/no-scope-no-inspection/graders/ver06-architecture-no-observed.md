---
type: regex
target: {source: file, path: docs/specs/context/architecture.md}
match: not_contains
---
observed_in|\*\*Observed\*\*|\|[ \t]*Observed[ \t]*\(
