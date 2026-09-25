---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-012\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bunknown\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:SET-01\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:deprecat|not active|inactive|retired))'
---
