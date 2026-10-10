---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:BRN|brainstorm)\b[^\n]*\?|\bwhich\b[^\n]{0,80}\bID\b|\b(?:give|provide|tell|name|send|pick|choose|say|supply)\b[^\n]{0,60}\b(?:BRN|brainstorm)\b
