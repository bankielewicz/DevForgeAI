---
type: regex
target:
  source: file
  path: docs/specs/brainstorm/BRN-001.md
match: not_contains
pattern: '```yaml items\n(?:(?!```)[^\n]*\n)*?[A-Za-z_][\w-]*:[^\n]*\n(?:(?!```)[^\n]*\n)*?[A-Za-z_][\w-]*:'
---
