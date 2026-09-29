---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-006\b(?=[^\n]{0,300}\bwon[’']?t\b)
