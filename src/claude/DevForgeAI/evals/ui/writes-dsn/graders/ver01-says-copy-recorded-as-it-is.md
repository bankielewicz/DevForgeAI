---
type: regex
target: last_message
match: contains
flags: i
---
\bas[- ]is\b|\bas it is\b|\brecorded\b[^\n]{0,60}\bcopy\b|\bcopy\b[^\n]{0,80}\b(?:recorded|record)\b
