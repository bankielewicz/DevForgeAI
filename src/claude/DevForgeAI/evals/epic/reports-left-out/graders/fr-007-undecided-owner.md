---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-007\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bundecided\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bowner\b))'
---
