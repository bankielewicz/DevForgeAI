---
type: regex
target: last_message
match: contains
---
(?:^|\n)[ \t]*(?:\*\*|__)?Next step[^\n]*(?:\n(?![ \t]*\n)[^\n]*)*\s*$
