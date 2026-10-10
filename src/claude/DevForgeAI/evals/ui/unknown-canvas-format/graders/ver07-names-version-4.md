---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:v|version)[ ]?4\b|\b4\b[^\n]{0,40}\b(?:version|format)\b|\b(?:version|format)\b[^\n]{0,60}\b4\b
