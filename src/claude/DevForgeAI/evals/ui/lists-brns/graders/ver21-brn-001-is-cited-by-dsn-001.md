---
type: regex
target: last_message
match: contains
flags: i
---
BRN-001[^\n]*\bDSN-001\b|\bDSN-001\b[^\n]*BRN-001
