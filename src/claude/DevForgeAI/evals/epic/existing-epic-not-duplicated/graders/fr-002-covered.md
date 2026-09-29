---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-002\b(?=[^\n]{0,300}\bcovered\b)(?=[^\n]{0,300}EPIC-001)
