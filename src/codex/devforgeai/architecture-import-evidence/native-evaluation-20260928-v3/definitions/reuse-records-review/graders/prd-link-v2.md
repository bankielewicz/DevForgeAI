---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
flags: m
---
^upstream:\n  - \{id: PRD-001, relation: informed_by, version: 2, hash: null\}\n
