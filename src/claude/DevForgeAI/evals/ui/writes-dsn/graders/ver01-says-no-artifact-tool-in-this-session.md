---
type: regex
target: last_message
match: contains
flags: i
---
\bno Artifact\b|\bArtifact tool\b[^\n]{0,40}\b(?:not|n['’]t|unavailable|missing|absent)\b|\b(?:without|lacks?|missing|has no|have no|don['’]t have|do not have|doesn['’]t have)\b[^\n]{0,30}\bArtifact\b
