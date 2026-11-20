---
type: regex
target: last_message
match: contains
flags: m
---
^[ \t]*First release: (?:IDEA-\d{2}(?:, IDEA-\d{2})* \(proposed, not confirmed\)|none)[ \t]*$
