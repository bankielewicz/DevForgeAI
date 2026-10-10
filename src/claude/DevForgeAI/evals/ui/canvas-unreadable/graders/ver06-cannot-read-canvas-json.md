---
type: regex
target: last_message
match: contains
flags: i
---
canvas\.json[^\n]{0,160}(?:can['’]?t|cannot|can not|unable|could(?:n['’]t| not)|not (?:be )?(?:read|readable|valid|parsed|parseable)|unreadable|damaged|invalid|corrupt)|(?:cannot|can['’]t|unable to|could not) (?:be )?(?:read|parse)[^\n]{0,100}canvas\.json
