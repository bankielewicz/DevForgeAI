---
type: regex
target: last_message
match: contains
flags: i
---
\bno Artifact\b|\bArtifact tool\b[^\n]{0,40}(?:\bnot\b|n['’]t\b|\bunavailable\b|\bmissing\b|\babsent\b)|\b(?:without|lacks?|missing|has no|have no|don['’]t have|do not have|doesn['’]t have)\b[^\n]{0,30}\bArtifact\b
