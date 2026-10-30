---
type: regex
target: last_message
match: contains
flags: i
---
^(?:(?!Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.)[\s\S])*?(?:(?:^|\n)```[^\n]*\n(?:(?!```|Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.)[\s\S])*?\n[ \t]*Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.[ \t]*(?=\n|$)(?:(?!```|Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.)[\s\S])*?```(?:(?!Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.)[\s\S])*?)+$
