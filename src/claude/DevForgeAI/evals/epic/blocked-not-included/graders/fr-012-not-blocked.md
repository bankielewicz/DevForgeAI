---
type: regex
target: last_message
flags: i
match: not_contains
pattern: '(?<![\w-])FR-012\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)(?<!\bor\s)\bblocked\b|(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\bunknown\b|\bcan[’'']?t be (?:established|checked|determined|verified|confirmed)\b|\bcannot be (?:established|checked|determined|verified|confirmed)\b|\bcould(?:n[’'']t| not) be (?:established|checked|determined|verified|confirmed)\b|\bundetermined\b))'
---
