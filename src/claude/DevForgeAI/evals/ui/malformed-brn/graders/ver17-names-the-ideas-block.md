---
type: regex
target: last_message
match: contains
flags: i
---
\bideas\b[^\n]{0,40}\bblock\b|\bblock\b[^\n]{0,40}\bideas\b
