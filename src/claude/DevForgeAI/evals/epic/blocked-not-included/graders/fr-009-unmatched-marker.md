---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-009\b(?=[^\n]{0,300}\bblocked\b)(?=[^\n]{0,300}marker)
