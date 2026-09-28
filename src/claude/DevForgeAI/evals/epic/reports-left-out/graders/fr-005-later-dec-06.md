---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-005\b(?=[^\n]{0,300}\blater\b)(?=[^\n]{0,300}\bDEC-06\b)(?=[^\n]{0,300}current release)
