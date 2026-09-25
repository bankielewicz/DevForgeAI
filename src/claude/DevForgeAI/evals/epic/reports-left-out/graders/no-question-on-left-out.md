---
type: regex
target: last_message
match: not_contains
pattern: '(?<![\w-])FR-00[567]\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*\?'
---
