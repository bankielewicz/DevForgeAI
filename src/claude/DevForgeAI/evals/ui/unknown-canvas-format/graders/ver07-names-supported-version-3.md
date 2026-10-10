---
type: regex
target: last_message
match: contains
flags: i
---
\b3\b[^\n]{0,60}\b(?:supported|only)\b|\b(?:supported|only)\b[^\n]{0,60}\b3\b
