---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
flags: m
---
^  model: "claude-[a-z0-9][a-z0-9.-]*"
