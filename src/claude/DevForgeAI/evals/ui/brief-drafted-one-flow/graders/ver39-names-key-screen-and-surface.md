---
type: regex
target: last_message
match: contains
flags: i
---
^(?=[\s\S]*\bkey screen\b)(?=[\s\S]*\b(?:terminal|web)\b)
