---
type: regex
target: last_message
match: contains
flags: i
---
\bmarkers?\b[^\n]{0,100}\b(?:remains?|left|still|open|blocks?)\b|\b(?:remains?|left|still|open|blocks?)\b[^\n]{0,100}\bmarkers?\b
