---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
flags: m
---
^- HMW-01 \(PRB-01\): How might we [^\n]+\? Ideas: IDEA-\d\d(?:, IDEA-\d\d)*\.$
