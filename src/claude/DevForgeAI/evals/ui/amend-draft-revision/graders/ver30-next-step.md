---
type: regex
target: last_message
match: contains
flags: i
---
(?:^|\n[ \t]*\n)[ \t]*(?:\*\*|__)?Next step\b(?=(?:(?!\n[ \t]*\n)[\s\S])*?/devforgeai:prd[` \t]+BRN-001\b)(?:(?!\n[ \t]*\n)[\s\S])*?\s*$
