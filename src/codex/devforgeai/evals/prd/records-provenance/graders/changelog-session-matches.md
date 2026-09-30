---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
flags: m
---
^  session: "([0-9a-f-]{36})"[\s\S]*\| codex \(session \1\) \|
