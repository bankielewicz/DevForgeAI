---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
flags: m
---
(^    kinds:\n      - "(user-interface|service|platform|api|relational-store|data-store|external)"\n|\[NEEDS CLARIFICATION: kinds of CMP-\d{2}\])
