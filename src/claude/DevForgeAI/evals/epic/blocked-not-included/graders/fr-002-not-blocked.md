---
type: regex
target: last_message
flags: i
match: not_contains
pattern: '(?<![\w-])FR-002\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?:(?!(?<![\w-])N?FR-\d{3}\b|\bnot\b|\bnever\b|n[’\'']t\b)[^\n])*?(?:\bblocked\b|\bunknown\b)'
---
