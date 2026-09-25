---
type: regex
target: last_message
flags: i
match: not_contains
pattern: '(?<![\w-])NFR-001\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\bcovered\s+by\s+EPIC-))'
---
