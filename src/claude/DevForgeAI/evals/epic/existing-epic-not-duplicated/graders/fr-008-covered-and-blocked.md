---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-008\b(?=[^\n]{0,300}\bcovered\b)(?=[^\n]{0,300}EPIC-001)(?=[^\n]{0,300}\bDEC-03\b)
