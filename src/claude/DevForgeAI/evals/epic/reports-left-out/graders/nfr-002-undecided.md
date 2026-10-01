---
type: regex
target: last_message
match: contains
flags: i
---
\bNFR-002\b(?=[^\n]{0,300}\bundecided\b)(?=[^\n]{0,300}PRD owner)
