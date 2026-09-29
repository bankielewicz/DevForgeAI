---
type: regex
target: last_message
match: contains
---
(?:^|\n)[*_ \t]*Result:[*_ \t]*(?:done|no_change)\b
