---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-002\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bcovered\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bEPIC-001\b))'
---
