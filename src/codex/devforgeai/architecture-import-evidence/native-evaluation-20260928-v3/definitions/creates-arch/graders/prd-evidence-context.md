---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
---
- id: EVD-\d{2}\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+kind: prd\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+classification: context\n
