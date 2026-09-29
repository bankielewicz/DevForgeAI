---
type: regex
target: last_message
match: contains
---
Next step[\s\S]*(?:\bnot|n't)[^\n.]{0,40}?\b(?:built|exist|available)
