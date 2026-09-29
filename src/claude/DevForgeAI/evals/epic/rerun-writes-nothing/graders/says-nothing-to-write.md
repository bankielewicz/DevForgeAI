---
type: regex
target: last_message
match: contains
flags: i
---
\bno new epics?\b|\bno (?:\w+ ){0,2}requirements? (?:\w+ ){0,2}needs? (?:a )?new epic
