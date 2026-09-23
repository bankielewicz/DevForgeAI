---
type: regex
target:
  source: file
  path: docs/specs/brainstorm/BRN-001.md
match: not_contains
pattern: '```yaml items\n(?:(?!```)[^\n]*\n)*? {4}(?!(?:id|status|superseded_by|upstream|statement|who|evidence|severity|idea|addresses|value|effort|risk|score|disposition|reason|validation|state):)[A-Za-z_][\w-]*:'
---
