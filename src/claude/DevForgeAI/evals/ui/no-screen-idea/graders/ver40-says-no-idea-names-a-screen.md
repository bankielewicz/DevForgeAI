---
type: regex
target: last_message
match: contains
flags: i
---
(?:\bno\b|\bnone\b|\bnothing\b|\bnot\b|n['’]t)[^\n]{0,100}\b(?:screens?|user interface|UI)\b
