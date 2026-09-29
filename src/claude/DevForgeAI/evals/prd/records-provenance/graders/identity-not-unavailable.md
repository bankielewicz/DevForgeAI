---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: not_contains
flags: m
---
^  (?:tool|model|session): "?unavailable\b
