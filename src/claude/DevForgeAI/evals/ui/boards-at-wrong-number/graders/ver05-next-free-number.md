---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:new|next)\b[^\n]{0,80}\bDSN-002\b|\bDSN-002\b[^\n]{0,80}\b(?:new|next)\b|\bDSN-002\b[^\n]{0,60}\b(?:would be|will be|is)\b
