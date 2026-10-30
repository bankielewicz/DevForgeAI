---
type: regex
target: last_message
match: not_contains
flags: i
---
(?:^|\n)```[^\n]*(?:(?!```|Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.)[\s\S])*?(?:^|\n)[ \t]*(?:\*\*|__)?Context\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?(?:(?!```|Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.)[\s\S])*?```
