---
type: regex
target: last_message
match: contains
flags: i
---
(?:\bsix\b|\b6\b)[^\n]{0,80}\b(?:candidates?|requirements?)\b|\b(?:candidates?|requirements?)\b[^\n]{0,80}(?:\bsix\b|\b6\b)
