---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:later|future|another|subsequent|interactive)\s+(?:run|session)\b|\bnext run\b|\bleft for later\b|\bwait\w*\b[^\n]{0,40}\b(?:run|session)\b
