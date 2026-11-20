---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
flags: m
---
^- Why chain for PRB-01: \S[^\n]* → because \S
