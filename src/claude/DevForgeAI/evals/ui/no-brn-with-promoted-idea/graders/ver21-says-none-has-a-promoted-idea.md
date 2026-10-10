---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:no|none|not)\b[^\n]{0,80}\bpromoted\b|\bpromoted\b[^\n]{0,80}\b(?:none|no|not)\b
