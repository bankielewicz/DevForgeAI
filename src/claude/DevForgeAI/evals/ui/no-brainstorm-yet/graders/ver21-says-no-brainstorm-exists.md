---
type: regex
target: last_message
match: contains
flags: i
---
\bno (?:brainstorm|BRN)\b[^\n]{0,60}|\bnot? brainstorm\b|brainstorm[^\n]{0,40}\b(?:exists?|yet|found)\b
