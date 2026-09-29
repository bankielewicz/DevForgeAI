---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
flags: m
---
^generated_by:\n^  tool: \"codex\"\n^  model: \"[^\"\n]+\"\n^  session: \"[^\"\n]+\"\n
