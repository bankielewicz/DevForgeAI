---
type: regex
target: last_message
match: contains
flags: i
---
(?:^|\n)(?![ \t>*-]*(?:\*\*)?Markers left:)(?=[^\n]*\bmarkers?\b)(?=[^\n]*\b(?:remains?|remaining|still|blocks?|blocked|waits?|waiting|until|unresolved|open)\b)[^\n]+
