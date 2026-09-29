---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
---
- id: EVD-\d{2}\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+source: "[^"\n]*ADR-002[^"\n]*"\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+classification: context\n
