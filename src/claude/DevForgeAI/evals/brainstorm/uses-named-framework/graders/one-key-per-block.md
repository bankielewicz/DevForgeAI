---
type: regex
target:
  source: file
  path: docs/specs/brainstorms/BRN-001-onboarding-drop-off.md
match: not_contains
pattern: '```yaml items\n(?:(?!```)[^\n]*\n)*?[A-Za-z_][\w-]*:[^\n]*\n(?:(?!```)[^\n]*\n)*?[A-Za-z_][\w-]*:'
---
