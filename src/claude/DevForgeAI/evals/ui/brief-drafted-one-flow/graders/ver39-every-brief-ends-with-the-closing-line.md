---
type: regex
target: last_message
match: not_contains
flags: i
---
(?:^|\n)```[^\n]*(?:(?!```|\n[ \t]*Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.[ \t]*(?=\n|$))[\s\S])*?(?:^|\n)[ \t]*(?:\*\*|__)?Context\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?(?:(?!```|\n[ \t]*Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.[ \t]*(?=\n|$))[\s\S])*?```
