---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-006\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bwon[’\'']?t\b|\bwont\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bno action\b|\bnone\b|\bnothing\b|\bno next action\b))'
---
