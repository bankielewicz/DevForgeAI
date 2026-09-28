---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
---
- id: DEC-\d{2}\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+question: "[^"\n]*[Rr]evo[^"\n]*"\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+state: open\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+- \{id: PRD-001, item: FR-001,
