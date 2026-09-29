---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: not_contains
---
resolved_by:(?:[^\n]*ADR-|\n[ \t]+- \"?ADR-)
