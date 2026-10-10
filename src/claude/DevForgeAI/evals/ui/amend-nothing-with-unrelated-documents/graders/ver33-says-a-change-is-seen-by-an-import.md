---
type: regex
target: last_message
match: contains
flags: i
---
\bimport(?:s|ed|ing)?\b[^\n]{0,100}\b(?:board|canvas|change)|\b(?:board|canvas|change)\w*[^\n]{0,100}\bimport
