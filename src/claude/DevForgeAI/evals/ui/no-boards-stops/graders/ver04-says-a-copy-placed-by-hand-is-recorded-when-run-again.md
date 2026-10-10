---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:by hand|yourself|manually|place[sd]?|put|cop(?:y|ied))\b[^\n]{0,160}\b(?:run|runs|rerun|re-run|ran)\b[^\n]{0,40}\bagain\b|\bagain\b[^\n]{0,160}\b(?:record\w*)\b|\b(?:record\w*)\b[^\n]{0,160}\b(?:run|runs|rerun|re-run)\b[^\n]{0,40}\bagain\b|\brecord\w*\b[^\n]{0,160}\b(?:next|following|later)\s+(?:run|time|session)\b|\b(?:next|following|later)\s+(?:run|time|session)\b[^\n]{0,160}\brecord\w*\b
