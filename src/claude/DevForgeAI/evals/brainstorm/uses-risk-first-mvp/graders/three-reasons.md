---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
flags: m
---
^- Reason 3: [^\n]+ \((?:ASM|PRB)-\d\d\)$
