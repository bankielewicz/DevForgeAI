---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-007\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\bundecided\b|\bno priority\b|priority (?:is |was )?(?:not set|unset|null|missing|not decided|undecided)|isn[’'']t (?:set|decided)|not (?:yet )?(?:set|decided)|\bnull\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bpriorit|\bnull\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bowner\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bnot undecided\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:(?<!\bnot\s)(?<!\bnot yet\s)(?<!\bnever\s)(?<!\bno longer\s)(?<!n[’'']t\s)(?<!\bneither\s)(?<!\bnor\s)(?<!\bnot be\s)(?<!\bnot been\s)(?<!\basserted\s)\beligible\b))(?!(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:priority (?:is |was )?(?:must|should|could|wont|won[’'']t)\b))'
---
