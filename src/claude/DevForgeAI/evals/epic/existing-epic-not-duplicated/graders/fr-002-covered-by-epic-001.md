---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-002\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\bcovered\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bEPIC-001\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bno action\b|\bnone\b|\bnothing to do\b|\bno next action\b|\bno further action\b|\bno new epic\b|\bnothing (?:is )?needed\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bnot (?:yet )?covered\b|n[’'']t covered\b|\bnever covered\b|\buncovered\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bEPIC-(?!001\b)\d{3}\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)(?<!\bor\s)\bblocked\b))'
---
