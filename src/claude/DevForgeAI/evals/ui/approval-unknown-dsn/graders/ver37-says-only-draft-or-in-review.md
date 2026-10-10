---
type: regex
target: last_message
match: contains
flags: i
---
\bonly\b[^\n]{0,80}\bdraft\b[^\n]{0,60}\bin-review\b|\bdraft\b[^\n]{0,30}\b(?:or|and)\b[^\n]{0,30}\bin-review\b[^\n]{0,60}\bonly\b|\bonly\b[^\n]{0,80}\bin-review\b[^\n]{0,60}\bdraft\b
