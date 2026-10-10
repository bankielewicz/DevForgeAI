---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:re-?)?import\w*\b[^\n]{0,80}\bagain\b|\bre-?import\b|\bcop(?:y|ied|ying)\b[^\n]{0,80}\bagain\b|\bre-?cop(?:y|ied|ying)\b|\bagain\b[^\n]{0,60}\b(?:import|cop(?:y|ied))
