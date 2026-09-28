---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-008\b(?=[^\n]{0,300}\bblocked\b)(?=[^\n]{0,300}\bDEC-03\b)(?=[^\n]{0,300}ADR-002)(?=[^\n]{0,300}supersed)
