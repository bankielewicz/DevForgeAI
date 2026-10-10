---
type: regex
target: last_message
match: contains
flags: i
---
\bamend run\b[^\n]{0,80}\bfirst\b|\bfirst\b[^\n]{0,80}\bamend\b
