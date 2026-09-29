---
type: regex
target: last_message
match: contains
---
ADR-002[^\n]{0,150}(?:[Ss]upersed|[Rr]eplac)|(?:[Ss]upersed|[Rr]eplac)[^\n]{0,150}ADR-002
