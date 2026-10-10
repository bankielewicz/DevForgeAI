---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:no|none of the|not any)\b[^\n.]{0,40}\b(?:documents?|PRDs?|docs)\b[^\n.]{0,60}\bcit\w+|\bnothing\b[^\n.]{0,40}\bcit\w+|\bnot cited by (?:any|a)\b|\bno one cites\b|\bnone\b[^\n.]{0,40}\bcit\w+
