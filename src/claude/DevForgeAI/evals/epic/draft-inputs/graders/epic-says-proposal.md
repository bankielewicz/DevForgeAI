---
type: regex
target: {source: file, path: docs/specs/epic/EPIC-001.md}
match: contains
flags: i
---
proposal[^\n]{0,200}\bdraft\b|\bdraft\b[^\n]{0,200}proposal
