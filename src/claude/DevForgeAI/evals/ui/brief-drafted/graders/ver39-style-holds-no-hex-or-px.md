---
type: regex
target: last_message
match: not_contains
---
(?:^|\n)[ \t>*#-]*(?:\*\*)?Style(?:\*\*)?[:.\s][^\n]*(?:#[0-9a-fA-F]{3,8}\b|\b\d+\s?px\b)
