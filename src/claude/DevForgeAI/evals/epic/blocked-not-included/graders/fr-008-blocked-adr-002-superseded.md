---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-008\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bblocked\b|\bopen again\b|\breopened\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bDEC-03\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bADR-002\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:supersed|replaced))'
---
