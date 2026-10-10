---
type: regex
target: last_message
match: contains
flags: i
---
BRN-002[^\n]*\b(?:none|no DSN|not (?:yet )?cited|uncited)\b|\b(?:none|no DSN)\b[^\n]*BRN-002
