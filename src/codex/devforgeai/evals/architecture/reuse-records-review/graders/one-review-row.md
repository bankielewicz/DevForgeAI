---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: not_contains
---
Reviewed against PRD-\d{3} v\d[\s\S]*Reviewed against PRD-\d{3} v\d
