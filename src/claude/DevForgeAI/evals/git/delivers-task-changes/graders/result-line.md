---
type: regex
target: last_message
match: contains
---
(?:^|\n)[*_ \t]*Result:[*_ \t]*(?:done|partial|blocked|awaiting_approval|no_change)\b
