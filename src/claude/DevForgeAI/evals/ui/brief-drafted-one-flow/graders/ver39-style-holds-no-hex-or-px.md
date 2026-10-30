---
type: regex
target: last_message
match: not_contains
flags: i
---
(?:^|\n)[ \t]*(?:\*\*|__)?Style\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?(?:(?!Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.)[\s\S])*?(?:#[0-9a-fA-F]{3,8}\b|\b\d+\s?px\b)
