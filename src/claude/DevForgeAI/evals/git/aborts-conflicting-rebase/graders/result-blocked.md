---
type: regex
target: last_message
match: contains
---
(?:^|\n)[*_ \t]*Result:[*_ \t]*(?:blocked|awaiting_approval)\b
