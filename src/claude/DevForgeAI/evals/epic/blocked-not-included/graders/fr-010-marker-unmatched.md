---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-010\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bblocked\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bmarker\b|NEEDS ADR))'
---
