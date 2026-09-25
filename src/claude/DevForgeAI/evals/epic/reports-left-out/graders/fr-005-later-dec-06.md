---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-005\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\blater\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bDEC-06\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bno action\b|\bnone\b|\bnothing\b|\bno next action\b))'
---
