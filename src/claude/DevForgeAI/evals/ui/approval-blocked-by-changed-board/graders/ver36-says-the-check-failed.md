---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:check|validation)\b[^\n]{0,100}\b(?:fail\w*|INVALID|did not pass|didn['’]t pass|errors?|not valid)\b|\b(?:fail\w*|INVALID|errors?)\b[^\n]{0,100}\b(?:check|validation)\b
