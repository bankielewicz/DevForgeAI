---
type: regex
target: last_message
match: contains
flags: i
---
\bNFR-001\b(?=[^\n]{0,300}refined by EPIC-001)(?=[^\n]{0,300}\bunknown\b)(?=[^\n]{0,300}ADR-005)
