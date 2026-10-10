---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:one|1)\b[^\n]{0,60}\bcandidate\b[^\n]{0,80}\b(?:left|later)|\bcandidate\b[^\n]{0,80}\b(?:left|later)\b[^\n]{0,60}\b(?:one|1)\b|FR-037[^\n]{0,80}\b(?:left|later)\b|\b(?:left|later)\b[^\n]{0,80}FR-037
