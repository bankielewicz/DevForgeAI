---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
---
- id: DEC-01\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+state: open\n[ \t]+resolved_by: \[\][ \t]*\n
