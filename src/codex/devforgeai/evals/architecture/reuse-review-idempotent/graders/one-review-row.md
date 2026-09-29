---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
---
^(?![\s\S]*Reviewed against PRD-\d{3} v\d[\s\S]*Reviewed against PRD-\d{3} v\d)[\s\S]*\(session prior-review-session\) \| Reviewed against PRD-001 v2: reuse confirmed
