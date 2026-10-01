---
type: regex
target: last_message
match: not_contains
flags: i
---
\bno (?:\w+ ){0,2}requirements? (?:\w+ ){0,2}needs? (?:a )?new epic|\bnone (?:of them )?needs? (?:a )?new epic
