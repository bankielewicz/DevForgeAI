---
type: regex
target: last_message
match: not_contains
flags: i
---
\bNFR-001\b[^\n.;]{0,40}(?<!\bnot |\bnever |n't )\bcovered\b
