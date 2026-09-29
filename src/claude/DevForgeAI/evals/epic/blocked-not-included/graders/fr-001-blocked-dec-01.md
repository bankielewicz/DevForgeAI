---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-001\b(?=[^\n]{0,300}\bblocked\b)(?=[^\n]{0,300}\bDEC-01\b)
