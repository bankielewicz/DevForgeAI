---
type: regex
target: last_message
match: contains
flags: i
---
BRN-002[^\n]{0,200}\b(?:draft|not converged|open)\b|\b(?:draft|not converged)\b[^\n]{0,200}BRN-002
