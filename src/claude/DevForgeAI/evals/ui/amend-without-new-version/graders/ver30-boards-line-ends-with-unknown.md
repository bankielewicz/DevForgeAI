---
type: regex
target: last_message
match: contains
---
(?:^|\n)[ \t>*-]*(?:\*\*)?Boards:(?:\*\*)?[ \t]*[^\n]*\bversion unknown[ \t]*(?:\n|$)
