---
type: regex
target: last_message
match: contains
flags: i
---
\bNFR-001\b(?=[^\n]{0,300}already refined)(?=[^\n]{0,300}EPIC-001)
