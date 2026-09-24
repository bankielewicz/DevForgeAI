---
type: regex
target: last_message
flags: i
pattern: '\bADR-002\b(?:(?!\bnot\b|\bnever\b|n[’'']t\b)[^\n.;]){0,80}?\b(?:superseded|replaced)\b(?!\s+ADR-)|\bADR-00[3-9]\b(?:(?!\bnot\b|\bnever\b|n[’'']t\b)[^\n.;]){0,60}?\b(?:supersedes|superseded|replaces|replaced)\s+ADR-002\b|(?<!\bnot\s)(?<!\bnever\s)(?<!n[’'']t\s)\b(?:superseded|replaced)\s+(?:resolver\s+|ADR\s+)?ADR-002\b'
---
