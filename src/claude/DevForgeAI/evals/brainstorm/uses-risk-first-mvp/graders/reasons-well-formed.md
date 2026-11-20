---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
flags: m
---
^- Reason \d+: (?![^\n]* \((?:ASM|PRB)-\d\d\)$)
