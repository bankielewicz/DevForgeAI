---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
---
- id: DEC-02\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+state: resolved\n[ \t]+resolved_by: \[ADR-001\][ \t]*\n
