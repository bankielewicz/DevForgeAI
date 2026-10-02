---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-012\b(?=[^\n]{0,300}\bblocked\b)(?=[^\n]{0,300}\bDEC-07\b)
