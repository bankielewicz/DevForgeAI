---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-007\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bundecided\b|\bno priority\b|priority (?:is |was )?(?:not set|unset|null|missing|not decided|undecided)|isn[’\'']t (?:set|decided)|not (?:yet )?decided|\bnull\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bowner\b))'
---
