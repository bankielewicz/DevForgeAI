---
type: regex
target: last_message
match: contains
flags: i
---
\bwhich\b[^\n]{0,100}\?|\?[^\n]{0,100}\bwhich\b
