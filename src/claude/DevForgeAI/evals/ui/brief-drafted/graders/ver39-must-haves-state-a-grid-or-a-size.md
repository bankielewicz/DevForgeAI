---
type: regex
target: last_message
match: contains
flags: i
---
\b\d{2,3}\s*(?:columns?|cols?)\s*(?:by|x|×|\*)\s*\d{2,3}\s*rows?\b|\b\d{3,4}\s*(?:px|pixels?)\b|\b\d{3,4}\s*(?:x|×|by)\s*\d{3,4}\b
