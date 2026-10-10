---
type: regex
target: last_message
match: contains
flags: i
---
\bDSN\b[^\n]*\?|\b(?:give|provide|tell|name|send|pick|choose|say|supply)\b[^\n]{0,60}\bDSN\b
