---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-006\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\bwon[’'']?t\b|(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\bwont\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bno action\b|\bnone\b|\bnothing to do\b|\bno next action\b|\bno further action\b|\bno new epic\b|\bnothing (?:is )?needed\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bnot (?:a )?won[’'']?t\b|\bisn[’'']t (?:a )?won[’'']?t\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\beligible\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\bundecided\b))'
---
