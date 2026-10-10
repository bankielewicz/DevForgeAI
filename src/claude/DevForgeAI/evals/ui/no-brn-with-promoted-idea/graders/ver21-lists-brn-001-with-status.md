---
type: regex
target: last_message
match: contains
flags: i
---
BRN-001[^\n]*\bdraft\b|\bdraft\b[^\n]*BRN-001
