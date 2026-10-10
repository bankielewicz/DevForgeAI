---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:DSN|design)\b[^\n]*\?|\bwhich\b[^\n]{0,80}\b(?:DSN|design)\b|\b(?:give|provide|tell|name|send|pick|choose|say|supply)\b[^\n]{0,60}\b(?:DSN|design)\b
