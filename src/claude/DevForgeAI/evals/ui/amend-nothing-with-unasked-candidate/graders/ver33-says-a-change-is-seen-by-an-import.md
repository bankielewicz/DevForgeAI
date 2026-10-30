---
type: regex
target: last_message
match: contains
flags: i
---
\b(?:board|canvas|change)\w*\b[^\n]{0,120}\b(?:seen|noticed|picked up|detected|found|shows? up|visible)\b[^\n]{0,80}\bimport\w*|\bimport\w*\b[^\n]{0,80}\b(?:sees?|shows?|reads?|picks? up|notices?)\b[^\n]{0,60}\b(?:board|canvas|change)
