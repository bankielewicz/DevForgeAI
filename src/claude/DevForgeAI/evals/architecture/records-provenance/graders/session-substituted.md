---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
flags: m
---
^  session: "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
