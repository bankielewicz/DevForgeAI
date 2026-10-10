---
type: regex
target: last_message
match: contains
flags: i
---
\bcop(?:y|ied|ying)\b[^\n]{0,80}\bagain\b|\bre-?cop(?:y|ied|ying)\b|\bagain\b[^\n]{0,60}\bcop(?:y|ied)|\bcop(?:y|ied|ies)\b[^\n]{0,100}\b(?:there|into|to)\b
