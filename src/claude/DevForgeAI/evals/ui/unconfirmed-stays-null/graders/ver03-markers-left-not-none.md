---
type: regex
target: last_message
match: contains
flags: i
---
(?:^|\n)[ \t>*-]*(?:\*\*)?Markers left:(?:\*\*)?[ \t]*(?!none\b)\S
