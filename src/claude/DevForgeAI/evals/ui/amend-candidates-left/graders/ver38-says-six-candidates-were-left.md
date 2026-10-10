---
type: regex
target: last_message
match: contains
flags: i
---
(?:\bsix\b|\b6\b)[^\n]{0,80}\bcandidates?\b|\bcandidates?\b[^\n]{0,80}(?:\bsix\b|\b6\b)
