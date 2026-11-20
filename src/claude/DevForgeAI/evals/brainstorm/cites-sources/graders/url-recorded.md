---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
\nsources:[\s\S]*?"(?:url|ticket): https://github\.com/example/cli/issues"[\s\S]*?\n---\n
