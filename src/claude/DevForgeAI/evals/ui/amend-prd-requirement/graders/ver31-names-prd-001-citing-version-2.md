---
type: regex
target: last_message
match: contains
flags: i
---
(?:^|\n)(?=[^\n]*\bPRD-001\b)(?=[^\n]*\bDSN-001\b)[^\n]*\b(?:version[ \t]*|v)2\b
