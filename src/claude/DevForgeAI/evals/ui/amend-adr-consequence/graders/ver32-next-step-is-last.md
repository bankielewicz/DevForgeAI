---
type: regex
target: last_message
match: contains
---
(?:^|\n[ \t]*\n)[ \t]*(?:\*\*|__)?Next step\b(?:(?!\n[ \t]*\n)[\s\S])*?\s*$
