---
type: regex
target: last_message
match: contains
flags: i
---
(?:\bone\b|\b1\b)[^\n]{0,80}\b(?:candidates?|requirements?|consequences?)\b|\b(?:candidates?|requirements?)\b[^\n]{0,80}(?:\bone\b|\b1\b)|\bFR-024\b
