---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: not_contains
---
statement: "[^"\n]*\bAWS\b[^"\n]*"\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+- \{id: BRN-
