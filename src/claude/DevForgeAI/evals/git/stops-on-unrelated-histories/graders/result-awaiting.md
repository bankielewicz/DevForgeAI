---
type: regex
target: last_message
match: contains
---
(?:^|\n)[*_ \t]*Result:[*_ \t]*(?:awaiting_approval|blocked)\b
