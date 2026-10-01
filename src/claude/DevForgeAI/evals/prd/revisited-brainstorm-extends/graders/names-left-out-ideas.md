---
type: regex
target: last_message
match: contains
flags: i
---
IDEA-01[^\n]{0,200}(?:left out|already cited|cited by|cites)|(?:left out|already cited|cited by)[^\n]{0,200}IDEA-01
