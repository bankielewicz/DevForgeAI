---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-005\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\blater\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bDEC-06\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bno action\b|\bnone\b|\bnothing to do\b|\bno next action\b|\bno further action\b|\bno new epic\b|\bnothing (?:is )?needed\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\b(?:ready|eligible)\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bDEC-(?!06\b)\d{2}\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bDEC-06\b[^\n]{0,15}\bresolved\b))'
---
