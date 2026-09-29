---
type: regex
target: last_message
match: contains
flags: i
---
proposal[^\n]{0,200}\bdraft\b|\bdraft\b[^\n]{0,200}proposal
