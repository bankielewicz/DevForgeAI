---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-012\b(?=[^\n]{0,300}\bunknown\b)(?=[^\n]{0,300}POL-001#SET-01)(?=[^\n]{0,300}(?:record|resolution))
