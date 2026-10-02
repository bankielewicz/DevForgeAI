---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: not_contains
---
- id: SM-\d{2}\n(?=(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+metric: "[^"\n]*(?:[Ss]atisf|[Ss]urvey))(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+upstream:[ \t]*(?:\n[ \t]+- |\[[ \t]*\{)
