---
type: regex
target: last_message
flags: i
match: not_contains
pattern: '(?<![\w-])NFR-001\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?:(?!(?<![\w-])N?FR-\d{3}\b|\bnot\b|\bnever\b|n[’\'']t\b)[^\n])*?(?:\bcovered\s+by\s+EPIC-)'
---
