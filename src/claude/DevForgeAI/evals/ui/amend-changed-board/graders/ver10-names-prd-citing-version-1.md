---
type: regex
target: last_message
match: contains
flags: i
---
PRD-001[^\n]*\b(?:version[ \t]*|v)1\b
