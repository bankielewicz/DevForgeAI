---
type: regex
target: last_message
match: contains
flags: i
---
\bFR-011\b(?=[^\n]{0,300}\bunknown\b)(?=[^\n]{0,300}ADR-004)
