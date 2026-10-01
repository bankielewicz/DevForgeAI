---
type: regex
target: last_message
match: contains
flags: i
---
suspect[^\n]{0,120}BRN-001|BRN-001[^\n]{0,120}suspect
