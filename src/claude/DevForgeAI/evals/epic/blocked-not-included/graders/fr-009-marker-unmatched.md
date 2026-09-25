---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-009\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bblocked\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bmarker\b|NEEDS ADR|\bopen question\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:no matching|without (?:a |any )?matching|unmatched|no (?:DEC|decision|question)\b|not answered|no corresponding|doesn[’\'']t (?:match|answer)|does not (?:match|answer)|nothing (?:matches|answers)))'
---
