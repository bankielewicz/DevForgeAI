---
type: regex
target: last_message
match: contains
flags: i
---
(?:\bnever\b|\bnot\b|n['’]t)[^\n]{0,60}\bfetch|\bfetch\w*[^\n]{0,60}\b(?:never|not)\b|\bno fetch
